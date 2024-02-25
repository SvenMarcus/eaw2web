import itertools
from pathlib import Path
from typing import NamedTuple
from xml.etree.ElementTree import Element

from eaw2web.gameobjecttypes import (
    CampaignCameraSettings,
    Campaign,
    CampaignMenuSettings,
    CampaignMetaSettings,
    CampaignPlayerSettings,
    StartingForce,
)
from eaw2web.gameobjecttypes.atomics import BaseObject
from eaw2web.text import Encyclopedia, from_csv_line, strip_entries
from eaw2web.xml.base import parse_base_object
from eaw2web.xml.tags import TagParser
from eaw2web.xml.text import collect_texts, text_or_empty


def parse_campaign(
    file: Path,
    child: Element,
    encyclopedia: Encyclopedia,
    variant: BaseObject | None = None,
) -> Campaign:
    parser = TagParser(child)
    return Campaign(
        **parse_base_object(file, child).model_dump(),
        active_player=parser.text("Starting_Active_Player"),
        textentry=encyclopedia.get_text(parser.text("Text_ID")),
        description=encyclopedia.get_text(parser.text("Description_Text")),
        planets=_parse_locations(child),
        traderoutes=strip_entries(
            from_csv_line(text_or_empty(child.find("Trade_Routes")))
        ),
        player_settings=_parse_player_settings(child),
        camera_settings=_parse_camera_settings(child),
        menu_settings=_parse_menu_settings(child),
        meta_settings=_parse_meta_settings(child),
        starting_forces=_parse_starting_forces(child),
    )


def _parse_locations(child: Element) -> list[str]:
    location_texts = collect_texts(child.findall("Locations"))
    return [
        planet.strip()
        for line in location_texts
        for planet in line.split(",")
        if planet.strip()
    ]


_tags_to_settings = {
    "Story_Name": "story_name",
    "AI_Player_Control": "ai_player_name",
    "Starting_Credits": "starting_credits",
    "Starting_Tech_Level": "starting_tech_level",
    "Max_Tech_Level": "max_tech_level",
    "Markup_Filename": "markup_filename",
}

_hardcoded_player_names = ["Empire", "Rebel", "Underworld"]


def _parse_player_settings(child: Element) -> list[CampaignPlayerSettings]:
    xml_settings = XmlPlayerSettings()
    generic_story_names = child.find("Story_Name")

    for tag_name, setting_name in _tags_to_settings.items():
        tags = child.findall(tag_name)
        xml_settings.insert_settings(setting_name, collect_texts(tags))

    story_mappings = strip_entries(text_or_empty(generic_story_names).split(","))
    for player_name, story_name in itertools.pairwise(story_mappings):
        xml_settings.insert_setting(player_name, Setting("story_name", story_name))

    for player_name in _hardcoded_player_names:
        tag = child.find(f"{player_name}_Story_Name")
        if not tag:
            continue

        xml_settings.insert_setting(
            player_name, Setting("story_name", text_or_empty(tag))
        )

    return xml_settings.to_player_settings()


def _parse_starting_forces(child: Element) -> list[StartingForce]:
    forces = collect_texts(child.findall("Starting_Forces"))
    split_forces = [force.split(",") for force in forces]
    return [
        StartingForce(
            player_name=player_name.strip(),
            location_name=location_name.strip(),
            type_name=type_name.strip(),
        )
        for player_name, location_name, type_name in split_forces
    ]


def _parse_camera_settings(child: Element) -> CampaignCameraSettings:
    return CampaignCameraSettings(
        shift=(
            float(child.findtext("Camera_Shift_X") or 0),
            float(child.findtext("Camera_Shift_Y") or 0),
        ),
        distance=float(child.findtext("Camera_Distance") or 0),
    )


def _parse_menu_settings(child: Element) -> CampaignMenuSettings:
    return CampaignMenuSettings(
        sort_order=int(child.findtext("Sort_Order") or 0),
        is_listed=bool(child.findtext("Is_Listed") or True),
        supports_custom_settings=bool(
            child.findtext("Supports_Custom_Settings") or False
        ),
        show_completed_tab=bool(child.findtext("Show_Completed_Tab") or True),
    )


def _parse_meta_settings(child: Element) -> CampaignMetaSettings:
    return CampaignMetaSettings(
        conquest_set=text_or_empty(child.find("Campaign_Set")),
        story_campaign=bool(child.findtext("Is_Story_Campaign") or False),
        tutorial=bool(child.findtext("Tutorial") or False),
        planet_auto_reveal=bool(child.findtext("Planet_Auto_Reveal") or True),
        autoresolve_allowed=bool(child.findtext("Is_Autoresolve_Allowed") or True),
    )


class Setting(NamedTuple):
    name: str
    value: int | float | str | None


class XmlPlayerSettings:
    def __init__(self) -> None:
        self._settings_by_player: dict[str, dict[str, int | float | str | None]] = {}

    def insert_setting(self, player_name: str, setting: Setting) -> None:
        player_settings = self._settings_by_player.setdefault(player_name, {})
        player_settings[setting.name] = setting.value

    def insert_settings(self, setting_name: str, values: list[str]) -> None:
        for text in values:
            player, setting_value, *_ = strip_entries(text.split(","))
            self.insert_setting(player, Setting(setting_name, setting_value))

    def to_player_settings(self) -> list[CampaignPlayerSettings]:
        return [
            CampaignPlayerSettings(
                player_name=player,
                **self._settings_by_player[player],  # type: ignore
            )
            for player in self._settings_by_player
        ]
