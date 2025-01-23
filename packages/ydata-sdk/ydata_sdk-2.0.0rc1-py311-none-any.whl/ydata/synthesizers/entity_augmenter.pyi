from _typeshed import Incomplete
from dataclasses import dataclass
from pandas import DataFrame as pdDataFrame
from typing import Literal
from ydata.metadata import Metadata as Metadata
from ydata.utils.random import RandomSeed as RandomSeed

@dataclass
class SmoothingConfig:
    enabled: bool = ...
    window: float = ...
    degree: int = ...
    derivative: int = ...
    def __init__(self, enabled=..., window=..., degree=..., derivative=...) -> None: ...

@dataclass
class FidelityConfig:
    strategy: Literal['gaussian', 'uniform'] = ...
    noise: float = ...
    def __init__(self, strategy=..., noise=...) -> None: ...

class EntityAugmenter:
    nrows: Incomplete
    n_entities: Incomplete
    original_sbk: Incomplete
    pert_blocks: Incomplete
    gauss_models: Incomplete
    pivot_columns: Incomplete
    all_columns: Incomplete
    sortbykey: Incomplete
    entities: Incomplete
    smoothing_strategy: Incomplete
    smoother_per_column: bool
    fidelity_strategy: Incomplete
    fidelity_per_column: bool
    gauss_config: Incomplete
    def __init__(self, X: pdDataFrame, metadata: Metadata, n_entities: int, pivot_columns: list[str]) -> None: ...
    def fit_block_bootstraper(self, block_name: str, X: pdDataFrame): ...
