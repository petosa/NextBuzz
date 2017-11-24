from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import pandas as pd
import numpy as np

# Remove all duplicate entries. This happens when we requery too fast,
# and NextBus does not get a chance to update.
def dedupe(df):
    before = df.shape[0]
    df = df.drop_duplicates(subset=["timestamp", "route", "stop"], keep="first").reset_index(drop=True)
    print("Removed " + str(before - df.shape[0]) + " duplicates.")
    print("There are " + str(df.shape[0]) + " instances.")
    return df

# Categorical -> One Hot
def onehot(df):
    synthesized_features = []
    if onehot:
        for column in df.columns:
            if df[column].dtype == np.object:
                lenc = LabelEncoder()
                le = lenc.fit_transform(df[column])
                new_df = pd.DataFrame(OneHotEncoder(sparse=True).fit_transform(le.reshape(-1, 1)).toarray())
                new_features = ["is_" + x for x in lenc.classes_]
                new_df.columns = new_features
                synthesized_features.append(new_features)
                df = df.join(new_df)
    return df, synthesized_features