from _typeshed import Incomplete
from ydata.metadata import Metadata as Metadata
from ydata.report.metrics import MetricType
from ydata.report.metrics.base_metric import BaseMetric

tstr_mapper: Incomplete
DECIMAL_PRECISION: int

class PredictiveScore(BaseMetric):
    def __init__(self, formatter=..., exclude_entity_col: bool = True) -> None: ...
    @property
    def name(self) -> str: ...

class TSTR(PredictiveScore):
    def __init__(self, formatter=...) -> None: ...

class TSTRTimeseries(PredictiveScore):
    def __init__(self, formatter=..., exclude_entity_col: bool = True) -> None: ...

def feature_importance(df_real, df_synth, target, visualize: bool = False): ...

class QScore(BaseMetric):
    max_cols: Incomplete
    n_queries: Incomplete
    n_bins: Incomplete
    max_categories: Incomplete
    compute_penalty: Incomplete
    def __init__(self, formatter=..., max_cols: int = 2, n_queries: int = 1000, n_bins: int = 100, compute_penalty: bool = False) -> None: ...
    @property
    def name(self) -> str: ...
    @staticmethod
    def penalty_score(matched_df, real_prematch, synth_prematch): ...

class FeatureImportance(BaseMetric):
    def __init__(self, formatter=..., include_plot: bool = True) -> None: ...
    @property
    def name(self) -> str: ...
    @property
    def type(self) -> MetricType: ...
    def feat_importance_score(self, importance_real, importance_synth, max_features: int = 10): ...
