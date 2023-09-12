from pathlib import Path
from typing import Iterable, TypeGuard

from eaw2web.gameobjecttypes.atomics import WithIcon


class IconDirectories:
    def __init__(self, icon_dirs: list[str], extension: str = ".TGA") -> None:
        self._dirs = [Path(_dir) for _dir in icon_dirs]
        self._ext = extension

    def iconpath(self, icon_name: str) -> Path:
        if icon_name:
            for _dir in self._dirs:
                for icon in _dir.glob(icon_name + self._ext):
                    return icon

        raise FileNotFoundError(icon_name)

    def icons_for_objects(self, objects: Iterable[WithIcon]) -> set[Path]:
        def _iconpath(obj: WithIcon) -> Path | None:
            try:
                return self.iconpath(obj.icon)
            except FileNotFoundError:
                return None

        def not_none(obj: Path | None) -> TypeGuard[Path]:
            return obj is not None

        valid_paths = filter(not_none, {_iconpath(obj) for obj in objects})
        return set(valid_paths)
