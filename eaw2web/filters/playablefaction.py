from eaw2web.gameobjecttypes import Faction


def only_playable(factions: list[Faction]) -> list[Faction]:
    return [faction for faction in factions if faction.is_playable]
