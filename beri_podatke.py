import pandas
import datetime

'''dtype=[('date', datetime.datetime), ('dayOfWeek', int), ('timeFrame', int), ('userID', int), ('siteID', int), ('campaignID', int), ('adID', int), ('zoneID', int), ('masterSiteID', int), ('siteCategory', int), ('adIndustry', int), ('requests', int), ('views', int), ('clicks', int)]'''


def read_data(t, file):
    return pandas.read_csv(file, delimiter='\t' ).values[:, t]







