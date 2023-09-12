from pathlib import Path
from typing import Any, Iterable, TypeGuard

from pydantic import BaseModel

from eaw2web import writers
from eaw2web.config import Config
from eaw2web.gameobjecttypes.atomics import WithIcon
from eaw2web.pipeline import Exporter


def has_icon(obj: Any) -> TypeGuard[WithIcon]:
    return isinstance(obj, WithIcon)


def exporter(config: Config, filename: str) -> Exporter[BaseModel]:
    def export(objects: Iterable[BaseModel]) -> None:
        output_dir = Path(config.outdir)
        output_dir.mkdir(exist_ok=True)

        writers.write_json(objects, output_dir / filename)

    return export
