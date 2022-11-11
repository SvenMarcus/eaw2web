from pathlib import Path
from typing import Iterable
import plotly.express as px  # type: ignore

from eaw2web.gameobjecttypes import Campaign, Planet


def plot_galaxy(campaign: Campaign, planets: Iterable[Planet], outdir: Path) -> None:
    planets_in_campaign = [
        planet for planet in planets if planet.xml_id in campaign.planets
    ]

    names = [planet.text for planet in planets_in_campaign]
    x, y, _ = zip(*[planet.coordinates for planet in planets_in_campaign])

    figure = px.scatter(x=x, y=y, hover_name=names, template="plotly_dark")
    with open(outdir / (campaign.xml_id + ".html"), "w") as f:
        f.write(figure.to_html())
