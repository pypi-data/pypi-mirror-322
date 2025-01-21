from pprint import pp

import pytest
from typer.testing import CliRunner

from uv_version.cli import cli


class TestCli(object):
    @pytest.fixture()
    def runner(self):
        return CliRunner()

    def test_root(self, runner: CliRunner):
        result = runner.invoke(cli)
        assert result.exit_code == 0

    def test_version(self, runner: CliRunner):
        result = runner.invoke(cli, ['--version'])
        pp(result.output)
        assert result.exit_code == 0

    def test_args(self, runner: CliRunner):
        result = runner.invoke(cli, ['--to-print', '--from-pyproject', '--from-git', '--from-env'])
        pp(result.output)
        assert result.exit_code == 0

    def test_increment(self, runner: CliRunner):
        result = runner.invoke(cli, ['--to-print', 'increment', 'major'])
        pp(result.output)
        pp(result.exception)
        assert result.exit_code == 0
