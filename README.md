# MazeQuest Mini — The Dam Auditor

A mini top-down puzzle adventure. You play **Inspector Bertie Castorum**, a
beaver who *files* dams rather than building them — a field auditor for the
fictional Woodland Bureau of Aquatic Infrastructure. Cross a one-level maze,
clear three compliance "puzzles," and get the Central Filing Dam on record.

**Play it:** open [`game/MazeQuest-Mini.html`](game/MazeQuest-Mini.html) directly
in a browser — it's a single self-contained file, no build step, no server.

## Contents

- `docs/MazeQuest_Mini_PRD.md` — the product requirements doc: level design,
  character design, mechanics, UI, and the full customize-screen spec.
- `design/` — the source `.dc.html` artboards for the UI reference mockups
  (Start Menu, Gameplay HUD, Field Desk) and their `canvas.json` layout.
- `game/` — the playable build:
  - `MazeQuest-Mini.html` — the finished, standalone game.
  - `part1_style.html`, `part2_markup.html`, `part3_script.html` — the CSS,
    markup, and JS the standalone file is assembled from.
  - `assemble.py` — concatenates the three parts (+ the base64'd portrait)
    into `MazeQuest-Mini.html`.
  - `build_map.py` — generates and BFS-validates the level's 25x17 tile map
    (reachability at every puzzle stage, log-routing, no skippable gates).
    This is the source of truth for the map layout.
  - `playtest.py` — a Playwright script that drives a full playthrough
    (menu → Field Desk → all three puzzles → exit) and screenshots each step.
  - `bertie.png` — the character portrait used in the game and mockups.

## How it plays

One maze level, "The North Culvert Circuit," with three gated puzzles:

1. **The log raft** — nudge three floating logs into the crossing lane
   (click-select-then-click-water, or just walk into a log to push it).
2. **The permit gate** — find the one correct form among four decoys in the
   Old Survey Shed filing cabinet.
3. **The cracked dam** — collect three shims and plug three leak slots to
   drain the flooded exit trail.

Six acorn stamps and three supply crates (unlocking Field Desk cosmetics) sit
off the critical path. The Field Desk customize screen has 4 hats x 4
implements x 4 pelts; the "Field Notes" panel is generated from a template
that combines each equipped item's trait clause, so all 64 combinations read
as a coherent line without being hand-written.

## Regenerating the standalone build

```
cd game
python3 assemble.py        # rebuilds MazeQuest-Mini.html from the 3 parts
python3 build_map.py       # re-validates/regenerates the map (prints the JS literal)
python3 playtest.py        # full-playthrough smoke test via Playwright
```
