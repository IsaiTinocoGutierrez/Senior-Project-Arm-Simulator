import time

from config import HOST, PORT
from robot.connection import send_urscript
from robot.manual_jog import jog_x_positive, jog_x_negative, stop_motion

SAFE_POSE = "movej([0, -1.2, 1.8, -1.0, -1.57, 0], a=0.5, v=0.15)"

print("Moving to safe pose...")
send_urscript(HOST, PORT, SAFE_POSE)
time.sleep(3)

print("Jogging X positive...")
jog_x_positive(HOST, PORT)
time.sleep(1)

print("Stopping...")
stop_motion(HOST, PORT)
time.sleep(1)

print("Jogging X negative...")
jog_x_negative(HOST, PORT)
time.sleep(1)

print("Stopping...")
stop_motion(HOST, PORT)