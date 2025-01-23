from _typeshed import Incomplete
from abc import ABC
from ydata.connectors.filetype import FileType

class ReaderException(Exception): ...

class AbstractReader(ABC):
    file_type: Incomplete
    def __init__(self, file_type: FileType) -> None: ...
    @property
    def read(self): ...

class DaskReader(AbstractReader):
    __FILETYPE_READER_MAP__: Incomplete

class PandasReader(AbstractReader):
    __FILETYPE_READER_MAP__: Incomplete
