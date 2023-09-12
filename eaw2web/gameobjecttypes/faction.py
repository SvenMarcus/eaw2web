from eaw2web.gameobjecttypes.atomics import BaseObject, WithText, WithIcon


class Faction(BaseObject, WithText, WithIcon):
    is_playable: bool
