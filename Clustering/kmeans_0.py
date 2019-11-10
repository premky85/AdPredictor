import numpy as np
import glob
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from random import randint
from collections import defaultdict
#PATH = r"C:\Users\Domen Brunček\Desktop\FRI\4 semester\Data Mining\Project\podatki\filtered_data\0\export_2019-02-23.csv"

d1 = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, 14: 14,
                           15: 15, 16: 16, 17: 17, 18: 18, 19: 19, 20: 20, 21: 21, 22: 2, 23: 23, 24: 24, 25: 25,
                           26: 26, 1000: 27, 1001: 28, 1002: 29, 1003: 30, 1004: 31, 1005: 32, 1006: 33, 1007: 34,
                           1008: 35, 1009: 36, 1010: 37}

d = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13, 14: 14,
                           15: 15, 16: 16, 17: 17, 18: 18, 19: 19, 20: 20, 21: 21, 22: 2, 23: 23, 24: 24, 25: 25,
                           26: 26, 27: 1000, 28: 1001, 29: 1002, 30: 1003, 31: 1004, 32: 1005, 33: 1006, 34: 1007,
                           35: 1008, 36: 1009, 37: 1010}

class ModelUsersWithNoClicks:
    def __init__(self, path):
        self.all_files = glob.glob(path)
        self.df, self.df2 = self.process_data()
        self.matrix_full = self.make_matrix()
        self.matrix = self.matrix_full[0]


    def process_data(self):
        original_df = pd.concat((pd.read_csv(f, header=0, sep='\t', usecols=[3, 9], names=["UserID", "SiteCategory"], dtype={"UserID": np.int64, "siteCategory": np.float}) for f in self.all_files), ignore_index=True)
        df = original_df.loc[(original_df["SiteCategory"] != 0)]
        df = df.groupby(["UserID", "SiteCategory"]).size()
        df2 = df.reset_index()
        df2.rename(columns={df2.columns[2]: "Visits"}, inplace=True)
        df = df.groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).reset_index()
        df.rename(columns={df.columns[2]: "Size"}, inplace=True)
        return df, df2

    def make_matrix(self):
        self.users = self.df["UserID"].unique()[:-1]  # vsi unikatni userji (no duplicates)
        self.categories = np.arange(38)#self.df["SiteCategory"].unique()[:-1]  # vse unikatne kategorija


        vector_users = defaultdict(dict)  # slovar slovarjev
        # user = UserID in SiteCategory in Size
        for index, user in self.df.iterrows():
            vector_users[user["UserID"]][user["SiteCategory"]] = user["Size"]  # prvi slovar so userji, kljuci so slovarji kategorij vrednosr je size(procenti)

        # fill matrix rows with 0
        matrika = []
        for _ in range(0, len(self.users)):
            row = []
            for _ in range(0, len(self.categories)):
                row.append(0)
            matrika.append(row)

        # skozi vse userje (i = vrstica) in skozi vse kategorije (j = stolpec)
        for i, user in enumerate(self.users):
            for j in self.categories:
                if user in vector_users and d[j] in vector_users[user]:
                    matrika[i][j] = vector_users[user][d[j]]
        return np.array(matrika), self.users

    def kMeans(self, k, plot=False, testing=False):
        self.k_clusters = k
        if not testing:
            embedding = PCA(n_components=2)
            self.dimension_reduce =  embedding.fit_transform(self.matrix)
            kmeans = KMeans(n_clusters=k, max_iter=150).fit(self.dimension_reduce)
        else:
            kmeans = KMeans(n_clusters=k, max_iter=150).fit(self.matrix)



        colors = ["#%06X" % randint(0, 0xFFFFFF) for i in range(k)]
        self.labels = kmeans.labels_
        self.centroids = kmeans.cluster_centers_
        #if plot: self.plot(dimension_reduce, colors, self.labels, self.centroids)

    def plot(self, dimensions, colors, labels, centroids):
        #print("plot")
        for c, x in zip(labels, dimensions):
            plt.plot(x[0], x[1], ".", color=colors[c], markersize=10.0)
        for x, y in centroids:
            plt.plot(x, y, "x", markersize=5, color="black")
        plt.show()
        #print("plotted")

    def show_df(self):
        print(self.matrix)

    def results(self):
        matrika = []
        for _ in range(self.k_clusters):
            row = []
            for _ in self.categories:
                row.append(0)
            matrika.append(row)

        self.userSkupina = {i: set() for i in range(self.k_clusters)}

        for i, x in enumerate(self.users):
            poizvedba = self.df2.loc[self.df2["UserID"] == x]
            views = poizvedba["Visits"].sum()
            self.userSkupina[self.labels[i]].add((x, views))

        for k, v in self.userSkupina.items():  # k = gruca a.k.a vrstice
            vsi = sum(n for _, n in v)  # vsi kliki v gruci
            for i in self.categories:  # za vsako kategorijo
                sestevek = 0
                for user, _ in v:  # za vsakega userja v gruci gledam koliko klikov na kategorijo ma
                    sql = self.df2.loc[(self.df2["UserID"] == user) & (self.df2["SiteCategory"] == i)]
                    if not sql.empty:
                        sestevek += sql.values[0][2]
                if vsi != 0:
                    z = np.where(self.categories == i)[0][0]
                    matrika[k][z] = sestevek / vsi
                else:
                    matrika[k][i] = 0
        return np.array(matrika), self.centroids
        #return None





#a = ModelUsersWithNoClicks(r"C:\Users\leonp\Documents\iProm_podatki\export_2019-02-23.csv")
#a.kMeans(5, testing=True)
#results = a.results()
#m = a.matrix

#TODO speed up the code !!!!!!!

