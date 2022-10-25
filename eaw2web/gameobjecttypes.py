from pydantic import BaseModel


class BaseObject(BaseModel):
    game_object_type: str
    xml_id: str


class GenericGameObject(BaseObject):
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
    coordinates: tuple[float, float, float]


class TradeRoute(BaseObject):
    point_a: str
    point_b: str


class Faction(GenericGameObject, WithIcon):
    pass
