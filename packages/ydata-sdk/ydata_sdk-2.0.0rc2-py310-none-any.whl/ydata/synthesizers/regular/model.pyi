from _typeshed import Incomplete
from pandas import DataFrame as pdDataFrame
from pathlib import Path
from typing import Callable
from ydata.connectors.storages.big_query_connector import BigQueryConnector as BigQueryConnector
from ydata.connectors.storages.object_storage_connector import ObjectStorageConnector as ObjectStorageConnector
from ydata.connectors.storages.rdbms_connector import RDBMSConnector as RDBMSConnector
from ydata.datascience.common import PrivacyLevel
from ydata.dataset import Dataset
from ydata.metadata.metadata import Metadata as Metadata
from ydata.preprocessors.methods.anonymization import AnonymizerConfigurationBuilder
from ydata.synthesizers.base_model import BaseModel, SegmentByType
from ydata.synthesizers.conditional import ConditionalFeature
from ydata.utils.random import RandomSeed as RandomSeed

logger: Incomplete

class RegularSynthesizer(BaseModel):
    filter_outliers: Incomplete
    def __init__(self, *, tmppath: str | Path = None, filter_outliers: bool = True, strategy: str = 'random') -> None: ...
    @property
    def SUPPORTED_DTYPES(self): ...
    anonymize: Incomplete
    is_fitted_: bool
    def fit(self, X: Dataset, metadata: Metadata, *, calculated_features: list[dict[str, str | Callable | list[str]]] | None = None, missing_values: list | None = None, anonymize: dict | AnonymizerConfigurationBuilder | None = None, privacy_level: PrivacyLevel | str = ..., condition_on: str | list[str] | None = None, anonymize_ids: bool = False, segment_by: SegmentByType = 'auto', holdout_size: float = 0.2, random_state: RandomSeed = None): ...
    def sample(self, n_samples: int = 1, condition_on: list[ConditionalFeature] | dict | pdDataFrame | None = None, balancing: bool = False, random_state: RandomSeed = None, connector: BigQueryConnector | ObjectStorageConnector | RDBMSConnector | None = None, **kwargs): ...
