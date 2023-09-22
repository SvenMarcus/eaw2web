from typing import Any, Callable, Concatenate, ParamSpec, TypeVar
from xml.etree import ElementTree as et
from eaw2web.text import from_csv_line, strip_entries


class ChildNotFoundError(RuntimeError):
    def __init__(self, parent: et.Element, child: str) -> None:
        super().__init__()
        self.message = f"""
        The tag {child} does not exist on the element 
        Type={parent.tag} Name={parent.get("Name")}
        """

    def __str__(self) -> str:
        return self.message


class ParsingError(RuntimeError):
    def __init__(self, parent: et.Element, child: str, reason: str = "Unknown") -> None:
        super().__init__()
        self.failed_because_of_empty_tag = False

        child_element = parent.find(child)
        if child_element is None:
            raise ChildNotFoundError(parent, child)

        if child_element.text is None:
            reason = "Text of tag is None"
            self.failed_because_of_empty_tag = True

        self.message = f"""
        An error occured while parsing the tag {child_element.tag}
        of parent Type={parent.tag} Name={parent.get("Name")}
        Reason: {reason}
        """

    def __str__(self) -> str:
        return self.message


def safeint(value: str) -> int:
    return int(float(value))


T = TypeVar("T")
P = ParamSpec("P")

ParserFunc = Callable[Concatenate[str, P], T]


def allow_missing(
    parser: ParserFunc[P, T],
    tag: str,
    fallback: T,
    *parserargs: P.args,
    **parserkwargs: P.kwargs,
) -> T:
    try:
        return parser(tag, *parserargs, **parserkwargs)
    except ChildNotFoundError:
        return fallback
    except ParsingError as ex:
        if ex.failed_because_of_empty_tag:
            return fallback
        else:
            raise ex


class TagParser:
    def __init__(self, element: et.Element) -> None:
        self._element = element

    def text(self, tag: str) -> str:
        child = self._element.find(tag)
        if child is None:
            raise ChildNotFoundError(self._element, tag)

        if child.text is None:
            raise ParsingError(self._element, tag)

        return child.text.strip()

    def integer(self, tag: str) -> int:
        try:
            return safeint(self.text(tag))
        except ValueError:
            raise ParsingError(
                self._element, tag, reason="Could not convert value to integer"
            )

    def floating(self, tag: str) -> float:
        try:
            return float(self.text(tag))
        except ValueError:
            raise ParsingError(
                self._element, tag, reason="Could not convert value to float"
            )

    def csv(
        self, tag: str, converters: list[Callable[[str], Any]] | None = None
    ) -> tuple[str, ...]:
        text = self.text(tag)

        split = list(from_csv_line(text))
        split = strip_entries(split)

        if not converters:
            return tuple(split)

        if len(converters) != len(split):
            raise ParsingError(
                self._element,
                tag,
                reason=f"""
                The number of converters does not match the number of elements.
                Expected: {len(converters)}, Got: {len(split)}
                Elements: {split}
                """,
            )

        return tuple(convert(element) for convert, element in zip(converters, split))

    def boolean(self, tag: str) -> bool:
        string = self.text(tag).lower()
        true_values = ("yes", "true")
        false_values = ("no", "false")
        if string not in (*true_values, *false_values):
            raise ParsingError(
                self._element,
                tag,
                reason="The tag does not contain a valid boolean value",
            )
        return string in true_values
