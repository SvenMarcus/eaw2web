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
from eaw2web.xml.traderoutes import parse_traderoute
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
        total_files = sum(len(files) for _, files in stack.filelists.items())
        p.add_task("Progress", total=total_files)

        for listname, files in stack.filelists.items():
            objects = load.load(cfg, collector, files)
            _export(cfg, output_name(listname), objects)


def output_name(filelist_name: str) -> str:
    return filelist_name.replace("Files.xml", "s.json").lower()


def parsers() -> dict[str, GameObjectParser]:
    return {
        "Planet": parse_planet,
        "TradeRoute": parse_traderoute,
        "Faction": parse_faction,
        "SpaceUnit": parse_unit_object,
        "GroundCompany": parse_unit_object,
        "UniqueUnit": parse_unit_object,
        "HeroUnit": parse_unit_object,
    }


def main():
    app()
