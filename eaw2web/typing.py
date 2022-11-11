from typing import TypeAlias, TypeVar


TFirst = TypeVar("TFirst")
TSecond = TypeVar("TSecond")

Pair: TypeAlias = tuple[TFirst, TSecond]

GameObjectType = TypeVar("GameObjectType")