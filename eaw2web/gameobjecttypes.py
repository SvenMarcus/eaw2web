from pathlib import Path

from pydantic import BaseModel


class BaseObject(BaseModel):
    file: Path
    game_object_type: str
    xml_id: str


class VariantType(BaseModel):
    variant_of: str


class TextEntry(BaseModel):
    key: str
    text: str


class WithText(BaseModel):
    textentry: TextEntry


class GenericGameObject(BaseObject, WithText, VariantType):
    pass


class WithIcon(BaseModel):
    icon: str


class WithTooltips(BaseModel):
    tooltips: list[TextEntry]


class Unit(GenericGameObject, WithIcon, WithTooltips):
    tech_level: str
    affiliation: list[str]


class BuildingSlots:
    land: int
    space: int


class PlanetAbilityInformation(WithText, WithIcon):
    pass


class Planet(GenericGameObject, WithTooltips):
    coordinates: tuple[float, float, float]
    max_starbase: int
    ability_info: PlanetAbilityInformation
    building_slots: BuildingSlots


class TradeRoute(BaseObject):
    point_a: str
    point_b: str


class Faction(BaseObject, WithText, WithIcon):
    is_playable: bool


class CampaignPlayerSettings(BaseModel):
    player_name: str
    ai_player_name: str | None = None
    home_location: str | None = None
    story_name: str | None = None
    markup_filename: str | None = None
    starting_credits: int | None = None
    starting_tech_level: int | None = None
    max_tech_level: int | None = None


class StartingForce(BaseModel):
    player_name: str
    location_name: str
    type_name: str


class CampaignMenuSettings(BaseModel):
    sort_order: int
    is_listed: bool
    supports_custom_settings: bool
    show_completed_tab: bool


class CampaignCameraSettings(BaseModel):
    shift: tuple[float, float]
    distance: float


class CampaignMetaSettings(BaseModel):
    conquest_set: str
    tutorial: bool
    story_campaign: bool
    planet_auto_reveal: bool
    autoresolve_allowed: bool


class Campaign(BaseObject, WithText):
    active_player: str
    planets: list[str]
    traderoutes: list[str]
    description: TextEntry
    starting_forces: list[StartingForce]
    player_settings: list[CampaignPlayerSettings]
    meta_settings: CampaignMetaSettings
    camera_settings: CampaignCameraSettings
    menu_settings: CampaignMenuSettings
