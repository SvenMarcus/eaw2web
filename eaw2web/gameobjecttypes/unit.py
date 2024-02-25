from eaw2web.gameobjecttypes.atomics import WithIcon, WithTooltips
from eaw2web.gameobjecttypes.generic import GenericGameObject


class Unit(GenericGameObject["Unit"], WithIcon, WithTooltips):
    tech_level: int
    affiliation: list[str]
