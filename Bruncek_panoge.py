import pandas as pd, numpy as np
import os, glob
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


path = r"C:\Users\Domen Brunček\Desktop\FRI\4 semester\Data Mining\Project\podatki"
all_files = glob.glob(os.path.join(path, "*.csv"))
df = pd.concat((pd.read_csv(f, header=None, sep='\t', usecols=[3, 9, 12]) for f in all_files), ignore_index=True)
data = df.loc[(df[9] != 0) & (df[12] > 0)][[3,9]].groupby(9).count().reset_index()


print(data.sort_values(by=3).values)



