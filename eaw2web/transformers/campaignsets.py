from typing import Iterator
from pydantic import BaseModel
from itertools import groupby

from eaw2web.gameobjecttypes import Campaign


class GalacticConquest(BaseModel):
    name: str
    faction: str
    planets: list[str]


class GalacticConquestSet(BaseModel):
    setname: str
    conquests: list[GalacticConquest]


def transform_to_gc_sets(campaigns: list[Campaign]) -> list[GalacticConquestSet]:
    sets = groupby(campaigns, lambda key: key.conquest_set)
    return [
        GalacticConquestSet(
            setname=setname,
            conquests=_gcs_in_set(campaigns_in_set),
        )
        for setname, campaigns_in_set in sets
    ]


def _gcs_in_set(campaigns: Iterator[Campaign]) -> list[GalacticConquest]:
    return [
        GalacticConquest(
            name=c.xml_id, faction=c.active_player, planets=list(c.planets)
        )
        for c in campaigns
    ]
