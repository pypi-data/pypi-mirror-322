from _typeshed import Incomplete
from ydata.__models._synthpop._methods import BaseMethod
from ydata.dataset.dataset import Dataset as Dataset
from ydata.utils.data_types import DataType as DataType
from ydata.utils.random import RandomSeed as RandomSeed

class PolyregMethod(BaseMethod):
    y_dtype: Incomplete
    proper: Incomplete
    random_state: Incomplete
    y_encoder: Incomplete
    polyreg: Incomplete
    def __init__(self, y_dtype: DataType, proper: bool = False, random_state: RandomSeed = None, *args, **kwargs) -> None: ...
    def fit(self, X: Dataset, y: Dataset, dtypes: dict = None, *args, **kwargs): ...
    def predict(self, X_test, dtypes: dict = None, random_state: RandomSeed = None): ...
