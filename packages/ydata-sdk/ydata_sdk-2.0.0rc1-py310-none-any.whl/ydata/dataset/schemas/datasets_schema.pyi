from _typeshed import Incomplete
from dataclasses import dataclass
from enum import Enum
from pydantic.v1 import BaseModel
from ydata.utils.data_types import VariableType

@dataclass(frozen=True)
class DatasetSchema:
    column: str
    vartype: VariableType
    format: str | None = ...
    def __init__(self, column, vartype, format=...) -> None: ...

class RelationType(Enum):
    ONE_TO_MANY = '1-n'
    ONE_TO_ONE = '1-1'
    MANY_TO_MANY = 'n-n'

class ForeignReference(BaseModel):
    table: str
    column: str
    parent_table: str
    parent_column: str
    relation_type: RelationType
    def __hash__(self): ...

class TableSchema(BaseModel):
    primary_keys: list[str]
    foreign_keys: list[ForeignReference]
    columns: dict
    class Config:
        extra: Incomplete
    def get_keys(self): ...

class MultiTableSchema(dict[str, TableSchema]):
    composite_keys: Incomplete
    def __init__(self, data: dict | RDBMS_Schema | None, tables: list[str] | None = None) -> None: ...
    def add_composite_keys(self, table: str, columns: list[str], parent_table: str, parent_columns: list[str]): ...
    @property
    def tables(self): ...
    def dict(self) -> dict: ...
    @property
    def foreign_keys(self) -> list[ForeignReference]: ...
    def add_foreign_key(self, table: str, column: str, parent_table: str, parent_column: str, relation_type: str | RelationType = ...): ...
    def add_primary_key(self, table: str, column: str): ...
    def filter(self, tables: list | str): ...
