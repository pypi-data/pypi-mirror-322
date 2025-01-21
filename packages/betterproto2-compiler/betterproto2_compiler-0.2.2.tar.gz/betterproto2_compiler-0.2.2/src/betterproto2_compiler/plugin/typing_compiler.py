import abc
import builtins
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import (
    dataclass,
    field,
)


class TypingCompiler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def optional(self, type_: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self, type_: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def dict(self, key: str, value: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def union(self, *types: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def iterable(self, type_: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def async_iterable(self, type_: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def async_iterator(self, type_: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def imports(self) -> builtins.dict[str, set[str] | None]:
        """
        Returns either the direct import as a key with none as value, or a set of
        values to import from the key.
        """
        raise NotImplementedError

    def import_lines(self) -> Iterator:
        imports = self.imports()
        for key, value in imports.items():
            if value is None:
                yield f"import {key}"
            else:
                yield f"from {key} import ("
                for v in sorted(value):
                    yield f"    {v},"
                yield ")"


@dataclass
class DirectImportTypingCompiler(TypingCompiler):
    _imports: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))

    def optional(self, type_: str) -> str:
        self._imports["typing"].add("Optional")
        return f"Optional[{type_}]"

    def list(self, type_: str) -> str:
        self._imports["typing"].add("List")
        return f"List[{type_}]"

    def dict(self, key: str, value: str) -> str:
        self._imports["typing"].add("Dict")
        return f"Dict[{key}, {value}]"

    def union(self, *types: str) -> str:
        self._imports["typing"].add("Union")
        return f"Union[{', '.join(types)}]"

    def iterable(self, type_: str) -> str:
        self._imports["typing"].add("Iterable")
        return f"Iterable[{type_}]"

    def async_iterable(self, type_: str) -> str:
        self._imports["typing"].add("AsyncIterable")
        return f"AsyncIterable[{type_}]"

    def async_iterator(self, type_: str) -> str:
        self._imports["typing"].add("AsyncIterator")
        return f"AsyncIterator[{type_}]"

    def imports(self) -> builtins.dict[str, set[str] | None]:
        return {k: v if v else None for k, v in self._imports.items()}


@dataclass
class TypingImportTypingCompiler(TypingCompiler):
    _imported: bool = False

    def optional(self, type_: str) -> str:
        self._imported = True
        return f"typing.Optional[{type_}]"

    def list(self, type_: str) -> str:
        self._imported = True
        return f"typing.List[{type_}]"

    def dict(self, key: str, value: str) -> str:
        self._imported = True
        return f"typing.Dict[{key}, {value}]"

    def union(self, *types: str) -> str:
        self._imported = True
        return f"typing.Union[{', '.join(types)}]"

    def iterable(self, type_: str) -> str:
        self._imported = True
        return f"typing.Iterable[{type_}]"

    def async_iterable(self, type_: str) -> str:
        self._imported = True
        return f"typing.AsyncIterable[{type_}]"

    def async_iterator(self, type_: str) -> str:
        self._imported = True
        return f"typing.AsyncIterator[{type_}]"

    def imports(self) -> builtins.dict[str, set[str] | None]:
        if self._imported:
            return {"typing": None}
        return {}


@dataclass
class NoTyping310TypingCompiler(TypingCompiler):
    _imports: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))

    def optional(self, type_: str) -> str:
        return f"{type_} | None"

    def list(self, type_: str) -> str:
        return f"list[{type_}]"

    def dict(self, key: str, value: str) -> str:
        return f"dict[{key}, {value}]"

    def union(self, *types: str) -> str:
        return f"{' | '.join(types)}"

    def iterable(self, type_: str) -> str:
        self._imports["collections.abc"].add("Iterable")
        return f"Iterable[{type_}]"

    def async_iterable(self, type_: str) -> str:
        self._imports["collections.abc"].add("AsyncIterable")
        return f"AsyncIterable[{type_}]"

    def async_iterator(self, type_: str) -> str:
        self._imports["collections.abc"].add("AsyncIterator")
        return f"AsyncIterator[{type_}]"

    def imports(self) -> builtins.dict[str, set[str] | None]:
        return {k: v if v else None for k, v in self._imports.items()}
