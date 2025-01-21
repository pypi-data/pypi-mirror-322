import logging
from pprint import pp
from typing import Optional

from packaging.version import InvalidVersion, Version
from packaging_version_increment import IncrementVersion, increment_version
from packaging_version_increment.enums import IncrementEnum

from uv_version.collectors.base import BaseCollector
from uv_version.enums import ReleaseTypeEnum
from uv_version.setters.base import BaseSetter

logger = logging.getLogger('uv-version')


class UvVersionManager(object):
    setters: list[BaseSetter]
    collectors: list[BaseCollector]
    versions: list[Version]

    def __init__(self) -> None:
        self.setters = []
        self.collectors = []
        self.versions = []

        self.use_local = False

    def set_option(self, release_type: ReleaseTypeEnum, use_local: bool = False):
        self.release_type = release_type
        self.use_local = use_local

    def add_setter(self, setter: BaseSetter):
        assert isinstance(setter, BaseSetter)

        self.setters.append(setter)

    def add_collector(self, collector: BaseCollector):
        assert isinstance(collector, BaseCollector)

        self.collectors.append(collector)

    def collect(self):
        for collector in self.collectors:
            raw_version = collector.collect()

            if raw_version is None:
                continue

            try:
                version = Version(raw_version)

            except InvalidVersion as ex:
                logger.exception(ex)
                continue

            self.versions.append(version)

    def get_current_version(self) -> Optional[Version]:
        if self.versions:
            return max(self.versions)

        return None

    def increment(self, increment_part: IncrementEnum):
        current_version = self.get_current_version()

        if current_version is None:
            return None

        pp([current_version, increment_part])
        
        new_version = IncrementVersion(str(current_version))
        new_version.increment(increment_part)

        pp([new_version])

        self.versions = [new_version]

    def set(self):
        current_version = self.get_current_version()

        if current_version is None:
            return None

        if not self.use_local:
            # Deleing local
            current_version = IncrementVersion(str(current_version)).update(**{
                self.release_type: 0
            })

        pp([self.versions, current_version])
        for setter in self.setters:
            setter.set(current_version)
