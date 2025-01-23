from _typeshed import Incomplete
from enum import Enum
from ydata.characteristics import ColumnCharacteristic

class DataType(Enum):
    NUMERICAL = 'numerical'
    CATEGORICAL = 'categorical'
    DATE = 'date'
    STR = 'string'
    LONGTEXT = 'longtext'

class VariableType(Enum):
    INT = 'int'
    FLOAT = 'float'
    STR = 'string'
    BOOL = 'bool'
    DATETIME = 'datetime'
    DATE = 'date'

class ScaleType(Enum):
    METRIC = 'metric'
    ORDINAL = 'ordinal'
    NOMINAL = 'nominal'

DATA_VARTYPE_MAP: Incomplete
CATEGORICAL_DTYPES: Incomplete

def type_check(data, _type, extra_msg: str = '') -> None: ...
def validate_datatypes(data_type: dict, valid_dtypes: list = None): ...
def is_characteristic_type_valid(characteristic: ColumnCharacteristic, vartype: VariableType) -> bool: ...
