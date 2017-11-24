import pandas as pd
import supervised
from sklearn import tree, ensemble, neural_network

df = pd.read_csv("dataset.csv")

#df = df.iloc[100000:200000,:].reset_index(drop=True)

# Features to train on
subset = [
    "secondsToArrival",
    "distance",
    "layover",
    "isDeparture",
    "minutesIntoDay",
    "cluster"
]
'''
    "kmperhr",
    "numBuses",
    "layover",
    "isDeparture",
    "secondsToArrival",
    "temperature",
    "pressure",
    "humidity",
    "visibility",
    "wind",
    "cloudCoverage",
    "dayOfWeek",
    "hour",
    "month",
    "minutesIntoDay",
    "isWeekend",
    "distance",
    "cluster"
'''

# Add onehot features
subset.extend([x for x in df.columns if x.startswith("is_")])
subset = subset[:-8] # Delete weather variables
# Add class
subset.append("actualSecondsToArrival")
print(subset)
print(len(subset))
df =df[subset]
config = {
    "do_pca": False,
    "pca_only": False,
    "kbest": "all",
}
#df.to_csv("dataset_clean.csv", index=False)
learner1 = tree.DecisionTreeRegressor(min_samples_split=300)
#learner = neural_network.MLPRegressor(hidden_layer_sizes=(3,3,3,3,3,3,3,3,3,3,3))
learner = ensemble.BaggingRegressor(base_estimator=learner1, n_estimators=100)
#learner = ensemble.AdaBoostRegressor(n_estimators=300)
supervised.rolling_kfold(df, learner, config, partitions=10, window=6)
#supervised.rolling_kfold(df, None)
#supervised.train_test_split(df, tree.DecisionTreeRegressor(min_samples_split=500))
#supervised.train_test_split(df[subset], ensemble.BaggingRegressor(n_estimators=20), kbest=8)
#supervised.train_test_split(df[subset], neighbors.NearestNeighbors())
#supervised.train_test_split(df[subset], neural_network.MLPRegressor(hidden_layer_sizes=()))
