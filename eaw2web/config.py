from configparser import ConfigParser, SectionProxy
from pathlib import Path
from typing import Type, TypeVar
from pydantic import BaseModel, Field


def SetField():
    return Field(default_factory=set)


def ListField():
    return Field(default_factory=list)


class Excludes(BaseModel):
    tags: set[str] = SetField()
    fragments: set[str] = SetField()


class Includes(BaseModel):
    modstack: list[str] = ListField()
    icondirs: list[str] = ListField()
    textcsv: list[str] = ListField()


class Config(BaseModel):
    outdir: str = "generated"
    includes: Includes
    excludes: Excludes


def to_list(value: str):
    return value.strip().splitlines()


def to_set(value: str):
    return set(to_list(value))


class MissingConfigError(RuntimeError):
    def __init__(self, config: str) -> None:
        super().__init__()
        self.config = config

    def __str__(self) -> str:
        return f"Missing required configuration value '{self.config}'"


TExpected = TypeVar("TExpected")


class ConfigTypeError(RuntimeError):
    def __init__(self, config: str, expected_type: Type[TExpected]) -> None:  # type: ignore
        super().__init__()
        self.config = config
        self.expected_type = expected_type

    def __str__(self) -> str:
        return f"Wrong type for '{self.config}'. Expected {self.expected_type}"


def get_or_raise(
    parser: ConfigParser | SectionProxy, key: str, expected_type: Type[TExpected]
) -> TExpected:
    if key not in parser:
        raise MissingConfigError(key)

    value = parser[key]
    if not isinstance(value, expected_type):
        raise ConfigTypeError(key, expected_type)

    return value


def parse(file: Path) -> Config:
    parser = ConfigParser(converters={"list": to_list, "set": to_set})
    parser.read(file)

    include_section = get_or_raise(parser, "include", SectionProxy)

    excludes = _parse_excludes(parser)
    includes = _parse_includes(include_section)  # type: ignore

    return Config(
        outdir=_parse_output(parser),
        includes=includes,
        excludes=excludes,
    )


def _parse_output(parser: ConfigParser) -> str:
    if "output" not in parser:
        return "generated"

    output_section = parser["output"]
    if "path" not in output_section:
        return "generated"

    return output_section["path"].strip()


def _parse_excludes(parser: ConfigParser):
    if "exclude" not in parser:
        return Excludes()

    exclude_section = parser["exclude"]
    return Excludes(
        tags=exclude_section.getset("tags", set()),  # type: ignore
        fragments=exclude_section.getset("fragments", set()),  # type: ignore
    )


def _parse_includes(include_section: SectionProxy):
    return Includes(
        modstack=to_list(get_or_raise(include_section, "modstack", str)),  # type: ignore
        icondirs=to_list(get_or_raise(include_section, "icondirs", str)),  # type: ignore
        textcsv=to_list(get_or_raise(include_section, "textcsv", str)),  # type: ignore
    )
