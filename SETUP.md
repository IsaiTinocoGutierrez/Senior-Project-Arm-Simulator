# Robot Chess Arm Simulator - Setup Guide

This guide explains how to install, configure, and run the Robot Chess Arm Simulator project.

---

# 1. Project Overview

This project combines:

- Python
- Universal Robots URSim
- Stockfish Chess Engine
- Tkinter Chess UI
- Robot motion scripting through URScript

The simulator allows a robotic arm to:

- Play chess against a human
- Physically simulate piece movement
- Connect to Stockfish for AI chess moves
- Display moves through a graphical chess interface

---

# 2. Software Requirements

Install the following software before running the project.

## Required Software

### Python 3.10+

Download:

```text
https://www.python.org/downloads/
```

Verify installation:

```bash
python --version
```

---

### Git

Download:

```text
https://git-scm.com/downloads
```

Verify installation:

```bash
git --version
```

---

### Docker Desktop

Download:

```text
https://www.docker.com/products/docker-desktop/
```

Verify installation:

```bash
docker --version
```

---

### GitHub Desktop (Optional but Recommended)

Download:

```text
https://desktop.github.com/
```

Useful for easier GitHub syncing and authentication.

---

# 3. Clone the Repository

Open PowerShell or terminal:

```bash
git clone https://github.com/IsaiTinocoGutierrez/Senior-Project-Arm-Simulator.git
```

Move into the project folder:

```bash
cd Senior-Project-Arm-Simulator
```

---

# 4. Install Python Dependencies

Install required Python packages:

```bash
pip install -r requirements.txt
```

Current requirements:

```text
python-chess
```

You can also install manually:

```bash
pip install python-chess
```

Verify installation:

```bash
pip list
```

You should see:

```text
python-chess
chess
```

---

# 5. Download Stockfish

Download Stockfish:

```text
https://stockfishchess.org/download/
```

Recommended version:

```text
Windows x64 AVX2
```

Extract the downloaded ZIP.

Move the extracted folder into the project directory.

Expected structure:

```text
Senior-Project-Arm-Simulator/
│
├── stockfish/
│   └── stockfish-windows-x86-64-avx2.exe
```

---

# 6. Configure Stockfish Path

Open:

```text
config.py
```

Set the Stockfish executable path:

```python
STOCKFISH_PATH = r"stockfish/stockfish-windows-x86-64-avx2.exe"
```

If the executable has a different name, update the path accordingly.

---

# 7. Start the Universal Robots Simulator

## Start Docker Desktop First

Make sure Docker Desktop is running.

---

## Launch URSim

Open PowerShell and run:

```powershell
docker run --rm -it --platform linux/amd64 `
-e ROBOT_MODEL=UR3e `
-p 5900:5900 `
-p 30001:30001 `
-p 30002:30002 `
-p 30004:30004 `
-p 6081:6080 `
--name ur3e_container `
universalrobots/ursim_e-series
```

---

## Open URSim in Browser

Open:

```text
http://localhost:6081/vnc.html
```

Click:

```text
Connect
```

---

# 8. Enable the Robot

Inside URSim:

1. Click the red status indicator
2. Power On the robot
3. Release brakes
4. Ensure robot status becomes:

```text
Normal
```

The simulator must remain running while using the chess application.

---

# 9. Run the Chess Application

Open a terminal in the project folder:

```bash
python main.py
```

The chess UI window should appear.

---

# 10. How to Play

## Human Move

1. Click a white piece
2. Click the destination square

Example:

```text
Pawn from E2 to E4
```

The robot arm simulator will execute the move.

---

## AI Move

After the human move:

1. Stockfish calculates a response
2. The robot executes the AI move automatically

---

# 11. Chess UI Features

The UI currently supports:

- Chess board display
- Human vs AI gameplay
- Captured pieces tracking
- Move logger
- Reset Game button
- Scrollable move history

---

# 12. Resetting the Game

Click:

```text
Reset Game
```

This resets:

- Board state
- Captured pieces
- Move log
- Chess engine state
- Robot neutral pose

---

# 13. Project Structure

```text
Senior-Project-Arm-Simulator/
│
├── main.py
├── config.py
├── requirements.txt
├── README.md
├── SETUP.md
├── .gitignore
│
├── robot/
│   ├── connection.py
│   ├── mapping.py
│   ├── motion.py
│   └── poses.py
│
├── ui/
│   ├── chess_app.py
│   ├── board_view.py
│   ├── side_panel.py
│   └── game_controller.py
│
├── services/
│   ├── capture_logic.py
│   ├── game_state.py
│   └── move_logger.py
│
├── shared/
│   └── piece_constants.py
│
├── stockfish/
│
└── old_files/
```

---

# 14. Common Problems

## Robot Does Not Move

Check:

- Docker is running
- URSim is powered on
- Robot status is "Normal"
- Port 30002 is exposed
- `HOST = "127.0.0.1"` in config

---

## Protective Stop

Usually caused by:

- Coordinates too close to robot base
- Singularities
- Sudden stop between motions

Fixes:

- Increase board distance
- Raise safe Z height
- Use smoother motion paths

---

## Stockfish Not Found

Check:

- Stockfish folder exists
- Executable path is correct
- Filename matches config.py

---

# 15. GitHub Usage

Push updates:

```bash
git add .
git commit -m "Updated project"
git push origin main
```

---

# 16. Future Improvements

Planned features:

- Real robotic gripper
- Physical chessboard calibration
- Chess cameras / computer vision
- Multiplayer online support
- Move highlighting
- Better robot path planning
- Real UR3 hardware support

---

# 17. Credits

Libraries and tools used:

- python-chess
- Stockfish
- Universal Robots URSim
- Docker
- Tkinter

---

# 18. Author

Created by:

```text
Isai Tinoco Gutierrez
```
