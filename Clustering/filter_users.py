import pandas as pd
import glob
import os

unique_user_id = r"./test/test.csv"
path = r"C:\Users\leonp\Documents\iProm_podatki"
df_ids = pd.read_csv(unique_user_id, header=0, sep='\t', usecols=[1])

all_files = glob.glob(os.path.join(path, "*.csv"))
for f in all_files:
    df = pd.read_csv(f, header=None, sep='\t',
                     names=["Date", "DayOfWeek", "TimeFrame", "UserID", "SiteID", "CampaignID", "AdID", "ZoneID",
                            "MasterSiteID", "SiteCategory", "AdIndustry", "Requests", "Views", "Clicks"],
                     index_col=False)

    name = os.path.basename(f)

    df = df.loc[df["UserID"].isin(df_ids.values)]

    df.to_csv(r"./test/" + os.path.basename(f), "\t",
              header=["Date", "DayOfWeek", "TimeFrame", "UserID", "SiteID", "CampaignID", "AdID", "ZoneID",
                      "MasterSiteID", "SiteCategory", "AdIndustry", "Requests", "Views", "Clicks"], index=False)



