import os
import sys
from typing import Any, Optional

from uv_version.collectors.base import BaseCollector


class StdinCollector(BaseCollector):
    def collect(self):  # pragma: no cover
        if os.isatty(sys.stdin.fileno()):
            return None

        return sys.stdin.read()

    def data(self) -> Optional[dict[str, Any]]:
        return {}
