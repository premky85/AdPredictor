import math

import pandas as pd
import glob
import os
from Clustering import kmeans1 as KMeans_1
from Clustering import kmeans_0 as KMeans_0
import Clustering.read_files
from sklearn.decomposition import PCA


path = r"C:\Users\leonp\Documents\iProm_podatki"

all_files = glob.glob(os.path.join(path, "*.csv"))
for f in all_files[:10]:

    Clustering.read_files.read_file(f)

    df = pd.read_csv(f, header=None, sep='\t',
                     names=["Date", "DayOfWeek", "TimeFrame", "UserID", "SiteID", "CampaignID", "AdID", "ZoneID",
                            "MasterSiteID", "SiteCategory", "AdIndustry", "Requests", "Views", "Clicks"],
                     index_col=False)




    test_df = df.tail(round(0.4 * df.shape[0]))
    a = round(0.5 * test_df.shape[0])
    t = test_df.tail(round(0.5 * test_df.shape[0]))
    Clustering.read_files.read_file_learn_about_users(f)


    file_name = os.path.basename(f)
    kmeans_0 = KMeans_0.ModelUsersWithNoClicks(r"C:\Users\leonp\Documents\iProm_podatki\0" + "\\" + file_name)

    kmeans_1 = KMeans_1.Model1(r"C:\Users\leonp\Documents\iProm_podatki\1" + "\\" + file_name)

    test_0 = KMeans_0.ModelUsersWithNoClicks(r"C:\Users\leonp\Documents\iProm_podatki\0" + "\\test_" + file_name).make_matrix()
    test_1 = KMeans_1.Model1(r"C:\Users\leonp\Documents\iProm_podatki\1" + "\\test_" + file_name).build_matrix_1()


    print(test_1[0])
    print(test_1[1])

    print(test_0[0])
    print(test_0[1])

    #clusters_0 =
    #clusters_1 =

    for x in t["UserID"]:



        if x in test_1[1]:

            distance = [math.sqrt(sum([(a - b) ** 2 for a, b in zip(test_1[1].indeof(x["UserID"]), y)])) for y in clusters_0]


        #TODO: Find nearest centroid and get







