from pathlib import Path

import pytest

from uv_version.collectors import env_collector, git_collector, pyproject_collector, stdin_collector


class TestEnvCollector(object):
    @pytest.fixture()
    def collector(self):
        return env_collector.EnvCollector()

    def test_init(self, collector: env_collector.EnvCollector):
        assert collector

    def test_collect(self, collector: env_collector.EnvCollector):
        collector.collect()

    def test_data(self, collector: env_collector.EnvCollector):
        collector.data()


class TestStdinCollector(object):
    @pytest.fixture()
    def collector(self):
        return stdin_collector.StdinCollector()

    def test_init(self, collector: stdin_collector.StdinCollector):
        assert collector

    def test_collect(self, collector: stdin_collector.StdinCollector):
        collector.collect()

    def test_data(self, collector: stdin_collector.StdinCollector):
        collector.data()


class TestPyprojectCollector(object):
    @pytest.fixture()
    def collector(self):
        path = Path('tests/test_pyproject.toml')
        return pyproject_collector.PyprojectCollector(path)

    def test_init(self, collector: pyproject_collector.PyprojectCollector):
        assert collector

    def test_collect(self, collector: pyproject_collector.PyprojectCollector):
        collector.collect()

    def test_data(self, collector: pyproject_collector.PyprojectCollector):
        collector.data()


class TestGitCollector(object):
    @pytest.fixture()
    def collector(self):
        return git_collector.GitCollector()

    def test_init(self, collector: git_collector.GitCollector):
        assert collector

    def test_collect(self, collector: git_collector.GitCollector):
        collector.collect()

    def test_data(self, collector: git_collector.GitCollector):
        collector.data()
