import threading
from _typeshed import Incomplete
from tlc.core.objects.tables.system_tables.indexing import _BlacklistExceptionHandler, _ScanIterator, _ScanUrl, _UrlIndex
from tlc.core.url_adapter import UrlAdapterDirEntry as UrlAdapterDirEntry
from tlc.core.url_adapter_registry import UrlAdapterRegistry as UrlAdapterRegistry
from typing import Generator, Sequence

logger: Incomplete

class _FileScanIterator(_ScanIterator):
    """An iterator that scans a single file like object."""
    def __init__(self, scan_urls: Sequence[_ScanUrl], tag: str, blacklist_config: Sequence[_BlacklistExceptionHandler] | None, stop_event: threading.Event | None) -> None: ...
    def scan(self) -> Generator[_UrlIndex, None, None]: ...
    def add_scan_url(self, scan_url: _ScanUrl) -> None:
        """Add a scan url to the iterator."""
    def bid(self, config: _ScanUrl) -> int: ...
