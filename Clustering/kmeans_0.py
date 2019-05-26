import numpy as np
import glob
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from random import randint
from collections import defaultdict
#PATH = r"C:\Users\Domen Brunček\Desktop\FRI\4 semester\Data Mining\Project\podatki\filtered_data\0\export_2019-02-23.csv"


class ModelUsersWithNoClicks:
    def __init__(self, path):
        self.all_files = glob.glob(path)
        self.df = self.process_data()
        self.matrix = self.make_matrix()[0]


    def process_data(self):
        original_df = pd.concat((pd.read_csv(f, header=0, sep='\t', usecols=[3, 9], names=["UserID", "SiteCategory"], dtype={"UserID": np.int64, "siteCategory": np.float}) for f in self.all_files), ignore_index=True)
        df = original_df.loc[(original_df["SiteCategory"] != 0)]
        df = df.groupby(["UserID", "SiteCategory"]).size()
        df = df.groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).reset_index()
        df.rename(columns={df.columns[2]: "Size"}, inplace=True)
        return df

    def make_matrix(self):
        self.users = self.df["UserID"].unique()[:-1]  # vsi unikatni userji (no duplicates)
        categories = self.df["SiteCategory"].unique()[:-1]  # vse unikatne kategorija

        vector_users = defaultdict(dict)  # slovar slovarjev
        # user = UserID in SiteCategory in Size
        for index, user in self.df.iterrows():
            vector_users[user["UserID"]][user["SiteCategory"]] = user["Size"]  # prvi slovar so userji, kljuci so slovarji kategorij vrednosr je size(procenti)

        # fill matrix rows with 0
        matrika = []
        for _ in range(0, len(self.users)):
            row = []
            for _ in range(0, len(categories)):
                row.append(0)
            matrika.append(row)

        # skozi vse userje (i = vrstica) in skozi vse kategorije (j = stolpec)
        for i, user in enumerate(self.users):
            for j, category in enumerate(categories):
                if user in vector_users and category in vector_users[user]:
                    matrika[i][j] = vector_users[user][category]
        return np.array(matrika), self.users

    def kMeans(self, k, plot=False, testing=False):
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
        for i in range(self.matrix.shape[0]):
            a = 1




a = ModelUsersWithNoClicks(r"C:\Users\leonp\Documents\iProm_podatki\export_2019-02-23.csv")
a.kMeans(5, testing=True)
a.results()

