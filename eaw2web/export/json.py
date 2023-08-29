from pathlib import Path
from typing import Any, Iterable, TypeGuard

from pydantic import BaseModel

from eaw2web import writers
from eaw2web.config import Config
from eaw2web.gameobjecttypes import WithIcon
from eaw2web.icon import IconDirectories
from eaw2web.pipeline import Exporter


def has_icon(obj: Any) -> TypeGuard[WithIcon]:
    return isinstance(obj, WithIcon)


def exporter(config: Config, filename: str) -> Exporter[BaseModel]:
    def export(objects: Iterable[BaseModel]) -> None:
        output_dir = Path(config.outdir)
        output_dir.mkdir(exist_ok=True)

        writers.write_json(objects, output_dir / filename)

        icons = IconDirectories(config.includes.icondirs)
        with_icons = filter(has_icon, objects)
        used_icons = icons.icons_for_objects(with_icons)

        icon_out_dir = output_dir / "icons"
        icon_out_dir.mkdir(exist_ok=True)
        writers.write_png(icon_out_dir, used_icons)

    return export
