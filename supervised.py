# A customer rolling k-fold implementation, which is capable of cross-validating
# time series data while avoiding look-ahead bias. How to interpret parameters:
# partitions=5, window = 3. ? means training set, ! means testing set.
# These are the operations that will run.
# [?|?|!| | ]
# [ |?|?|!| ]
# [ | |?|?|!]
# rolling_kfold will average the results of these runs and return them to you.
def rolling_kfold(data, learner, partitions=5, window=3):
    partition_size = data.shape[0]/partitions
    print partition_size
    window_start = 0
    for iteration in range(0, partitions - window + 1):
        left = window_start
        middle = window_start + partition_size*(window-1)
        right = window_start + partition_size*(window)
        training_set = data.iloc[left:middle]
        testing_set = data.iloc[(middle + 1):right]
        print left
        print middle
        print right
        print "rest"
        window_start += partition_size
