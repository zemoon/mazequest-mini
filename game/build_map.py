#!/usr/bin/env python3
"""Build + validate the MazeQuest Mini level map."""
from collections import deque

W, H = 25, 17
WALL = '#'
g = [[WALL] * W for _ in range(H)]


def hline(y, x1, x2, ch='.'):
    for x in range(x1, x2 + 1):
        g[y][x] = ch


def vline(x, y1, y2, ch='.'):
    for y in range(y1, y2 + 1):
        g[y][x] = ch


def rect(x1, y1, x2, y2, ch='.'):
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            g[y][x] = ch


# ---- South: dock + main trail -------------------------------------------
vline(3, 11, 15)                 # dock trail north
g[15][3] = 'S'                   # START (dock)

# ---- Loop A: Meadow Cache (optional, west) ------------------------------
hline(11, 1, 3)
vline(1, 9, 11)
rect(1, 8, 3, 9)

# ---- Main trail east to the west riverbank ------------------------------
hline(11, 3, 10)
vline(6, 9, 10)                  # dead-end spur north (hides an acorn)
vline(8, 12, 13)                 # dead-end spur south (an honest wrong turn)

# ---- River + banks ------------------------------------------------------
vline(10, 7, 13)                 # west bank
rect(11, 7, 13, 13, '~')         # the river
vline(14, 4, 13)                 # east bank + north corridor
g[8][13] = 'o'                   # rock
g[12][11] = 'o'                  # rock

# ---- Loop B: Old Survey Shed (optional, south-east) ---------------------
hline(13, 14, 19)
rect(17, 11, 19, 13)
g[11][18] = 'C'                  # filing cabinet (solid furniture)

# ---- Permit gate --------------------------------------------------------
g[6][14] = 'G'

# ---- Dam approach, work yard, dam face ----------------------------------
hline(4, 8, 20)                  # approach corridor
hline(5, 8, 10)                  # yard bay 1
hline(5, 12, 14)                 # yard bay 2
hline(5, 16, 16)                 # yard bay 3
hline(3, 8, 16, 'W')             # the cracked dam wall
for sx in (10, 12, 14):
    g[3][sx] = 'w'               # shim slot on the dam face

# ---- Flood + exit -------------------------------------------------------
hline(4, 17, 19, 'F')            # flooded stretch
vline(20, 1, 4)
g[1][20] = 'X'                   # EXIT
g[3][21] = '.'                   # hidden nook

# ---- Signpost -----------------------------------------------------------
g[14][2] = 'P'

# ---- Entities -----------------------------------------------------------
LOGS = [(11, 13), (13, 13), (12, 7)]
LANE = [(11, 10), (12, 10), (13, 10)]
SHIMS = [(8, 5), (13, 5), (16, 5)]
CRATES = [(2, 8), (19, 12), (21, 3)]
ACORNS = [(1, 9), (3, 8), (17, 13), (19, 11), (9, 5), (6, 9)]

SOLID = set('#WwCG')          # blocks movement (G until opened)
WATER = set('~o')


def walkable(x, y, opened_gate=False, dam_fixed=False, logs=frozenset()):
    if not (0 <= x < W and 0 <= y < H):
        return False
    c = g[y][x]
    if c == 'G':
        return opened_gate
    if c == 'F':
        return dam_fixed
    if c == '~':
        return (x, y) in logs
    if c == 'o':
        return False
    return c not in SOLID


def bfs(start, **kw):
    seen = {start}
    q = deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n not in seen and walkable(n[0], n[1], **kw):
                seen.add(n)
                q.append(n)
    return seen


START = (3, 15)

# --- Stage 1: nothing solved ---------------------------------------------
s1 = bfs(START)
print("STAGE 1 (start):", len(s1), "tiles reachable")
for name, pos in [("meadow crate", CRATES[0]), ("signpost-adj", (3, 14)),
                  ("west bank @lane", (10, 10))]:
    assert pos in s1 or g[pos[1]][pos[0]] == 'P', f"{name} unreachable"
    print(f"   ok  {name} {pos}")
assert (14, 10) not in s1, "east bank reachable without the raft!"
print("   ok  east bank correctly blocked by the river")

# --- Stage 2: raft built --------------------------------------------------
s2 = bfs(START, logs=frozenset(LANE))
print("STAGE 2 (raft built):", len(s2), "tiles")
assert (14, 10) in s2 and (18, 12) in s2 and (19, 12) in s2
print("   ok  east bank + survey shed reachable")
assert (14, 5) not in s2, "past the gate without a permit!"
print("   ok  gate correctly blocks the way north")

# --- Stage 3: gate open ---------------------------------------------------
s3 = bfs(START, opened_gate=True, logs=frozenset(LANE))
print("STAGE 3 (gate open):", len(s3), "tiles")
for i, sh in enumerate(SHIMS):
    assert sh in s3, f"shim {i} at {sh} unreachable"
    print(f"   ok  shim {i+1} {sh}")
for sx in (10, 12, 14):
    assert (sx, 4) in s3, "cannot stand below dam slot"
print("   ok  all three dam slots approachable from the yard")
assert (20, 1) not in s3, "exit reachable before the dam is fixed!"
print("   ok  flood correctly blocks the exit")

# --- Stage 4: dam fixed ---------------------------------------------------
s4 = bfs(START, opened_gate=True, dam_fixed=True, logs=frozenset(LANE))
print("STAGE 4 (dam fixed):", len(s4), "tiles")
assert (20, 1) in s4 and CRATES[2] in s4
print("   ok  exit + hidden crate reachable")

# --- Collectibles all reachable, no overlaps ------------------------------
spots = ACORNS + SHIMS + CRATES
assert len(set(spots)) == len(spots), "two pickups share a tile"
for p in spots:
    assert p in s4, f"pickup {p} never reachable"
print("   ok  all", len(spots), "pickups reachable, no overlaps")

# --- Log routing check ----------------------------------------------------
def log_route_ok():
    """Each log must reach its lane slot through open water."""
    water = {(x, y) for y in range(H) for x in range(W) if g[y][x] == '~'}
    routes = {
        (11, 13): [(12, 13), (12, 12), (12, 11), (11, 11), (11, 10)],
        (13, 13): [(13, 12), (13, 11), (13, 10)],
        (12, 7):  [(12, 8), (12, 9), (12, 10)],
    }
    for src, path in routes.items():
        cur = src
        for step in path:
            assert abs(step[0] - cur[0]) + abs(step[1] - cur[1]) == 1, f"non-adjacent {cur}->{step}"
            assert step in water, f"log route hits non-water at {step}"
            cur = step
        assert cur in LANE, f"log from {src} ends at {cur}, not a lane slot"
        print(f"   ok  log {src} -> {cur} in {len(path)} nudges")
    return True

log_route_ok()

# --- Render ---------------------------------------------------------------
for (x, y) in LOGS:   g[y][x] = 'L'
for (x, y) in SHIMS:  g[y][x] = 'm'
for (x, y) in CRATES: g[y][x] = 'k'
for (x, y) in ACORNS: g[y][x] = 'a'

print("\n" + "\n".join("".join(r) for r in g))
print("\nrows =", H, " cols =", W)
print("\nJS literal:")
print("[")
for r in g:
    print('  "' + "".join(r) + '",')
print("]")
