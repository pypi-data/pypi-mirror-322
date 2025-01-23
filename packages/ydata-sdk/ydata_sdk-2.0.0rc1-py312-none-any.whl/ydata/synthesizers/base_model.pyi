from _typeshed import Incomplete
from pathlib import Path
from ydata.connectors.storages.big_query_connector import BigQueryConnector as BigQueryConnector
from ydata.dataset import Dataset
from ydata.metadata.column import Column as Column
from ydata.utils.random import RandomSeed as RandomSeed

logger: Incomplete
SegmentByType: Incomplete

def get_default_tmppath(folder: Path = None) -> Path: ...

class BaseModel:
    is_fitted_: bool
    DEFAULT_LAB_TMP: str
    MIN_ROWS: int
    LOW_ROWS: int
    calculated_features: Incomplete
    pipelines: Incomplete
    segment_by: str
    dataset_preprocessor: Incomplete
    features_order: Incomplete
    data_types: Incomplete
    fitted_dataset_schema: Incomplete
    segmenter: Incomplete
    slicer: Incomplete
    segmentation_strategy: Incomplete
    slicing_strategy: Incomplete
    dataset_type: Incomplete
    uuid: Incomplete
    tmppath: Incomplete
    anonymize: Incomplete
    entity_augmenter: Incomplete
    pivot_columns: Incomplete
    entities_type: Incomplete
    time_series: bool
    metadata_summary: Incomplete
    categorical_vars: Incomplete
    random_state: Incomplete
    def __init__(self, tmppath: str | Path = None) -> None: ...
    @property
    def privacy_level(self): ...
    @property
    def anonymized_columns(self) -> list[str]: ...
    def fit(self, X, y: Incomplete | None = None, segment_by: SegmentByType = 'auto', anonymize: dict | None = None, random_state: RandomSeed = None): ...
    def sample(self, n_samples: int = 1) -> Dataset: ...
    @property
    def SUPPORTED_DTYPES(self) -> None: ...
    def save(self, path: str, copy: bool = False): ...
    @staticmethod
    def load(path): ...
