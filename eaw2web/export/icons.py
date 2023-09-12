from collections.abc import Iterable
from pathlib import Path

from eaw2web.config import Config
from eaw2web.gameobjecttypes.atomics import WithIcon
from eaw2web.icon import IconDirectories
from eaw2web.pipeline import Exporter
from eaw2web import writers


def export(config: Config) -> Exporter[WithIcon]:
    def export(objects: Iterable[WithIcon]) -> None:
        output_dir = Path(config.outdir)
        icons = IconDirectories(config.includes.icondirs)
        used_icons = icons.icons_for_objects(objects)

        icon_out_dir = output_dir / "icons"
        icon_out_dir.mkdir(exist_ok=True)
        writers.write_png(icon_out_dir, used_icons)

    return export
