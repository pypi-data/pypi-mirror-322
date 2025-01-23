from typing import Sequence

class BracketInterval: ...

class ExplicitBracketInterval(BracketInterval):
    endpoint_1: float
    endpoint_2: float

class LowerEndpointAndGuess(BracketInterval):
    lower_endpoint: float
    initial_guess: float

class NoBracketIntervalFoundError(Exception): ...
class NoOptimumFoundError(Exception): ...

def calibrate_dp_mechanism(target_epsilon: float, target_delta: float, bracket_interval: BracketInterval | None = None, orders: Sequence[float] | None = None, discrete: bool = False, tol: float | None = None) -> float | int: ...
