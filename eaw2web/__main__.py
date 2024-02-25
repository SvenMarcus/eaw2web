from pathlib import Path
from typing import Any, TypeGuard

import typer
from rich.progress import Progress

from eaw2web import config, load
from eaw2web.cli.progressreporters import RichProgressReporter
from eaw2web.cli.wrappers import reporting_collector
from eaw2web.export import xml, json
from eaw2web.gameobjecttypes import Campaign, Faction, Planet, TradeRoute, Unit
from eaw2web.modstack import ModStack
from eaw2web.pipeline import Pipeline
from eaw2web.text import Encyclopedia
from eaw2web.transformers.campaignsets import GalacticConquestSet, transform_to_gc_sets
from eaw2web.xml.collectors import GameObjectCollector

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

    encyclopedia = Encyclopedia(cfg.includes.textcsv)
    collector = reporting_collector(GameObjectCollector(stack, encyclopedia), reporter)
    _pipelines = pipelines()

    with progress_bar as p:
        total_files = sum(len(files) for _, files in stack.filelists.items())
        p.add_task("Progress", total=total_files)

        for _, files in stack.filelists.items():
            objects = load.load(cfg, collector, files)
            for pipeline in _pipelines:
                pipeline.save_relevant(objects)

        for pipeline in _pipelines:
            json_exporter = json.exporter(
                cfg, output_name(pipeline.result_type.__name__)
            )
            pipeline.export(json_exporter)

            if exports_campaign(pipeline):
                xml_exporter = xml.exporter(cfg, "campaigns.xml")
                pipeline.export(xml_exporter)


def exports_campaign(
    pipeline: Pipeline[Any, Any]
) -> TypeGuard[Pipeline[Campaign, Campaign]]:
    return pipeline.result_type == Campaign


Pipelines = list[
    Pipeline[Campaign, GalacticConquestSet]
    | Pipeline[Campaign, Campaign]
    | Pipeline[Planet, Planet]
    | Pipeline[Faction, Faction]
    | Pipeline[TradeRoute, TradeRoute]
    | Pipeline[Unit, Unit]
]


def pipelines() -> Pipelines:
    return [
        Pipeline(Campaign, GalacticConquestSet, [transform_to_gc_sets]),
        Pipeline(Campaign, Campaign, []),
        Pipeline(Planet, Planet, []),
        Pipeline(TradeRoute, TradeRoute, []),
        Pipeline(Faction, Faction, []),
        Pipeline(Unit, Unit, []),
    ]


def output_name(object_typename: str) -> str:
    return object_typename.lower() + "s.json"


def main() -> None:
    app()
