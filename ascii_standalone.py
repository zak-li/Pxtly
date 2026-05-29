#!/usr/bin/env python3
"""Pixel-Bird ASCII Art Coloré — autonome, stdlib uniquement."""
import base64, zlib, math, sys

ENCODED = "eNr7/38UjIJRMApGwSgYDuDA9h1zpsygHAHNGRL+ndjVz8TATzma2NU3VPzLzChAORrM/kWOF0/PkLefPlOOvLxCkI0d9S9NQU1ZjYaqIVakqWbUXd0MR/nJuXq6VmSg1PiM9QuWb1+xDoIsje2R/Ytso7dbwNK5C2jq38yUbFwFCzCvrZ4+D44qsorJK6DcbD0X9E2Fm2OqZ41LpY6m6ewpM+jpX19nv6SweDjydvSDIzNUd9o5+KTnlMIRL48UXIqHUwLZkEjfCB9nf7g5kiJKg8e/7eUN8IhYNW0unljLKaresu8wHImKKsOlRATlkRNGelQKL6cEMSlhuPoXuXoaWP8Sj/D4Fz9aumIdcnHNyiw06l+6+TfdXqExQJUYtLou4MTcXDiaNnlK/6QZxCCgpYPHvyuytK+2GZOBXj27R17zg87+7W3r9nILgKPaYP3uMDUoCle/u6acSPT61VMiPXj/6fObDx7BUVh4YmhoPATFx2VUl9W0N7RC0Ooly2jd3NLVMoOHNguTIFUakGgIaAtyxn/z8ROylJ2tJ9wBGclZo/6lbv7tmzYX2TFU8eC1uw+Q/Xjn0RMiNZZXNqIU7NRoWo/6d9S/I8e/z16/haMXb99Txb/X7z5ANpZ4//Z39GxZvRaK1qyjhX+REVq7iGz/oiHk8hm/f5ERsJUy6l/q+nfr/iPkWbHtwBFcZkKCERfYuOvA6i274EhV1Yie/h1wpK5uQrl/N6xYPbGrH468vEItLF2xotjEbFr4wtLaHZeNaKi+qgHuzkndE6jenkRDQBtp4V9gq5XYjjMNhi71tM1wzQsA/bt57yE42rIPBSFL4UdoGtH8y8zIj8sBtB6qxT9/1BCgitz/leQXJjKapsZqIGtkYaLr+NWofyn3r4SYMrLG2rIafqTR6VH/Dk7/rl++MjUhA46WdRZfWloNR4UZWXCpwuwiZI1L5i7ISc+Dy26cUIqsMT0RYWZNaQ3ZDeNRMApGwSgYogAADiOoag=="
WIDTH = 80
HEIGHT = 46
BG = (207, 198, 198)
THRESHOLD = 25
BLOCK = "█"

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        
    raw = zlib.decompress(base64.b64decode(ENCODED))
    pixels = [raw[i:i+3] for i in range(0, len(raw), 3)]
    for y in range(HEIGHT):
        line = []
        for x in range(WIDTH):
            r, g, b = pixels[y * WIDTH + x]
            if (r, g, b) == (255, 255, 255):
                line.append(" ")
                continue
            dist = math.sqrt((r - BG[0])**2 + (g - BG[1])**2 + (b - BG[2])**2)
            if dist < THRESHOLD:
                line.append(" ")
            else:
                line.append("\033[38;2;{};{};{}m{}\033[0m".format(r, g, b, BLOCK))
        print("".join(line))

if __name__ == "__main__":
    main()
