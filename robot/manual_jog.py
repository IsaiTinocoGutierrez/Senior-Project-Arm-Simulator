from robot.connection import send_urscript

# -----------------------------
# Manual jog tuning
# -----------------------------

# Cartesian TCP jog speed in meters/second.
# 0.05 = 50 mm/s
JOG_SPEED = 0.08

# Cartesian acceleration
JOG_ACCEL = 1.0

# How long each jog command runs
JOG_DURATION = 0.08

# Joint jog speed in radians/second
JOINT_SPEED = 0.3

# Joint acceleration
JOINT_ACCEL = 0.5

# Smooth stop deceleration
STOP_DECEL = 0.5


# -----------------------------
# Core jog helpers
# -----------------------------

def speedl_jog(host, port, x=0.0, y=0.0, z=0.0,
               rx=0.0, ry=0.0, rz=0.0,
               accel=JOG_ACCEL, duration=JOG_DURATION):
    """
    Jog the robot TCP using speedl.

    x, y, z are linear TCP speeds in meters/second.
    rx, ry, rz are rotational TCP speeds in rad/second.
    """
    cmd = (
        f"speedl([{x}, {y}, {z}, {rx}, {ry}, {rz}], "
        f"{accel}, {duration})"
    )
    send_urscript(host, port, cmd)


def speedj_jog(host, port, joints,
               accel=JOINT_ACCEL, duration=JOG_DURATION):
    """
    Jog robot joints using speedj.

    joints must be a list of 6 joint speeds in rad/second.
    Example:
        [0.3, 0, 0, 0, 0, 0]
    """
    if len(joints) != 6:
        raise ValueError("speedj_jog requires exactly 6 joint speed values.")

    cmd = f"speedj({joints}, {accel}, {duration})"
    send_urscript(host, port, cmd)


def stop_motion(host, port):
    """
    Smoothly stop robot TCP motion.
    """
    send_urscript(host, port, f"stopl({STOP_DECEL})")


def stop_joint_motion(host, port):
    """
    Smoothly stop robot joint motion.
    """
    send_urscript(host, port, f"stopj({STOP_DECEL})")


# -----------------------------
# Cartesian TCP jog buttons
# -----------------------------

def jog_x_positive(host, port):
    speedl_jog(host, port, x=JOG_SPEED)


def jog_x_negative(host, port):
    speedl_jog(host, port, x=-JOG_SPEED)


def jog_y_positive(host, port):
    speedl_jog(host, port, y=JOG_SPEED)


def jog_y_negative(host, port):
    speedl_jog(host, port, y=-JOG_SPEED)


def jog_z_positive(host, port):
    speedl_jog(host, port, z=JOG_SPEED)


def jog_z_negative(host, port):
    speedl_jog(host, port, z=-JOG_SPEED)


# -----------------------------
# TCP orientation jog helpers
# -----------------------------

def jog_rx_positive(host, port):
    speedl_jog(host, port, rx=JOINT_SPEED)


def jog_rx_negative(host, port):
    speedl_jog(host, port, rx=-JOINT_SPEED)


def jog_ry_positive(host, port):
    speedl_jog(host, port, ry=JOINT_SPEED)


def jog_ry_negative(host, port):
    speedl_jog(host, port, ry=-JOINT_SPEED)


def jog_rz_positive(host, port):
    speedl_jog(host, port, rz=JOINT_SPEED)


def jog_rz_negative(host, port):
    speedl_jog(host, port, rz=-JOINT_SPEED)


# -----------------------------
# Individual joint jog helpers
# Joint order:
# 0 = Base
# 1 = Shoulder
# 2 = Elbow
# 3 = Wrist 1
# 4 = Wrist 2
# 5 = Wrist 3
# -----------------------------

def jog_joint(host, port, joint_index, direction):
    """
    Jog a single joint.

    joint_index: 0 to 5
    direction: +1 or -1
    """
    if joint_index < 0 or joint_index > 5:
        raise ValueError("joint_index must be between 0 and 5.")

    speeds = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    speeds[joint_index] = direction * JOINT_SPEED

    speedj_jog(host, port, speeds)


def jog_base_positive(host, port):
    jog_joint(host, port, 0, +1)


def jog_base_negative(host, port):
    jog_joint(host, port, 0, -1)


def jog_shoulder_positive(host, port):
    jog_joint(host, port, 1, +1)


def jog_shoulder_negative(host, port):
    jog_joint(host, port, 1, -1)


def jog_elbow_positive(host, port):
    jog_joint(host, port, 2, +1)


def jog_elbow_negative(host, port):
    jog_joint(host, port, 2, -1)


def jog_wrist1_positive(host, port):
    jog_joint(host, port, 3, +1)


def jog_wrist1_negative(host, port):
    jog_joint(host, port, 3, -1)


def jog_wrist2_positive(host, port):
    jog_joint(host, port, 4, +1)


def jog_wrist2_negative(host, port):
    jog_joint(host, port, 4, -1)


def jog_wrist3_positive(host, port):
    jog_joint(host, port, 5, +1)


def jog_wrist3_negative(host, port):
    jog_joint(host, port, 5, -1)