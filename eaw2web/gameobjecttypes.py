from pydantic import BaseModel


class GenericGameObject(BaseModel):
    game_object_type: str
    xml_id: str
    text: str
    variant_of: str


class WithIcon(BaseModel):
    icon: str

class WithTooltips(BaseModel):
    tooltips: list[str]


class Unit(GenericGameObject, WithIcon, WithTooltips):
    tech_level: str
    affiliation: list[str]


class Planet(GenericGameObject, WithTooltips):
    pass


class Faction(GenericGameObject, WithIcon):
    pass
