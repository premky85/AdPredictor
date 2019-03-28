from beri_podatke import read_data as read
import matplotlib.pyplot as plt
import numpy as np
import os

path = 'C:/Users/leonp/Documents/iProm_podatki/'


files = [] #["C:/Users/Leon/Documents/iProm_podatki/export_2019-03-09.csv", "C:/Users/Leon/Documents/iProm_podatki/export_2019-03-10.csv", "C:/Users/Leon/Documents/iProm_podatki/export_2019-03-11.csv",
         #"C:/Users/Leon/Documents/iProm_podatki/export_2019-03-12.csv", "C:/Users/Leon/Documents/iProm_podatki/export_2019-03-13.csv", "C:/Users/Leon/Documents/iProm_podatki/export_2019-03-14.csv",
         #"C:/Users/Leon/Documents/iProm_podatki/export_2019-03-15.csv", "C:/Users/Leon/Documents/iProm_podatki/export_2019-03-16.csv", "C:/Users/Leon/Documents/iProm_podatki/export_2019-03-17.csv",
         #"C:/Users/Leon/Documents/iProm_podatki/export_2019-03-18.csv", "C:/Users/Leon/Documents/iProm_podatki/export_2019-03-19.csv", "C:/Users/Leon/Documents/iProm_podatki/export_2019-03-20.csv",
         #"C:/Users/Leon/Documents/iProm_podatki/export_2019-03-21.csv", "C:/Users/Leon/Documents/iProm_podatki/export_2019-03-22.csv", "C:/Users/Leon/Documents/iProm_podatki/export_2019-03-23.csv",
         #"C:/Users/Leon/Documents/iProm_podatki/export_2019-03-24.csv"]

for r, d, f in os.walk(path):
    for file in f:
        if '.csv' in file:
            files.append(os.path.join(r, file))

data = read([5, 13], files[0])
data = np.array([[x, y] for [x, y] in data[:, [0, 1]] if x > 0 and y > 0])
i = 1
print(i)

for file in files[1:]:
    temp = read([5, 13], file)
    temp = np.array([[x, y] for [x, y] in temp[:, [0, 1]] if x > 0 and y > 0])
    data = np.concatenate((data, temp))
    i += 1
    print(i)
#data = np.sort(data, axis=0)
#data = data[data[:, 1].argsort()][::-1]
#data = data[:-1]
#print(data)




plt.scatter(data[:, 0], data[:, 1], 1)
plt.xlabel("ID_kampanje")
plt.ylabel('stevilo_klikov')
plt.show()