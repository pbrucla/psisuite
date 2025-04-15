from mitmproxy import http
from mitmproxy import tcp

def log(*args, **kwargs):
    with open("log.txt", "a+") as fout:
        print(*args, **kwargs, file=fout)

def tcp_message(flow: tcp.TCPFlow) -> None:
    log("TCP Flow")
    for msg in flow.messages:
        log(f"[{msg.from_client}] {msg.content}")
        log("=======")
