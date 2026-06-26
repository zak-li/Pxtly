#!/usr/bin/env python3

import sys


def rgb(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"

def lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)

def lc(c0: tuple, c1: tuple, t: float) -> tuple:
    return (lerp(c0[0],c1[0],t), lerp(c0[1],c1[1],t), lerp(c0[2],c1[2],t))

RESET = "\033[0m"

C = 12

def make_body(ca: tuple, cb: tuple, mode: str = "diag"):
    def body(r: int, c: int, rows: int, cols: int) -> str:
        if mode == "vert":
            t = r / (rows - 1)
        elif mode == "horiz":
            t = c / (cols - 1)
        elif mode == "diag":
            t = r / (rows - 1) * 0.55 + c / (cols - 1) * 0.45
        elif mode == "rdiag":
            t = r / (rows - 1) * 0.55 + (1 - c / (cols - 1)) * 0.45
        return rgb(*lc(ca, cb, min(1.0, t))) + "██"
    return body

def render_shape(sh: dict) -> None:
    grid    = sh["grid"]
    rows    = len(grid)
    ec      = sh["ec"]
    er      = sh["er"]
    offset_x = sh.get("eye_offset_x", 0)
    el_pos  = (er, ec + offset_x)
    er_pos  = (er, C - 1 - ec + offset_x)
    body    = make_body(sh["ca"], sh["cb"], sh.get("mode", "diag"))

    print()
    for r in range(rows):
        seg = "  "
        for c in range(C):
            if (r, c) == el_pos or (r, c) == er_pos:
                seg += rgb(*sh["eye_col"]) + "██"
            elif grid[r][c] == 1:
                seg += body(r, c, rows, C)
            elif "palette" in sh and grid[r][c] in sh["palette"]:
                seg += rgb(*sh["palette"][grid[r][c]]) + "██"
            else:
                seg += "  "
        print(seg + RESET)

SHAPES = [
    # 1. Haut-de-forme (Top Hat Élegant)
    dict(
        grid=[
            # Haut de forme limité au corps
            [0,0,2,2,2,2,2,2,2,2,0,0],
            [0,0,2,2,2,2,2,2,2,2,0,0],
            [0,0,2,2,2,2,2,2,2,2,0,0],
            [0,0,2,2,2,2,2,2,2,2,0,0],
            [0,0,3,3,3,3,3,3,3,3,0,0], # Ruban rouge
            [2,2,2,2,2,2,2,2,2,2,2,2], # Bord du chapeau (prolongé à gauche et à droite)
            # Corps
            [0,1,1,1,1,1,1,1,1,1,1,0], # Ligne sous le chapeau
            [0,1,1,1,1,1,1,1,1,1,1,0], # Ligne des yeux
            [1,1,1,1,1,1,1,1,1,1,1,1], # Mains
            [0,1,1,1,1,1,1,1,1,1,1,0],
            [0,0,1,0,0,0,0,0,0,1,0,0],
        ],
        ec=3, er=7, eye_offset_x=1,
        ca=(123, 243, 252), cb=(0, 73, 255), eye_col=(0,0,0), mode="diag",
        palette={2: (30, 30, 30), 3: (220, 20, 60)} # Noir profond et Ruban Cramoisi
    ),
]

def animate():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    render_shape(SHAPES[0])

if __name__ == "__main__":
    animate()