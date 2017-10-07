import pandas as pd
with open("predictions.csv", "r") as file:
    csv = pd.read_csv(file)
    print(csv)
