from _typeshed import Incomplete
from dataclasses import dataclass
from pandas import DataFrame as pdDataFrame, Series as pdSeries
from typing import Callable
from ydata.dataset import Dataset
from ydata.utils.data_types import DataType, ScaleType, VariableType

class MeasureAssociations:
    mapping: Incomplete
    discretizer: Incomplete
    def __init__(self, mapping: PairwiseMatrixMapping, n_bins: int = 10) -> None: ...
    columns: Incomplete
    vartypes: Incomplete
    datatypes: Incomplete
    column_pairs: Incomplete
    def compute_pairwise_matrix(self, dataset: Dataset | pdDataFrame, datatypes: dict = None, vartypes: dict | None = None, columns: list[str] | None = None) -> pdDataFrame: ...
    @staticmethod
    def resolve_params(col_1: ColumnMetric, col_2: ColumnMetric, params: PairwiseMatrixMapping, df: pdDataFrame, df_discretized: pdDataFrame) -> dict: ...

class ColumnMetric:
    name: Incomplete
    data_type: Incomplete
    variable_type: Incomplete
    scale_type: Incomplete
    def __init__(self, column_name: str, data_type: DataType, variable_type: VariableType) -> None: ...

class MeasureAssociationsPandas(MeasureAssociations):
    datatypes: Incomplete
    vartypes: Incomplete
    columns: Incomplete
    column_pairs: Incomplete
    def compute_pairwise_matrix(self, dataframe: pdDataFrame, datatypes: dict, vartypes: dict, columns: list[str] | None = None) -> pdDataFrame: ...

@dataclass
class PairwiseTask:
    method: Callable[[pdSeries, pdSeries], float]
    params: PairwiseParams
    def __init__(self, method, params) -> None: ...

@dataclass
class PairwiseParams:
    discretize: tuple[bool, bool]
    combined_calculation: bool
    def __init__(self, discretize, combined_calculation) -> None: ...

@dataclass
class PairwiseMatrixMapping:
    mapping: dict[tuple[ScaleType, ScaleType], PairwiseTask]
    def __init__(self, mapping) -> None: ...
