import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random

SESSION_THRESH = 10000
APPROACH_BACKOFF = 40
ACTIVATION_THRESH = 80
FIELD = "sqerror"
DISTINGUISH = "route"

df = pd.read_csv("predictions_new.csv")
before = df.size
df.drop_duplicates(subset=["timestamp", "route", "stop"], keep="first", inplace=True)
print("Removed " + str(before - df.size) + " duplicates.")

# Calculate the "session" column. If there is a break of more than SESSION_THRESH
# seconds, a session is assumed to have ended, and the session value is increased
# for subsequent entries per [route, stop] grouping. This is useful for capturing
# large breaks in service, and hints that a new day has started. We cannot just
# use the current date as our session variable, as the midnight rambler spans
# two days every 24 hours.
grouped = df.groupby(["route", "stop"], as_index=True)
df["session"] = df["timestamp"] - grouped["timestamp"].shift(1)
df["session"] = grouped["session"].apply(lambda x: x > SESSION_THRESH)
df["session"] = df["session"].astype(int)
df["session"] = grouped["session"].agg("cumsum")

# Print statistics about sessions
temp = grouped["session"].unique().apply(lambda x: x.size)
print(str(temp.sum()) + " total sessions detected.")
print(str(temp.mean()) + " days of data.")

# Use a heuristic to determine when a new approach begins. Uses APPROACH_BACKOFF
# as a threshold to determine if a sudden change in predicted arrival indicates
# that the bus has arrived.
grouped = df.groupby(["route", "stop", "session"], as_index=True)
df["busChange"] = ((df["busID"] - grouped["busID"].shift(1)).fillna(0) != 0.0)
df["newApproach"] = df["secondsToArrival"] - grouped["secondsToArrival"].shift(1)
df["newApproach"] = grouped["newApproach"].apply(lambda x: x > APPROACH_BACKOFF)
df["newApproach"] = df["newApproach"] & (grouped["secondsToArrival"].shift(1) < ACTIVATION_THRESH)
df["approach"] = df["newApproach"].astype(int)
df["approach"] = grouped["approach"].agg("cumsum")

grouped = df.groupby(["route", "stop", "session"], as_index=True)

# Print statistics about approaches
temp = grouped["approach"].unique().apply(lambda x : x.size)
print(str(temp.sum()) + " approaches detected.")
print(str(temp.mean()) + " average loops per day for all routes.")
temp = temp.groupby(level=[0])
print(temp.mean())


# Now that we know the distributions, we can assign each tick a true arrival time.
grouped = df.groupby(["route", "stop", "session", "approach"])
df["actualArrival"] = grouped["timestamp"].transform("max") # Get actual arrival timestamp
df["actualSecondsToArrival"] = df["actualArrival"] - df["timestamp"] # To seconds at each
df["error"] = df["predictedArrival"] - df["actualArrival"] # Predicted - Actual
df["abserror"] = abs(df["error"])
df["sqerror"] = df["error"] * df["error"] # Squared error


sample_keys = random.sample(list(grouped.indices.keys()), 10)
for key in sample_keys:
    frame = grouped.get_group(key)
    plt.plot(frame["timestamp"], frame["secondsToArrival"], linewidth=3)
    plt.plot(frame["timestamp"], frame["actualSecondsToArrival"], linewidth=3, c="y")
    for index, row in frame.iterrows():
        if row["newApproach"]:
            plt.axvline(x=row["timestamp"], c="r")
        if row["busChange"]:
            plt.axvline(x=row["timestamp"], c="g",linestyle='--')
    plt.show()



# Plot it
colors = plt.get_cmap("Set1")(np.linspace(0, 1, len(df[DISTINGUISH].unique())))
cmapping = {}
count = 0
for item in df[DISTINGUISH].unique():
    cmapping[item] = colors[count]
    count += 1
group_keys = ["route", "stop", "session", "approach"]
grouped = df.groupby(group_keys)
aggmapping = {}
for item in grouped.groups.keys():
    dkey = item[group_keys.index(DISTINGUISH)]
    desired_col = grouped.get_group(item)[FIELD].reset_index(drop=True)
    if not dkey in aggmapping:
        aggmapping[dkey] = (1, pd.DataFrame(desired_col))
    else:
        aggmapping[dkey] = (aggmapping[dkey][0] + 1, aggmapping[dkey][1].add(pd.DataFrame(desired_col), fill_value=0))
    desired_col.plot(c=cmapping[dkey])

handler = []
for item in cmapping:
    handler.append(mpatches.Patch(color=cmapping[item], label=item))
plt.legend(handles=handler)
plt.show()
plt.close()
for item in aggmapping:
    (aggmapping[item][1]/aggmapping[item][0])[FIELD].plot(c=cmapping[item])
plt.legend(handles=handler)
plt.show()