import pandas as pd
import cleaner as cleaner
import feature_engineering as fe
import analysis as analysis
from georgiatech import GeorgiaTech
import unsupervised as unsupervised
import supervised as supervised

# Initialize Georgia Tech context object
gt_context = GeorgiaTech()

# Load in data
file_name = "data/big_predictions.csv"
df = pd.read_csv(file_name)

# Clean our data
df = cleaner.clean(df, onehot=True)

# Engineer features
df = fe.heuristic(df, 10000, 40, 300, 80)
df = fe.temporal(df)
df = fe.georgiatech(df, gt_context)

print(list(df.columns))

'''
# Unsupervised learning
cluster_features = ["stop", "route", ""]
subset = df[["secondsToArrival", "wind", "temperature", "cloudCoverage", "pressure", "humidity"]]
df["cluster"] = unsupervised.kmeans(subset, 5)
'''

'''
# Supervised Learning
supervised.rolling_kfold(df, None)
'''

'''
# Plot data
df_sample = analysis.sample(df, 2000, ["route", "stop", "session", "approach"])
analysis.plot(df_sample, gt_context, "route", ("numBuses", "abserror"), 3)
analysis.plot(df_sample, gt_context, "route", ("cloudCoverage", "abserror"), 3)
analysis.plot(df_sample, gt_context, "route", ("wind", "abserror"), 3)
analysis.plot(df_sample, gt_context, "route", ("pressure", "abserror"), 3)
analysis.plot(df_sample, gt_context, "route", ("humidity", "abserror"), 3)
analysis.plot(df_sample, gt_context, "route", ("visibility", "abserror"), 3)
analysis.plot(df_sample, gt_context, "route", ("secondsToArrival", "abserror"), 2)
analysis.plot(df_sample, gt_context, "cluster", ("secondsToArrival", "abserror"), 2)
'''

'''
# Ancillary plots, showing heuristic validation and distance validation
df_sample = analysis.sample(df, 1, ["route", "stop", "session"])
#analysis.plot_validation(df_sample)
#analysis.plot_distance(df_sample)
'''