import numpy as np

pred_probs_by_class: dict[int, np.ndarray]
prune_count_matrix_cols: dict[int, np.ndarray]

def round_preserving_sum(iterable) -> np.ndarray: ...
def round_preserving_row_totals(confident_joint) -> np.ndarray: ...
