from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import pandas as pd
import numpy as np

def clean(df, onehot=True):

    # Remove all duplicate entries. This happens when we requery too fast,
    # and NextBus does not get a chance to update.
    before = df.shape[0]
    df = df.drop_duplicates(subset=["timestamp", "route", "stop"], keep="first").reset_index(drop=True)
    print("Removed " + str(before - df.shape[0]) + " duplicates.")
    print("There are " + str(df.shape[0]) + " instances.")

    # Categorical -> One Hot
    if onehot:
        for column in df.columns:
            if df[column].dtype == np.object:
                lenc = LabelEncoder()
                le = lenc.fit_transform(df[column])
                new_df = pd.DataFrame(OneHotEncoder(sparse=True).fit_transform(le.reshape(-1, 1)).toarray())
                new_df.columns = ["is_" + x for x in lenc.classes_]
                df = df.join(new_df)
    return df