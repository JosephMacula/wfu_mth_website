# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

This repo is a prototyping space for things to add to the Wake Forest University Math Department website (see `README.md`). It has no site code, build system, package manifest, linter, or tests yet, so there are no build/lint/test commands. Add them here once a stack is chosen.

## Files in the working tree

- `Math Department Brochure.pdf` is a reference copy only, not site content. It is gitignored and should not be committed.
- `ctx_count.py` and `context_tracker.md` are local Claude Code status line tooling, not part of the project. They are gitignored. `ctx_count.py` prints the session's context-window token count for the status line, and `context_tracker.md` documents it. Claude Code runs the installed copy at `~/.claude/ctx_count.py`, so after editing the repo copy, run `cp ctx_count.py ~/.claude/ctx_count.py`.
