import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import datetime as datetime

# Perform cluster sampling on our dataframe.
# num_clusters is the number of clusters that should be sampled.
# sample_hierarchy is the group_by sequence to reach a cluster.
def sample(df, num_clusters, sample_hierarchy):
    sample_grouped = df.groupby(sample_hierarchy)
    print("Before: " + str(len(sample_grouped.indices.keys())))
    key_sample = random.sample(sample_grouped.indices.keys(), num_clusters)
    sample = pd.DataFrame()
    for key in key_sample:
        data = sample_grouped.get_group(key).reset_index(drop=True)
        sample = data if sample.size == 0 else sample.append(data, ignore_index=True)
    print("After: " + str(len(sample.groupby(sample_hierarchy).indices.keys())))
    return sample


def plot(df, gt_context, distinguish, axes, poly):
    colors = plt.get_cmap("Set1")(np.linspace(0, 1, len(df[distinguish].unique())))
    cmapping = {}
    count = 0
    for item in df[distinguish].unique():
        if distinguish == "route":
            cmapping[str(item)] = gt_context.route_colors[item]
        else:
            cmapping[str(item)] = colors[count]
        count += 1
    grouped = df.groupby(["route", "stop", "session", "approach"])
    for item in grouped.groups.keys():
        dkey = grouped.get_group(item)[distinguish].iloc[0]
        scatter_x = grouped.get_group(item)[axes[0]].reset_index(drop=True)
        scatter_y = grouped.get_group(item)[axes[1]].reset_index(drop=True)
        plt.scatter(x=scatter_x, y=scatter_y, c=cmapping[str(dkey)], s=1)
    corcoeff_mapping = {}
    for dkey in df[distinguish].unique():
        grouped = df.groupby([distinguish])
        grouped.get_group(dkey).reset_index(drop=True)
        scatter_x = grouped.get_group(dkey)[axes[0]].reset_index(drop=True)
        scatter_y = grouped.get_group(dkey)[axes[1]].reset_index(drop=True)
        corcoeff_mapping[str(dkey)] = float(np.corrcoef(scatter_x, scatter_y)[0,1])
        if poly >= 0:
            plt.plot(np.unique(scatter_x), np.poly1d(np.polyfit(scatter_x, scatter_y, poly))(np.unique(scatter_x)), c=cmapping[str(dkey)], linewidth=4)
    plt.title("Correlator")
    plt.xlabel(axes[0])
    plt.ylabel(axes[1])
    handler = []
    for item in cmapping:
        handler.append(mpatches.Patch(color=cmapping[str(item)], label=item + " (" + str(round(corcoeff_mapping[str(item)], 2)) + ")"))
    plt.legend(handles=handler)
    plt.show()
    plt.close()

# Plot NextBus prediction vs time to show how this is a reliable metric for detecting
# arrivals, despite the fact that it is an indirect measure. Green dotted lines are validated arrivals.
def plot_validation(data):
    session_group = data.groupby(["route", "stop", "session"])
    key = random.choice(session_group.indices.keys())
    frame = session_group.get_group(key)
    plt.title("Segmented Approach " + str(key))
    plt.plot(frame["timestamp"].astype(np.int64), frame["secondsToArrival"], linewidth=3)
    #plt.plot(frame["timestamp"], frame["actualSecondsToArrival"], linewidth=3, c="y")
    #plt.plot(frame["timestamp"], frame["distance"], linewidth=2, c="b")
    plt.xlabel("Timestamp")
    plt.ylabel("Seconds to Arrival")
    plt.legend()
    for index, row in frame.iterrows():
        temp = frame["timestamp"].astype(np.int64)
        if row["newApproach"]:
            plt.axvline(x=temp[index], linewidth=2, c="r")
        if row["validated"]:
            plt.axvline(x=temp[index], linewidth=2, c="g",linestyle='--')
    plt.show()

# Plot distance versus time to show why using distance is an unreliable metric for detecting
# arrivals, despite the fact that it is a direct measure. Green dotted lines are validated arrivals.
def plot_distance(data):
    session_group = data.groupby(["route", "stop", "session"])
    key = random.choice(session_group.indices.keys())
    frame = session_group.get_group(key)
    plt.title("Bus Distance From Stop " + str(key))
    plt.plot(frame["timestamp"].astype(np.int64), frame["distance"], linewidth=3)
    plt.xlabel("Timestamp")
    plt.ylabel("Distance from Stop")
    plt.legend()
    for index, row in frame.iterrows():
        temp = frame["timestamp"].astype(np.int64)
        #if row["validated"]:
            #plt.axvline(x=temp[index], linewidth=2, c="g",linestyle='--')
    plt.show()