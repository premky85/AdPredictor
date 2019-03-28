import pandas

file = "C:/Users/Leon/Documents/iProm_podatki/export_2019-03-09.csv"

def read_data(t, file):
    return pandas.read_csv(file, delimiter='\t').values[:, t]

print(read_data([0, 2], file))






