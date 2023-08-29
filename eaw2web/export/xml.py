from pathlib import Path
from typing import Iterable

from jinja2 import Template

from eaw2web.config import Config
from eaw2web.gameobjecttypes import Campaign
from eaw2web.pipeline import Exporter

_templates = Path(__file__).parent / "templates"


def exporter(config: Config, filename: str) -> Exporter[Campaign]:
    def export(objects: Iterable[Campaign]) -> None:
        output_dir = Path(config.outdir)
        output_dir.mkdir(exist_ok=True)
        out = output_dir / filename

        template: Template = Template((_templates / "campaign.xml.j2").read_text())
        rendered = template.render(campaigns=objects)
        out.write_text(rendered)

    return export
