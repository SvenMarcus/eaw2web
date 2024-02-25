from pathlib import Path
from typing import Generic, TypeVar
from pydantic import BaseModel


class BaseObject(BaseModel):
    file: Path
    game_object_type: str
    xml_id: str


TGameObject = TypeVar("TGameObject", bound=BaseObject)


class VariantType(BaseModel, Generic[TGameObject]):
    variant_of: TGameObject | None


class TextEntry(BaseModel):
    key: str
    text: str


class WithText(BaseModel):
    textentry: TextEntry


class WithIcon(BaseModel):
    icon: str


class WithTooltips(BaseModel):
    tooltips: list[TextEntry]
