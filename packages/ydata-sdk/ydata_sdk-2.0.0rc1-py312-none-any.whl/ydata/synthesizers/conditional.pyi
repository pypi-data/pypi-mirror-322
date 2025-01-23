import abc
from abc import ABC
from dataclasses import dataclass
from numpy import ndarray as ndarray
from pandas import DataFrame as pdDataFrame
from typing import Generator as GeneratorType
from ydata.preprocessors.base import Preprocessor
from ydata.utils.random import RandomSeed as RandomSeed

@dataclass
class ConditionalFeature(ABC, metaclass=abc.ABCMeta):
    name: str
    def sample(self, n_samples: int, random_state: RandomSeed = None) -> ndarray: ...
    def __init__(self, name) -> None: ...

@dataclass
class Category:
    VALUE_DTYPES = str | int | bool | float
    value: VALUE_DTYPES
    percentage: float = ...
    def __init__(self, value, percentage=...) -> None: ...

@dataclass
class CategoricalValues(ConditionalFeature):
    categories: list[Category | Category.VALUE_DTYPES | tuple[Category.VALUE_DTYPES, float] | dict] | None = ...
    balancing: bool = ...
    def __init__(self, name: str, categories: list[Category | Category.VALUE_DTYPES | tuple[Category.VALUE_DTYPES, float]] | None = None, balancing: bool = False, value_counts_normalized: dict = None) -> None: ...

@dataclass
class NumericalRange(ConditionalFeature):
    minimum: float
    maximum: float
    def __init__(self, name, minimum, maximum) -> None: ...

@dataclass
class Generator(ConditionalFeature):
    def __init__(self, name: str, function: GeneratorType) -> None: ...

class ConditionalFactory:
    @staticmethod
    def create_from_dict(condition_on: dict, data_types: dict, metadata_summary: dict) -> list[ConditionalFeature]: ...

class ConditionalUtils:
    @staticmethod
    def prepare_conditional_sample(condition_on: list[ConditionalFeature] | dict | pdDataFrame, conditional_features: list[str], data_types: dict, n_samples: int, preprocessor: Preprocessor, metadata_summary: dict, random_state: RandomSeed = None) -> pdDataFrame: ...
    @staticmethod
    def validate_conditional_features(condition_on: list[str], dataset_columns: list[str], anonymize_columns: list[str], dataset_attrs: dict): ...
    @staticmethod
    def validate_condition_types(condition_on: list[ConditionalFeature], data_types: dict): ...
