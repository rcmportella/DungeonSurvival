#!/usr/bin/env python3
"""
Convert PSPMAP01.png (a blue-and-white graph-paper dungeon map) into maps/PSPMAP01.json

Floors and walls are read from the image automatically: the picture is a grid of
43 x 53 squares, and each square is white (open) or blue (rock). Thin room outlines
are detected from the image as well. Symbols such as doors, stairs and statues are
too small to detect reliably, so their positions were read by hand and are listed in
the tables below (grid coordinates: column i, row j, counted from the top-left square).

Each map square becomes a 2x2 block of tiles plus a shared border, so walls and doors
can sit on the lines between squares: square (i, j) is tile (2i+1, 2j+1).
"""
import os
import numpy as np
from PIL import Image
from dungeon_map import DungeonMap, Tile
from door import Door

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGE = os.path.join(HERE, "PSPMAP01.png")
OUTPUT = os.path.join(HERE, "maps", "PSPMAP01.json")

# Grid fitted to the scan: x = X0 + DX * column, y = Y0 + DY * row
X0, DX = 14.56, 14.46
Y0, DY = 6.3, 14.545
COLS, ROWS = 43, 53
WALL_LINE_THRESHOLD = 185  # mean red value below which a grid line is a wall outline

# Squares covered by the legend and the numbered call-out bubbles (not part of the map)
BLANK_AREAS = [
    (16, COLS - 1, 46, ROWS - 1),  # legend
    (21, 23, 2, 4), (27, 30, 2, 4),  # bubbles 1A, 1B
    (26, 28, 25, 29),  # bubble 20
    (32, 35, 31, 33), (34, 34, 34, 34),  # bubble UL
    (18, 21, 43, 45), (16, 17, 45, 45),  # bubble TL
]
KEEP_OPEN = [(26, 24)]  # pit between rooms 19 and 21, drawn under the tail of bubble 20

# Outlines wrongly detected on cave walls and on the octagon's inner room
IGNORE_WALL_LINES = [
    (0, 8, 26, 31), (9, 13, 31, 35), (2, 7, 35, 41), (15, 19, 35, 40),
    (38, 42, 5, 14), (3, 6, 5, 8),
]
# Outline of rooms 6 and 7 that the detector misses: vertical line at column 14
EXTRA_VERTICAL_LINES = [(14, j) for j in range(9, 21)]

# Doors on a vertical line between squares (i-1, j) and (i, j)
DOORS_V = [
    (18, 7), (18, 11), (18, 14), (18, 17), (14, 13), (10, 14), (10, 16), (31, 7), (24, 10),
    (14, 19), (14, 22), (21, 24), (21, 32), (16, 29), (32, 19), (32, 22), (26, 24), (27, 24),
    (29, 24), (22, 29), (40, 34), (40, 38), (33, 40), (8, 47), (9, 47), (8, 48), (8, 49),
    (11, 41), (15, 43), (12, 45), (13, 45),
]
# Doors on a horizontal line between squares (i, j-1) and (i, j) given as (j, i)
DOORS_H = [
    (11, 14), (12, 29), (16, 38), (23, 24), (26, 21), (26, 33), (20, 36), (35, 38),
    (42, 9), (42, 16), (41, 20), (50, 8), (50, 9), (50, 10), (50, 11), (50, 12), (50, 13),
    (49, 13),
]
# Secret doors (hard to open) and portcullises (very hard)
SECRET_V = [(15, 12), (17, 12), (35, 21), (36, 17)]
SECRET_H = [(10, 26), (12, 26), (28, 17)]
PORTCULLIS_H = [(1, 24), (1, 25), (1, 26), (23, 21)]
PORTCULLIS_V = [(13, 43)]

STATUES = [(3, 19), (2, 29), (11, 38), (16, 35), (33, 39), (5, 37), (6, 38), (5, 39), (6, 39)]
STAIRS_UP = (25, 2)     # dungeon entrance, just south of the entrance portcullis
STAIRS_DOWN = (15, 46)  # "TL" staircase


def read_squares(red):
    """Return a ROWS x COLS boolean array: True where the square is white (open)"""
    white = np.zeros((ROWS, COLS), bool)
    for j in range(ROWS):
        for i in range(COLS):
            x0, x1 = int(X0 + DX * i + 3), int(X0 + DX * (i + 1) - 2)
            y0, y1 = int(Y0 + DY * j + 3), int(Y0 + DY * (j + 1) - 2)
            white[j][i] = (red[y0:y1, x0:x1] > 150).mean() > 0.5
    for c0, c1, r0, r1 in BLANK_AREAS:
        white[r0:r1 + 1, c0:c1 + 1] = False
    for i, j in KEEP_OPEN:
        white[j][i] = True
    return white


def read_wall_lines(red, white):
    """Detect thin room outlines drawn on the lines between two open squares"""
    def vertical_score(i, j):
        x = X0 + DX * i
        ys = slice(int(Y0 + DY * j + 3), int(Y0 + DY * (j + 1) - 2))
        return min(red[ys, xx].mean() for xx in range(int(round(x)) - 1, int(round(x)) + 2))

    def horizontal_score(i, j):
        y = Y0 + DY * j
        xs = slice(int(X0 + DX * i + 3), int(X0 + DX * (i + 1) - 2))
        return min(red[yy, xs].mean() for yy in range(int(round(y)) - 1, int(round(y)) + 2))

    vertical = np.zeros((ROWS, COLS + 1), bool)    # vertical[j][i]: line left of square (i, j)
    horizontal = np.zeros((ROWS + 1, COLS), bool)  # horizontal[j][i]: line above square (i, j)
    for j in range(ROWS):
        for i in range(1, COLS):
            if white[j][i] and white[j][i - 1] and vertical_score(i, j) < WALL_LINE_THRESHOLD:
                vertical[j][i] = True
    for j in range(1, ROWS):
        for i in range(COLS):
            if white[j][i] and white[j - 1][i] and horizontal_score(i, j) < WALL_LINE_THRESHOLD:
                horizontal[j][i] = True

    # A real outline is at least two squares long; isolated hits are text or hatching
    for i in range(COLS + 1):
        keep_runs(vertical[:, i])
    for j in range(ROWS + 1):
        keep_runs(horizontal[j, :])

    for c0, c1, r0, r1 in IGNORE_WALL_LINES:
        vertical[r0:r1 + 1, c0:c1 + 1] = False
        horizontal[r0:r1 + 1, c0:c1 + 1] = False
    for i, j in EXTRA_VERTICAL_LINES:
        vertical[j][i] = True
    return vertical, horizontal


def keep_runs(line, minimum=2):
    """In place: clear runs of True shorter than 'minimum'"""
    n = len(line)
    k = 0
    while k < n:
        if line[k]:
            end = k
            while end < n and line[end]:
                end += 1
            if end - k < minimum:
                line[k:end] = False
            k = end
        else:
            k += 1


def build_map():
    red = np.array(Image.open(IMAGE).convert("RGB")).astype(float)[:, :, 0]
    white = read_squares(red)
    vertical, horizontal = read_wall_lines(red, white)

    width, height = 2 * COLS + 1, 2 * ROWS + 1
    open_tile = np.zeros((height, width), bool)
    for j in range(ROWS):
        for i in range(COLS):
            if white[j][i]:
                open_tile[2 * j + 1][2 * i + 1] = True
    # Openings between two open squares, unless a thin wall is drawn there
    for j in range(ROWS):
        for i in range(1, COLS):
            if white[j][i] and white[j][i - 1] and not vertical[j][i]:
                open_tile[2 * j + 1][2 * i] = True
    for j in range(1, ROWS):
        for i in range(COLS):
            if white[j][i] and white[j - 1][i] and not horizontal[j][i]:
                open_tile[2 * j][2 * i + 1] = True
    # Corners are open only when everything around them is open
    for j in range(ROWS + 1):
        for i in range(COLS + 1):
            around = [(2 * i - 1, 2 * j), (2 * i + 1, 2 * j), (2 * i, 2 * j - 1), (2 * i, 2 * j + 1)]
            if all(0 <= x < width and 0 <= y < height and open_tile[y][x] for x, y in around):
                open_tile[2 * j][2 * i] = True

    dungeon = DungeonMap(width=width, height=height)
    for y in range(height):
        for x in range(width):
            dungeon.tiles[y][x] = Tile.create_floor() if open_tile[y][x] else Tile.create_wall()

    for i, j in STATUES:
        if white[j][i]:
            dungeon.tiles[2 * j + 1][2 * i + 1] = Tile.create_wall()

    def put_door(x, y, vertical_line, locked=False, lockpick_dc=15, smash_dc=18):
        if not (open_tile[y][x] or dungeon.tiles[y][x].blocked):
            return
        door = Door(horizontal=not vertical_line, locked=locked,
                    lockpick_dc=lockpick_dc, smash_dc=smash_dc)
        door.is_open = False  # closed; locked doors need a lockpick or a smash
        dungeon.tiles[y][x] = Tile.create_door(horizontal=not vertical_line)
        dungeon.place_door(door, x, y)

    for i, j in DOORS_V:
        put_door(2 * i, 2 * j + 1, True)
    for j, i in DOORS_H:
        put_door(2 * i + 1, 2 * j, False)
    for i, j in SECRET_V:
        put_door(2 * i, 2 * j + 1, True, True, 25, 22)
    for j, i in SECRET_H:
        put_door(2 * i + 1, 2 * j, False, True, 25, 22)
    for i, j in PORTCULLIS_V:
        put_door(2 * i, 2 * j + 1, True, True, 30, 25)
    for j, i in PORTCULLIS_H:
        put_door(2 * i + 1, 2 * j, False, True, 30, 25)

    ux, uy = 2 * STAIRS_UP[0] + 1, 2 * STAIRS_UP[1] + 1
    dx, dy = 2 * STAIRS_DOWN[0] + 1, 2 * STAIRS_DOWN[1] + 1
    dungeon.stairs_up, dungeon.stairs_down = (ux, uy), (dx, dy)
    dungeon.tiles[uy][ux] = Tile(Tile.STAIRS_UP, blocked=False)
    dungeon.tiles[dy][dx] = Tile(Tile.STAIRS_DOWN, blocked=False)
    return dungeon


def main():
    dungeon = build_map()
    DungeonMap.save_multilevel_dungeon([dungeon], OUTPUT)
    print(f"Saved {OUTPUT} ({dungeon.width}x{dungeon.height} tiles, {len(dungeon.doors)} doors)")


if __name__ == "__main__":
    main()
