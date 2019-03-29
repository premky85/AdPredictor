import pandas
import datetime

def read_data(t, file):
    return pandas.read_csv(file, delimiter='\t', usecols=t).values







