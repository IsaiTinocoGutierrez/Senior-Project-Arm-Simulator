# for real robot IP
#HOST = "192.168.0.205"
HOST = "127.0.0.1"
PORT = 30002

FILES = "ABCDEFGH"
RANKS = "12345678"

# Safe neutral pose
NEUTRAL_MOVEJ = "movej([0, -1.2, 1.8, -1.0, -1.57, 0], a=0.8, v=0.15)"

# Board placement
X_A1 = 0.52
Y_A1 = -0.20
SQUARE_SIZE = 0.057

# Heights
Z_ABOVE = 0.22
Z_TOUCH = 0.12

# Orientation
RX = 0.0
RY = 3.14
RZ = 0.0

# Motion tuning
MOVEJ_A = 0.6
MOVEJ_V = 0.3
MOVEL_A = 0.25
MOVEL_V = 0.08

# Timing
SEND_DELAY = 3
STARTUP_DELAY = 2.5
MOVE_DELAY = 2.5

# Stockfish
STOCKFISH_PATH = r"C:\Users\isait\OneDrive\Desktop\senior project\stockfish\stockfish-windows-x86-64-avx2.exe"
THINK_TIME = 0.2
