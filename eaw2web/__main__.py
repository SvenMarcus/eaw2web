from pathlib import Path

import typer
from rich.progress import Progress

from eaw2web import config, load
from eaw2web.cli.progressreporters import RichProgressReporter
from eaw2web.cli.wrappers import reporting_collector
from eaw2web.modstack import ModStack
from eaw2web.xml.collectors import (
    GameObjectCollector,
    GameObjectParser,
)
from eaw2web.xml.faction import parse_faction
from eaw2web.xml.planet import parse_planet
from eaw2web.xml.units import parse_unit_object
from eaw2web.export import export as _export

app = typer.Typer()


@app.command()
def export(config_file: Path) -> None:
    """
    Export a mods data into a web friendly format
    """

    cfg = config.parse(config_file)
    stack = ModStack(cfg.includes.modstack)
    progress_bar = Progress()
    reporter = RichProgressReporter(progress_bar)

    collector = reporting_collector(GameObjectCollector(stack, parsers()), reporter)

    with progress_bar as p:
        total_files = len(stack.gameobjectfiles) + len(stack.factionfiles)
        p.add_task("Progress", total=total_files)
        objects = load.load(cfg, collector, stack.gameobjectfiles)
        _export(cfg, "gameobjects.json", objects)

        factions = load.load(cfg, collector, stack.factionfiles)
        _export(cfg, "factions.json", factions)


def parsers() -> dict[str, GameObjectParser]:
    return {
        "Planet": parse_planet,
        "Faction": parse_faction,
        "SpaceUnit": parse_unit_object,
        "GroundCompany": parse_unit_object,
        "UniqueUnit": parse_unit_object,
        "HeroUnit": parse_unit_object,
    }


def main():
    app()
