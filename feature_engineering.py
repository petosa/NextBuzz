import pandas as pd
import numpy as np
import xmltodict
import math

# Engineers features related to sessions and arrival events, which are
# completely heuristics based.
def heuristic(df, session_thresh, approach_spike, single_bus_spike, activation_below):

    df = df.copy()

    # Calculate the "session" column. If there is a break of more than SESSION_THRESH
    # seconds, a session is assumed to have ended, and the session value is increased
    # for subsequent entries per [route, stop] grouping. This is useful for capturing
    # large breaks in service, and hints that a new day has started. We cannot just
    # use the current date as our session variable, as the midnight rambler spans
    # two days every 24 hours.
    grouped = df.groupby(["route", "stop"], as_index=True)
    df["session"] = df["timestamp"] - grouped["timestamp"].shift(1)
    df["session"] = grouped["session"].apply(lambda x: x > session_thresh)
    df["session"] = df["session"].astype(int)
    df["session"] = grouped["session"].agg("cumsum")

    # Print statistics about sessions
    temp = grouped["session"].unique().apply(lambda x: x.size)
    print(str(temp.sum()) + " total sessions detected.")
    print(str(temp.max()) + " days of data.")

    # Use a heuristic to determine when a new approach begins. Uses APPROACH_BACKOFF
    # as a threshold to determine if a sudden change in predicted arrival indicates
    # that the bus has arrived.
    grouped = df.groupby(["route", "stop", "session"], as_index=True)
    df["busChange"] = ((df["busID"] - grouped["busID"].shift(1)).fillna(0) != 0.0)
    df["newApproach"] = df["secondsToArrival"] - grouped["secondsToArrival"].shift(1)
    df["newApproach"] = grouped["newApproach"].apply(lambda x: x > approach_spike)
    df["newApproach"] = df["newApproach"] & (grouped["secondsToArrival"].shift(1) < activation_below)
    df["approach"] = df["newApproach"].astype(int)
    df["approach"] = grouped["approach"].agg("cumsum")

    # Print statistics about approaches
    grouped = df.groupby(["route", "stop", "session"], as_index=True)
    temp = grouped["approach"].unique().apply(lambda x : x.size)
    approaches_detected = str(temp.sum())
    print(approaches_detected + " approaches detected.")
    print(str(temp.mean()) + " average loops per day for all routes.")
    temp = temp.groupby(level=[0])
    print(temp.mean())

    # Now that we know the distributions, we can assign each tick a true arrival time.
    grouped = df.groupby(["route", "stop", "session", "approach"])
    df["actualArrival"] = grouped["timestamp"].transform("max") # Get actual arrival timestamp
    df["actualSecondsToArrival"] = df["actualArrival"] - df["timestamp"] # To seconds at each
    df["error"] = df["actualSecondsToArrival"] - df["secondsToArrival"]  # Actual - Predicted
    df["abserror"] = abs(df["error"])
    df["percenterror"] = df["abserror"]/(df["actualSecondsToArrival"] + .01) # Avoid divide by 0 error
    df["sqerror"] = df["error"] * df["error"] # Squared error

    # Evaluate accuracy of approach components. Validate our heuristic.
    def validate(numBuses, busChange, newApproach, delta):
        if numBuses > 1:
            return busChange and newApproach
        return newApproach and delta > single_bus_spike
    df["validated"] = np.vectorize(validate)(df["numBuses"], df["busChange"], df["newApproach"], df["secondsToArrival"] - df.groupby(["route", "stop", "session"])["secondsToArrival"].shift(1))
    df["validated_cumsum"] = df["validated"].cumsum()
    print("World fidelity: " + str(float(df["validated_cumsum"].max())/float(approaches_detected)))
    df.drop(["validated_cumsum"], axis=1, inplace=True)
    return df

# Engineers features related to time.
def temporal(df):
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    df["timestamp"] = df["timestamp"].dt.tz_localize("UTC").dt.tz_convert("US/Eastern")
    df["dayOfWeek"] = df["timestamp"].dt.dayofweek # Monday=0, Sunday=6
    df["hour"] = df["timestamp"].dt.hour
    df["month"] = df["timestamp"].dt.month
    df["minutesIntoDay"] = df["timestamp"].dt.hour*60 + df["timestamp"].dt.minute
    df["isWeekend"] = df["dayOfWeek"] >= 5
    df["morningRush"] = (df["dayOfWeek"] <= 4) & (df["minutesIntoDay"] >= 420) & (df["minutesIntoDay"] <= 600)
    df["eveningRush"] = (df["dayOfWeek"] <= 4) & (df["minutesIntoDay"] >= 210) & (df["minutesIntoDay"] <= 405)
    return df

# Engineers features related to Georgia Tech domain knowledge.
def georgiatech(df, gt_context):
    df = df.copy()

    # Calculate the distance of each bus from its stop.
    if gt_context.stop_coords != {}: # If we are online...
        def coordError(route, stop, coord, choice):
            return abs(float(gt_context.stop_coords[(route, stop)][choice]) - float(coord))
        df["latDistance"] = np.vectorize(coordError)(df["route"], df["stop"], df["busLat"], 0)
        df["lonDistance"] = np.vectorize(coordError)(df["route"], df["stop"], df["busLong"], 1)
        df["distance"] = np.sqrt(df["latDistance"]**2 + df["lonDistance"]**2)
        df.drop(["latDistance", "lonDistance"], axis=1, inplace=True)
    
    # Class mode is for before or after all classes, 1 for during class, 2 for between classes.
    def classFinder(dow, mid):
        if dow == 0 or dow == 2:
            sched = gt_context.mw_class_schedule
        elif dow == 1 or dow == 3:
            sched = gt_context.tr_class_schedule
        elif dow == 4:
            sched = gt_context.f_class_schedule
        else:
            return 0
        fp = sched[0]
        lp = sched[-1]
        if mid < fp[0] or mid > lp[1]:
            return 0
        for pair in sched:
            if mid >= pair[0] and mid <= pair[1]:
                return 1
        return 2
    df["classMode"] = np.vectorize(classFinder)(df["dayOfWeek"], df["minutesIntoDay"])    

    return df