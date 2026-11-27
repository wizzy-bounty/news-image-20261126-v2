#!/usr/bin/env python3
"""news-image-20261126 entry: one broadsheet image of Thursday world news.

Deterministic, standard library only, no network. Writes entry.png (1024x1024)
to $MAKEFUN_OUTPUT_DIR when set, otherwise to ./output.
"""

import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (247, 243, 234)
INK = (24, 24, 28)
MUTED = (96, 92, 82)
RULE = (60, 58, 52)
RED = (176, 34, 52)
BLUE = (30, 76, 120)
TEAL = (18, 110, 110)
GOLD = (184, 132, 26)
GREEN = (24, 118, 66)
AMBER = (168, 108, 16)
PURPLE = (128, 36, 96)
WHITE = (255, 255, 255)
SKY = (168, 200, 224)
NIGHT = (32, 44, 66)

BADGE_COLORS = {"CONFIRMED": GREEN, "REPORTED": AMBER, "CLAIM": PURPLE}

FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11100", "10010", "10001", "10001", "10001", "10010", "11100"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "01010", "00100", "00100", "00100", "01010", "10001"),
    "Y": ("10001", "01010", "00100", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "01010", "00000", "00000", "00000", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "+": ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "|": ("00100", "00100", "00100", "00100", "00100", "00100", "00100"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "=": ("00000", "00000", "01110", "00000", "01110", "00000", "00000"),
}


class Canvas:
    def __init__(self, width, height, color):
        self.w = width
        self.h = height
        self.px = bytearray(color * (width * height))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        row = bytes(color) * max(0, x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.px[i:i + len(row)] = row

    def frame(self, x, y, w, h, color, t=1):
        self.rect(x, y, w, t, color)
        self.rect(x, y + h - t, w, t, color)
        self.rect(x, y, t, h, color)
        self.rect(x + w - t, y, t, h, color)

    def line(self, x0, y0, x1, y1, color, t=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            for ox in range(t):
                for oy in range(t):
                    self.set(x + ox, y + oy, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def circle(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy) <= r * r:
                    self.set(xx, yy, color)

    def ring(self, cx, cy, r, color, t=2):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d = (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy)
                if (r - t) * (r - t) <= d <= r * r:
                    self.set(xx, yy, color)

    def ellipse(self, cx, cy, rx, ry, color):
        for yy in range(cy - ry, cy + ry + 1):
            for xx in range(cx - rx, cx + rx + 1):
                if ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1.0:
                    self.set(xx, yy, color)

    def tri(self, x0, y0, x1, y1, x2, y2, color):
        minx = max(0, min(x0, x1, x2))
        maxx = min(self.w - 1, max(x0, x1, x2))
        miny = max(0, min(y0, y1, y2))
        maxy = min(self.h - 1, max(y0, y1, y2))
        den = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if den == 0:
            return
        for yy in range(miny, maxy + 1):
            for xx in range(minx, maxx + 1):
                a = ((y1 - y2) * (xx - x2) + (x2 - x1) * (yy - y2)) / den
                b = ((y2 - y0) * (xx - x2) + (x0 - x2) * (yy - y2)) / den
                c = 1.0 - a - b
                if a >= 0 and b >= 0 and c >= 0:
                    self.set(xx, yy, color)

    def poly(self, points, color):
        if len(points) < 3:
            return
        for i in range(1, len(points) - 1):
            self.tri(points[0][0], points[0][1], points[i][0], points[i][1],
                     points[i + 1][0], points[i + 1][1], color)


def char_advance(scale):
    return 5 * scale + max(1, scale)


def text_width(text, scale):
    if not text:
        return 0
    return len(text) * char_advance(scale) - max(1, scale)


def draw_text(cv, x, y, text, scale, color, bold=False):
    text = text.upper()
    cx = x
    for ch in text:
        glyph = FONT.get(ch, FONT["?"])
        for gy, row in enumerate(glyph):
            for gx, bit in enumerate(row):
                if bit == "1":
                    cv.rect(cx + gx * scale, y + gy * scale, scale, scale, color)
                    if bold:
                        cv.rect(cx + gx * scale + 1, y + gy * scale, scale, scale, color)
        cx += char_advance(scale)
    return cx


def draw_center(cv, cx, y, text, scale, color, bold=False):
    draw_text(cv, cx - text_width(text, scale) // 2, y, text, scale, color, bold)


def wrap(text, max_chars):
    words = text.upper().split()
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(cv, x, y, text, max_chars, scale, color, max_lines, bold=False, leading=None):
    lines = wrap(text, max_chars)[:max_lines]
    step = leading or (7 * scale + 3)
    for i, line in enumerate(lines):
        draw_text(cv, x, y + i * step, line, scale, color, bold)
    return y + len(lines) * step


def badge(cv, x, y, label):
    color = BADGE_COLORS[label]
    w = text_width(label, 2) + 10
    cv.rect(x, y, w, 17, color)
    draw_text(cv, x + 5, y + 2, label, 2, WHITE, bold=True)
    return w


def number_chip(cv, x, y, number):
    label = str(number)
    w = text_width(label, 2) + 10
    cv.rect(x, y, w, 19, RED)
    draw_text(cv, x + 5, y + 3, label, 2, WHITE, bold=True)
    return w


def scene_storm(cv, x, y, w, h):
    cv.rect(x, y, w, h, (70, 92, 118))
    for i in range(0, w, 14):
        cv.line(x + i, y + 4, x + i - 8, y + h - 26, (170, 205, 235), 2)
    cv.rect(x, y + h - 24, w, 24, (52, 96, 128))
    for i in range(0, w, 26):
        cv.line(x + i, y + h - 16, x + i + 14, y + h - 16, (190, 220, 240), 2)
    px = x + w // 3
    cv.line(px, y + h - 22, px + 14, y + 22, (40, 34, 28), 4)
    cv.line(px + 14, y + 22, px + 34, y + 30, (40, 34, 28), 3)
    cv.line(px + 14, y + 22, px - 6, y + 34, (40, 34, 28), 3)
    cv.line(px + 34, y + 30, px + 52, y + h - 24, (240, 210, 90), 2)
    bx = x + (2 * w) // 3
    cv.ellipse(bx, y + 34, 30, 22, (214, 96, 60))
    cv.tri(bx - 8, y + 52, bx + 8, y + 52, bx, y + 66, (214, 96, 60))
    cv.rect(bx - 10, y + 66, 20, 8, (120, 84, 48))
    cv.line(bx - 10, y + 66, bx - 4, y + 56, INK, 1)
    cv.line(bx + 10, y + 66, bx + 4, y + 56, INK, 1)
    cv.rect(x + 8, y + h - 34, 44, 12, (30, 34, 40))
    cv.circle(x + 18, y + h - 21, 5, (16, 16, 18))
    cv.circle(x + 42, y + h - 21, 5, (16, 16, 18))


def scene_drone(cv, x, y, w, h):
    cv.rect(x, y, w, h, (196, 168, 120))
    cv.rect(x, y + h - 18, w, 18, (150, 122, 82))
    dx = x + w // 4
    cv.tri(dx - 26, y + h - 18, dx + 26, y + h - 18, dx, y + 34, (210, 214, 218))
    cv.line(dx, y + 34, dx, y + h - 18, (120, 126, 132), 3)
    cv.rect(dx - 4, y + h - 30, 8, 12, (90, 96, 102))
    cx = x + (3 * w) // 5
    cy = y + 30
    cv.rect(cx - 16, cy - 4, 32, 8, (38, 40, 46))
    for ox, oy in ((-24, -10), (24, -10), (-24, 10), (24, 10)):
        cv.ring(cx + ox, cy + oy, 7, (38, 40, 46), 2)
        cv.line(cx, cy, cx + ox, cy + oy, (38, 40, 46), 2)
    ex = x + (4 * w) // 5
    ey = y + h - 34
    for ang in range(0, 360, 30):
        import math
        cv.line(ex, ey, ex + int(22 * math.cos(math.radians(ang))),
                ey + int(16 * math.sin(math.radians(ang))), (232, 120, 40), 3)
    cv.circle(ex, ey, 9, (250, 196, 64))
    cv.circle(ex, ey, 5, (255, 240, 180))
    cv.line(cx + 10, cy + 6, ex - 8, ey - 10, (120, 120, 120), 1)


def scene_summit(cv, x, y, w, h):
    cv.rect(x, y, w, h, (214, 224, 234))
    cv.rect(x + 10, y + 8, w - 20, 34, (120, 140, 160))
    for i in range(6):
        cv.rect(x + 18 + i * ((w - 36) // 6), y + 14, 14, 22, (226, 236, 246))
    ty = y + h - 26
    cv.rect(x + 16, ty, w - 32, 10, (96, 70, 44))
    cv.rect(x + 22, ty + 10, 8, 10, (76, 54, 34))
    cv.rect(x + w - 30, ty + 10, 8, 10, (76, 54, 34))
    flags = [(30, 76, 160), (240, 200, 60), (176, 34, 52), (24, 118, 66), (240, 240, 240)]
    for i, col in enumerate(flags):
        fx = x + 26 + i * ((w - 52) // 5)
        cv.line(fx, ty, fx, ty - 24, INK, 2)
        cv.rect(fx + 1, ty - 24, 16, 10, col)
    cv.circle(x + w // 2, ty - 8, 11, GOLD)
    draw_center(cv, x + w // 2, ty - 14, "E", 2, WHITE, bold=True)


def scene_blocks(cv, x, y, w, h):
    cv.rect(x, y, w, h, (196, 190, 178))
    for i, bh in enumerate((34, 46, 28)):
        bx = x + 8 + i * ((w - 16) // 3)
        bw = (w - 24) // 3
        cv.rect(bx, y + h - bh, bw, bh, (150, 142, 128))
        for wy in range(y + h - bh + 5, y + h - 6, 10):
            for wx in range(bx + 5, bx + bw - 6, 10):
                cv.rect(wx, wy, 5, 6, (226, 220, 200))
    cv.circle(x + w - 18, y + 14, 9, (120, 118, 112))
    cv.circle(x + w - 30, y + 10, 7, (140, 138, 130))
    cv.line(x + 6, y + 8, x + w - 22, y + 16, (90, 90, 90), 2)


def scene_tankerfire(cv, x, y, w, h):
    cv.rect(x, y, w, h, (56, 52, 60))
    cv.rect(x, y + h - 12, w, 12, (36, 34, 38))
    tx = x + w // 3
    cv.rect(tx - 30, y + h - 30, 60, 14, (210, 210, 214))
    cv.rect(tx + 30, y + h - 26, 16, 10, (160, 160, 166))
    cv.circle(tx - 18, y + h - 14, 5, (14, 14, 16))
    cv.circle(tx + 20, y + h - 14, 5, (14, 14, 16))
    cv.circle(tx + 38, y + h - 14, 5, (14, 14, 16))
    for i, fh in enumerate((18, 24, 16)):
        fx = tx - 22 + i * 20
        cv.tri(fx, y + h - 30, fx + 12, y + h - 30, fx + 6, y + h - 30 - fh, (232, 110, 36))
        cv.tri(fx + 3, y + h - 30, fx + 9, y + h - 30, fx + 6, y + h - 30 - fh + 8, (250, 196, 64))
    cv.circle(x + w - 16, y + 12, 8, (110, 108, 104))


def scene_tents(cv, x, y, w, h):
    cv.rect(x, y, w, h, (206, 222, 206))
    cv.rect(x, y + h - 12, w, 12, (140, 160, 120))
    for i in range(2):
        tx = x + 10 + i * (w // 2)
        tw = w // 2 - 16
        cv.tri(tx, y + h - 12, tx + tw, y + h - 12, tx + tw // 2, y + 14, (240, 240, 236))
        cv.rect(tx + tw // 2 - 2, y + 24, 4, 12, RED)
        cv.rect(tx + tw // 2 - 6, y + 28, 12, 4, RED)
    cv.circle(x + w - 14, y + 12, 6, (250, 210, 90))


def scene_refinery(cv, x, y, w, h):
    cv.rect(x, y, w, h, (188, 204, 220))
    cv.rect(x, y + h - 12, w, 12, (110, 116, 120))
    for i, th in enumerate((38, 48, 32)):
        tx = x + 12 + i * ((w - 24) // 3)
        cv.rect(tx, y + h - 12 - th, 12, th, (150, 158, 166))
        cv.rect(tx - 2, y + h - 14 - th, 16, 4, (120, 128, 136))
    fx = x + w // 2
    cv.tri(fx - 10, y + h - 46, fx + 10, y + h - 46, fx, y + 4, (232, 110, 36))
    cv.tri(fx - 5, y + h - 46, fx + 5, y + h - 46, fx, y + 16, (250, 196, 64))
    cv.circle(fx + 16, y + 10, 8, (90, 92, 96))
    cv.circle(fx + 26, y + 6, 6, (110, 112, 116))


def scene_mine(cv, x, y, w, h):
    cv.rect(x, y, w, h, (120, 128, 116))
    cv.poly([(x, y + h), (x + w // 2, y + 10), (x + w, y + h)], (96, 104, 88))
    mx = x + w // 2
    cv.rect(mx - 8, y + h - 26, 16, 26, (30, 28, 26))
    cv.rect(x, y + h - 10, w, 10, (52, 96, 128))
    for i in range(0, w, 12):
        cv.line(x + i, y + 2, x + i - 5, y + 18, (180, 210, 235), 1)
    cv.line(mx - 20, y + 16, mx - 4, y + h - 24, (240, 220, 160), 2)
    cv.circle(mx - 20, y + 16, 4, (240, 180, 60))


def scene_port(cv, x, y, w, h):
    cv.rect(x, y, w, h, (176, 204, 226))
    cv.rect(x, y + h - 14, w, 14, (60, 110, 150))
    cv.rect(x + 8, y + h - 26, w - 16, 10, (70, 80, 96))
    cols = [(176, 34, 52), (30, 76, 160), (24, 118, 66), (184, 132, 26)]
    for i, col in enumerate(cols):
        cv.rect(x + 12 + i * ((w - 24) // 4), y + h - 38, (w - 28) // 4, 11, col)
    cx = x + w - 24
    cv.line(cx, y + h - 26, cx, y + 8, INK, 3)
    cv.line(cx, y + 8, cx - 26, y + 8, INK, 3)
    cv.line(cx - 26, y + 8, cx - 26, y + 22, INK, 1)
    cv.rect(cx - 32, y + 22, 12, 8, GOLD)


def scene_bank(cv, x, y, w, h):
    cv.rect(x, y, w, h, (222, 226, 232))
    cv.tri(x + 10, y + 18, x + w - 10, y + 18, x + w // 2, y + 4, (120, 132, 150))
    for i in range(4):
        cv.rect(x + 16 + i * ((w - 32) // 4), y + 20, 8, h - 32, (170, 180, 196))
    cv.rect(x + 8, y + h - 12, w - 16, 6, (120, 132, 150))
    cv.circle(x + w - 16, y + 16, 9, GREEN)
    cv.line(x + w - 22, y + 22, x + w - 10, y + 10, WHITE, 2)
    cv.line(x + w - 22, y + 10, x + w - 10, y + 22, WHITE, 2)


def scene_seats(cv, x, y, w, h):
    cv.rect(x, y, w, h, (226, 230, 236))
    for row in range(3):
        for col in range(8):
            cx = x + 12 + col * ((w - 24) // 8)
            cy = y + 12 + row * 14
            colr = BLUE if col < 4 else (RED if col < 7 else GOLD)
            cv.circle(cx, cy, 4, colr)
    cv.line(x + w // 2, y + 6, x + w // 2, y + h - 8, INK, 2)


def scene_towers(cv, x, y, w, h):
    cv.rect(x, y, w, h, (200, 214, 230))
    cv.rect(x + w // 3, y + 8, 16, h - 18, (90, 120, 160))
    cv.rect(x + w // 3 + 22, y + 16, 14, h - 26, (110, 140, 180))
    cv.line(x + w // 3 + 16, y + 22, x + w // 3 + 22, y + 26, (90, 120, 160), 3)
    for wy in range(y + 14, y + h - 16, 9):
        cv.rect(x + w // 3 + 4, wy, 4, 5, (230, 238, 248))
        cv.rect(x + w // 3 + 26, wy + 4, 4, 5, (230, 238, 248))
    cv.circle(x + w - 18, y + 16, 10, GOLD)
    draw_center(cv, x + w - 18, y + 10, "E", 2, WHITE, bold=True)
    cv.rect(x, y + h - 10, w, 10, (110, 120, 130))


def scene_ship(cv, x, y, w, h):
    cv.rect(x, y, w, h, (150, 190, 216))
    cv.rect(x, y + h - 16, w, 16, (44, 100, 140))
    for i in range(0, w, 22):
        cv.line(x + i, y + h - 10, x + i + 12, y + h - 10, (190, 220, 240), 2)
    sx = x + w // 2
    cv.poly([(sx - 34, y + h - 20), (sx + 30, y + h - 26), (sx + 22, y + h - 12), (sx - 26, y + h - 12)], (70, 80, 96))
    cv.rect(sx - 6, y + h - 38, 16, 12, (200, 200, 204))
    cv.line(sx - 26, y + h - 20, sx - 14, y + h - 34, (200, 200, 204), 3)
    cv.circle(sx + 30, y + 12, 7, (250, 210, 90))


def scene_clinic(cv, x, y, w, h):
    cv.rect(x, y, w, h, (214, 232, 220))
    cv.rect(x + 10, y + 16, w - 20, h - 26, (240, 244, 240))
    cv.tri(x + 6, y + 16, x + w - 6, y + 16, x + w // 2, y + 4, (140, 170, 150))
    cv.rect(x + w // 2 - 3, y + 24, 6, 16, RED)
    cv.rect(x + w // 2 - 8, y + 29, 16, 6, RED)
    sx = x + w - 20
    cv.line(sx, y + 14, sx - 12, y + 34, (90, 140, 180), 4)
    cv.line(sx - 12, y + 34, sx - 16, y + 40, (60, 60, 60), 2)
    cv.rect(x, y + h - 10, w, 10, (140, 170, 150))


def scene_rescue(cv, x, y, w, h):
    cv.rect(x, y, w, h, (204, 208, 216))
    cv.rect(x + 12, y + 8, w - 24, h - 16, (160, 166, 178))
    for wy in range(y + 14, y + h - 14, 11):
        for wx in range(x + 18, x + w - 22, 12):
            cv.rect(wx, wy, 6, 7, (226, 232, 240))
    cv.rect(x + w // 2 - 8, y + h - 22, 16, 14, (90, 96, 108))
    cv.circle(x + w // 2 - 14, y + h - 12, 4, GOLD)
    cv.circle(x + w // 2 + 14, y + h - 12, 4, GOLD)


SCENES = {
    "storm": scene_storm, "drone": scene_drone, "summit": scene_summit,
    "blocks": scene_blocks, "tankerfire": scene_tankerfire, "tents": scene_tents,
    "refinery": scene_refinery, "mine": scene_mine, "port": scene_port,
    "bank": scene_bank, "seats": scene_seats, "towers": scene_towers,
    "ship": scene_ship, "clinic": scene_clinic, "rescue": scene_rescue,
}


# number, region, badge, headline, body, key figure, source, scene, lon, lat
HEROES = [
    (1, "NORTH AMERICA", "CONFIRMED", "STORM KNOCKS OUT POWER",
     "Storm floods streets and cuts power across the US East.",
     "961,000", "AP / BBC", "storm", -77, 39),
    (2, "MIDDLE EAST", "CLAIM", "DRONE STRIKE KILLS 2 ITALIANS",
     "Italy blames Iran drones; Iran denies role.",
     "2 KILLED", "REUTERS/BBC", "drone", 47, 29),
    (3, "EUROPE", "REPORTED", "EU DEFERS UKRAINE LOAN",
     "Leaders delay the loan decision to December; 24 backed it.",
     "EUR 45BN", "REUTERS / AP", "summit", 2, 47),
]

GRID = [
    (4, "MIDDLE EAST", "REPORTED", "GAZA STRIKES KILL 8", "3 STRIKES HIT HOMES", "8 DEAD", "BBC/AP", "blocks", 34, 31),
    (5, "AFRICA", "CONFIRMED", "CAIRO DRIVER HELD, TOLL 31", "FINAL TOLL RISES TO 31", "31 DEAD", "AP", "tankerfire", 31, 27),
    (6, "AFRICA", "CONFIRMED", "EBOLA CASES PASS 12,000", "DEATH TOLL 5,904", "12,021 CASES", "AP/REUTERS", "tents", 28, -3),
    (7, "ASIA", "CONFIRMED", "BANGKOK REFINERY BLAST", "3 IN CRITICAL CONDITION", "9 INJURED", "AP/BBC", "refinery", 100, 13),
    (8, "ASIA", "CONFIRMED", "MINE SEARCH HALTED, 13 DEAD", "RAIN HALTS RESCUE WORK", "13 TRAPPED", "REUTERS", "mine", 106, -6),
    (9, "ASIA", "REPORTED", "TARIFF BACKLASH SPREADS", "PARTNERS PROTEST PLAN", "14 ECONOMIES", "AP/REUTERS", "port", 116, 40),
    (10, "LATIN AMERICA", "CONFIRMED", "ARGENTINA BANS MONEY PRINTING", "LAW PASSES; 99 ABSTAIN", "141-0", "AP", "bank", -58, -34),
    (11, "OCEANIA", "CONFIRMED", "NZ COALITION 1 SEAT SHORT", "FINAL COUNT IS IN", "65/130 SEATS", "BBC/REUTERS", "seats", 174, -41),
    (12, "EUROPE", "CONFIRMED", "DE COS TO LEAD ECB", "LAGARDE SUCCESSOR CHOSEN", "359M PEOPLE", "AP", "towers", 12, 53),
    (13, "EUROPE", "CONFIRMED", "TANKER CAPSIZES OFF IBIZA", "17 CREW RESCUED AT SEA", "7,000 TONNES", "REUTERS", "ship", 1, 39),
    (14, "AFRICA", "CONFIRMED", "HIV JAB AT $40 A YEAR", "SHOTS REACH ZAMBIA FIRST", "$40 / YEAR", "BBC", "clinic", 28, -15),
    (15, "ASIA", "REPORTED", "164 FREED FROM CYBER SCAMS", "DELHI POLICE FREE 164", "164 RESCUED", "REUTERS", "rescue", 77, 28),
]

ALSO = [
    "GUINEA-BISSAU VOTE 2028", "KENYA CULT CHIEF GUILTY", "SERBIA VOTE SET DEC 27",
    "IRAQ SHUTS 2 CROSSINGS", "VENEZUELA SEEKS LOANS", "JERA TALKS AI CENTRES",
    "DEPARDIEU TO STAND TRIAL", "UK-EU DEAL: 10-YEAR EXIT", "MYANMAR DEFIES ICJ RULING",
    "TRAIN ATTACKER GUILTY: 14", "TRUMP: GDP FAKE, 4.3%", "NIKKEI JUMPS 1.4% ON TECH",
    "BRENT $96.57, MINE CLAIM", "UKRAINE: N KOREA PAUSES", "ZELENSKY WARNS AMERICA",
    "HONG KONG MOURNS 168", "ANDY TAYLOR DIES AT 65", "UK NET MIGRATION 1997 LOW",
]

DATE_CHECK = [
    "25 NOV TARIFF PLAN", "25 NOV 1M SATS OK", "25 NOV FEDEX OVERRUN",
    "25 NOV ABC BLOCKED", "25 NOV CAIRO CRASH", "23 NOV MINE FLOOD",
]

# lon0, lon1, lat0, lat1 boxes approximating the continents for the dotted map
LAND_RECTS = [
    (-168, -140, 55, 72), (-140, -110, 48, 70), (-125, -95, 32, 55), (-110, -75, 25, 50),
    (-95, -65, 18, 42), (-85, -77, 7, 18), (-55, -22, 60, 75),
    (-80, -60, -5, 10), (-75, -45, -20, 5), (-72, -48, -35, -15), (-70, -55, -55, -32),
    (-10, 30, 43, 60), (0, 40, 50, 65), (10, 45, 55, 70), (-9, 3, 36, 44),
    (12, 28, 38, 46), (-5, 2, 50, 59),
    (-17, 35, 15, 35), (-10, 30, 5, 20), (8, 32, -12, 8), (12, 35, -28, -8),
    (18, 33, -35, -24), (43, 50, -25, -12),
    (33, 60, 12, 32), (44, 63, 25, 40), (60, 90, 35, 55), (40, 180, 50, 75),
    (75, 122, 20, 45), (72, 88, 20, 28), (75, 85, 8, 22), (92, 108, 5, 22),
    (95, 110, -6, 5), (110, 125, -10, 2), (125, 141, -8, -1), (129, 146, 31, 45),
    (126, 130, 34, 40),
    (113, 142, -26, -11), (115, 150, -39, -24), (166, 178, -47, -34),
]

PIN_NUDGE = {2: (6, -2), 3: (0, -6), 4: (7, -5), 5: (-7, 6), 6: (0, -6),
             7: (0, -4), 8: (0, 4), 12: (8, -4), 13: (0, 7), 14: (0, 6)}


def draw_masthead(cv):
    cv.rect(24, 12, 976, 3, INK)
    draw_center(cv, 512, 20, "WORLD NEWS IN ONE IMAGE", 2, MUTED, bold=True)
    draw_center(cv, 512, 38, "THURSDAY 26 NOVEMBER 2026", 6, INK, bold=True)
    draw_center(cv, 512, 86, "33 STORIES - 7 REGIONS - 15 ILLUSTRATED REPORTS - ALL TIMES UTC", 2, RED, bold=True)
    cv.rect(24, 106, 976, 2, INK)


def draw_stats(cv):
    stats = [("961,000", "US WITHOUT POWER"), ("EUR 45BN", "UKRAINE LOAN HELD"),
             ("12,021", "EBOLA CASES CONGO"), ("31 DEAD", "CAIRO FIRE TOLL")]
    cv.rect(24, 112, 976, 40, INK)
    for i, (num, label) in enumerate(stats):
        cx = 24 + i * 244 + 122
        draw_center(cv, cx, 116, num, 3, (250, 214, 110), bold=True)
        draw_center(cv, cx, 138, label, 2, WHITE, bold=True)
        if i:
            cv.rect(24 + i * 244, 118, 2, 28, (90, 90, 96))


def draw_hero(cv, story, x, y, w, h):
    num, region, badge_label, headline, body, figure, source, scene, lon, lat = story
    cv.rect(x, y, w, h, WHITE)
    cv.frame(x, y, w, h, RULE, 2)
    SCENES[scene](cv, x + 2, y + 2, w - 4, 104)
    number_chip(cv, x + 8, y + 8, num)
    ty = y + 110
    draw_text(cv, x + 10, ty, region + " - " + source, 2, MUTED, bold=True)
    ty = draw_wrapped(cv, x + 10, ty + 16, headline, 25, 2, INK, 2, bold=True, leading=16)
    ty = draw_wrapped(cv, x + 10, ty + 2, body, 25, 2, (52, 50, 46), 3, leading=15)
    fy = y + h - 24
    draw_text(cv, x + 10, fy, figure, 3, RED, bold=True)
    bw = text_width(badge_label, 2) + 10
    badge(cv, x + w - bw - 10, fy + 2, badge_label)


def draw_map(cv, x, y, w, h):
    cv.rect(x, y, w, h, (238, 240, 238))
    cv.frame(x, y, w, h, RULE, 2)
    draw_text(cv, x + 10, y + 6, "WHERE IT HAPPENED - PINS MATCH CARD NUMBERS", 2, INK, bold=True)
    mx0 = x + 14
    my0 = y + 28
    mw = w - 28
    mh = h - 38
    lat = 74
    while lat >= -60:
        lon = -178
        while lon <= 178:
            if any(r[0] <= lon <= r[1] and r[2] <= lat <= r[3] for r in LAND_RECTS):
                dx = mx0 + int((lon + 180) / 360 * mw)
                dy = my0 + int((75 - lat) / 135 * mh)
                cv.rect(dx, dy, 3, 2, (120, 140, 128))
            lon += 4
        lat -= 6
    for story in HEROES + GRID:
        num, lon, lat = story[0], story[8], story[9]
        px = mx0 + int((lon + 180) / 360 * mw)
        py = my0 + int((75 - lat) / 135 * mh)
        ndx, ndy = PIN_NUDGE.get(num, (0, 0))
        px += ndx
        py += ndy
        cv.circle(px, py, 9, RED)
        label = str(num)
        draw_text(cv, px - text_width(label, 1) // 2, py - 3, label, 1, WHITE, bold=True)


def draw_date_check(cv, x, y, w, h):
    cv.rect(x, y, w, h, (252, 246, 230))
    cv.frame(x, y, w, h, GOLD, 2)
    draw_text(cv, x + 10, y + 5, "DATE CHECK", 2, RED, bold=True)
    draw_text(cv, x + 10, y + 21, "EXCLUDED ON PURPOSE", 2, INK)
    ly = y + 38
    for item in DATE_CHECK:
        draw_text(cv, x + 10, ly, item, 2, (52, 50, 46))
        ly += 15


def draw_grid_card(cv, story, x, y, w, h):
    num, region, badge_label, headline, body, figure, source, scene, lon, lat = story
    cv.rect(x, y, w, h, WHITE)
    cv.frame(x, y, w, h, RULE, 1)
    SCENES[scene](cv, x + 1, y + 1, 92, h - 2)
    number_chip(cv, x + 5, y + 5, num)
    tx = x + 100
    draw_text(cv, tx, y + 3, headline, 2, INK, bold=True)
    draw_text(cv, tx, y + 20, body, 2, (52, 50, 46))
    draw_text(cv, x + w - text_width(source, 2) - 8, y + 20, source, 2, MUTED, bold=True)
    draw_text(cv, tx, y + 37, region, 2, MUTED, bold=True)
    draw_text(cv, tx + text_width(region, 2) + 12, y + 37, figure, 2, RED, bold=True)
    bw = text_width(badge_label, 2) + 10
    badge(cv, x + w - bw - 8, y + 35, badge_label)


def draw_also(cv, x, y, w):
    cv.rect(x, y, w, 2, INK)
    draw_text(cv, x, y + 6, "ALSO ON THURSDAY", 2, RED, bold=True)
    draw_text(cv, x + w - text_width("18 MORE REPORTS", 2), y + 6, "18 MORE REPORTS", 2, MUTED, bold=True)
    col_w = w // 3
    for col in (1, 2):
        cv.rect(x + col * col_w - 8, y + 24, 1, 88, (200, 196, 186))
    for i, item in enumerate(ALSO):
        col = i % 3
        row = i // 3
        ix = x + col * col_w
        iy = y + 24 + row * 15
        cv.rect(ix, iy + 3, 6, 6, TEAL)
        draw_text(cv, ix + 11, iy, item, 2, INK)


def render():
    cv = Canvas(W, H, PAPER)
    draw_masthead(cv)
    draw_stats(cv)
    hero_y = 158
    for i, story in enumerate(HEROES):
        draw_hero(cv, story, 24 + i * 328, hero_y, 320, 228)
    draw_map(cv, 24, 394, 700, 128)
    draw_date_check(cv, 732, 394, 268, 128)
    draw_text(cv, 24, 528, "THE DAY IN BRIEF", 2, RED, bold=True)
    draw_text(cv, 1000 - text_width("12 MORE ILLUSTRATED REPORTS", 2), 528,
              "12 MORE ILLUSTRATED REPORTS", 2, MUTED, bold=True)
    grid_y = 548
    for i, story in enumerate(GRID):
        col = i % 2
        row = i // 2
        draw_grid_card(cv, story, 24 + col * 494, grid_y + row * 57, 482, 54)
    draw_also(cv, 24, 892, 976)
    draw_center(cv, 512, 1008,
                "SOURCES REUTERS AP AFP BBC | CONFIRMED FACT - REPORTED 1 SOURCE - CLAIM 1 SIDE",
                2, MUTED, bold=True)
    return cv


def encode_png(cv):
    raw = bytearray()
    stride = cv.w * 3
    for yy in range(cv.h):
        raw.append(0)
        raw.extend(cv.px[yy * stride:(yy + 1) * stride])

    def chunk(kind, data):
        out = struct.pack(">I", len(data)) + kind + data
        out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b""))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    os.makedirs(out_dir, exist_ok=True)
    data = encode_png(render())
    with open(os.path.join(out_dir, "entry.png"), "wb") as fh:
        fh.write(data)


if __name__ == "__main__":
    main()
