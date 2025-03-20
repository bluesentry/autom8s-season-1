from abc import abstractmethod
from typing import Protocol


class Read(Protocol):
    @abstractmethod
    def read(self) -> None: ...


class Write(Protocol):
    @abstractmethod
    def save(self) -> None: ...


class ReadWrite(Read, Write): ...
