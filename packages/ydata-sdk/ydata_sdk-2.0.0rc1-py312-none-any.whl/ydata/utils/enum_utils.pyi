from enum import Enum
from typing import Literal

def enum_to_literal(e: type[Enum]) -> Literal: ...

class EnumToLiteralMixIn(Enum):
    @classmethod
    def to_literal(cls) -> Literal: ...
