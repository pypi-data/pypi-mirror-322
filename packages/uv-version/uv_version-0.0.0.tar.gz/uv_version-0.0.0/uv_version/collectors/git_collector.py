
import logging
from typing import Any, Optional
from uv_version.enums import ReleaseTypeEnum
from packaging_version_git import GitVersion

from uv_version.collectors.base import BaseCollector

logger = logging.getLogger('uv-version')


class GitCollector(BaseCollector):
    def __init__(self, release_type: ReleaseTypeEnum = ReleaseTypeEnum.dev) -> None:
        super().__init__()

        self.release_type = release_type

    def collect(self) -> Optional[str]:
        if self.release_type == ReleaseTypeEnum.base:
            return str(GitVersion.from_tag())

        if self.release_type == ReleaseTypeEnum.alpha:
            return str(GitVersion.from_commit(as_alpha=True))

        if self.release_type == ReleaseTypeEnum.beta:
            return str(GitVersion.from_commit(as_beta=True))

        if self.release_type == ReleaseTypeEnum.rc:
            return str(GitVersion.from_commit(as_rc=True))

        if self.release_type == ReleaseTypeEnum.post:
            return str(GitVersion.from_commit(as_post=True))

        if self.release_type == ReleaseTypeEnum.dev:
            return str(GitVersion.from_commit(as_dev=True))

        return str(GitVersion.from_tag())

    def data(self) -> Optional[dict[str, Any]]:
        return {}
