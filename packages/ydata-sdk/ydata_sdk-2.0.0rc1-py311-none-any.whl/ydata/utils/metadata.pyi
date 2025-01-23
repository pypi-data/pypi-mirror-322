import pandas as pd
from _typeshed import Incomplete
from enum import Enum
from json import JSONEncoder
from ydata.dataset import Dataset
from ydata.metadata import Metadata

DATA_TYPES: Incomplete

class JsonSerializer(JSONEncoder):
    def default(self, o): ...

class Activation(Enum):
    SIGMOID = 'sigmoid'
    TANH = 'tanh'
    SOFTMAX = 'softmax'
    @staticmethod
    def valid_activation(activation): ...

def get_types(df: pd.DataFrame, int_as_cat_threshold: int = 20) -> dict: ...
def infer_pandas_dtypes(df: pd.DataFrame): ...
def are_columns_matching(X: Dataset, metadata: Metadata): ...
