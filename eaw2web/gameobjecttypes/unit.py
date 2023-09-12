from eaw2web.gameobjecttypes.atomics import WithIcon, WithTooltips
from eaw2web.gameobjecttypes.generic import GenericGameObject


class Unit(GenericGameObject, WithIcon, WithTooltips):
    tech_level: str
    affiliation: list[str]
