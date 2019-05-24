import scipy.cluster.hierarchy as sch
import scipy
import numpy as np
import glob
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import NMF
import matplotlib
import matplotlib.pyplot as plt
#from Clustering.clustering_functions import KMeans
from sklearn.decomposition import PCA

path = r"C:\dataMining\1\export_2019-02-23.csv"


all_files = glob.glob(path)

df = pd.concat((pd.read_csv(f, header=0, sep='\t', usecols=[3, 10, 13], dtype={"Clicks": np.float},  names=["UserID", "AdIndustry", "Clicks"]) for f in all_files), ignore_index=True)


df = df.loc[(df["AdIndustry"] != 0)] #& (df["AdIndustry"] != "0")]
df = df.groupby(["UserID", "AdIndustry"]).sum()
df = df.loc[df["Clicks"] > 0]
df2 = df.copy().reset_index() # real clicks
del df2["AdIndustry"]
df2 = df2.groupby("UserID").sum().reset_index()
df = df.groupby(level=0).apply(lambda x: 100 * x/x.sum()).reset_index()
df.rename(columns={df.columns[2]: "Size"}, inplace=True)

users = df["UserID"].unique() # vsi unikatni userji (no duplicates)
categories = np.arange(23)

from collections import defaultdict
vektoruser = defaultdict(dict) # slovar slovarjev

# index je row index(tega nerabmo)
# user = UserID in SiteCategory in Size
for index, user in df.iterrows():
    vektoruser[user["UserID"]][user["AdIndustry"]] = user["Size"] # prvi slovar so userji, kljuci so slovarji kategorij vrednosr je size(procenti)

# predpripavimo matriko, tako da vse vrednosti nastavimo na 0
matrika=[]
for _ in range(0,len(users)):
    row=[]
    for _ in range(0,len(categories)):
        row.append(0)
    matrika.append(row)

# skozi vse userje (i = vrstica) in skozi vse kategorije (j = stolpec)
for i,user in enumerate(users):
    for j,category in enumerate(categories):
        if user in vektoruser and category in vektoruser[user]:
            matrika[i][j] = vektoruser[user][category]
matrika=np.array(matrika)

#print(matrika[:10, :])

k_clusters = 6
embedding = PCA(n_components=2)
dimension_reduce =  embedding.fit_transform(matrika)
kmeans = KMeans(n_clusters=k_clusters, max_iter=150).fit(dimension_reduce)
labels = kmeans.labels_
centroids = kmeans.cluster_centers_

'''
kmeans = KMeans(K=6, X=dimension_reduce, M=dimension_reduce, resolve_empty='singleton')
kmeans.initialise()
kmeans.cluster()
clustering_results = kmeans.clustering_results
labels = np.where(clustering_results == 1)[1]
'''

#plt.figure(figsize=(10, 10))
color = {0:"red", 1:"blue", 2:"yellow", 3:'green', 4:'violet', 5:'pink'}
for c, x in zip(labels, dimension_reduce):
    plt.plot(x[0], x[1], ".", color=color[c], markersize=10.0, alpha=0.2)

for x,y in centroids:
    plt.plot(x,y,"x", color="black", markersize=20.0, alpha=0.4)
plt.show()

userSkupina = { i: set() for i in range(k_clusters)}
userSkupinaProcent = { i: set() for i in range(k_clusters)}
for i,x in enumerate(users):
    userSkupina[labels[i]].add((x,df2.loc[df2["UserID"] == x].values[0][1]))

for k,v in userSkupina.items():
    vsi = sum(n for _,n in v)
    userSkupinaProcent[k].update([(x[0],x[1]/vsi) for x in v])

#model = NMF(n_components=2, init='random')
#W = model.fit_transform(matrika)
#H = model.components_