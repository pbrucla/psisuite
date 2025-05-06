import socket
import ssl
import threading


def race_requests_http11(reqs: list[str]) -> list[str]:
    """
    Send each http request in reqs such that they arrive at the exact same time
    at the server.

    This function works for http/1.1 only.

    Example invocation:
    >>> reqs = ["HTTP/1.1 GET /\r\nHost: example.com\r\n\r\n"] * 10
    >>> resps = race_requests_http11(reqs)
    """
    num_threads = len(reqs)
    barrier = threading.Barrier(num_threads)
    responses = [None] * num_threads

    def fetch(thread_id: int):
        try:
            hostname = ''
            port = 443

            # Extract hostname from Host header
            for line in reqs[thread_id].splitlines():
                if line.lower().startswith('host:'):
                    hostname = line.split(':', 1)[1].strip()
                    print(hostname)
                    break
            if not hostname:
                raise ValueError("Missing Host header in request")

            # Establish SSL connection
            context = ssl.create_default_context()
            sock = socket.create_connection((hostname, port))
            ssl_sock = context.wrap_socket(sock, server_hostname=hostname)

            # Split request into partial and final chunk
            request = reqs[thread_id]
            partial = request[:-4]
            final = request[-4:]

            ssl_sock.sendall(partial.encode())
            print(f"[Thread {thread_id}] Sent partial request, waiting at barrier...")

            barrier.wait()

            ssl_sock.sendall(final.encode())
            print(f"[Thread {thread_id}] Sent final chunk")

            # Read response
            response = b""
            while True:
                chunk = ssl_sock.recv(4096)
                if not chunk:
                    break
                response += chunk

            responses[thread_id] = response.decode(errors='ignore')
            ssl_sock.close()
        except Exception as e:
            responses[thread_id] = f"[Thread {thread_id}] Error: {e}"

    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=fetch, args=(i,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return responses


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
