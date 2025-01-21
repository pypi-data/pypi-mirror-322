import threading
from _typeshed import Incomplete
from datetime import datetime
from tlc.core.objects.tables.system_tables.indexing import _BlacklistExceptionHandler, _ScanUrl, _UrlIndex
from tlc.core.objects.tables.system_tables.project_scan_iterator import _ProjectScanIterator
from tlc.core.url import Url as Url
from tlc.core.url_adapter_registry import UrlAdapterRegistry as UrlAdapterRegistry
from typing import Generator

logger: Incomplete

class _ProjectConfigScanIterator(_ProjectScanIterator):
    """A scan iterator that yields all Config from a 3LC directory layout.

    Config files are stored in a fixed folder structure:
        - Pattern: <projects_dir>/<project_name>/config.3lc.yaml
        - Glob: <projects_dir>/*/config.3lc.yaml
    """
    def __init__(self, scan_urls: list[_ScanUrl], tag: str, blacklist_config: list[_BlacklistExceptionHandler] | None, stop_event: threading.Event | None = None) -> None: ...
    def add_scan_url(self, scan_url: _ScanUrl) -> None:
        """Try to add a scan_url to the iterator.

        If that doesn't work, raise a ValueError."""
    def scan(self) -> Generator[_UrlIndex, None, None]: ...
    def scan_project_url(self, project_url: Url, _: int) -> Generator[tuple[Url, datetime], None, None]: ...
    def bid(self, config: _ScanUrl) -> int: ...
