import os

import  pandas as pd
import glob

path = r"C:\Users\leonp\Documents\iProm_podatki"


all_files = glob.glob(os.path.join(path, "*.csv"))
df = pd.concat((pd.read_csv(f, header=None, sep='\t', usecols=[3, 13], names=["userID", "Clicks"]) for f in all_files), ignore_index=True)

total_clicks = df

#TODO get original acc