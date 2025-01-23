from pandas import DataFrame as pdDataFrame
from ydata.quality.outlier.prototype import BaseClusteringOperator, OutlierCluster

class IndividualClustering(BaseClusteringOperator):
    def predict(self, X: pdDataFrame) -> list[OutlierCluster]: ...
