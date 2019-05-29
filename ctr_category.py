import pandas as pd, numpy as np
import os, glob
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


path = r"C:\Users\Domen Brunček\Desktop\FRI\4 semester\Data Mining\Project\podatki"
path = 'C:/Users/Leon/Documents/iProm_podatki/'
all_files = glob.glob(os.path.join(path, "*.csv"))
df = pd.concat((pd.read_csv(f, header=None, sep='\t', usecols=[3, 9, 12]) for f in all_files), ignore_index=True)
data = df.loc[(df[9] != 0) & (df[12] > 0)][[3,9]].groupby(9).mean().reset_index()

sortedValues= data.sort_values(by=3).values
_panoge = ["dom in vrt", "arts & entertainment", "nepremičnine",
           "careers", "Mlade družine", "Novice",
           "Sports", "law Govt & Politics", "Technology & Computing",
           "Style & Fashion", "Travel","Business", "Kulinarika"]
y_pos = np.arange(len(_panoge))


print(sortedValues)

fig, ax = plt.subplots()
ax.barh(y_pos, sortedValues[:, 1], align='center',
        color='green', ecolor='black')
ax.set_yticks(y_pos)
ax.set_yticklabels(_panoge)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('CTR')
ax.set_title('CTR per SiteCategory')
plt.plot()
plt.show()