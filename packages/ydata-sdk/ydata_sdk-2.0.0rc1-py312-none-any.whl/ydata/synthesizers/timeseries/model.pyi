from _typeshed import Incomplete
from pandas import DataFrame as pdDataFrame
from pathlib import Path
from typing import Callable
from ydata.connectors.storages.big_query_connector import BigQueryConnector as BigQueryConnector
from ydata.connectors.storages.object_storage_connector import ObjectStorageConnector as ObjectStorageConnector
from ydata.connectors.storages.rdbms_connector import RDBMSConnector as RDBMSConnector
from ydata.datascience.common import PrivacyLevel
from ydata.dataset import Dataset
from ydata.metadata import Metadata
from ydata.preprocessors.methods.anonymization import AnonymizerConfigurationBuilder
from ydata.synthesizers.base_model import BaseModel, SegmentByType
from ydata.synthesizers.conditional import ConditionalFeature
from ydata.synthesizers.entity_augmenter import FidelityConfig, SmoothingConfig
from ydata.utils.random import RandomSeed as RandomSeed

logger: Incomplete

class TimeSeriesSynthesizer(BaseModel):
    sortbykey: Incomplete
    bypass_entities_anonymization: Incomplete
    def __init__(self, tmppath: str | Path = None) -> None: ...
    @property
    def SUPPORTED_DTYPES(self): ...
    anonymize: Incomplete
    entity_merged_col: Incomplete
    entities_type: Incomplete
    is_fitted_: bool
    def fit(self, X: Dataset, metadata: Metadata, extracted_cols: list = None, calculated_features: list[dict[str, str | Callable | list[str]]] | None = None, missing_values: list | None = None, anonymize: dict | AnonymizerConfigurationBuilder | None = None, privacy_level: PrivacyLevel | str = ..., condition_on: str | list[str] | None = None, anonymize_ids: bool = False, segment_by: SegmentByType = 'auto', random_state: RandomSeed = None): ...
    def sample(self, n_entities: int | None = None, smoothing: bool | dict | SmoothingConfig = False, fidelity: float | dict | FidelityConfig | None = None, sort_result: bool = True, condition_on: list[ConditionalFeature] | dict | pdDataFrame | None = None, balancing: bool = False, random_state: RandomSeed = None, connector: BigQueryConnector | ObjectStorageConnector | RDBMSConnector | None = None, **kwargs) -> Dataset: ...
