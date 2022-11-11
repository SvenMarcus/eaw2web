from pydantic import BaseModel


class BaseObject(BaseModel):
    game_object_type: str
    xml_id: str


class VariantType(BaseModel):
    variant_of: str


class WithText(BaseModel):
    text: str


class GenericGameObject(BaseObject, WithText, VariantType):
    pass


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


class Faction(BaseObject, WithText, WithIcon):
    is_playable: bool


class Campaign(BaseObject, WithText):
    conquest_set: str
    active_player: str
    planets: list[str]
    traderoutes: list[str]
    description: str
