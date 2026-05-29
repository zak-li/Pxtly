#!/usr/bin/env python3
"""
Standalone Premium Bird ASCII Animation for Pex
Includes game-loop design, double buffering, and keyboard interrupt safety.
"""

import sys
import time
import math
import os

# ── ANSI Helpers ───────────────────────────────────────────────
RESET = "\033[0m"
BOLD = "\033[1m"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
CLEAR_SCREEN = "\033[2J"
HOME_CURSOR = "\033[H"

def rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

# ── Color Palette ──────────────────────────────────────────────
PALETTE = {
    '.': None,                     # Transparent / Background
    'k': (15, 23, 42),             # Ultra-Dark Outline (Slate 900)
    'B': (30, 58, 138),            # Deep Blue Shadow
    'b': (37, 99, 235),            # Royal Blue Body
    'c': (123, 243, 252),          # Neon Cyan Highlight
    'w': (255, 255, 255),          # Pure White (Belly & Sunglasses Shine)
    'g': (203, 213, 225),          # Slate Gray (Belly Shadow)
    'o': (249, 115, 22),           # Vibrant Orange (Beak & Feet Base)
    'y': (251, 191, 36),           # Golden Yellow (Beak Highlight)
    's': (15, 23, 42)              # Black Sunglasses Frame/Lenses
}

# ── Animation Frames (15 Cols × 14 Rows) ────────────────────────
BIRD_FRAME_A = [
    ".....kkkkk.....",
    "....kbbccbk....",
    "...kbbccccbk...",
    "...kbsssssbk...",
    "..kbsswssswbk..",
    "...kbboyobbk...",
    "..kbbwwwwwbbk..",
    "..kbwwwwwwwbk..",
    ".kbbwwwwwggbbk.",
    "kbbbwwwggggbbbk",
    "..kbbwggggbbk..",
    "...kbbbbbbbk...",
    "....kkkkkkk....",
    "....koo.ook...."
]

BIRD_FRAME_B = [
    ".....kkkkk.....",
    "....kbbccbk....",
    "...kbbccccbk...",
    "...kbsssssbk...",
    "..kbsswssswbk..",
    "...kbboyobbk...",
    "..kbbwwwwwbbk..",
    ".kbbwwwwwwwbbk.",  # Wings slightly raised
    "kbbbwwwwwggbbbk",
    ".kbbwwwggggbbk.",  # Flapping up
    "..kbbwggggbbk..",
    "...kbbbbbbbk...",
    "....kkkkkkk....",
    "....koo.ook...."
]

COLS = 15
ROWS = 14

def get_terminal_size():
    """Returns the width and height of the terminal."""
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except OSError:
        return 80, 24

def build_frame_buffer(frame, x_pad, y_pad):
    """
    Constructs the frame in memory (Double Buffering principle)
    to prevent terminal screen tearing and flickering.
    """
    buffer = []
    # Vertical padding
    for _ in range(y_pad):
        buffer.append("\n")
    
    for row in frame:
        line = " " * x_pad
        for char in row:
            col = PALETTE.get(char)
            if col:
                # Use double-width block characters for square pixel ratio
                line += rgb(*col) + "██"
            else:
                line += "  "
        buffer.append(line + RESET + "\n")
        
    return "".join(buffer)

def run_animation():
    """Loops the game-like bouncing and wing-flapping idle animation."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # Save screen state and hide cursor
    sys.stdout.write(HIDE_CURSOR + CLEAR_SCREEN + HOME_CURSOR)
    sys.stdout.flush()

    start_time = time.time()
    try:
        while True:
            t = time.time() - start_time
            term_w, term_h = get_terminal_size()

            # Physics-based hover math (smooth sine wave)
            # Oscillation amplitude: 1-2 lines depending on terminal height
            max_y_offset = min(4, max(1, term_h // 10))
            y_offset = int((math.sin(t * 5.0) + 1.0) * (max_y_offset / 2.0))

            # Select frame (flapping wings on the upward motion)
            moving_up = math.cos(t * 5.0) > 0
            frame = BIRD_FRAME_B if moving_up else BIRD_FRAME_A

            # Calculate dynamic horizontal centering (double-width blocks mean COLS * 2 width)
            x_pad = max(0, (term_w - (COLS * 2)) // 2)
            y_pad = max(0, (term_h - ROWS) // 2 - max_y_offset + y_offset)

            # Redraw directly from home position (Flicker-Free rendering)
            sys.stdout.write(HOME_CURSOR)
            
            # Print the double-buffered frame
            frame_content = build_frame_buffer(frame, x_pad, y_pad)
            sys.stdout.write(frame_content)
            
            # Flush buffer to screen
            sys.stdout.flush()

            # Target ~30 FPS
            time.sleep(0.033)

    except KeyboardInterrupt:
        # Graceful exit: restore cursor and clear screen
        sys.stdout.write(SHOW_CURSOR + CLEAR_SCREEN + HOME_CURSOR)
        sys.stdout.flush()
        print("Animation terminated. Have a great day!")

def print_static():
    """Prints a single static frame centered in the terminal."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        
    term_w, term_h = get_terminal_size()
    x_pad = max(0, (term_w - (COLS * 2)) // 2)
    y_pad = max(0, (term_h - ROWS) // 2)
    
    # Draw static frame A
    frame_content = build_frame_buffer(BIRD_FRAME_A, x_pad, y_pad)
    sys.stdout.write(frame_content + "\n")
    sys.stdout.flush()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--static":
        print_static()
    else:
        run_animation()
