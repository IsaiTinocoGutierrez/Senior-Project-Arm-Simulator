import socket
import time

from config import SEND_DELAY


def send_urscript(host: str, port: int, command: str):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))

            if not command.endswith("\n"):
                command += "\n"

            s.sendall(command.encode("utf-8"))
            print(f">> Sent: {command.strip()}")
            time.sleep(SEND_DELAY)

    except Exception as e:
        print(f"[ERROR] {e}")