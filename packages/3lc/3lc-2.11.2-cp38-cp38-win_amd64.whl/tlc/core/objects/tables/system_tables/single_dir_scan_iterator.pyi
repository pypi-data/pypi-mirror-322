import threading
from _typeshed import Incomplete
from tlc.core.objects.tables.system_tables.indexing import _BlacklistExceptionHandler, _ScanIterator, _ScanUrl, _UrlIndex
from tlc.core.url import Url as Url
from tlc.core.url_adapter import UrlAdapterDirEntry as UrlAdapterDirEntry
from tlc.core.url_adapter_registry import UrlAdapterRegistry as UrlAdapterRegistry
from typing import Generator, Sequence

logger: Incomplete

class _SingleDirScanIterator(_ScanIterator):
    """Private class for indexing Urls in a single directory.

    :param scan_urls: The URLs of the directories to iterate over.
    """
    def __init__(self, scan_urls: Sequence[_ScanUrl], extensions: Sequence[str], tag: str, blacklist_config: Sequence[_BlacklistExceptionHandler] | None, stop_event: threading.Event | None) -> None: ...
    @staticmethod
    def single_dir_readme() -> str: ...
    is_first_scan: bool
    def scan(self) -> Generator[_UrlIndex, None, None]: ...
    def scan_url(self, dir_url: Url) -> Generator[_UrlIndex, None, None]: ...
    def scan_package_url(self, dir_url: Url) -> Generator[_UrlIndex, None, None]: ...
    def bid(self, scan_url: _ScanUrl) -> int: ...
