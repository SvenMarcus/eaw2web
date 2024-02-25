from typing import Generic
from eaw2web.gameobjecttypes.atomics import (
    TGameObject,
    BaseObject,
    WithText,
    VariantType,
)


class GenericGameObject(
    BaseObject, WithText, VariantType[TGameObject], Generic[TGameObject]
):
    pass
