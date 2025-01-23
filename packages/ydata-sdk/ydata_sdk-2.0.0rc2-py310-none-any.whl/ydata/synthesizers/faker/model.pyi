from _typeshed import Incomplete
from ydata.dataset import Dataset
from ydata.metadata import Metadata as Metadata
from ydata.metadata.column import Column as Column

logger: Incomplete

class FakerSynthesizer:
    metadata: Incomplete
    columns: Incomplete
    locale: Incomplete
    def __init__(self, locale: str = 'en') -> None: ...
    domains: Incomplete
    nunique: Incomplete
    missings: Incomplete
    nrows: Incomplete
    extra_data: Incomplete
    value_counts: Incomplete
    def fit(self, metadata: Metadata): ...
    def sample(self, sample_size) -> Dataset: ...
    def save(self, path) -> None: ...
    @classmethod
    def load(cls, path: str): ...
