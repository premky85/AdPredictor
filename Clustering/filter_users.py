import pandas as pd
import glob
import os

unique_user_id_1 = r"C:\Users\Leon\Documents\iProm_podatki\test\users_1.csv"
unique_user_id_0 = r"C:\Users\Leon\Documents\iProm_podatki\test\users_0.csv"
path = r"C:\Users\Leon\Documents\iProm_podatki"
#path = r"C:\Users\Leon\Documents\iProm_podatki\export_2019-02-23.csv"


df_ids_1 = pd.read_csv(unique_user_id_1, header=0, sep='\t', usecols=[1])
df_ids_0 = pd.read_csv(unique_user_id_0, header=0, sep='\t', usecols=[1])


all_files = glob.glob(os.path.join(path, "*.csv"))
for f in all_files:
    df = pd.read_csv(f, header=None, sep='\t',
                     names=["Date", "DayOfWeek", "TimeFrame", "UserID", "SiteID", "CampaignID", "AdID", "ZoneID",
                            "MasterSiteID", "SiteCategory", "AdIndustry", "Requests", "Views", "Clicks"],
                     index_col=False)

    name = os.path.basename(f)

    df_0 = df.loc[df["UserID"].isin(df_ids_0.values)]

    df_0.to_csv(r"C:\Users\Leon\Documents\iProm_podatki\test\0" + "\\" + name, "\t",
              header=["Date", "DayOfWeek", "TimeFrame", "UserID", "SiteID", "CampaignID", "AdID", "ZoneID",
                      "MasterSiteID", "SiteCategory", "AdIndustry", "Requests", "Views", "Clicks"], index=False)

    df_1 = df.loc[df["UserID"].isin(df_ids_1.values)]

    df_1.to_csv(r"C:\Users\Leon\Documents\iProm_podatki\test\1" + "\\" + name, "\t",
                header=["Date", "DayOfWeek", "TimeFrame", "UserID", "SiteID", "CampaignID", "AdID", "ZoneID",
                        "MasterSiteID", "SiteCategory", "AdIndustry", "Requests", "Views", "Clicks"], index=False)



