from recommendation_system.Data_tools import *
from predictors.Slope_one import*
from recommendation_system.recommender import Recommender

#rd = Reader("../data")
#rd.read(0, 2)
#rd.segment_users()
#rd.filter_data()

uim = UserItemData("../data/users_1/u1_data.csv")
sop = SlopeOnePredictor()
rec = Recommender(sop)
rec.fit(uim, uim.ad_industries, "AdIndustry")
rec.recommend(175341321)

