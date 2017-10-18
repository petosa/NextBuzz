import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

SESSION_THRESH = 10000
APPROACH_BACKOFF = 15
FIELD = "abserror"
DISTINGUISH = "route"

df = pd.read_csv("predictions_new.csv")
df.drop_duplicates(subset=["timestamp","route","stop"], keep="first", inplace=True)

# Calculate the "session" column. If there is a break of more than SESSION_THRESH
# seconds, a session is assumed to have ended, and the session value is increased
# for subsequent entries per [route, stop] grouping. This is useful for capturing
# large breaks in service, and hints that a new day has started. We cannot just
# use the current date as our session variable, as the midnight rambler spans
# two days every 24 hours.
grouped = df.groupby(["route", "stop"])
df["session"] = df["timestamp"] - grouped["timestamp"].shift(1)
df["session"] = grouped["session"].apply(lambda x: x > SESSION_THRESH)
df["session"] = df["session"].astype(int)
df["session"] = grouped["session"].agg("cumsum")

# Use a heuristic to determine when a new approach begins. Uses APPROACH_BACKOFF
# as a threshold to determine if a sudden change in predicted arrival indicates
# that the bus has arrived.
grouped = df.groupby(["route", "stop", "session"])
df["approach"] = df["secondsToArrival"] - grouped["secondsToArrival"].shift(1)
df["approach"] = grouped["approach"].apply(lambda x: x > APPROACH_BACKOFF)
df["approach"] = df["approach"].astype(int)
df["approach"] = grouped["approach"].agg("cumsum")

# Now that we know the distributions, we can assign each tick a true arrival time.
grouped = df.groupby(["route", "stop", "session", "approach"])
df["actualArrival"] = grouped["timestamp"].transform("max") # Get actual arrival timestamp
df["actualSecondsToArrival"] = df["actualArrival"] - df["timestamp"] # To seconds at each
df["error"] = df["predictedArrival"] - df["actualArrival"] # Predicted - Actual
df["abserror"] = abs(df["error"])
df["sqerror"] = df["error"] * df["error"] # Squared error

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