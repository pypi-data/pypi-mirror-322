import pandas as pd
from _typeshed import Incomplete
from sklearn.base import BaseEstimator, TransformerMixin
from typing import NamedTuple
from ydata.metadata.metadata import Metadata as Metadata
from ydata.preprocessors.base import Preprocessor

logger: Incomplete

class ActInfo(NamedTuple):
    dim: Incomplete
    activation_fn: Incomplete

class ColumnTransformInfo(NamedTuple):
    column_name: Incomplete
    column_type: Incomplete
    output_info: Incomplete
    output_dimensions: Incomplete

class SynthpopPreprocessor(Preprocessor):
    def __init__(self, sortbykey: Incomplete | None = None, anonymize_config: dict | None = None, metadata: Metadata = None) -> None: ...

class SynthpopSegmentPreprocessor(Preprocessor):
    def __init__(self, metadata: Metadata = None) -> None: ...

class DataProcessor(BaseEstimator, TransformerMixin):
    SUPPORTED_DTYPES: Incomplete
    num_cols: Incomplete
    cat_cols: Incomplete
    dt_cols: Incomplete
    num_pipeline: Incomplete
    cat_pipeline: Incomplete
    dt_pipeline: Incomplete
    def __init__(self, *, num_cols: list[str] = None, cat_cols: list[str] = None, dt_cols: list[str] = None) -> None: ...
    col_order_: Incomplete
    def fit(self, X, y: Incomplete | None = None): ...
    num_col_idx_: Incomplete
    cat_col_idx_: Incomplete
    dt_col_idx_: Incomplete
    def transform(self, X, y: Incomplete | None = None): ...
    def fit_transform(self, X, y: Incomplete | None = None, **fit_params): ...
    def inverse_transform(self, X) -> pd.DataFrame: ...
