import pandas as pd
import glob
import os

path = r"C:\Users\leonp\Documents\iProm_podatki"
path = r"C:\Users\Leon\Documents\iProm_podatki\export_2019-02-23.csv"

all_files = glob.glob(path)#os.path.join(path, "*.csv"))
df = pd.concat((pd.read_csv(f, header=None, sep='\t', usecols=[3, 13], names=["userID", "Clicks"]) for f in all_files), ignore_index=True)

df1 = df.groupby(["userID"]).sum().reset_index()
df1 = df1[df1["Clicks"] != 0]
df1.to_csv(r"C:\Users\Leon\Documents\iProm_podatki\test\users_1.csv", "\t", header=["userID", "Clicks"])

df2 = df.groupby(["userID"]).sum().reset_index()
df2 = df2[df2["Clicks"] == 0]
df2.to_csv(r"C:\Users\Leon\Documents\iProm_podatki\test\users_0.csv", "\t", header=["userID", "Clicks"])
