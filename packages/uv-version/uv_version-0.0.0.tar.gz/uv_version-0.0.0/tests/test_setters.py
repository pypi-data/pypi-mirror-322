from pathlib import Path

import pytest
from packaging.version import Version

from uv_version.setters import print_setter, pyproject_setter


class TestPrintSetter(object):
    @pytest.fixture()
    def setter(self):
        return print_setter.PrintSetter()

    def test_init(self, setter: print_setter.PrintSetter):
        assert setter

    def test_set(self, setter: print_setter.PrintSetter):
        setter.set(Version('0.1.0'))


class TestPyprojectSetter(object):
    @pytest.fixture()
    def setter(self):
        path = Path('tests/test_pyproject.toml')
        return pyproject_setter.PyprojectSetter(path)

    def test_init(self, setter: pyproject_setter.PyprojectSetter):
        assert setter

    def test_set(self, setter: pyproject_setter.PyprojectSetter):
        setter.set(Version('0.1.0'))
