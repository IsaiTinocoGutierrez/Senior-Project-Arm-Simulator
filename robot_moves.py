from config import MOVEJ_A, MOVEJ_V, MOVEL_A, MOVEL_V
from robot_comm import send_urscript


def movej_cmd(pose_str: str, a: float = MOVEJ_A, v: float = MOVEJ_V) -> str:
    return f"movej({pose_str}, a={a}, v={v})"


def movel_cmd(pose_str: str, a: float = MOVEL_A, v: float = MOVEL_V) -> str:
    return f"movel({pose_str}, a={a}, v={v})"


def pick_and_place_one_program(host, port, above, touch, src, dst):
    script = f"""
def chess_pick_place():
  movej({above[src]}, a={MOVEJ_A}, v={MOVEJ_V})
  movel({touch[src]}, a={MOVEL_A}, v={MOVEL_V})
  movel({above[src]}, a={MOVEL_A}, v={MOVEL_V})

  movej({above[dst]}, a={MOVEJ_A}, v={MOVEJ_V})
  movel({touch[dst]}, a={MOVEL_A}, v={MOVEL_V})
  movel({above[dst]}, a={MOVEL_A}, v={MOVEL_V})
end
chess_pick_place()
"""
    send_urscript(host, port, script)