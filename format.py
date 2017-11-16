import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random
import requests
import xmltodict
import math

SESSION_THRESH = 10000
APPROACH_BACKOFF = 40
SINGLE_BUS_BACKOFF = 300
ACTIVATION_THRESH = 80
FIELD = "abserror"
DISTINGUISH = "route"
# Cluster sampling
SAMPLE_HIERARCHY = ["route", "stop", "session"] # Cluster granularity: approach
NUM_CLUSTERS = 100



# Read in data, drop all duplicates.
df = pd.read_csv("big_predictions.csv")
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
df["error"] = df["predictedArrival"] - df["actualArrival"] # Predicted - Actual
df["abserror"] = abs(df["error"])
df["sqerror"] = df["error"] * df["error"] # Squared error

# Calculate the distance of each bus from its stop.
session = requests.Session()
session.headers.update({"User-Agent": "NextBuzz"})
response = session.get("https://gtbuses.herokuapp.com/agencies/georgia-tech/routes")
routes = xmltodict.parse(response.text)["body"]["route"]
sched = {}
for route in routes:
    for stop in route["stop"]:
        sched[(route["@tag"], stop["@tag"])] = ((float(route["@latMin"]) + float(route["@latMax"]))/2, (float(route["@lonMin"]) + float(route["@lonMax"]))/2)
def coordError(route, stop, coord, choice):
    return abs(float(sched[(route, stop)][choice]) - float(coord))
df["latDistance"] = np.vectorize(coordError)(df["route"], df["stop"], df["busLat"], 0)
df["longDistance"] = np.vectorize(coordError)(df["route"], df["stop"], df["busLong"], 1)
df["distance"] = np.sqrt(df["latDistance"]**2 + df["longDistance"]**2)

# Evaluate accuracy of approach components. Validate our heuristic.

def validate(numBuses, busChange, newApproach, delta):
    if numBuses > 1:
        return busChange and newApproach
    return newApproach and delta > SINGLE_BUS_BACKOFF
df["validated"] = np.vectorize(validate)(df["numBuses"], df["busChange"], df["newApproach"], df["secondsToArrival"] - df.groupby(["route", "stop", "session"])["secondsToArrival"].shift(1)).cumsum()
print(float(df["validated"].max())/float(approaches_detected))

# Sample our dataframe
sample_grouped = df.groupby(SAMPLE_HIERARCHY)
key_sample = random.sample(sample_grouped.indices.keys(), NUM_CLUSTERS)
sample = pd.DataFrame()
for key in key_sample:
    data = sample_grouped.get_group(key).reset_index(drop=True)
    if sample.size == 0:
        sample = data
    else:
        sample = sample.append(data, ignore_index=True)
    


for key in key_sample:
    frame = sample_grouped.get_group(key)
    plt.title("Segmented Approach " + str(key))
    plt.plot(frame["timestamp"], frame["secondsToArrival"], linewidth=3)
    #plt.plot(frame["timestamp"], frame["actualSecondsToArrival"], linewidth=3, c="y")
    #plt.plot(frame["timestamp"], frame["distance"], linewidth=2, c="b")
    plt.xlabel("Timestamp")
    plt.ylabel("Distance")
    plt.legend()

    for index, row in frame.iterrows():
        if row["newApproach"]:
            plt.axvline(x=row["timestamp"], linewidth=2, c="r")
        if row["busChange"]:
            plt.axvline(x=row["timestamp"], linewidth=2, c="g",linestyle='--')
    #plt.show()


# Plot it
colors = plt.get_cmap("Set1")(np.linspace(0, 1, len(sample[DISTINGUISH].unique())))
cmapping = {}
count = 0
for item in sample[DISTINGUISH].unique():
    cmapping[item] = colors[count]
    count += 1
group_keys = ["route", "stop", "session", "approach"]
grouped = sample.groupby(group_keys)
aggmapping = {}
for item in grouped.groups.keys():
    dkey = item[group_keys.index(DISTINGUISH)]
    desired_col = grouped.get_group(item)[FIELD].reset_index(drop=True)
    scatter_x = grouped.get_group(item)["actualSecondsToArrival"].reset_index(drop=True)
    if not dkey in aggmapping:
        aggmapping[dkey] = (1, pd.DataFrame(desired_col))
    else:
        aggmapping[dkey] = (aggmapping[dkey][0] + 1, aggmapping[dkey][1].add(pd.DataFrame(desired_col), fill_value=0))
    plt.scatter(x=scatter_x, y=desired_col, c=cmapping[dkey])

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