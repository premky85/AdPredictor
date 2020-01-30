import pandas as pd

class Recommender():
    def __init__(self, predictor):
        self.predictor = predictor

    def fit(self, uim, item, item_name):
        self.item_name = item_name
        self.predictor.fit(uim, item, self.item_name)

    def recommend(self, userID, n=10):
        self.user = userID
        self.recomended = self.predictor.predict(userID)
        self.recomended = pd.DataFrame(list(self.recomended.items()), columns=[self.item_name, "Ocena"])
        self.recomended.sort_values(by=["Ocena"], inplace=True, ascending=False)

