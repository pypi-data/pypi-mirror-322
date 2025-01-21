import abc
from typing import Any, Optional


class BaseCollector(abc.ABC):
    """Базовый коллектор для определения версии."""

    @abc.abstractmethod
    def collect(self) -> Optional[str]:
        pass

    @abc.abstractmethod
    def data(self) -> Optional[dict[str, Any]]:
        pass
