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

    # Start at safe position
    send_urscript(host, port,
                  "movej([0, -1.2, 1.8, -1.0, -1.57, 0], a=1.0, v=0.1)")
    time.sleep(2)

    # Define square corners
    A = "movel(p[0.25, -0.25, 0.35, 0, 3.14, 0], a=0.3, v=0.1)"
    B = "movel(p[0.35, -0.25, 0.35, 0, 3.14, 0], a=0.3, v=0.1)"
    C = "movel(p[0.35, -0.35, 0.35, 0, 3.14, 0], a=0.3, v=0.1)"
    D = "movel(p[0.25, -0.35, 0.35, 0, 3.14, 0], a=0.3, v=0.1)"

    # Move to starting corner A
    send_urscript(host, port, A)
    time.sleep(2)

    # Trace square path
    send_urscript(host, port, B)
    time.sleep(2)

    send_urscript(host, port, C)
    time.sleep(2)

    send_urscript(host, port, D)
    time.sleep(2)

    # Back to start A
    send_urscript(host, port, A)
    time.sleep(2)

    print("Square motion complete!")

if __name__ == "__main__":
    main()
