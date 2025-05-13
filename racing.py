import socket
import ssl
import threading
import subprocess
from time import sleep
from h2spacex import H2OnTlsConnection


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
            port = 443
            hostname = get_host(reqs[thread_id])

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

def prepare_frames(h2_conn, raw_req: str, stream_id: int):
    head, _, body = raw_req.partition("\r\n\r\n")
    lines = head.split("\r\n")
    method, path, _ = lines[0].split(" ", 2)
    headers_string = "\r\n".join(lines[1:])

    if method.upper() == "GET" or not body:
        return h2_conn.create_single_packet_http2_get_request_frames(
            method=method,
            headers_string=headers_string,
            scheme="https",
            stream_id=stream_id,
            authority=h2_conn.hostname,
            path=path
        )
    else:
        return h2_conn.create_single_packet_http2_post_request_frames(
            method=method,
            headers_string=headers_string,
            scheme="https",
            stream_id=stream_id,
            authority=h2_conn.hostname,
            body=body,
            path=path
        )


def race_requests_http2(reqs: list[str]) -> list[str]:
    """
    Send each http request in reqs such that they arrive at the exact same time
    at the server.

    This function works for http/2 only.

    Example invocation:
    >>> reqs = ["HTTP/1.1 GET /\r\nHost: example.com\r\n\r\n"] * 10
    >>> resps = race_requests_http11(reqs)
    """
    """
    Send HTTP/2 requests “in parallel,” print each block, and return
    a list of those formatted blocks as strings.
    """
    if not reqs:
        return []

    hostname = get_host(reqs[0])
    conn = H2OnTlsConnection(hostname=hostname, port_number=443)
    conn.setup_connection()
    conn.send_ping_frame()

    # prepare frames
    stream_ids = conn.generate_stream_ids(len(reqs))
    hdrs, datas = [], []
    for raw, sid in zip(reqs, stream_ids):
        h, last = prepare_frames(conn, raw, sid)
        hdrs.append(bytes(h))
        datas.append(bytes(last))

    # race them
    conn.send_frames(b"".join(hdrs))
    sleep(0.05)
    conn.send_ping_frame()
    conn.send_frames(b"".join(datas))

    conn.start_thread_response_parsing(_timeout=5)
    while not conn.is_threaded_response_finished:
        sleep(0.01)

    # get raw items
    items = list(conn.threaded_frame_parser.headers_and_data_frames.items())

    output_blocks: list[str] = []
    for sid, info in sorted(items, key=lambda x: x[0]):
        header_blob: str = info.get('header', '')
        data_blob: bytes = info.get('data', b'')
        ts: int = info.get('nano_seconds', 0)

        # build block exactly like your printout
        block_lines = [
            f"--- Stream {sid} ---",
            f"  RTT (ns): {ts}",
            f"  Response headers:",
        ]
        # indent each header line
        for line in header_blob.splitlines():
            block_lines.append(f"   {line}")

        if data_blob:
            body_str = data_blob.decode(errors='replace')
            block_lines.append(f"  Body ({len(data_blob)} bytes):")
            # no extra indent for body so it prints raw
            block_lines.extend(body_str.splitlines())
        else:
            block_lines.append("  (no body)")

        # join into one string
        block = "\n".join(block_lines)
        print(block + "\n")     # still print to terminal
        output_blocks.append(block)

    return output_blocks


def get_host(req: str) -> str:
    """
    Get host from the host field of an http request.
    """
    for line in req.splitlines():
        if line.lower().startswith("host:"):
            # Extract everything after "Host:"
            host = line.split(":", 1)[1].strip()
            # If the host has a port (e.g., example.com:8080), remove it
            return host.split(":")[0]
    raise ValueError("Missing Host header in request")


def get_http_version(url: str) -> str:
    """
    Get HTTP/HTTPS version of a website.
    """
    
    command = ["curl", "--http2", "-sI", url, "-o", "/dev/null", "-w", "'%{http_version}\n'"]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = result.stdout

    if result.returncode == 0:
        return output[1:-2]
    else:
        raise Exception("Return code was " + str(result.returncode))


# Example usage of http2 racing
# if __name__ == "__main__":
#     raw = (
#         "POST /du HTTP/1.1\r\n"
#         "Host: maxverstappen.acmcyber.com\r\n"
#         "User-Agent: Mozilla/5.0\r\n"
#         "Accept: */*\r\n"
#         "Content-Type: application/json\r\n"
#         "Origin: https://maxverstappen.acmcyber.com\r\n"
#         "Referer: https://maxverstappen.acmcyber.com/\r\n"
#         "Cookie: userid=user-c0655be4\r\n"
#         "\r\n"
#     )
#     reqs = [raw] * 15

#     blocks = race_requests_http2(reqs)
#     print(f"Total DU requests raced: {len(blocks)}")
