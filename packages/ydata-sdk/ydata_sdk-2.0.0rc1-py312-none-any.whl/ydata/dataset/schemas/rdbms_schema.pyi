from _typeshed import Incomplete
from dataclasses import dataclass

logger: Incomplete

@dataclass(frozen=True)
class ForeignKey:
    column: str
    parent: str
    def __init__(self, column, parent) -> None: ...

@dataclass(frozen=True)
class TableColumn:
    name: str
    variable_type: str
    primary_key: bool
    is_foreign_key: bool
    foreign_keys: list
    nullable: bool
    format: str | None = ...
    @staticmethod
    def from_database_column(column, table): ...
    def __init__(self, name, variable_type, primary_key, is_foreign_key, foreign_keys, nullable, format=...) -> None: ...

@dataclass(frozen=True)
class Table:
    name: str
    columns: list[TableColumn]
    primary_keys: list[TableColumn]
    foreign_keys: list[TableColumn]
    @staticmethod
    def from_database_table(table, columns): ...
    @property
    def dtypes(self): ...
    def __init__(self, name, columns, primary_keys, foreign_keys) -> None: ...

@dataclass
class Schema:
    name: str
    tables: dict
    def __init__(self, name, tables) -> None: ...
