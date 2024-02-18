"""Block blocking calls being done in asyncio."""
from http.client import HTTPConnection
import time

from httpx import Client

from .util.async_ import protect_loop


def enable() -> None:
    """Enable the detection of blocking calls in the event loop."""
    # Prevent urllib3 and requests doing I/O in event loop
    HTTPConnection.putrequest = protect_loop(  # type: ignore[method-assign]
        HTTPConnection.putrequest
    )

    # Prevent httpx doing I/O in event loop
    Client.request = protect_loop(Client.request)  # type: ignore[method-assign]

    # Prevent sleeping in event loop. Non-strict since 2022.02
    time.sleep = protect_loop(time.sleep, strict=False)

    # Currently disabled. pytz doing I/O when getting timezone.
    # Prevent files being opened inside the event loop
    # builtins.open = protect_loop(builtins.open)
