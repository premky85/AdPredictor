import pandas
import datetime

def read_data(t, file):
    return pandas.read_csv(file, delimiter='\t', usecols=t).values

def read_data_pd(t, file):
    if len(t) > 0:
        return pandas.read_csv(file, delimiter='\t', usecols=t)
    else:
        return pandas.read_csv(file, delimiter='\t')






