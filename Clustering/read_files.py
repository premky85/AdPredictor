import pandas as pd
import glob
import os

path = r"C:\Users\leonp\Documents\iProm_podatki"

all_files = glob.glob(os.path.join(path, "*.csv"))
df = pd.concat((pd.read_csv(f, header=None, sep='\t', usecols=[3, 13], names=["userID", "Clicks"]) for f in all_files), ignore_index=True)
df = df.groupby(["userID"]).sum().reset_index()
df = df[df["Clicks"] > 0]
df.to_csv("./test/test.csv", "\t", header=["userID", "Clicks"])
print(df.shape)

print(df)