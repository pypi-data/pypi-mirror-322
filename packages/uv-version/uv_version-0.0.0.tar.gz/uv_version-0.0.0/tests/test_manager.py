import pytest

from uv_version.collectors.git_collector import GitCollector
from uv_version.manager import BaseSetter, IncrementEnum, UvVersionManager


class TestManager(object):
    @pytest.fixture()
    def manager(self):
        return UvVersionManager()

    def test_init(self, manager: UvVersionManager):
        assert manager

    def test_add_collector(self, manager: UvVersionManager):
        manager.add_collector(GitCollector())
        assert manager.collectors

    def test_add_collector_error(self, manager: UvVersionManager):
        with pytest.raises(AssertionError):
            manager.add_collector(None)  # type: ignore

        assert not manager.collectors

    def test_add_setter(self, manager: UvVersionManager):
        manager.add_setter(BaseSetter())
        assert manager.setters

    def test_add_setter_error(self, manager: UvVersionManager):
        with pytest.raises(AssertionError):
            manager.add_setter(None)  # type: ignore

        assert not manager.setters

    def test_workflow(self, manager: UvVersionManager):
        manager.add_collector(GitCollector())
        manager.add_setter(BaseSetter())

        manager.collect()
        manager.get_current_version()
        manager.increment(IncrementEnum.minor)
        manager.set()
