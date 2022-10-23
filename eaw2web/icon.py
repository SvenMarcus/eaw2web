from pathlib import Path
from typing import Any, Iterable, Optional, cast

from eaw2web.gameobjecttypes import WithIcon


class IconDirectories:
    def __init__(self, icon_dirs: list[str], extension: str = ".TGA") -> None:
        self._dirs = [Path(_dir) for _dir in icon_dirs]

    def iconpath(self, icon_name: str) -> Path:
        if icon_name:
            for _dir in self._dirs:
                for icon in _dir.glob(icon_name + ".TGA"):
                    return icon

        raise FileNotFoundError(icon_name)

    def icons_for_objects(self, objects: Iterable[WithIcon]) -> set[Path]:
        def _iconpath(obj: WithIcon) -> Optional[Path]:
            try:
                return self.iconpath(obj.icon)
            except FileNotFoundError:
                return None

        def not_none(obj: Any) -> bool:
            return obj is not None

        valid_paths = filter(not_none, {_iconpath(obj) for obj in objects})
        return cast(set[Path], set(valid_paths))
