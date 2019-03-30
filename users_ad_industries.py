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

data = read([3, 10, 12], files[0])
data = np.array([[x, y] for [x, y, z] in data[:, [0, 1, 2]] if x > 0 and y > 0 and z > 1])
i = 1
print(i)




for file in files[1:]:
    temp = read([3, 10, 12], file)
    temp = np.array([[x, y] for [x, y, z] in temp[:, [0, 1, 2]] if x > 0 and y > 0 and z > 1])
    data = np.concatenate((data, temp))
    i += 1
    print(i)

indexes = np.arange(len(data[:, 0]))

plt.scatter(data[:, 0], data[:, 1], [np.count_nonzero(i) for i in data[:, 1]])
plt.xlabel("user_ID")
plt.ylabel('ad_industry')
plt.show()