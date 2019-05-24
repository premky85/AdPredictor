
import scipy.cluster.hierarchy as sch
import scipy
import numpy as np
import glob
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from random import randint

path = r"C:\Users\Domen Brunček\Desktop\FRI\4 semester\Data Mining\Project\podatki\filtered_data\0\export_2019-02-23.csv"


all_files = glob.glob(path)

df = pd.concat((pd.read_csv(f, header=0, sep='\t', usecols=[3, 9], names=["UserID", "SiteCategory"], dtype={"UserID":np.float, "siteCategory":np.float}) for f in all_files), ignore_index=True)


df = df.loc[(df["SiteCategory"] != 0)]
df = df.groupby(["UserID", "SiteCategory"]).size()
df = df.groupby(level=0).apply(lambda x: 100 * x/float(x.sum())).reset_index() # reset_index() da mi pretvor iz series nazaj v dataframe
df.rename(columns={df.columns[2]: "Size"}, inplace=True) # zadnji stolpec, kjer so procenti preimenujem (prej ni bil poimenovan) v Size

users = df["UserID"].unique()[:-1]  # vsi unikatni userji (no duplicates)
categories = df["SiteCategory"].unique()[:-1]  #vse unikatne kategorija

from collections import defaultdict
vektoruser = defaultdict(dict)  # slovar slovarjev

siteCategories = np.array(["*Manjkajoč podatek",
"Arts & Entertainment",
"Avtomobilizem",
"Business",
"Mlade družine",
"Zdravje",
"Kulinarika",
"Hobbies & Interests",
"Dom in Vrt",
"Novice",
"Sports",
"Style & Fashion",
"Technology & Computing",
"Travel",
"Nepremičnine",
"Careers",
"Education",
"Law Govt & Politics",
"Personal Finance",
"Society",
"Science",
"Pets",
"Shopping",
"Religion and Spirituality",
"Uncategorized",
"Non Standard Content",
"Illegal Content",
"Aktivni športniki",
"Šport",
"Mladi in Najmlajši",
"Gospodarstvo in Posel",
"Lifestyle/Trendi",
"iTech & Mobile & Foto",
"Turizem",
"Prosti čas",
"Test",
"Test",
"zavarovalnistvo"])


# index je row index(tega nerabmo)
# user = UserID in SiteCategory in Size
for index, user in df.iterrows():
    vektoruser[user["UserID"]][user["SiteCategory"]] = user["Size"] # prvi slovar so userji, kljuci so slovarji kategorij vrednosr je size(procenti)

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

embedding = PCA(n_components=2)
dimension_reduce = embedding.fit_transform(matrika[:5000])
print(dimension_reduce)
'''
kmeans = KMeans(K=7, X=dimension_reduce, M=dimension_reduce, resolve_empty='singleton')
kmeans.initialise()
kmeans.cluster()
clustering_results = kmeans.clustering_results
labels = np.where(clustering_results == 1)[1]'''

print("kmeans")
k = 200
color = ["#%06X" % randint(0, 0xFFFFFF) for i in range(k)]
kmeans = KMeans(n_clusters=k, max_iter=1000).fit(dimension_reduce)
labels = kmeans.labels_
centroids = kmeans.cluster_centers_

print("plot")
#plt.figure(figsize=(10, 10))
for c, x in zip(labels, dimension_reduce):
    plt.plot(x[0], x[1], ".", color=color[c], markersize=10.0)
for x,y in centroids:
    plt.plot(x,y, "x", markersize=5, color="black")
plt.show()
print("plotted")
