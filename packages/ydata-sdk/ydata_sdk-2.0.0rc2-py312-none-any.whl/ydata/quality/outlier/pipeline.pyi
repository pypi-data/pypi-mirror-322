from _typeshed import Incomplete
from pandas import DataFrame as pdDataFrame
from ydata.dataset import Dataset as Dataset
from ydata.metadata import Metadata as Metadata
from ydata.quality.outlier.prototype import OutlierCluster, OutlierSteps

class OutlierPipeline:
    steps: Incomplete
    outlier_score_: Incomplete
    cluster_index_: Incomplete
    dataset_len: Incomplete
    columns: Incomplete
    def __init__(self, steps: dict | OutlierSteps) -> None: ...
    def fit_predict(self, X: Dataset, metadata: Metadata, outlier_col: str = ...) -> list[OutlierCluster]: ...
    def represent(self, X: Dataset) -> pdDataFrame: ...
    def plot(self, X: Dataset, ax: Incomplete | None = None, **kwargs): ...
    def summary(self, details: bool = False) -> dict: ...
