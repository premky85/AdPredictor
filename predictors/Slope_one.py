import pandas as pd
import numpy as np

class SlopeOnePredictor:
    def fit(self, X, item, item_name):
        self.item_name = item_name
        self.uim = X
        header = ["UserID"] + item.tolist()

        groups = self.uim.df.groupby("UserID")
        matrix = np.zeros((len(self.uim.users), len(header)))
        self.df = pd.DataFrame(matrix, columns=header)
        self.df["UserID"] = self.uim.users
        self.df.set_index("UserID", inplace=True)
        self.df = self.df.T
        for x in self.uim.users:
            b = groups.get_group(x)[[self.item_name, "Clicks"]].groupby(self.item_name).sum().to_dict()["Clicks"]
            #df.loc[x] = pd.Series(self.uim.movies, index=self.uim.movies).map(b).to_list()
            self.df[x] = self.df.index.map(b).to_list()
        self.df = self.df.T


    def predict(self, user_id):
        unknown = self.df.loc[user_id].loc[self.df.loc[user_id].isna()].index.to_list()#.columns[self.df.isna().any()].tolist()
        #test = self.df.loc[user_id]
        known = self.df.loc[user_id].loc[self.df.loc[user_id].notnull()].index.to_list()
        header = [self.item_name, "Clicks"]
        matrix = np.ones((len(unknown), len(header)))
        self.rez = pd.DataFrame(matrix, columns=header)
        self.rez[self.item_name] = unknown
        self.rez.set_index(self.item_name, inplace=True)
        for x in unknown:
            scores = []
            for y in known:
                test = self.df[self.df[x].notnull() & self.df[y].notnull()]
                a = self.df.loc[user_id][y] + test[x] - test[y]
                scores += a.to_list()
            self.rez.loc[x] = np.mean(scores)
        return self.rez.to_dict()["Clicks"]