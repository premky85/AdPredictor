import pandas as pd
import glob
import Clustering.filter_users
import os

class Reader:
    def __init__(self, path):
        self.path = path
        self.df_users0 = None
        self.df_users1 = None
        self.df_users_test = None

    def read(self, first=0, last=0, learn_size=0.8):
        if(os.path.isfile(self.path)):
            self.df = pd.read_csv(self.path, header=None, sep='\t',
                         names=["Date", "DayOfWeek", "TimeFrame", "UserID", "SiteID", "CampaignID", "AdID", "ZoneID",
                                "MasterSiteID", "SiteCategory", "AdIndustry", "Requests", "Views", "Clicks"],
                         index_col=False)

        elif(os.path.isdir(self.path)):
            all_files = glob.glob(os.path.join(self.path, "*.csv"))
            if(last == 0):
                last = len(all_files)
            self.df = pd.concat((pd.read_csv(f, header=None, sep='\t',
                         names=["Date", "DayOfWeek", "TimeFrame", "UserID", "SiteID", "CampaignID", "AdID", "ZoneID",
                                "MasterSiteID", "SiteCategory", "AdIndustry", "Requests", "Views", "Clicks"],
                         index_col=False) for f in all_files[first: last]), ignore_index=True)

        self.learn = round(learn_size * self.df.shape[0])
        self.test = round((1 - learn_size) * self.df.shape[0])

    def segment_users(self):

        p = os.path.dirname(self.path) + "/"
        if not os.path.exists(p + "temp_data"):
            os.makedirs(p + "temp_data")

        df_learn = self.df.head(self.learn).groupby(["UserID"]).sum().reset_index()
        self.df_users1 = df_learn[df_learn["Clicks"] != 0][["UserID", "Clicks"]]
        self.df_users1.to_csv(p + "temp_data/users_1.csv", "\t", header=["UserID", "Clicks"])

        self.df_users0 = df_learn[df_learn["Clicks"] == 0][["UserID", "Clicks"]]
        self.df_users0.to_csv(p + "temp_data/users_0.csv", "\t", header=["UserID", "Clicks"])

        df_test = self.df.tail(self.test).groupby(["UserID"]).sum().reset_index()
        self.df_users_test = df_test[df_test["Clicks"] != 0][["UserID", "Clicks"]]
        self.df_users_test.to_csv(p + "temp_data/test.csv", "\t", header=["UserID", "Clicks"])

    def filter_data(self):
        p = os.path.dirname(self.path) + "/"
        if not os.path.exists(p + "users_1"):
            os.makedirs(p + "users_1")

        if not os.path.exists(p + "users_0"):
            os.makedirs(p + "users_0")

        if not os.path.exists(p + "users_t"):
            os.makedirs(p + "users_t")

        if self.df_users0 is None:
            self.df_users0 = pd.read_csv(p + "temp_data/users_0.csv", header=0, sep='\t', usecols=[1])
        if self.df_users1 is None:
            self.df_users1 = pd.read_csv(p + "temp_data/users_1.csv", header=0, sep='\t', usecols=[1])
        if self.df_users_test is None:
            self.df_users_test = pd.read_csv(p + "temp_data/test.csv", header=0, sep='\t', usecols=[1])
        test = self.df[self.df.index.duplicated()]
        self.df_0 = self.df.head(self.learn).loc[self.df["UserID"].isin(self.df_users0.values)]
        self.df_0.to_csv(p + "users_0/u0_data.csv" , "\t",
                    header=["Date", "DayOfWeek", "TimeFrame", "UserID", "SiteID", "CampaignID", "AdID", "ZoneID",
                            "MasterSiteID", "SiteCategory", "AdIndustry", "Requests", "Views", "Clicks"], index=False)

        self.df_1 = self.df.head(self.learn).loc[self.df["UserID"].isin(self.df_users1.values)]
        self.df_1.to_csv(p + "users_1/u1_data.csv", "\t",
                    header=["Date", "DayOfWeek", "TimeFrame", "UserID", "SiteID", "CampaignID", "AdID", "ZoneID",
                            "MasterSiteID", "SiteCategory", "AdIndustry", "Requests", "Views", "Clicks"], index=False)

        self.df_t = self.df.tail(self.test).loc[self.df["UserID"].isin(self.df_users_test.values)]
        self.df_t.to_csv(p + "users_t/ut_data.csv", "\t",
                    header=["Date", "DayOfWeek", "TimeFrame", "UserID", "SiteID", "CampaignID", "AdID", "ZoneID",
                            "MasterSiteID", "SiteCategory", "AdIndustry", "Requests", "Views", "Clicks"], index=False)

class UserItemData:
    def __init__(self, path):
        self.df = pd.read_csv(path, sep='\t', index_col=False)

        self.users = self.df["UserID"].unique()
        self.ad_industries = self.df["AdIndustry"].unique()
        self.site_categories = self.df["SiteCategory"].unique()
