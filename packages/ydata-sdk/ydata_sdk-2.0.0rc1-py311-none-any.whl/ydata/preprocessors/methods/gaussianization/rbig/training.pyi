import numpy as np
from ydata.preprocessors.methods.gaussianization.rbig.base import FlowModel
from ydata.preprocessors.methods.gaussianization.rbig.config import RBIGConfig

def train_rbig_info_loss(X: np.ndarray, config: RBIGConfig, progress_bar: bool = False) -> FlowModel: ...
