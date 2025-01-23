import numpy as np
import pandas as pd
from _typeshed import Incomplete
from sklearn.base import BaseEstimator, TransformerMixin
from ydata.dataset import Dataset
from ydata.metadata import Metadata as Metadata
from ydata.quality.labels.enums import LabelFilter
from ydata.quality.labels.methods.rank import RankedBy

def get_unique_classes(labels, multi_label: Incomplete | None = None) -> set: ...
def num_unique_classes(labels, multi_label: Incomplete | None = None) -> int: ...
def get_num_classes(labels: Incomplete | None = None, pred_probs: Incomplete | None = None, label_matrix: Incomplete | None = None, multi_label: Incomplete | None = None) -> int: ...

class FindInconsistentLabelsEngine(BaseEstimator, TransformerMixin):
    filter_type: Incomplete
    ranked_by: Incomplete
    frac_noise: Incomplete
    num_to_remove_per_class: Incomplete
    min_examples_per_class: Incomplete
    def __init__(self, filter_type: str | LabelFilter = ..., frac_noise: float = 1.0, num_to_remove_per_class: list[int] | None = None, min_examples_per_class: int = 1, indices_ranked_by: str | RankedBy = ...) -> None: ...
    confident_joint: Incomplete
    n_classes: Incomplete
    big_dataset: Incomplete
    label_counts: Incomplete
    def fit(self, X: Dataset | pd.DataFrame, metadata: Metadata, confident_joint: np.ndarray | None = None): ...
    def transform(self, X: Dataset | pd.DataFrame, label_name: str, pred_probs: np.ndarray, n_jobs: int | None = None): ...
    def fit_transform(self, X: Dataset | pd.DataFrame, label_name: str, pred_probs: np.ndarray, metadata: Metadata, confident_joint: np.ndarray | None = None, n_jobs: int | None = None): ...
