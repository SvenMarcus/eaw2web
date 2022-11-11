from pathlib import Path
from typing import Any

import typer
from rich.progress import Progress

from eaw2web import config, load
from eaw2web.cli.progressreporters import RichProgressReporter
from eaw2web.cli.wrappers import reporting_collector
from eaw2web.gameobjecttypes import Campaign, Faction, Planet, TradeRoute, Unit
from eaw2web.modstack import ModStack
from eaw2web.pipeline import Pipeline
from eaw2web.transformers.campaignsets import GalacticConquestSet, transform_to_gc_sets
from eaw2web.xml.collectors import (
    GameObjectCollector,
    GameObjectParser,
)
from eaw2web.xml.campaign import parse_campaign
from eaw2web.xml.faction import parse_faction
from eaw2web.xml.planet import parse_planet
from eaw2web.xml.traderoutes import parse_traderoute
from eaw2web.xml.units import parse_unit_object

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
    _pipelines = pipelines()

    with progress_bar as p:
        total_files = sum(len(files) for _, files in stack.filelists.items())
        p.add_task("Progress", total=total_files)

        for _, files in stack.filelists.items():
            objects = load.load(cfg, collector, files)
            for pipeline in _pipelines:
                pipeline.save_relevant(objects)

        for pipeline in _pipelines:
            pipeline.export(cfg, output_name(pipeline.result_type.__name__))


def parsers() -> dict[str, GameObjectParser]:
    return {
        "Campaign": parse_campaign,
        "Planet": parse_planet,
        "TradeRoute": parse_traderoute,
        "Faction": parse_faction,
        "SpaceUnit": parse_unit_object,
        "GroundCompany": parse_unit_object,
        "UniqueUnit": parse_unit_object,
        "HeroUnit": parse_unit_object,
    }


def pipelines() -> list[Pipeline[Any, Any]]:
    return [
        Pipeline(Campaign, GalacticConquestSet, [transform_to_gc_sets]),
        Pipeline(Planet, Planet, []),
        Pipeline(TradeRoute, TradeRoute, []),
        Pipeline(Faction, Faction, []),
        Pipeline(Unit, Unit, []),
    ]


def output_name(object_typename: str) -> str:
    return object_typename.lower() + "s.json"


def main():
    app()
