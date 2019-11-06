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
siteCategory_adIndustry = {1: 9, 2: 1, 3: 11, 4: 5, 6: 6, 7: 9, 8: 4, 9: 15, 10: 18, 11: 7, 12: 8, 13: 14, 14: 16,
                           15: 15, 16: 12, 17: 15, 18: 11, 19: 15, 20: 12, 21: 15, 22: 17, 23: 15, 24: 15, 25: 15,
                           26: 15, 1000: 18, 1001: 18, 1002: 15, 1003: 13, 1004: 7, 1005: 10, 1006: 14, 1007: 9,
                           1008: 21, 1009: 22, 1010: 13}
observed_0 = 0
observed_1 = 0
hit_0 = 0
hit_1 = 0
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




    test_df_ = df.tail(round(0.4 * df.shape[0]))
    #a = round(0.5 * test_df.shape[0])
    #t = test_df.tail(round(0.5 * test_df.shape[0]))
    Clustering.read_files.read_file_learn_about_users(f)


    kmeans_0 = KMeans_0.ModelUsersWithNoClicks(r"C:\Users\leonp\Documents\iProm_podatki\0" + "\\" + file_name)
    print("Model 0 created")
    kmeans_1 = KMeans_1.Model1(r"C:\Users\leonp\Documents\iProm_podatki\1" + "\\" + file_name, testing=True)
    print("Model 1 created")

    test_df_0 = KMeans_0.ModelUsersWithNoClicks(r"C:\Users\leonp\Documents\iProm_podatki" + "\\test_" + file_name).matrix_full
    test_df_1 = KMeans_1.Model1(r"C:\Users\leonp\Documents\iProm_podatki" + "\\test_" + file_name, testing=True).build_matrix_1()

    matrix_0 = kmeans_0.matrix_full
    print("Matrix 0 built")
    #test_1 = KMeans_1.Model1(r"C:\Users\leonp\Documents\iProm_podatki" + "\\test_" + file_name, testing=True).build_matrix_1()
    matrix_1 = kmeans_1.build_matrix_1()
    print("Matrix 1 built")

    #print(test_1[0])
    #print(test_1[1])

    #print(test_0[0])
    #print(test_0[1])

    #clusters_0 =

    #lala = t[t["Clicks"] != 0]

    kmeans_0.kMeans(5, testing=True)
    results_0, clusters_0 = kmeans_0.results()
    print("KMeans 0 done")

    kmeans_1.kmeans(k=6, iter=150)
    results_1, clusters_1 = kmeans_1.results()
    print("KMeans 1 done")
    for _, x_ in test_df_.iterrows():
        x = x_["UserID"]
        if x in matrix_1[1] and x_["Clicks"] != 0 and x_["AdIndustry"] != 0:
            observed_1 += 1
            zx = np.where(test_df_1[1] == x)[0]
            z = test_df_1[0][zx]
            distances = [distance.euclidean(z, y) for y in clusters_1]

            result = distances.index(min(distances))
            result_category = np.where(results_1[result] == np.max(results_1[result]))[0][0]

            if result_category == x_["AdIndustry"]:
                hit_1 += 1
            print("guessed_1: ", hit_1, "observed_1: ", observed_1, "Predicted: ",  result_category, "Actual: ", x_["AdIndustry"])

        elif x in matrix_0[1] and x_["Clicks"] != 0 and x_["SiteCategory"] != 0 and x_["AdIndustry"] != 0:
            observed_0 += 1
            zx = np.where(test_df_0[1] == x)[0]
            z = test_df_0[0][zx]
            distances = [distance.euclidean(z, y) for y in clusters_0]

            result = distances.index(min(distances))
            result_category = np.where(results_0[result] == np.max(results_0[result]))[0][0]

            if siteCategory_adIndustry[result_category] == x_["AdIndustry"]:
                hit_0 += 1
            print("guessed_0: ", hit_0, "observed_0: ", observed_0, "Predicted: ",  siteCategory_adIndustry[result_category], "Actual: ", x_["AdIndustry"])



    print("Percentage: ",  (hit_1 + hit_0) / (observed_1 + observed_0) * 100)
    print()

prediction_ratio = (hit_1 + hit_0) / (observed_1 + observed_0) * 100

print("Model has ", prediction_ratio, "% ratio.")
