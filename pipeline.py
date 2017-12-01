import pandas as pd
import cleaner as cleaner
import feature_engineering as fe
import analysis as analysis
from georgiatech import GeorgiaTech
import unsupervised as unsupervised

# Initialize Georgia Tech context object
gt_context = GeorgiaTech()

# Load in data
file_name = "data/rawdata.csv"
df = pd.read_csv(file_name)

# Clean our data
df = cleaner.dedupe(df)
df, synth = cleaner.onehot(df)

# Engineer features
df = fe.heuristic(df, 10000, 40, 300, 80)
df = fe.temporal(df)
df = fe.georgiatech(df, gt_context)

df.to_csv("dataset.csv", index=False)