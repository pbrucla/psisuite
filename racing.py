def race_requests_http11(reqs: list[str]) -> list[str]:
    """
    Send each http request in reqs such that they arrive at the exact same time
    at the server.

    This function works for http/1.1 only.

    Example invocation:
    >>> reqs = ["HTTP/1.1 GET /\r\nHost: example.com\r\n\r\n"] * 10
    >>> resps = race_requests_http11(reqs)
    """
    return reqs


def race_requests_http2(reqs: list[str]) -> list[str]:
    """
    Send each http request in reqs such that they arrive at the exact same time
    at the server.

    This function works for http/2 only.

    Example invocation:
    >>> reqs = ["HTTP/1.1 GET /\r\nHost: example.com\r\n\r\n"] * 10
    >>> resps = race_requests_http11(reqs)
    """
    return reqs


def get_host(req: str) -> str:
    """
    Get host from the host field of an http request.
    """
    ...
