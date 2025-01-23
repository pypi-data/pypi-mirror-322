from _typeshed import Incomplete
from ydata.__models._synthpop._methods import NormMethod

class NormRankMethod(NormMethod):
    sigma: Incomplete
    y_sorted: Incomplete
    def fit(self, X, y, dtypes: dict = None): ...
    def predict(self, X_test, dtypes: dict = None): ...
