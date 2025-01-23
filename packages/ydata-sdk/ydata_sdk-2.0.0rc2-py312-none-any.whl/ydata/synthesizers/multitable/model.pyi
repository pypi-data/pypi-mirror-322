from _typeshed import Incomplete
from dataclasses import dataclass
from enum import Enum
from pandas import DataFrame as pdDataFrame
from pathlib import Path
from typing import Callable
from ydata.connectors.storages.rdbms_connector import RDBMSConnector as RDBMSConnector
from ydata.core.connectors import WriteMode
from ydata.dataset import MultiDataset
from ydata.metadata.metadata import Metadata
from ydata.metadata.multimetadata import MultiMetadata as MultiMetadata
from ydata.synthesizers.base_model import BaseModel
from ydata.synthesizers.faker import FakerSynthesizer
from ydata.synthesizers.multitable.encoder import EncoderType
from ydata.synthesizers.regular import RegularSynthesizer
from ydata.synthesizers.timeseries import TimeSeriesSynthesizer
from ydata.utils.random import RandomSeed as RandomSeed

logger: Incomplete
SYNTHESIZER = type[RegularSynthesizer | TimeSeriesSynthesizer | FakerSynthesizer]

@dataclass
class Component:
    tables: list[str]
    relations: dict
    visitor_sequence: list
    merged_order: dict
    schema: dict
    synthesizer: BaseModel
    merged_rows: int
    num_entities: int
    def __init__(self, tables, relations, visitor_sequence, merged_order, schema, synthesizer, merged_rows, num_entities) -> None: ...

@dataclass
class _AnonymizationData:
    anonymized_columns: dict[str, list[str]]
    key_mappings: dict[str, dict[str, dict]]
    builders = ...
    def __init__(self) -> None: ...

class SAMPLE_METHOD(Enum):
    ORIGINAL = 1
    RELATION_BASED = 2

class MultiTableSynthesizer(BaseModel):
    schema: Incomplete
    components: Incomplete
    tables_schemas: Incomplete
    tables_columns: Incomplete
    mt_anonymize: Incomplete
    sample_method: Incomplete
    tables_dataset_attrs: Incomplete
    def __init__(self, *, tmppath: str | Path | None = None) -> None: ...
    @property
    def SUPPORTED_DTYPES(self): ...
    def anonymize_table_pks(self, table: str, table_df: pdDataFrame) -> pdDataFrame: ...
    def update_anonymized_columns_metadata(self, table: str, metadata: Metadata, dataset_schema, anonymization_data: _AnonymizationData): ...
    def create_synthesizers(self): ...
    def is_attribute_table(self, table: str) -> bool: ...
    calculated_features: Incomplete
    attribute_tables: Incomplete
    relationships: Incomplete
    is_fitted_: bool
    def fit(self, X: MultiDataset, metadata: MultiMetadata, anonymize: dict | None = None, limit: int = 50000000, calculated_features: list[dict[str, str | Callable | list[str]]] | None = None, attribute_tables: list[str] | set[str] | str | None = None, random_state: RandomSeed = None, encoder_type: EncoderType = ...): ...
    def get_condition_df(self, table, previous_table, sample_tables, shapes, fraction): ...
    def sample(self, n_samples: float | None = None, connector: RDBMSConnector | None = None, if_exists: str | WriteMode = ..., random_state: RandomSeed = None) -> MultiDataset: ...
    def save(self, path: str): ...
    @classmethod
    def load(cls, path: str): ...
