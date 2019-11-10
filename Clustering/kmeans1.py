import numpy as np
import glob
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
class Model1:

    def __init__(self,path, testing):
        self.path = path
        self.all_files = glob.glob(path)
        self.df, self.df2, self.df_site_category = self.read_to_df(self.all_files)
        self.k_clusters = 6
        self.categories = np.arange(23)
        self.testing = testing
        self.users = ""
        self.labels = ""
        self.centroids = ""
        self.dimension_reduce = ""
        self.userSkupina = ""

    def read_to_df(self,all_files):
        df = pd.concat((pd.read_csv(f, header=0, sep='\t', usecols=[3, 9, 10, 13], dtype={"Clicks": np.float},  names=["UserID", "SiteCategory", "AdIndustry", "Clicks"]) for f in all_files), ignore_index=True)
        df = df.loc[(df["AdIndustry"] != 0)] #& (df["AdIndustry"] != "0")]
        d = df.copy()
        df = df.drop(columns=["SiteCategory"])
        df_site_category = d.loc[d["SiteCategory"] != 0].drop(columns=["UserID"])
        df_site_category = df_site_category.groupby(["SiteCategory", "AdIndustry"]).sum()

        #df_site_category = df_site_category
        df = df.groupby(["UserID", "AdIndustry"]).sum()
        df = df.loc[df["Clicks"] > 0]
        df_site_category = df_site_category.loc[df_site_category["Clicks"] > 0]
        df_site_category = df_site_category.groupby(level=0).apply(lambda x: 100 * x / x.sum()).reset_index()
        pomozni = df.copy().reset_index()
        #df2 = df.copy().reset_index() # real clicks
        #del df2["AdIndustry"]
        #df2 = df2.groupby("UserID").sum().reset_index()
        df = df.groupby(level=0).apply(lambda x: 100 * x/x.sum()).reset_index()
        df.rename(columns={df.columns[2]: "Size"}, inplace=True)
        df_site_category.rename(columns={df_site_category.columns[2]: "Size"}, inplace=True)
        #self.df = df
        #self.df2 = df2
        return df, pomozni, df_site_category


    def build_matrix_1(self):
        from collections import defaultdict
        self.users = self.df["UserID"].unique() # vsi unikatni userji (no duplicates)

        vektoruser = defaultdict(dict) # slovar slovarjev

        # index je row index(tega nerabmo)
        # user = UserID in SiteCategory in Size
        for index, user in self.df.iterrows():
            vektoruser[user["UserID"]][user["AdIndustry"]] = user["Size"] # prvi slovar so userji, kljuci so slovarji kategorij vrednosr je size(procenti)

        # predpripavimo matriko, tako da vse vrednosti nastavimo na 0
        matrika=[]
        for _ in range(0,len(self.users)):
            row=[]
            for _ in range(0,len(self.categories)):
                row.append(0)
            matrika.append(row)

        # skozi vse userje (i = vrstica) in skozi vse kategorije (j = stolpec)
        for i,user in enumerate(self.users):
            for j,category in enumerate(self.categories):
                if user in vektoruser and category in vektoruser[user]:
                    matrika[i][j] = vektoruser[user][category]
        return np.array(matrika), self.users

    def build_ad_site_corelation(self):
        from collections import defaultdict
        site_categories = self.df_site_category["SiteCategory"].unique()  # vse unikatni kategorije spletnih strani (no duplicates)

        vektor_site_categories = defaultdict(dict)  # slovar slovarjev

        # index je row index(tega nerabmo)
        # user = UserID in SiteCategory in Size
        for index, site_cat in self.df_site_category.iterrows():
            vektor_site_categories[site_cat["SiteCategory"]][site_cat["AdIndustry"]] = site_cat[
                "Size"]  # prvi slovar so userji, kljuci so slovarji kategorij vrednosr je size(procenti)

        # predpripavimo matriko, tako da vse vrednosti nastavimo na 0
        matrika = []
        for _ in range(0, len(site_categories)):
            row = []
            for _ in range(0, len(self.categories)):
                row.append(0)
            matrika.append(row)

        # skozi vse userje (i = vrstica) in skozi vse kategorije (j = stolpec)
        for i, site_cat in enumerate(site_categories):
            for j, category in enumerate(self.categories):
                if site_cat in site_categories and category in vektor_site_categories[site_cat]:
                    matrika[i][j] = vektor_site_categories[site_cat][category]
        return np.array(matrika), site_categories

    def kmeans(self, k, iter):
        self.k_clusters = k
        matrika = self.build_matrix_1()[0]
        if not self.testing:
            embedding = PCA(n_components=2)
            self.dimension_reduce =  embedding.fit_transform(matrika)
            kmeans = KMeans(n_clusters=self.k_clusters, max_iter=iter).fit(self.dimension_reduce)
        else:
            kmeans = KMeans(n_clusters=self.k_clusters, max_iter=iter).fit(matrika)
        self.labels = kmeans.labels_
        self.centroids = kmeans.cluster_centers_



    '''
    kmeans = KMeans(K=6, X=dimension_reduce, M=dimension_reduce, resolve_empty='singleton')
    kmeans.initialise()
    kmeans.cluster()
    clustering_results = kmeans.clustering_results
    labels = np.where(clustering_results == 1)[1]
    '''
    def plot(self):
        color = {0:"red", 1:"blue", 2:"yellow", 3:'green', 4:'violet', 5:'pink', 6: 'black'}
        for c, x in zip(self.labels, self.dimension_reduce):
            plt.plot(x[0], x[1], ".", color=color[c], markersize=10.0, alpha=0.2)

        for x,y in self.centroids:
            plt.plot(x,y,"x", color="black", markersize=20.0, alpha=0.4)
        plt.show()

    def results(self):
        matrika = []
        for _ in range(self.k_clusters):
            row = []
            for _ in self.categories:
                row.append(0)
            matrika.append(row)

        self.userSkupina = { i: set() for i in range(self.k_clusters)}

        for i,x in enumerate(self.users):
            poizvedba = self.df2.loc[self.df2["UserID"] == x]
            kliki = poizvedba["Clicks"].sum()
            self.userSkupina[self.labels[i]].add((x,kliki))

        for k,v in self.userSkupina.items(): # k = gruca a.k.a vrstice
            vsi = sum(n for _,n in v)    # vsi kliki v gruci
            for i in self.categories:    # za vsako kategorijo
                sestevek = 0
                for user,_ in v:         # za vsakega userja v gruci gledam koliko klikov na kategorijo ma
                    sql = self.df2.loc[(self.df2["UserID"] == user) & (self.df2["AdIndustry"] == i)]
                    if not sql.empty:
                        sestevek += sql.values[0][2]
                if vsi != 0:
                    matrika[k][i] = sestevek/vsi
                else: matrika[k][i] = 0
        return np.array(matrika), self.centroids


#modelMario = Model1(r"C:\Users\leonp\Documents\iProm_podatki\1\export_2019-03-18.csv", testing=True)
#n = modelMario.build_ad_site_corelation()
#modelMario.kmeans(k=25,iter=150)
#print(modelMario.results())
