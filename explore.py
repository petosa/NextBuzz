

import analysis
from georgiatech import GeorgiaTech
import pandas as pd

gt_context = GeorgiaTech()

df = pd.read_csv("dataset_small.csv")

print()



# Plot data
df_sample = analysis.sample(df, 1000, ["route", "stop", "session", "approach"])
analysis.plot(df_sample, gt_context, "route", ("actualSecondsToArrival", "abserror"), 1)
'''
analysis.plot(df_sample, gt_context, "route", ("isDeparture", "actualSecondsToArrival"), 3)
analysis.plot(df_sample, gt_context, "route", ("wind", "actualSecondsToArrival"), 3)
analysis.plot(df_sample, gt_context, "route", ("pressure", "actualSecondsToArrival"), 3)
analysis.plot(df_sample, gt_context, "route", ("humidity", "actualSecondsToArrival"), 3)
analysis.plot(df_sample, gt_context, "route", ("visibility", "actualSecondsToArrival"), 3)
analysis.plot(df_sample, gt_context, "route", ("secondsToArrival", "actualSecondsToArrival"), 2)
analysis.plot(df_sample, gt_context, "cluster", ("secondsToArrival", "actualSecondsToArrival"), 2)

'''
# Ancillary plots, showing heuristic validation and distance validation
df_sample = analysis.sample(df, 10, ["route", "stop", "session"])
analysis.plot_validation(df_sample)
for x in range(0,10):
    analysis.plot_distance(df_sample)
