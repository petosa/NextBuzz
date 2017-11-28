import pandas as pd
from sklearn.externals import joblib
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import median_absolute_error
import math

maxes = [5939.0, 90.369132314, 1.0, 1.0, 2.0, 1.0, 1.0, 1439.0, 29.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
mins = [0.0, 9.99999997475e-07, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


df = pd.read_csv("../dataset.csv")
model = joblib.load("../model.pkl")



# Features to train on
subset = [
    "secondsToArrival",
    "distance",
    "layover",
    "isDeparture",
    "classMode",
    "morningRush",
    "eveningRush",
    "minutesIntoDay",
    "kmperhr"
]
# Add onehot features
subset.extend([x for x in df.columns if x.startswith("is_")])
subset = subset[:-8] # Delete weather variables
# Add class
subset.append("actualSecondsToArrival")

df =df[subset]

percent_train = .9
middle = int(df.shape[0]*percent_train)
bottom = df.shape[0]
df = df.iloc[middle + 1:bottom,:].reset_index(drop=True)
df_left = df.iloc[:,:-1]
maxes_np = pd.DataFrame(maxes).transpose()
mins_np = pd.DataFrame(mins).transpose()
temp = maxes_np - mins_np
temp[temp == 0] = 1

df_left = df_left.values - mins_np.values

df_left /= temp

df_right = df.iloc[:,-1].reshape((-1,1))
#print df_left
guess = model.predict(df_left)

guess = pd.DataFrame(guess.transpose().reshape((-1,1)))
guess.columns = ["myPrediction"]

df = df.join(guess)
df = df[["actualSecondsToArrival", "secondsToArrival", "myPrediction"]]
df["theirError"] = df["actualSecondsToArrival"] - df["secondsToArrival"]
df["myError"] = df["actualSecondsToArrival"] - df["myPrediction"]
df["myErrorAbs"] = abs(df["myError"])
df["theirErrorAbs"] = abs(df["theirError"])


print "them"
err = {}
predicted = df["secondsToArrival"]
err["mae"] = mean_absolute_error(df["actualSecondsToArrival"], predicted)
err["rmse"] = math.sqrt(mean_squared_error(df["actualSecondsToArrival"], predicted))
err["medae"] = median_absolute_error(df["actualSecondsToArrival"], predicted)
print err

print "me"
err = {}
predicted = df["myPrediction"]
err["mae"] = mean_absolute_error(df["actualSecondsToArrival"], predicted)
err["rmse"] = math.sqrt(mean_squared_error(df["actualSecondsToArrival"], predicted))
err["medae"] = median_absolute_error(df["actualSecondsToArrival"], predicted)
print err


df.to_csv("errors.csv", index=False)

print df


