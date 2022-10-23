import json
from pathlib import Path
from typing import Any, Iterable, Protocol
from PIL import Image


def write_png(icon_out_dir: Path, used_icons: set[Path]) -> None:
    for icon in used_icons:
        with Image.open(icon) as img:
            filename = icon_out_dir / (Path(icon).name + ".PNG")
            img.save(filename, "PNG")


class IntoDict(Protocol):
    def dict(self) -> dict[str, Any]:
        ...


def write_json(data: Iterable[IntoDict], path: Path) -> None:
    out = json.dumps([o.dict() for o in data], indent=4)
    with path.open("w") as f:
        f.write(out)
