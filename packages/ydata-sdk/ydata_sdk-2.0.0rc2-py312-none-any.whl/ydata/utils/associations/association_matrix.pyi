from dask.dataframe import DataFrame as ddDataFrame
from pandas import DataFrame as pdDataFrame
from ydata.dataset import Dataset
from ydata.utils.associations.measure_associations import MeasureAssociations, PairwiseMatrixMapping

def association_matrix(dataset: Dataset | ddDataFrame | pdDataFrame, datatypes: dict | None = None, vartypes: dict | None = None, columns: dict | None = None, association_measurer: type[MeasureAssociations] = None, mapping: PairwiseMatrixMapping | None = ...) -> pdDataFrame: ...
