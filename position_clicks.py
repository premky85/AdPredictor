from beri_podatke import read_data as read
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

path = 'C:/Users/leonp/Documents/iProm_podatki/'


files = []

for r, d, f in os.walk(path):
    for file in f:
        if '.csv' in file:
            files.append(os.path.join(r, file))

data = read([7, 13], files[0])
#data = np.array([[x, y] for [x, y] in data[:, [0, 1]]])
i = 1
print(i)

for file in files[1:]:
    temp = read([7, 13], file)
    #temp = np.array([[x, y] for [x, y] in temp[:, [0, 1]]])
    data = np.concatenate((data, temp))
    i += 1
    print(i)

print(data)

df = pd.DataFrame(data, columns=['zone', 'click'])
df = df.groupby(['zone']).mean().reset_index()
df = df.sort_values(by=['click'], ascending=False)
df.describe()

data = df.to_numpy()

data = data[data[:, 1] > 0]
indexes = np.arange(len(data[:, 0]))
print(indexes)


plt.bar(indexes, data[:, 1])
plt.xlabel("polozaj")
plt.ylabel('CTR')
plt.show()