from typing import Protocol, ClassVar, Any, TypeVar
from dataclasses import Field

class DataclassInstance(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]

T = TypeVar("T", bound=DataclassInstance)

def fromdict[V: DataclassInstance](d: dict[str, Any], ty: type[V]) -> V:
    """Return a dataclass instance by mapping the dictionary to the dataclass fields.
    
    Example usage::

        @dataclass
        class Dataclass:
            x: int
            y: int

        dictionary = {"x": "1", "y": "2"}
        
        assert fromdict(dictionary, Dataclass) == Dataclass(x=1, y=2)

    """

    return ty(**d)
