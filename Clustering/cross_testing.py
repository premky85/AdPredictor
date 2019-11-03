import math

import pandas as pd
import glob
import os
from Clustering import kmeans1 as KMeans_1
from Clustering import kmeans_0 as KMeans_0
import Clustering.read_files
import numpy as np
from scipy.spatial import distance
from sklearn.decomposition import PCA



path = r"C:\Users\leonp\Documents\iProm_podatki"

all_files = glob.glob(os.path.join(path, "*.csv"))

observed = 0
hit = 0
i = 0
for f in all_files[:10]:
    file_name = os.path.basename(f)
    print(i, ": ", file_name)
    i += 1

    Clustering.read_files.read_file(f)

    df = pd.read_csv(f, header=None, sep='\t',
                     names=["Date", "DayOfWeek", "TimeFrame", "UserID", "SiteID", "CampaignID", "AdID", "ZoneID",
                            "MasterSiteID", "SiteCategory", "AdIndustry", "Requests", "Views", "Clicks"],
                     index_col=False)




    test_df = df.tail(round(0.4 * df.shape[0]))
    #a = round(0.5 * test_df.shape[0])
    #t = test_df.tail(round(0.5 * test_df.shape[0]))
    Clustering.read_files.read_file_learn_about_users(f)


    kmeans_0 = KMeans_0.ModelUsersWithNoClicks(r"C:\Users\leonp\Documents\iProm_podatki\0" + "\\" + file_name)
    print("Model 0 created")
    kmeans_1 = KMeans_1.Model1(r"C:\Users\leonp\Documents\iProm_podatki\1" + "\\" + file_name, testing=True)
    print("Model 1 created")

    test_0 = KMeans_0.ModelUsersWithNoClicks(r"C:\Users\leonp\Documents\iProm_podatki\0" + "\\test_" + file_name).matrix_full
    print("Matrix 0 built")
    test_1 = KMeans_1.Model1(r"C:\Users\leonp\Documents\iProm_podatki\1" + "\\test_" + file_name, testing=True).build_matrix_1()
    print("Matrix 1 built")

    #print(test_1[0])
    #print(test_1[1])

    #print(test_0[0])
    #print(test_0[1])

    #clusters_0 =
    kmeans_1.kmeans(k=6,iter=150)
    results_1, clusters_1 = kmeans_1.results()
    print("KMeans 1 done")
    #lala = t[t["Clicks"] != 0]

    kmeans_0.kMeans(50, testing=True)
    results_0, clusters_0 = kmeans_0.results()
    print("KMeans 0 done")

    for _, x_ in test_df.iterrows():
        x = x_["UserID"]
        if x in test_1[1] and x_["Clicks"] != 0:
            observed += 1
            zx = np.where(test_1[1] == x)[0]
            z = test_1[0][zx]
            distances = [distance.euclidean(z, y) for y in clusters_1]

            result = distances.index(min(distances))
            result_category = np.where(results_1[result] == np.max(results_1[result]))[0][0]

            if result_category == x_["AdIndustry"]:
                hit += 1
            print(hit)
            
        #TODO add case for users with no clicks (choose right ad industry based on their site visits)

    print("Percentage: ",  hit / observed * 100)
    print()

prediction_ratio = hit / observed * 100

print("Model has ", prediction_ratio, "% ratio.")
