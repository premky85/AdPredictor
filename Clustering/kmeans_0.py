import numpy as np
import glob
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from random import randint
from collections import defaultdict
PATH = r"C:\Users\Domen Brunček\Desktop\FRI\4 semester\Data Mining\Project\podatki\filtered_data\0\export_2019-02-23.csv"


class ModelUsersWithNoClicks:
    def __init__(self, path, k, plot=False):
        self.all_files = glob.glob(path)
        self.k = k
        self.plot = plot
        self.df, self.original_df = self.process_data()
        self.categories = np.arange(38)
        self.matrix = self.make_matrix()
        self.kmeans, self.labels, self.centroids, self.colors = self.k_means()
        self.results()

    def process_data(self):
        original_df = pd.concat((pd.read_csv(f, header=0, sep='\t', usecols=[3, 9], names=["UserID", "SiteCategory"],
                                             dtype={"UserID": np.int64, "siteCategory": np.float}) for f in self.all_files), ignore_index=True)
        df = original_df.loc[(original_df["SiteCategory"] != 0)]
        df = df.groupby(["UserID", "SiteCategory"]).size()
        df = df.groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).reset_index()
        df.rename(columns={df.columns[2]: "Size"}, inplace=True)
        return df, original_df

    def make_matrix(self):
        users = self.df["UserID"].unique()[:-1]  # vsi unikatni userji (no duplicates)
        categories = self.df["SiteCategory"].unique()[:-1]  # vse unikatne kategorija

        vector_users = defaultdict(dict)  # slovar slovarjev
        # user = UserID in SiteCategory in Size
        for index, user in self.df.iterrows():
            vector_users[user["UserID"]][user["SiteCategory"]] = user["Size"]  # prvi slovar so userji, kljuci so slovarji kategorij vrednosr je size(procenti)
        matrika = np.zeros([len(users), len(categories)])

        # skozi vse userje (i = vrstica) in skozi vse kategorije (j = stolpec)
        for i, user in enumerate(users):
            for j, category in enumerate(categories):
                if user in vector_users and category in vector_users[user]:
                    matrika[i][j] = vector_users[user][category]
        return np.array(matrika)

    def k_means(self):
        """ vrne """
        embedding = PCA(n_components=2)
        dimension_reduce = embedding.fit_transform(self.matrix[:500])
        #print(dimension_reduce)

        colors = ["#%06X" % randint(0, 0xFFFFFF) for i in range(self.k)]
        kmeans = KMeans(n_clusters=self.k, max_iter=1000).fit(dimension_reduce)
        labels = kmeans.labels_
        centroids = kmeans.cluster_centers_
        if self.plot: self.plot_graph(dimension_reduce, colors, labels, centroids)
        return kmeans, labels, centroids, colors

    def results(self):
        cluster_results = np.zeros([self.k, self.categories.shape[0]])
        user_skupina = {i: set() for i in range(self.k)}
        users = self.df["UserID"].unique()


        print(self.labels)

        for i,x in enumerate(users):
            poizvedba = self.original_df.loc[self.original_df["UserID"] == x]
            categories = poizvedba['SiteCategory'].value_counts()

            print(x, categories)
            break


    @staticmethod
    def plot_graph(dimensions, colors, labels, centroids):
        print("plot")
        for c, x in zip(labels, dimensions):
            plt.plot(x[0], x[1], ".", color=colors[c], markersize=10.0)
        for x, y in centroids:
            plt.plot(x, y, "x", markersize=5, color="black")
        plt.show()
        print("plotted")

    def show_df(self):
        print(self.matrix)


a = ModelUsersWithNoClicks(PATH, 5, False)


