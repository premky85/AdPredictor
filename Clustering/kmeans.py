import scipy.cluster.hierarchy as sch
import scipy
import numpy as np
import glob
import pandas as pd
from sklearn.decomposition import NMF
import matplotlib
import matplotlib.pyplot as plt
from Clustering.clustering_functions import KMeans
from sklearn.decomposition import PCA

path = r"C:\Users\Leon\Documents\iProm_podatki\Filtered\export_2019-02-23.csv"



all_files = glob.glob(path)

df = pd.concat((pd.read_csv(f, header=None, sep='\t', usecols=[3, 9], names=["UserID", "SiteCategory"]) for f in all_files), ignore_index=True)


df = df.loc[(df["SiteCategory"] != 0) & (df["SiteCategory"] != "0")]
df = df.groupby(["UserID", "SiteCategory"]).size()
df = df.groupby(level=0).apply(lambda x: 100 * x/float(x.sum())).reset_index() # reset_index() da mi pretvor iz series nazaj v dataframe
df.rename(columns={df.columns[2]: "Size"}, inplace=True) # # zadnji stolpec, kjer so procenti preimenujem (prej ni bil poimenovan) v Size

users = df["UserID"].unique()[:-1] # vsi unikatni userji (no duplicates)
categories = df["SiteCategory"].unique()[:-1] # vse unikatne kategorija

from collections import defaultdict
vektoruser = defaultdict(dict) # slovar slovarjev

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

#print(matrika[:10, :])



embedding = PCA(n_components=2)
dimension_reduce =  embedding.fit_transform(matrika[:1000, :])
print(dimension_reduce)

kmeans = KMeans(K=6, X=matrika[:1000, :], M=matrika[:1000, :], resolve_empty='singleton')
kmeans.initialise()
kmeans.cluster()
clustering_results = kmeans.clustering_results
labels = np.where(clustering_results == 1)[1]


plt.figure(figsize=(10, 10))
color = {0:"red", 1:"blue", 2:"yellow", 3:'green', 4:'violet', 5:'pink'}
for c, x in zip(labels, dimension_reduce):
    plt.plot(x[0], x[1], ".", color=color[c], markersize=10.0)
plt.show()



#model = NMF(n_components=2, init='random')
#W = model.fit_transform(matrika)   # TODO: Razdeli na testno in učno množico glej notebook 106-1_NMF
#H = model.components_

