from beri_podatke import read_data as read
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

path = 'C:/Users/Leon/Documents/iProm_podatki/'


files = []

for r, d, f in os.walk(path):
    for file in f:
        if '.csv' in file:
            files.append(os.path.join(r, file))

data = read([3, 10], files[0])
data = np.array([[x, y] for [x, y] in data[:, [0, 1]] if x > 0 and y > 0])
i = 1
print(i)


for file in files[1:]:
    temp = read([3, 10], file)
    temp = np.array([[x, y] for [x, y] in temp[:, [0, 1]] if x > 0 and y > 0])
    data = np.concatenate((data, temp))
    i += 1
    print(i)

print(data)

#df = pd.DataFrame(data, columns=['user', 'ad_industry'])
#df = df.groupby(['user'])#.sum().reset_index()
#df = df.sort_values(by=['ocena'])
#df.describe

#print(df)

#data = df.to_numpy()


indexes = np.arange(len(data[:, 0]))
print(data)

plt.scatter(data[:, 0], data[:, 1], 1)
plt.xlabel("user_ID")
plt.ylabel('ad_industry')
plt.show()