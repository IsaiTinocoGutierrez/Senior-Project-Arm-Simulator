# Setup Guide

This guide explains how to set up and run the Robot Chess Arm Simulator project.

## 1. Requirements

Install the following:

- Python 3.10+
- Docker Desktop
- Git
- Stockfish
- Universal Robots URSim Docker container

## 2. Clone the Repository

```bash
git clone https://github.com/IsaiTinocoGutierrez/Senior-Project-Arm-Simulator.git
cd Senior-Project-Arm-Simulator

## 3. Install Python Dependencies

```bash
pip install -r requirements.txt
If requirements.txt only contains:

```bash
python-chess

you can also install manually:
```bash
pip install python-chess

## 4. Download Stockfish

Download Stockfish from:

```bash
[pip install python-chess](https://stockfishchess.org/download/)

Extract it into the project folder.

Expected structure:

```bash
Senior-Project-Arm-Simulator/
└── stockfish/
    └── stockfish-windows-x86-64-avx2.exe

Then check that config.py points to the correct file:

```bash
STOCKFISH_PATH = r"stockfish/stockfish-windows-x86-64-avx2.exe"
