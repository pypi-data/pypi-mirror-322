from _typeshed import Incomplete

def is_subclass_but_not_base(cls, base): ...

class InheritanceTracker(type):
    __inheritors__: Incomplete
    def __new__(cls, name, bases, dct): ...
