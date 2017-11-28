import pandas as pd
import supervised
from sklearn import tree, ensemble, neural_network
from sklearn.externals import joblib

df = pd.read_csv("dataset.csv")

#df = df.iloc[0:1000,:].reset_index(drop=True)

# Features to train on
subset = [
    "secondsToArrival",
    "distance",
    "layover",
    #"isDeparture",
    #"classMode",
    #"morningRush",
    #"eveningRush",
    "minutesIntoDay",
    #"kmperhr",
    #"dayOfWeek",
    #"pressure"
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

learner1 = tree.DecisionTreeRegressor(criterion="mse")# , min_samples_split=500)
learner = ensemble.BaggingRegressor(base_estimator=learner1, max_samples=.03, n_estimators=150)
model = supervised.train_test_split(df, learner, config, percent_train=.80)
joblib.dump(model, 'longnight.pkl')
supervised.rolling_kfold(df, learner, config, partitions=10, window=5)
