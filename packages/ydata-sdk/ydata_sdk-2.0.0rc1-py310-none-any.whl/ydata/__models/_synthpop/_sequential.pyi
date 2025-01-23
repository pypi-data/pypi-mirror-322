from _typeshed import Incomplete
from pandas import DataFrame as pdDataFrame
from ydata.metadata import Metadata as Metadata
from ydata.metadata.column import Column as Column
from ydata.synthesizers.base_synthesizer import BaseSynthesizer
from ydata.utils.random import RandomSeed as RandomSeed

methods: Incomplete
methods_map: Incomplete

class SeqSynthpop(BaseSynthesizer):
    DEVICE: Incomplete
    proper: Incomplete
    default_method: Incomplete
    random_state: Incomplete
    order: Incomplete
    smoothing: Incomplete
    smoothing_strategy: Incomplete
    visit_sequence: Incomplete
    columns_info: Incomplete
    max_n_samples: Incomplete
    col_to_method: Incomplete
    col_to_function: Incomplete
    origin_dates: Incomplete
    def __init__(self, proper: bool = False, smoothing: str = 'NA', default_method: str = 'cart', random_state: RandomSeed = None, regression_order: int = 5) -> None: ...
    saved_methods: Incomplete
    def fit(self, X: pdDataFrame, metadata: Metadata, dtypes: dict[str, Column] | None = None, extracted_cols: list[str] | None = None, bootstrapping_cols: list[str] | None = None) -> SeqSynthpop: ...
    def sample(self, n_samples: int = 100, bootstrapping: pdDataFrame | None = None, random_state: RandomSeed = None) -> pdDataFrame: ...
    def save(self, path: str): ...
    @staticmethod
    def load(path: str) -> SeqSynthpop: ...
