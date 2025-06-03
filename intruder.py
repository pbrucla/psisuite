import time

def send_requests_http11(reqs: list[str]) -> list[str]:
    """
    Send requests as fast as possible using http/1.1

    Return all responses.

    Example invocation:
    >>> reqs = ["HTTP/1.1 GET /\r\nHost: example.com\r\n\r\n"] * 10
    >>> resps = send_requests_http11(reqs)
    """
    time.sleep(0.3 * len(reqs))
    return reqs


def send_requests_http2(reqs: list[str]) -> list[str]:
    """
    Send requests as fast as possible using http/2

    Return all responses.

    Example invocation:
    >>> reqs = ["HTTP/1.1 GET /\r\nHost: example.com\r\n\r\n"] * 10
    >>> resps = send_requests_http11(reqs)
    """
    return reqs


def find_interesting_responses(resps: list[str]) -> list[str]:
    return resps
