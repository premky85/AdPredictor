from beri_podatke import read_data as read
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from scipy.stats import chi
from scipy import stats


path = 'C:/Users/Leon/Documents/iProm_podatki/'


files = []

for r, d, f in os.walk(path):
    for file in f:
        if '.csv' in file:
            files.append(os.path.join(r, file))

data = read([3, 13], files[0])
i = 1
print(i)

for file in files[1:]:
    temp = read([3, 13], file)
    data = np.concatenate((data, temp))
    i += 1
    print(i)

df = pd.DataFrame(data, columns=['user', 'CTR'])
df = df.groupby(['user']).mean().reset_index()
df = df[df.CTR > 0]

df = df.mul([1, 100])
'''
data = df.to_numpy()
print(np.signbit(data).any())
print(np.isfinite(data).all())
print((data < 0).any())

#lnspc = np.linspace(0, 2, len(data))

lnspc = np.linspace(chi.ppf(0.01, df),
                 chi.ppf(1.99, df), len(data))

parameters = chi.fit(data)
#P_fit = [chi.pdf(x, *parameters) for x in lnspc]


#plt.plot(lnspc, P_fit, label="P(X) ocenjena", linewidth=2.0)
ax.plot(lnspc, chi.pdf(lnspc, df['CTR']),
        'r-', lw=5, alpha=0.6, label='chi pdf')
'''
ax = df['CTR'].hist(bins=30, range=[0, 2])
ax.set_xlabel("CTR")
ax.set_ylabel("Number of users")
plt.show(block=True)


