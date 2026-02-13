import socket
import time

def send_urscript(host: str, port: int, command: str):
    """
    Send a URScript command to a Universal Robots e-Series robot or simulator.

    Args:
        host: IP address or hostname of the robot (e.g., '127.0.0.1')
        port: UR primary interface port (default 30002)
        command: String containing valid URScript command(s)
    """
    try:
        # open a TCP connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            # ensure newline termination
            if not command.endswith("\n"):
                command += "\n"
            s.sendall(command.encode('utf-8'))
            print(f">> Sent: {command.strip()}")
            time.sleep(0.2)  # small delay for controller to process
    except Exception as e:
        print(f"[ERROR] {e}")

def main():
    host = "127.0.0.1"
    port = 30002

    # Start safely
    send_urscript(host, port, 
        "movej([0, -1.2, 1.8, -1.0, -1.57, 0], a=1.0, v=0.1)")
    time.sleep(2)

    # ---- Move above A2 ----
    send_urscript(host, port,
        "movel(p[0.20, -0.25, 0.15, 0, 3.14, 0], a=0.3, v=0.1)")
    time.sleep(2)

    # ---- Lower to piece at A2 ----
    send_urscript(host, port,
        "movel(p[0.20, -0.25, 0.05, 0, 3.14, 0], a=0.3, v=0.1)")
    time.sleep(2)

    # * Here robot would close the gripper (future) *

    # ---- Lift up from A2 ----
    send_urscript(host, port,
        "movel(p[0.20, -0.25, 0.15, 0, 3.14, 0], a=0.3, v=0.1)")
    time.sleep(2)

    # ---- Move above A4 ----
    send_urscript(host, port,
        "movel(p[0.20, -0.15, 0.15, 0, 3.14, 0], a=0.3, v=0.1)")
    time.sleep(2)

    # ---- Lower to place on A4 ----
    send_urscript(host, port,
        "movel(p[0.20, -0.15, 0.05, 0, 3.14, 0], a=0.3, v=0.1)")
    time.sleep(2)

    # * Here robot would release gripper (future) *

    # ---- Return to neutral pose ----
    send_urscript(host, port,
        "movel(p[0.25, -0.30, 0.25, 0, 3.14, 0], a=0.3, v=0.1)")
    time.sleep(2)

    print("Chess move A2 → A4 complete")
