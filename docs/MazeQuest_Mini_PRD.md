# Product Requirements Document

## MazeQuest Mini: The Dam Auditor

**Genre:** Top-down puzzle adventure (single level, mini/short-form)
**Version:** Draft 1.0
**Date:** August 24, 2026
**Project:** CreativeWorkflow

---

## 1. Concept

MazeQuest Mini casts the player as a beaver who works for the Woodland Bureau of Aquatic Infrastructure — not as a builder, but as a **dam auditor**. Where every other beaver in fiction stacks logs, this one carries a clipboard, a rubber stamp, and a deep, weary conviction that most dams are, technically, out of code.

The player steers the auditor through a single maze-like forest-and-river level, filing paperwork on unlicensed dams, prying open jammed gates with the correct permit, and rerouting leaks before they flood the survey route. The tone is dry office-comedy laid over a cozy nature setting: puzzles are framed as compliance problems, and every collectible is some flavor of bureaucratic form.

The reference art (`dabar.png`, supplied by the user) establishes the visual tone: a round, big-toothed beaver in a green Bureau vest and a jaunty cap, styled like a folk-costume mascot. This PRD treats that illustration as the base silhouette for the player character and the starting point for the customization system below.

**One-line pitch:** *A beaver bureaucrat audits a river of illegally-built dams, and you help her file the paperwork.*

---

## 2. Goals & Scope (MVP)

This is a **mini** game — one level, one character, no persistent meta-progression beyond the customize screen. In scope for the MVP:

- One maze level with a clear Start and Exit.
- One controllable character with four-directional movement and wall/obstacle collision.
- At least three distinct puzzles or obstacles.
- Collectibles that reward exploration off the critical path.
- Interactive objects (river logs) that respond to click and/or movement.
- A clickable start menu and in-level UI.
- A character customize screen (four hats, four implements, four pelts) with a dynamically-rewriting "Field Notes / Observed Traits" panel.

Out of scope for the MVP: multiple levels, save/load, enemies or fail states beyond soft puzzle resets, audio implementation (sound design is noted but not specified), and multiplayer.

---

## 3. Character Design

### 3.1 The Player Character

**Name:** Inspector Bertie Castorum (working name — "Bertie" for short)
**Role:** Field Auditor, Woodland Bureau of Aquatic Infrastructure
**Silhouette:** Round-bodied beaver, big flat tail, oversized front teeth, based on the supplied reference art — green vest, sash of rank, soft cap, over-the-top folk-official styling played for laughs against a mundane office job.

Bertie is the single controllable character for the MVP. There are no NPCs to control or swap between; other beavers appear only as scenery or as the subjects of Bertie's audits (e.g., a dam-builder beaver glimpsed through the trees, never directly interactive).

### 3.2 Movement Mechanics

| Input | Action |
|---|---|
| Up / W / ↑ | Move north one step (or continuous, see below) |
| Down / S / ↓ | Move south one step |
| Left / A / ← | Move west one step |
| Right / D / → | Move east one step |
| Click on reachable tile (stretch) | Path Bertie to that tile, stopping at the first obstacle |

- **Movement model:** Grid-based, tile-to-tile movement (recommended for a "maze" level — makes puzzle logic and collision predictable). Each key press or held direction advances Bertie one tile at a fixed step duration (e.g., 150–200ms), with a short walk-cycle animation.
- **Facing:** Bertie always faces the last direction moved; idle animation plays when no input is held.
- **Collision:** Bertie cannot move into tiles flagged as solid (trees, rocks, dam walls, water without a raft bridge, closed gates). A blocked move attempt plays a small "bonk" animation/sound and does not consume a turn-based cost (movement is real-time, not turn-based — the block simply cancels that step).
- **Interaction key/click:** A separate "inspect/use" action (Spacebar, E, or click-on-adjacent-object) lets Bertie pick up collectibles, read signage, and trigger puzzle interactions when standing adjacent to an interactive object.

---

## 4. Level Design — "The North Culvert Circuit"

### 4.1 Layout Overview

One self-contained maze level connecting a **Start** (the Bureau rowboat dock, at the level's south edge) to an **Exit** (the Central Filing Dam, at the level's north edge), via a branching path of forest trail and riverbank tiles. The map reads as a loose figure-eight: a main critical path from Start to Exit, plus two optional loops that hold collectibles and the customization unlocks.

```
 [START: Dock]
      |
 [Trail Fork] ----> [Optional Loop A: Meadow Cache] (collectibles)
      |
 [Puzzle 1: Log Raft Crossing]
      |
 [Riverbank Junction] ----> [Optional Loop B: Old Survey Shed] (collectibles + customization unlock)
      |
 [Puzzle 2: Permit Gate]
      |
 [Puzzle 3: Leaky Dam Reroute]
      |
 [EXIT: Central Filing Dam]
```

- The critical path is short enough to complete in 5–10 minutes; the optional loops roughly double playtime for a completionist run.
- Sightlines are kept short (hedgerows, tree clusters) so the "maze" feeling comes from partial visibility and branching, not from a large grid — appropriate for a mini/short-form title.
- A signpost near Start briefly states the objective in-fiction: *"File the Central Dam by end of day. Shortcuts through the culvert are logged."*

### 4.2 Puzzles / Obstacles (minimum 3)

**Puzzle 1 — Log Raft Crossing (Sokoban-style push puzzle)**
A river gap blocks the main trail. Three loose logs float in a holding pool nearby. The player clicks a log to select it, then clicks an adjacent water tile to nudge it one space (or walks into it to push it, matching the interactive-object behavior in §5.2). The player must arrange the three logs into a contiguous raft bridging the gap, working around one log that's snagged against a rock and can only be pushed sideways. Solved when all three logs form an unbroken path across the water.

**Puzzle 2 — Permit Gate**
A locked gate (a beaver-built barricade, ironically un-permitted) blocks the path to the Central Filing Dam. A posted notice lists a permit code (e.g., *"Form 12-B, Riverside Class"*). The Old Survey Shed loop (optional but effectively required to solve this without trial and error) contains a small filing cabinet with four form collectibles, only one of which matches the posted code — the other three are red herrings with plausible-but-wrong codes. Presenting the correct form at the gate opens it; presenting a wrong one triggers a polite rejection stamp animation and the gate stays shut (no penalty, just retry).

**Puzzle 3 — Leaky Dam Reroute**
Near the Exit, a cracked dam is flooding the last stretch of trail, making it impassable. Three wooden shims are scattered around a small sub-area (visible but requiring minor pathfinding around obstacles). The player collects all three and returns to the dam to plug the leak points (an "insert shim" interaction at three marked slots on the dam face). Once all three slots are filled, the water recedes and the trail to the Exit opens. This puzzle doubles as a light collect-and-return objective layered on top of the maze traversal.

*(Optional stretch puzzle — not required for MVP but noted for future scope: a stamp-sequencing puzzle in the Old Survey Shed, where the player must apply stamps to a form in the correct order shown on a faded reference card, rewarding a hidden customization item.)*

### 4.3 Collectibles

| Collectible | Count | Location | Purpose |
|---|---|---|---|
| Filed Forms | 4 | Old Survey Shed loop | Required for Puzzle 2 (one correct, three decoys); also count toward a completion tally |
| Acorn Stamps (currency/flavor) | 6 | Scattered across both optional loops | Optional collection goal, no gameplay gate — rewards exploration |
| Wooden Shims | 3 | Small sub-area near Exit | Required for Puzzle 3 |
| Customization Unlocks (hat/implement/pelt items) | 3 | One per optional loop + one hidden near the Exit | Unlock new options on the Customize screen (see §6) |

Collectibles use a soft sparkle/glint visual cue and a short pickup animation + UI toast (e.g., "Acquired: Form 12-B") to confirm pickup without interrupting movement flow.

---

## 5. Mechanics & UI

### 5.1 Movement & Collision

- Tile-based solid/passable flags per map tile (trees, rocks, water, gates = solid; grass, dirt trail, completed raft, opened gate = passable).
- Collision is checked before each step is committed; failed moves cancel cleanly with visual/audio feedback rather than partial movement.
- Water tiles are passable only once bridged (Puzzle 1) or never (decorative river elsewhere), so the collision map effectively changes state as puzzles are solved.

### 5.2 Interactive Objects — River Logs

Logs are the primary interactive-object type and appear in Puzzle 1 (and optionally as set dressing elsewhere):

- **Click response:** Clicking a log within the holding pool selects it (highlighted outline); clicking a valid adjacent water tile moves the log there. Clicking an invalid tile (occupied, out of bounds, snagged log's disallowed direction) is a no-op with a small shake animation.
- **Movement response:** Walking directly into a log from a cardinal direction pushes it one tile in that direction, if the destination tile is open water — this lets keyboard-only play solve the puzzle without the mouse.
- Both input methods drive the same underlying "log position" state so the puzzle is solvable via keyboard, mouse, or a mix of both.
- Once three logs form a connected path across the gap, the game auto-detects the solved state, snaps the logs into a fixed "bridge" visual, and updates the collision map to make that path walkable.

### 5.3 Clickable UI

**Start Menu** (first screen on launch):
- **Play** — begins the level at the Dock.
- **Customize** — opens the Customize screen (§6).
- **How to Play** — a single-screen overlay explaining movement, the interact key, and the audit objective.
- **Quit** — exits (or returns to a hosting shell, if embedded).

**In-Level UI (HUD):**
- Objective tracker (top-left): current goal, e.g., "Find a raft crossing" → updates as puzzles resolve.
- Inventory strip (top-right): icons for held Filed Forms and Wooden Shims, so the player can see at a glance what they're carrying into Puzzle 2 / Puzzle 3.
- Collectible tally (bottom-right, small): Acorn Stamps collected / 6.
- Pause button (top corner): opens a simple Pause overlay with Resume, Customize (mid-run, cosmetic-only), How to Play, and Quit to Menu.

**Interaction prompts:** A small contextual icon (e.g., a hand or stamp glyph) appears above interactive objects/NPC signage when Bertie is adjacent, indicating the interact key/click will do something there.

---

## 6. Customize Screen

Framed in-fiction as Bertie's **field desk** — a flat-lay "desktop" of items she can equip before heading out, styled like a cluttered civil-service office drawer rather than a fantasy equipment screen. Three slots: **Hat**, **Implement**, **Pelt**. Each slot cycles through four unlockable options (one is available from the start per slot; the other three are found as Customization Unlocks in the level, per §4.3). Selecting an item shows its **flavor line** immediately; the **Field Notes / Observed Traits** panel at the bottom of the screen rewrites live as any of the three slots change.

### 6.1 Hats

| # | Name | Flavor Line | Trait Clause |
|---|---|---|---|
| 1 *(default)* | Regulation Bureau Cap | "Standard issue felt cap, third generation. Keeps the drizzle off the paperwork." | wearing the standard-issue cap |
| 2 | Novelty Eyeshade | "Green plastic visor, confiscated from a raccoon accountant. Adds real gravitas to spreadsheet review." | wearing a confiscated eyeshade |
| 3 | Woodpecker-Feather Fedora | "Traded for two blank permit forms. The feather has opinions." | sporting a traded fedora |
| 4 | Waterproof Field Hood | "Standard river-crew rain hood. Smells faintly of pond." | hooded against the weather |

### 6.2 Implements

| # | Name | Flavor Line | Trait Clause |
|---|---|---|---|
| 1 *(default)* | Rubber Stamp of Record | "APPROVED / DENIED, dual-sided. Mostly used for the latter." | carrying the dual-sided stamp |
| 2 | Chewed Pencil Stub | "Gnawed to a nub across years of compliance notes." | gripping a well-chewed pencil |
| 3 | Brass Calipers | "For measuring dam width against Bureau Code 14-B, to the millimeter." | armed with brass calipers |
| 4 | Clipboard of Record | "Holds up to forty forms and one (1) standing grudge." | clutching the full clipboard |

### 6.3 Pelts

| # | Name | Flavor Line | Trait Clause |
|---|---|---|---|
| 1 *(default)* | Standard Slick Pelt | "Regulation-approved sheen, per uniform code 3." | maintaining a regulation sheen |
| 2 | Damp Fieldwork Pelt | "Permanently damp. Smells of long pond duty." | still faintly damp from fieldwork |
| 3 | Silver-Streaked Senior Pelt | "Earned after two decades auditing river dams. Commands quiet respect from junior otters." | showing the silver streaks of seniority |
| 4 | Scarred Veteran Pelt | "One nick per contested permit. There have been many." | carrying the scars of contested permits |

### 6.4 Field Notes / Observed Traits (dynamic panel)

The panel is generated from a single template that slots in each equipped item's **Trait Clause** (rightmost column above), so any of the 4×4×4 = 64 combinations produces a coherent one-paragraph "field note" without needing 64 pieces of hand-written text:

> *"Field Notes — Inspector Bertie Castorum was observed [hat trait clause], [implement trait clause], and [pelt trait clause]. Bureau assessment: compliant, if a little theatrical."*

**Worked examples:**

- Default loadout: *"Field Notes — Inspector Bertie Castorum was observed wearing the standard-issue cap, carrying the dual-sided stamp, and maintaining a regulation sheen. Bureau assessment: compliant, if a little theatrical."*
- Novelty Eyeshade + Brass Calipers + Silver-Streaked Senior Pelt: *"Field Notes — Inspector Bertie Castorum was observed wearing a confiscated eyeshade, armed with brass calipers, and showing the silver streaks of seniority. Bureau assessment: compliant, if a little theatrical."*
- Woodpecker-Feather Fedora + Chewed Pencil Stub + Scarred Veteran Pelt: *"Field Notes — Inspector Bertie Castorum was observed sporting a traded fedora, gripping a well-chewed pencil, and carrying the scars of contested permits. Bureau assessment: compliant, if a little theatrical."*

**Implementation note:** the closing "Bureau assessment" line can stay fixed for MVP simplicity, or (stretch scope) be selected from a small pool of 3–4 closing lines keyed to specific item combinations (e.g., any Senior/Veteran pelt swaps in "Bureau assessment: compliant, and mildly intimidating.") — this is a cheap way to add replay charm without hand-authoring all 64 notes.

---

## 7. Success Criteria (MVP "done" definition)

- Player can complete a full loop: Start Menu → Play → navigate the maze → solve all 3 puzzles in any reachable order allowed by the level gating → reach the Exit.
- All four hats, four implements, and four pelts are reachable in a single playthrough (one per slot is default; three per slot are found in-level).
- Field Notes panel correctly reflects all 64 equip combinations with no missing or malformed text.
- No collision or soft-lock states: every puzzle is solvable without external items other than what the level itself provides, and there is no way to strand Bertie in an unreachable area.
- Start Menu, HUD, and Pause menu are fully clickable and keyboard-navigable is a nice-to-have, not required for MVP.

## 8. Open Questions / Stretch Goals

- Should movement be strictly grid-locked, or smoothed/interpolated between tiles for a softer feel? (Recommendation: grid-locked for MVP; revisit if playtesting feels stiff.)
- Should wrong-permit attempts at the Gate have a light comedic penalty (e.g., a stamp of "DENIED" briefly covers the screen) versus a purely neutral no-op?
- Stretch: a second small level ("The South Weir") reusing the same systems, to validate that the puzzle/customize framework generalizes beyond one hand-built map.
- Stretch: simple ambient audio (river burble, stamp thunk, footstep) — not specified in this PRD, flagged for a follow-up audio pass.
