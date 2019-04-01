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

data = read([5, 13], files[0])
i = 1
print(i)

for file in files[1:]:
    temp = read([5, 13], file)
    data = np.concatenate((data, temp))
    i += 1
    print(i)

print(data)

df = pd.DataFrame(data, columns=['kamp', 'click'])
df = df.groupby(['kamp']).mean().reset_index()
df = df.sort_values(by=['click'], ascending=False)
df.describe()

data = df.to_numpy()

data = data[data[:, 1] > 0]
indexes = np.arange(len(data[:, 0]))
print(data)

plt.bar(indexes, data[:, 1])
plt.xlabel("ID_kampanje")
plt.ylabel('CTR')
plt.show()