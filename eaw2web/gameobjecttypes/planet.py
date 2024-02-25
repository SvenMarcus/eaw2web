from pydantic.main import BaseModel
from eaw2web.gameobjecttypes.generic import GenericGameObject
from eaw2web.gameobjecttypes.atomics import TextEntry, WithIcon, WithText, WithTooltips


class BuildingSlots(BaseModel):
    land: int
    space: int


class PlanetAbilityInformation(WithText, WithIcon):
    pass


class PlanetTacticalDescriptions(BaseModel):
    History: TextEntry
    Population: TextEntry
    Terrain: TextEntry
    Weather: TextEntry
    Wildlife: TextEntry


class WeatherInformation(WithIcon):
    name: TextEntry
    description: TextEntry


class Planet(GenericGameObject["Planet"], WithTooltips):
    coordinates: tuple[float, float, float]
    credit_income: int
    building_slots: BuildingSlots
    max_starbase: int
    ability_info: PlanetAbilityInformation
    weather_info: WeatherInformation
    tactical_descriptions: PlanetTacticalDescriptions
