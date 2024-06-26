from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Protocol,
    Type,
    TypeGuard,
    TypeVar,
    cast,
)

from pydantic import BaseModel

from eaw2web.typing import GameObjectType

PipelineResult = TypeVar("PipelineResult", bound=BaseModel, contravariant=True)


class Exporter(Protocol, Generic[PipelineResult]):
    def __call__(self, objects: Iterable[PipelineResult]) -> None:
        ...


class Pipeline(Generic[GameObjectType, PipelineResult]):
    def __init__(
        self,
        origin_type: Type[GameObjectType],
        result_type: Type[PipelineResult],
        pipeline: list[Callable[[list[Any]], Any]],
    ) -> None:
        self._objects: list[GameObjectType] = []
        self._pipeline = pipeline

        self.object_type = origin_type

        # we are not doing anything with this, but it helps us with type hinting
        self.result_type = result_type

    def save_relevant(self, objects: Iterable[BaseModel]) -> None:
        def is_type(o: Any) -> TypeGuard[GameObjectType]:
            return isinstance(o, self.object_type)

        self._objects.extend(filter(is_type, objects))

    def run(self) -> list[PipelineResult]:
        transformed = self._objects
        for pipe in self._pipeline:
            transformed = pipe(transformed)

        return cast(list[PipelineResult], transformed)

    def export(self, exporter: Exporter[PipelineResult]) -> None:
        exporter(self.run())
