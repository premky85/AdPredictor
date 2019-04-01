import pandas as pd, numpy as np
import os, glob
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

path = 'C:/Users/leonp/Documents/iProm_podatki/'

all_files = glob.glob(os.path.join(path, "*.csv"))
df = pd.concat((pd.read_csv(f, header=None, sep='\t', usecols=[1,12,13]) for f in all_files), ignore_index=True)


data = df.loc[df[12] > 0].groupby(1)[[1,13]].mean()
print(data)

dnevi = ['Ponedeljek', 'Torek', 'Sreda', 'Četrtek', 'Petek', 'Sobota', 'Nedelja']
y_pos = np.arange(len(dnevi))
clicks = data.values[:, 1]


ax = plt.axes()
ax.yaxis.set_major_formatter(ticker.PercentFormatter(1.0, decimals=2))


plt.bar(y_pos, clicks, align='center', alpha=0.5)
plt.xticks(y_pos, dnevi)
plt.ylabel('CTR')

plt.show()