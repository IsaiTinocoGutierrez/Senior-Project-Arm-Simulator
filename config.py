# for real robot IP
#HOST = "192.168.0.205"
HOST = "127.0.0.1"
PORT = 30002

FILES = "ABCDEFGH"
RANKS = "12345678"

# Safe neutral pose
NEUTRAL_MOVEJ =  "movej([1.080, -1.682, 1.906, -1.804, -1.584, -0.496], a=0.3, v=0.08)"

# Board placement
X_A1 = -0.089
Y_A1 = -0.500 #shifts the whole board closer or further from arm.
SQUARE_SIZE = 0.052

# Heights
Z_ABOVE = 0.30
Z_TOUCH = 0.25

# Orientation
RX = 0.008
RY = -3.126
RZ = 0.003

# Motion tuning
MOVEJ_A = 0.6
MOVEJ_V = 0.3
MOVEL_A = 0.25
MOVEL_V = 0.08

# Timing
SEND_DELAY = 2
STARTUP_DELAY = 1.0
MOVE_DELAY = 1.0

# Stockfish
STOCKFISH_PATH = r"C:\Users\isait\OneDrive\Desktop\senior project\stockfish\stockfish-windows-x86-64-avx2.exe"
THINK_TIME = 0.2
