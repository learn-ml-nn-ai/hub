# Runbook — `3brown1blue`

**What:** the from-first-principles ML curriculum (phases 01–06).

## Setup (first clone)

```bash
cd ~/ML/3brown1blue
direnv allow .
uv sync --all-packages
```

## Daily use

- Pick the next unchecked item in `ROADMAP.md`.
- Work inside the relevant `phase-NN-*/projects/NN-<slug>/`.
- Phase progress is rolled up into the hub's `STATUS.md` via `just snapshot`.
