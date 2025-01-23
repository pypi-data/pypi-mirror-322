from _typeshed import Incomplete
from dataclasses import dataclass
from pandas import DataFrame as pdDataFrame
from ydata.datascience.common import PrivacyLevel
from ydata.utils.random import RandomSeed as RandomSeed

@dataclass
class PrivacyParameters:
    epsilon: float
    delta: float
    def __init__(self, epsilon, delta) -> None: ...

class DifferentialPrivacyLayer:
    random_state: Incomplete
    def __init__(self, time_series: bool = False, random_state: RandomSeed = None) -> None: ...
    def apply(self, X: pdDataFrame, privacy_level: PrivacyLevel, input_dtypes: dict): ...
