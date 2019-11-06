import pandas as pd
import glob
import os


#path = r"C:\Users\Leon\Documents\iProm_podatki\Filtered\export_2019-02-23.csv"

def create(path):
    #path = r"C:\Users\leonp\Documents\iProm_podatki"
    all_files = glob.glob(os.path.join(path, "*.csv"))

    df = pd.concat((pd.read_csv(f, header=None, sep='\t', usecols=[3, 9], names=["UserID", "SiteCategory"]) for f in all_files), ignore_index=True)


    df = df.loc[(df["SiteCategory"] != 0) & (df["SiteCategory"] != "0")]
    df = df.groupby(["UserID", "SiteCategory"]).size()
    df = df.groupby(level=0).apply(lambda x: 100 * x/float(x.sum()))
    #print(df)

create(r"C:\Users\leonp\Documents\iProm_podatki")

