import pandas as pd
import glob
import os


path = r"C:\Users\leonp\OneDrive\Documents\PycharmProjects\PR19_LP_MB_DB\Clustering\test\export_2019-02-23.csv"


all_files = glob.glob(path)

df = pd.concat((pd.read_csv(f, header=None, sep='\t', usecols=[3, 9], names=["UserID", "SiteCategory"]) for f in all_files), ignore_index=True)


df = df.loc[(df["SiteCategory"] != 0) & (df["SiteCategory"] != "0")]
df = df.groupby(["UserID", "SiteCategory"]).size()
df = df.groupby(level=0).apply(lambda x: 100 * x/float(x.sum()))
print(df)


