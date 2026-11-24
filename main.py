"""The World in One Day -- Monday 23 November 2026.

Draws a single 1024x1024 PNG front page summing up the world's news of
Monday 23 November 2026: 36 dated stories across 7 regions. A markets
hero (Nvidia's Jensen Huang returns, shares up 31 percent) and a
climate hero (COP31 collapses with no deal) sit above a four-number
stat strip and a seven-section region grid, with an "also on Monday"
closer. Pure Python 3 standard library, no network, no clock reads,
no randomness: two runs write identical bytes.

Run:  python3 main.py
Writes entry.png into $MAKEFUN_OUTPUT_DIR (default /output).
"""

import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (247, 243, 232)
INK = (17, 17, 17)
NAVY = (20, 38, 74)
RED = (176, 30, 36)
GREEN = (18, 122, 62)
GOLD = (150, 108, 20)
GREY = (108, 108, 100)
LIGHT = (228, 222, 208)
MIDGREY = (190, 184, 170)
WHITE = (255, 255, 255)


def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(path, rgb, w, h):
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw += rgb[y * w * 3:(y + 1) * w * 3]
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png += _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += _chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


class Canvas:
    """A plain RGB canvas drawn with filled rectangles only."""

    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg * (w * h))

    def fill(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        r, g, b = color
        row = bytes((r, g, b)) * (x1 - x0)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            self.px[base:base + len(row)] = row

    def dot(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            base = (y * self.w + x) * 3
            self.px[base:base + 3] = bytes(color)

    def hline(self, x, y, w, color, t=1):
        self.fill(x, y, w, t, color)

    def vline(self, x, y, h, color, t=1):
        self.fill(x, y, t, h, color)

    def box(self, x, y, w, h, color, t=1):
        self.hline(x, y, w, color, t)
        self.hline(x, y + h - t, w, color, t)
        self.vline(x, y, h, color, t)
        self.vline(x + w - t, y, h, color, t)

    def line(self, x0, y0, x1, y1, color, t=1):
        """Bresenham line, t pixels thick."""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.fill(x0 - t // 2, y0 - t // 2, t, t, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy


# A 5x7 bitmap lettering set, written for this poster. Each glyph is
# seven rows of five cells; '#' is ink, '.' is blank. Only capitals,
# digits and the punctuation the headlines need.
GLYPHS = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
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
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", "..#..", ".#..."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "...##.", "..#..", ".....", "..#.."),
    "-": (".....", ".....", ".....", ".###.", ".....", ".....", "....."),
    "/": ("....#", "...#.", "...#.", "..#..", ".#...", ".#...", "#...."),
    "+": (".....", "..#..", "..#..", ".###.", "..#..", "..#..", "....."),
    "%": ("##..#", "##.#.", "....#", "...#.", "..#..", ".#..#", "#..##"),
    "(": ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
    ")": (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
    "$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    "&": (".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
}


def glyph_width(scale):
    return 6 * scale


def text_width(text, scale):
    return len(text) * glyph_width(scale) - scale


def draw_text(cv, x, y, text, scale, color):
    """Draw one line of text at (x, y); returns the width used."""
    cx = x
    for ch in text:
        rows = GLYPHS.get(ch)
        if rows is None:
            rows = GLYPHS[" "]
        for ry, row in enumerate(rows):
            for rx, cell in enumerate(row):
                if cell == "#" or cell == "1":
                    cv.fill(cx + rx * scale, y + ry * scale,
                            scale, scale, color)
        cx += glyph_width(scale)
    return cx - x - scale


def text_lines(text, scale, max_w):
    """Greedy word wrap; returns a list of lines fitting max_w."""
    words = text.split(" ")
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(cv, x, y, text, scale, max_w, color, leading=None,
                 max_lines=None):
    """Draw wrapped text; returns the y just below the last line."""
    if leading is None:
        leading = 9 * scale
    lines = text_lines(text, scale, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    cy = y
    for line in lines:
        draw_text(cv, x, cy, line, scale, color)
        cy += leading
    return cy

# ---------------------------------------------------------------- data

HERO_LEFT_KICKER = "MARKETS"
HERO_LEFT_HEAD = ["HUANG IS BACK", "NVIDIA +31%"]
HERO_LEFT_DECK = [
    "BOARD REINSTATES CEO; $1TN ADDED IN A DAY",
    "BEST DAY FOR THE STOCK SINCE 2003",
]
HERO_RIGHT_KICKER = "CLIMATE - ANTALYA"
HERO_RIGHT_HEAD = ["COP31", "COLLAPSES"]
HERO_RIGHT_DECK = [
    "TALKS END WITHOUT A PACT AFTER TWO WEEKS",
    "EU REJECTED A TEXT WITH NO FOSSIL FUELS",
]

STATS = [
    ("+6.5%", GREEN, "NASDAQ, BEST DAY SINCE APRIL 2025"),
    ("450", RED, "GERMAN SCHOOLS GET BOMB THREATS"),
    ("258", NAVY, "DEMOCRATS WIN HOUSE SEATS"),
    ("$55,130", RED, "BITCOIN SAT LOW, 7TH LOSING WEEK"),
]

# Seven labeled regions; every headline is one dated story.
SECTIONS = [
    ("EUROPE", [
        "KRYVYI RIH: BOY 7, PARAMEDIC KILLED",
        "3 MISSILES LAND IN POLAND",
        "KYIV FLAT BLOCK HIT, 14 MISSING",
        "RUSSIA STRIKES 11 REGIONS",
        "DENMARK SCHOOLS HIT TOO",
        "BALTIC FLEET BASE HIT, A FIRST",
    ]),
    ("MIDDLE EAST", [
        "HORMUZ: 3 TANKERS HIT MINES",
        "IRAN STRIKE WOUNDS 2 IN BAHRAIN",
        "HOUTHIS CLAIM SAUDI REFINERY HIT",
        "3 US CARRIER GROUPS IN THE GULF",
        "COALITION STOPS HOUTHI MISSILE",
    ]),
    ("AFRICA", [
        "SOUTH SUDAN: 24 CIVILIANS KILLED",
        "WHO: FIGHTING NEARS EBOLA OUTBREAK",
        "BENGHAZI: UKRAINE CLAIMS WARSHIP SUNK",
        "UN SEEKS PROBE INTO BENGHAZI STRIKES",
    ]),
    ("ASIA-PACIFIC", [
        "EU-INDONESIA PACT: TARIFFS TO ZERO",
        "INDONESIA FACTORY FIRE, 3 DEAD",
        "JAPAN QUAKE 6.1 JOLTS NORTH",
        "TRUMP, XI, PUTIN MEET AT APEC",
    ]),
    ("NORTH AMERICA", [
        "TRUMP PRESSED BOARD ON HUANG",
        "SENATE: DEMOCRATS WIN 56 SEATS",
    ]),
    ("LATIN AMERICA", [
        "EL CHAPO ISIDRO CAPTURED, 11 KILLED",
    ]),
    ("MARKETS", [
        "DOW +1,448 AS STOCKS SURGE",
        "CHIP RALLY: MICRON +19%, AMD +10%",
        "BRENT $92.44 AS HORMUZ MINES HIT",
        "COREWEAVE +22% AS CHIPS RALLY",
    ]),
]

ALSO = [
    "LIVERPOOL HAMMER MAN UTD 4-0",
    "UN LETHAL-AI TALKS CONTINUE",
    "ELECTRIFICATION PLEDGE: 90+ NATIONS",
    "ODESA SCHOOLS GO REMOTE",
]


# ---------------------------------------------------------------- drawing

def draw_masthead(cv):
    draw_text(cv, 24, 22, "THE WORLD IN ONE DAY", 8, INK)
    draw_text(cv, 24, 92, "MONDAY 23 NOVEMBER 2026", 3, RED)
    right = "36 STORIES - 7 REGIONS"
    draw_text(cv, W - 24 - text_width(right, 3), 92, right, 3, INK)
    cv.hline(24, 116, W - 48, INK, 4)
    cv.hline(24, 122, W - 48, INK, 1)


def draw_chart(cv, x, y, w, h):
    """A rising market line inside the hero panel."""
    cv.box(x, y, w, h, MIDGREY, 1)
    for frac in (0.25, 0.5, 0.75):
        gy = y + int(h * frac)
        cv.hline(x + 1, gy, w - 2, LIGHT, 1)
    pts = [(0.02, 0.72), (0.18, 0.68), (0.32, 0.78), (0.46, 0.60),
           (0.58, 0.52), (0.72, 0.34), (0.86, 0.20), (0.98, 0.06)]
    prev = None
    for fx, fy in pts:
        px = x + int(w * fx)
        py = y + int(h * fy)
        if prev is not None:
            cv.line(prev[0], prev[1], px, py, GREEN, 4)
        prev = (px, py)
    ex, ey = prev
    cv.line(ex, ey, ex - 14, ey + 2, GREEN, 4)
    cv.line(ex, ey, ex - 2, ey + 14, GREEN, 4)
    cv.fill(ex - 5, ey - 5, 10, 10, GREEN)


def draw_hero_left(cv, x, y, w, h):
    cv.fill(x, y, w, h, WHITE)
    cv.box(x, y, w, h, INK, 2)
    ix = x + 16
    iy = y + 12
    draw_text(cv, ix, iy, HERO_LEFT_KICKER, 2, RED)
    cy = iy + 24
    for line in HERO_LEFT_HEAD:
        draw_text(cv, ix, cy, line, 7, INK)
        cy += 56
    draw_chart(cv, ix, cy + 2, w - 32, 64)
    cy += 74
    for line in HERO_LEFT_DECK:
        draw_text(cv, ix, cy, line, 2, GREY)
        cy += 15


def draw_doc(cv, x, y, w, h):
    """A pact document crossed out in red."""
    cv.fill(x, y, w, h, WHITE)
    cv.box(x, y, w, h, INK, 2)
    for i in range(4):
        ly = y + 16 + i * 16
        cv.fill(x + 12, ly, w - 24, 5, MIDGREY)
    cv.line(x + 6, y + 6, x + w - 6, y + h - 6, RED, 5)
    cv.line(x + w - 6, y + 6, x + 6, y + h - 6, RED, 5)


def draw_hero_right(cv, x, y, w, h):
    cv.fill(x, y, w, h, NAVY)
    cv.box(x, y, w, h, INK, 2)
    ix = x + 16
    iy = y + 12
    draw_text(cv, ix, iy, HERO_RIGHT_KICKER, 2, GOLD)
    draw_text(cv, ix, iy + 26, "COP31", 8, WHITE)
    draw_text(cv, ix, iy + 88, "COLLAPSES", 4, WHITE)
    draw_doc(cv, ix + 250, iy + 26, 110, 86)
    sy = iy + 126
    cv.fill(ix, sy, 150, 36, RED)
    cv.box(ix, sy, 150, 36, WHITE, 2)
    draw_text(cv, ix + 11, sy + 8, "NO DEAL", 3, WHITE)
    cy = sy + 48
    for line in HERO_RIGHT_DECK:
        cy = draw_wrapped(cv, ix, cy, line, 2, w - 32, WHITE,
                          leading=16, max_lines=2)
        cy += 2


def draw_stats(cv, y):
    cw = 238
    gap = 8
    for i, (num, color, label) in enumerate(STATS):
        x = 24 + i * (cw + gap)
        cv.fill(x, y, cw, 80, WHITE)
        cv.box(x, y, cw, 80, INK, 1)
        cv.fill(x, y, cw, 4, color)
        draw_text(cv, x + 12, y + 12, num, 5, color)
        draw_wrapped(cv, x + 12, y + 48, label, 2, cw - 24, INK,
                     leading=15, max_lines=2)


def draw_grid(cv, y0):
    col_w = 235
    gap = 12
    row_h = 222
    for idx, (header, items) in enumerate(SECTIONS):
        col = idx % 4
        row = idx // 4
        x = 24 + col * (col_w + gap)
        y = y0 + row * (row_h + gap)
        draw_text(cv, x, y, header, 2, RED)
        cv.hline(x, y + 20, col_w, RED, 2)
        cy = y + 30
        for item in items:
            cy = draw_wrapped(cv, x, cy, item, 2, col_w, INK,
                              leading=14, max_lines=2)
            cy += 5
    ax = 24 + 3 * (col_w + gap)
    ay = y0 + 1 * (row_h + gap)
    draw_text(cv, ax, ay, "ALSO ON MONDAY", 2, RED)
    cv.hline(ax, ay + 20, col_w, RED, 2)
    cy = ay + 30
    for item in ALSO:
        cy = draw_wrapped(cv, ax, cy, item, 2, col_w, INK,
                          leading=14, max_lines=2)
        cy += 5


def draw_footer(cv, y):
    cv.hline(24, y, W - 48, INK, 4)
    draw_text(cv, 24, y + 12,
              "DATE CHECK: EVERY STORY DATED MONDAY 23 NOVEMBER 2026",
              2, INK)
    draw_text(cv, 24, y + 32,
              "SOURCES: REUTERS, AP, CNN, LE MONDE, WSJ, UKMTO",
              2, GREY)


def main():
    cv = Canvas(W, H, PAPER)
    draw_masthead(cv)
    draw_hero_left(cv, 24, 134, 572, 250)
    draw_hero_right(cv, 608, 134, 392, 250)
    draw_stats(cv, 396)
    draw_grid(cv, 488)
    draw_footer(cv, 948)
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    write_png(path, cv.px, W, H)
    print("wrote", path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
