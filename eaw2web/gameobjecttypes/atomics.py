from pathlib import Path
from typing import Any, Generic, TypeVar

from pydantic import BaseModel


class BaseObject(BaseModel):
    file: Path
    game_object_type: str
    xml_id: str


TGameObject = TypeVar("TGameObject", bound=BaseObject)


class VariantType(BaseModel, Generic[TGameObject]):
    variant_of: TGameObject | None

    def __getattr__(self, name: str) -> Any:
        value = super().__getattribute__(name)
        if value:
            return value
        else:
            variant = super().__getattribute__("variant_of")
            return getattr(variant, name, None)


class TextEntry(BaseModel):
    key: str
    text: str


class WithText(BaseModel):
    textentry: TextEntry


class WithIcon(BaseModel):
    icon: str


class WithTooltips(BaseModel):
    tooltips: list[TextEntry]
