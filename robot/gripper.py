# import socket
#
# from config import HOST
#
# DASHBOARD_PORT = 29999
#
# URP_DIR = "/programs/hanoi/"
# PROG_ACTIVATE = URP_DIR + "gripactive.urp"
# PROG_OPEN = URP_DIR + "gripopen.urp"
# PROG_CLOSE = URP_DIR + "gripclose.urp"
#
#
# def send_dashboard_command(command: str) -> str:
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((HOST, DASHBOARD_PORT))
#
#         # Read dashboard greeting
#         s.recv(1024)
#
#         s.sendall((command + "\n").encode("utf-8"))
#         response = s.recv(1024).decode("utf-8").strip()
#
#         return response
#
#
# def run_urp_program(program_path: str):
#     send_dashboard_command("stop")
#     load_response = send_dashboard_command(f"load {program_path}")
#     play_response = send_dashboard_command("play")
#
#     print(f"Loaded {program_path}: {load_response}")
#     print(f"Play response: {play_response}")
#
#
# def activate_gripper():
#     run_urp_program(PROG_ACTIVATE)
#
#
# def open_gripper():
#     run_urp_program(PROG_OPEN)
#
#
# def close_gripper():
#     run_urp_program(PROG_CLOSE)