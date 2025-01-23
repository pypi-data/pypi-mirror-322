from _typeshed import Incomplete
from enum import Enum
from pandas import DataFrame as pdDataFrame
from ydata.utils.data_types import DataType

class DiscretizationType(Enum):
    UNIFORM = 'uniform'
    QUANTILE = 'quantile'

class Discretizer:
    discretization_type: Incomplete
    n_bins: Incomplete
    reset_index: Incomplete
    def __init__(self, method=..., n_bins: int = 10, reset_index: bool = False) -> None: ...
    def discretize_dataframe(self, dataframe: pdDataFrame, data_types: dict[str, DataType] | None = None) -> pdDataFrame: ...
