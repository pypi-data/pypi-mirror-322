import os
from typing import Any, Optional

from uv_version import settings
from uv_version.collectors.base import BaseCollector


class EnvCollector(BaseCollector):
    def __init__(self) -> None:
        super().__init__()

    def collect(self) -> Optional[str]:
        return os.getenv(settings.UV_PACKAGE_VERSION_COLLECTOR_ENV_NAME, None)

    def data(self) -> Optional[dict[str, Any]]:
        return {}
