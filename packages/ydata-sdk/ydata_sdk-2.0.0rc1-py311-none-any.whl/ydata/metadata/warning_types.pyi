from _typeshed import Incomplete
from enum import Enum

class Level(Enum):
    MODERATE = 1
    HIGH = 2

class WarningType(Enum):
    SKEWNESS = 'skewness'
    MISSINGS = 'missings'
    CARDINALITY = 'cardinality'
    DUPLICATES = 'duplicates'
    IMBALANCE = 'imbalance'
    CONSTANT = 'constant'
    INFINITY = 'infinity'
    ZEROS = 'zeros'
    CORRELATION = 'correlation'
    UNIQUE = 'unique'
    UNIFORM = 'uniform'
    CONSTANT_LENGTH = 'constant_length'

class WarningOrientation(Enum):
    COLUMN = 'column'
    DATASET = 'dataset'

WARNING_MAPS: Incomplete

class Warning:
    column: Incomplete
    type: Incomplete
    details: Incomplete
    def __init__(self, warning_type: WarningType, details: dict, column: dict = None) -> None: ...

class BaseWarning:
    def __init__(self, warning_type: WarningType, orientation: WarningOrientation, metric_name: str = None) -> None: ...
    def evaluate(self, summary: dict, dtypes: dict) -> list[Warning]: ...
    @property
    def type(self): ...
    @property
    def orientation(self): ...

class WarningEngine:
    warnings: dict[str, BaseWarning]
    def __init__(self, warnings: dict[str, BaseWarning]) -> None: ...
    def evaluate(self, summary: dict, dtypes: dict): ...

class SkewnessWarning(BaseWarning):
    def __init__(self) -> None: ...

class DuplicatesWarning(BaseWarning):
    def __init__(self) -> None: ...

class HighCardinalityWarning(BaseWarning):
    def __init__(self) -> None: ...

class ImbalanceWarning(BaseWarning):
    def __init__(self) -> None: ...

class MissingValuesWarning(BaseWarning):
    def __init__(self) -> None: ...

class ConstantWarning(BaseWarning):
    def __init__(self) -> None: ...

class ZerosWarning(BaseWarning):
    def __init__(self) -> None: ...

class InfinityWarning(BaseWarning):
    def __init__(self) -> None: ...

class CorrelationWarning(BaseWarning):
    def __init__(self) -> None: ...

class UniqueWarning(BaseWarning):
    def __init__(self) -> None: ...

class UniformWarning(BaseWarning):
    def __init__(self) -> None: ...

class ConstantLengthWarning(BaseWarning):
    def __init__(self) -> None: ...
