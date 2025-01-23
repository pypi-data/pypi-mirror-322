from _typeshed import Incomplete
from pandas import DataFrame
from ydata.__models._synthpop.maps import METHODS_MAP, SYNTHPOP_FLAVOR
from ydata.metadata import Metadata as Metadata
from ydata.metadata.column import Column as Column
from ydata.synthesizers.base_synthesizer import BaseSynthesizer
from ydata.utils.random import RandomSeed as RandomSeed

methods: Incomplete
methods_map: Incomplete

class Synthpop(BaseSynthesizer):
    FLAVOR: Incomplete
    DEVICE: Incomplete
    visit_sequence: Incomplete
    predictor_matrix: Incomplete
    columns_info: Incomplete
    proper: Incomplete
    smoothing: Incomplete
    smoothing_strategy: Incomplete
    default_method: Incomplete
    col_to_method: Incomplete
    col_to_function: Incomplete
    random_state: Incomplete
    def __init__(self, proper: bool = False, smoothing: str = 'NA', default_method: str = 'cart', random_state: RandomSeed = None) -> None: ...
    saved_methods: Incomplete
    def fit(self, X: DataFrame, metadata: Metadata, dtypes: dict[str, Column] = None, method: list | METHODS_MAP[SYNTHPOP_FLAVOR.TAB] | None = None, cont_na: dict | None = None, bootstrapping_cols: list[str] | None = None) -> Synthpop: ...
    def sample(self, n_samples: int = 100, bootstrapping: DataFrame | None = None, random_state: RandomSeed = None) -> DataFrame: ...
    def save(self, path: str): ...
    @staticmethod
    def load(path: str) -> Synthpop: ...
