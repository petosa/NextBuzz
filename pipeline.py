import pandas as pd
import cleaner as cleaner
import feature_engineering as fe
import analysis as analysis
from georgiatech import GeorgiaTech
import unsupervised as unsupervised

# Initialize Georgia Tech context object
gt_context = GeorgiaTech()

# Load in data
file_name = "data/big_predictions.csv"
df = pd.read_csv(file_name)

# Clean our data
df = cleaner.dedupe(df)
df, synth = cleaner.onehot(df)

# Engineer features
df = fe.heuristic(df, 10000, 40, 300, 80)
df = fe.temporal(df)
df = fe.georgiatech(df, gt_context)


# Unsupervised learning
'''
    "kmperhr",
    "numBuses",
    "layover",
    "isDeparture",
    "secondsToArrival",
    "dayOfWeek",
    "hour",
    "month",
    "minutesIntoDay",
    "isWeekend",
    "morningRush",
    "eveningRush",
    "distance",
    "classMode"
'''
subset = [
    "temperature",
    "pressure",
    "humidity",
    "visibility",
    "wind",
    "cloudCoverage"
]
# Add onehot features
#subset.extend([x for x in df.columns if x.startswith("is_")])
df["cluster"] = unsupervised.kmeans(df[subset], 3)

df.to_csv("dataset.csv", index=False)
df.iloc[100000:200000,:].to_csv("dataset_small.csv", index=False)

