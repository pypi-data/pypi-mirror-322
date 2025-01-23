from _typeshed import Incomplete

class MutualInfoRBIG:
    bins: Incomplete
    alpha: Incomplete
    bound_ext: Incomplete
    eps: Incomplete
    rotation: Incomplete
    zero_tolerance: Incomplete
    max_layers: Incomplete
    def __init__(self, bins: int | str = 'auto', alpha: float = 1e-10, bound_ext: float = 0.3, eps: float = 1e-10, rotation: str = 'PCA', zero_tolerance: int = 60, max_layers: int = 1000) -> None: ...
    rbig_model_X: Incomplete
    rbig_model_Y: Incomplete
    rbig_model_XY: Incomplete
    def fit(self, X, Y): ...
    def mutual_info(self): ...
