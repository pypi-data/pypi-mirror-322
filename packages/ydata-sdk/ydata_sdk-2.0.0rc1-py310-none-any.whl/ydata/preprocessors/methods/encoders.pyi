import numpy as np
from _typeshed import Incomplete
from dask.array import Array
from sklearn.base import BaseEstimator, TransformerMixin
from typing import TypeVar

DataFrameType: Incomplete
ArrayLike = TypeVar('ArrayLike', Array, np.ndarray)
SeriesType: Incomplete

class OrdinalEncoder(BaseEstimator, TransformerMixin):
    columns: Incomplete
    def __init__(self, columns: Incomplete | None = None) -> None: ...
    columns_: Incomplete
    categorical_columns_: Incomplete
    non_categorical_columns_: Incomplete
    dtypes_: Incomplete
    def fit(self, X: DataFrameType, y: ArrayLike | SeriesType | None = None) -> OrdinalEncoder: ...
    def transform(self, X: DataFrameType, y: ArrayLike | SeriesType | None = None) -> DataFrameType: ...
    def inverse_transform(self, X: ArrayLike | DataFrameType) -> ArrayLike | DataFrameType: ...
