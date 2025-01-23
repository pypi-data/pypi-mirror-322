from _typeshed import Incomplete
from pandas import DataFrame as pdDataFrame, Series as pdSeries

def spearman(df: pdDataFrame) -> float: ...
def cramers_v(col_1: pdSeries, col_2: pdSeries) -> float: ...

mapping: Incomplete
