from pathlib import Path
from typing import TypeGuard

import eaw2web.writers as writers
from eaw2web.config import Config
from eaw2web.gameobjecttypes import Faction, GenericGameObject, WithIcon
from eaw2web.icon import IconDirectories
from eaw2web.modstack import ModStack
from eaw2web.text import parse_to_text_dict
from eaw2web.xml.collectors import DataCollector, collect_from_files


def should_include(object: GenericGameObject, excluded_name_fragments: set[str]):
    return all(fragment not in object.xml_id for fragment in excluded_name_fragments)


def has_icon(obj: GenericGameObject) -> TypeGuard[WithIcon]:
    return isinstance(obj, WithIcon)


def export(
    config: Config,
    mod_stack: ModStack,
    gameobject_collector: DataCollector[GenericGameObject],
    faction_collector: DataCollector[Faction],
):
    output_dir = Path(config.outdir)
    output_dir.mkdir(exist_ok=True)

    text_dict: dict[str, str] = {}
    for csv in config.includes.textcsv:
        text_dict.update(parse_to_text_dict(csv))

    gameobjects = collect_from_files(
        files=mod_stack.gameobjectfiles,
        collector=gameobject_collector,
        mod_stack=mod_stack,
        text_dict=text_dict,
    )

    gameobjects = [
        obj for obj in gameobjects if should_include(obj, config.excludes.fragments)
    ]

    factions = collect_from_files(
        files=mod_stack.factionfiles,
        collector=faction_collector,
        mod_stack=mod_stack,
        text_dict=text_dict,
    )

    writers.write_json(gameobjects, output_dir / "gameobjects.json")
    writers.write_json(factions, output_dir / "factions.json")

    icons = IconDirectories(config.includes.icondirs)
    with_icons = filter(has_icon, gameobjects)
    used_icons = icons.icons_for_objects(with_icons)

    icon_out_dir = output_dir / "icons"
    icon_out_dir.mkdir(exist_ok=True)
    writers.write_png(icon_out_dir, used_icons)
