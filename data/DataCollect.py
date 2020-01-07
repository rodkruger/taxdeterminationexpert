import pandas as pd

data = pd.read_csv("/home/rkruger/Downloads/merge_nfitems.csv")

for col in data.columns:
    print(col)