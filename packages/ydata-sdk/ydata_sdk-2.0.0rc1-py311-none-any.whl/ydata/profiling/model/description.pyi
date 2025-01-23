from dataclasses import dataclass
from typing import Any
from ydata_profiling.model.description import BaseDescription as Base

@dataclass
class BaseDescription(Base):
    outliers: Any = ...
    def __init__(self, *generated_args, outliers=..., **generated_kwargs) -> None: ...
