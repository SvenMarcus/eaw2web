from pathlib import Path
from pydantic import BaseModel


class BaseObject(BaseModel):
    file: Path
    game_object_type: str
    xml_id: str


class VariantType(BaseModel):
    variant_of: BaseObject | None


class TextEntry(BaseModel):
    key: str
    text: str


class WithText(BaseModel):
    textentry: TextEntry


class WithIcon(BaseModel):
    icon: str


class WithTooltips(BaseModel):
    tooltips: list[TextEntry]
