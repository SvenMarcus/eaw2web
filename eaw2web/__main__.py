from pathlib import Path

import typer
from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from eaw2web import config, load
from eaw2web.cli.progressreporters import RichProgressReporter
from eaw2web.cli.wrappers import reporting_collector
from eaw2web.modstack import ModStack
from eaw2web.xml.collectors import (
    FactionCollector,
    GameObjectCollector,
    GameObjectParser,
)
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
    progress_bar, file_progress = progress_bars()
    reporter = RichProgressReporter(progress_bar, file_progress)

    gameobject_collector = reporting_collector(GameObjectCollector(parsers()), reporter)
    faction_collector = reporting_collector(FactionCollector(), reporter)

    with live_console(progress_bar, file_progress):
        total_files = len(stack.gameobjectfiles) + len(stack.factionfiles)
        progress_bar.add_task("Progress", total=total_files)
        objects = load.load(cfg, stack, gameobject_collector, stack.gameobjectfiles)
        _export(cfg, "gameobjects.json", objects)

        factions = load.load(cfg, stack, faction_collector, stack.factionfiles)
        _export(cfg, "factions.json", factions)


def progress_bars():
    progress_bar = Progress()
    file_progress = Progress(
        SpinnerColumn(), TextColumn("{task.description}"), transient=True
    )

    return progress_bar, file_progress


def live_console(progress_bar: Progress, file_progress: Progress):
    group = Group(progress_bar, file_progress)
    live = Live(Panel(group))
    return live


def parsers() -> dict[str, GameObjectParser]:
    return {
        "Planet": parse_planet,
        "SpaceUnit": parse_unit_object,
        "GroundCompany": parse_unit_object,
        "UniqueUnit": parse_unit_object,
        "HeroUnit": parse_unit_object,
    }


def main():
    app()
