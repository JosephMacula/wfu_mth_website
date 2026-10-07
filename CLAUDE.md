# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

This repo is a prototyping space for things to add to the Wake Forest University Math Department website (see `README.md`). There is no site code, linter, or test suite yet.

## Narrated flowchart animations (`animations/`)

Manim animations of the course flowcharts on page 2 of the brochure, narrated with `manim-voiceover` using gTTS. gTTS needs network access the first time each line is spoken; the audio is then cached under `media/`.

Setup (system packages: `ffmpeg libcairo2-dev libpango1.0-dev pkg-config sox`):

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

Render from inside `animations/`, because `flowcharts.py` imports its sibling `course_graphs.py`:

```bash
cd animations
../.venv/bin/manim -ql flowcharts.py CalculusSequence     # 480p preview; -qh for 1080p
../.venv/bin/manim -ql flowcharts.py FoundationalCourses
```

Output goes to `animations/media/videos/flowcharts/<quality>/`, with an `.mp4`, a `.srt` subtitle file, and a `.wav`.

- `course_graphs.py` holds the data. Each chart is a `CourseGraph` of courses and directed edges, where an edge `(a, b)` means course b can be taken after course a. It is deliberately not modeled as a strict prerequisite graph. Node positions are in manim scene units and follow the brochure's layout.
- `flowcharts.py` holds the rendering. `FlowchartScene` turns a list of `Step`s (narration plus the courses to show, edges to draw, and courses to highlight) into voiceover blocks. Each chart is a subclass that only sets `graph` and `steps`.

## Files in the working tree

- `Math Department Brochure.pdf` is a reference copy only, not site content. It is gitignored and should not be committed.
- `ctx_count.py` and `context_tracker.md` are local Claude Code status line tooling, not part of the project. They are gitignored. `ctx_count.py` prints the session's context-window token count for the status line, and `context_tracker.md` documents it. Claude Code runs the installed copy at `~/.claude/ctx_count.py`, so after editing the repo copy, run `cp ctx_count.py ~/.claude/ctx_count.py`.
