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
    host = "127.0.0.1"   # or your simulator IP
    port = 30002         # UR primary interface port

    # Example 1: Joint move (movej)
    movej_cmd = "movej([0.0, -1.57, 0.0, -1.57, 0.0, 0.0], a=1.2, v=0.25)"

    # Example 2: Linear move (movel)
    movel_cmd = "movel(p[0.30, -0.10, 0.20, 0.0, 3.14, 0.0], a=0.5, v=0.1)"

    # Send commands
    send_urscript(host, port, movej_cmd)
    time.sleep(1)
    send_urscript(host, port, movel_cmd)

    print("Done.")

if __name__ == "__main__":
    main()
