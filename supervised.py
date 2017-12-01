from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import median_absolute_error
import feature_transformation as ft
import math
import pandas as pd

# A customer rolling k-fold implementation, which is capable of cross-validating
# time series data while avoiding look-ahead bias. How to interpret parameters:
# partitions=5, window = 3. ? means training set, ! means testing set.
# These are the operations that will run.
# [?|?|!| | ]
# [?|?|?|!| ]
# [?|?|?|?|!]
# rolling_kfold will average the results of these runs and return them to you.
def rolling_kfold(data, learner, config, partitions=5, window=3):
    partition_size = data.shape[0]/partitions
    
    window_start = 0
    count = 0
    nbtr_final = pd.DataFrame()
    nbte_final = pd.DataFrame()
    tr_final = pd.DataFrame()
    te_final = pd.DataFrame()
    for iteration in range(0, partitions - window + 1):
        print("\nNEW ITERATION")
        left = 0
        middle = window_start + partition_size*(window-1)
        right = window_start + partition_size*(window)
        training_set = data.iloc[left:middle]
        testing_set = data.iloc[(middle + 1):right]
        model, nbtr_err, nbte_err, tr_err, te_err = learn(training_set, testing_set, learner, config["kbest"], config["do_pca"], config["pca_only"])
        window_start += partition_size
        nbtr_final = nbtr_final.append(pd.DataFrame(nbtr_err, index=[0]))
        nbte_final = nbte_final.append(pd.DataFrame(nbte_err, index=[0]))
        tr_final = tr_final.append(pd.DataFrame(tr_err, index=[0]))
        te_final = te_final.append(pd.DataFrame(te_err, index=[0]))
        print("\n")
    
    print("*"*20)
    print("NEXTBUS TRAIN FINAL")
    print(nbtr_final.mean())
    print("TRAIN FINAL")
    print(tr_final.mean())
    print("NEXTBUS TEST FINAL")
    print(nbte_final.mean())
    print("TEST FINAL")
    print(te_final.mean())
    print("*"*20)
    print((nbte_final.mean() - te_final.mean())/nbte_final.mean())

def train_test_split(data, learner, config, percent_train=.80):
    top = 0
    middle = int(data.shape[0]*percent_train)
    bottom = data.shape[0]
    training_set = data.iloc[top:middle,:]
    testing_set = data.iloc[middle + 1:bottom,:]
    model, nbtr_err, nbte_err, tr_err, te_err = learn(training_set, testing_set, learner, config["kbest"], config["do_pca"], config["pca_only"])
    print("*"*20)
    print("NEXTBUS TRAIN FINAL")
    print(nbtr_err)
    print("TRAIN FINAL")
    print(tr_err)
    print("NEXTBUS TEST FINAL")
    print(nbte_err)
    print("TEST FINAL")
    print(te_err)
    print("*"*20)
    return model

def learn(train, test, learner, kbest, do_pca, pca_only):

    train = train.reset_index(drop=True)
    test = test.reset_index(drop=True)
    train_left = train.iloc[:,:-1]
    train_right = train.iloc[:,-1].reshape((-1,1))
    test_left = test.iloc[:,:-1]
    test_right = test.iloc[:,-1].reshape((-1,1))

    print("Training set size: " + str(train_left.shape[0]))
    print("Test set size: " + str(test_left.shape[0]))

    selected = ft.kbest(train_left, train_right, k=kbest)
    train_left = train_left[selected]
    test_left = test_left[selected]
    #print(selected)

    train_sta = train_left["secondsToArrival"]
    test_sta = test_left["secondsToArrival"]

    train_left, train_max, train_min = normalize(train_left)
    print("Max values from normalization:")
    print(list(train_max))
    print("Min values from normalization:")
    print(list(train_min))
    test_left, train_max, train_min = normalize(test_left, max=train_max, min=train_min)

    if do_pca and pca_only:
        train_left = ft.pca(train_left)
        test_left = ft.pca(test_left)
    elif do_pca:
        train_left = train_left.join(ft.pca(train_left))
        test_left = test_left.join(ft.pca(test_left))

    nbtr_err = error_report("NEXTBUS TRAIN ERROR", pd.DataFrame(train_right), train_sta)
    learner = learner.fit(train_left, train_right)
    guess = learner.predict(train_left)
    tr_err = error_report("TRAIN SET", train_right, guess)
    nbte_err = error_report("NEXTBUS TEST ERROR", pd.DataFrame(test_right), test_sta)
    guess = learner.predict(test_left)
    te_err = error_report("TEST SET", test_right, guess)

    return learner, nbtr_err, nbte_err, tr_err, te_err

def error_report(title, actual, predicted):
    err = {}
    print("**" + title + "**")
    err["mae"] = mean_absolute_error(actual, predicted)
    err["rmse"] = math.sqrt(mean_squared_error(actual, predicted))
    err["medae"] = median_absolute_error(actual, predicted)
    print("MAE: " + str(err["mae"]))
    print("RMSE: " + str(err["rmse"]))
    print("MEDAE: " + str(err["medae"]))
    return err

def normalize(df, min=None, max=None):
    if min is None:
        min = df.min(axis=0)
    if max is None:
        max = df.max(axis=0)
    temp = max - min
    temp[temp == 0] = 1
    df -= min
    df /= temp
    return df, max, min