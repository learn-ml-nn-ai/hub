# ML Hub — Design Spec

**Date:** 2026-05-24
**Status:** Approved (pending written-spec review)
**Owner identity:** `mehdisalescale`

## 1. Mission

`ML` is the **superset / umbrella** for everything in this learning-and-building journey across ML, neural networks, and AI. It does **no ML work itself**. Its single job is to **know the whole picture and steer the journey** — it holds the *map*, the *compass*, and the *next step* for a fleet of dedicated child repos.

- **Children do the work** — each child repo owns one slice (`3brown1blue` = learn-from-first-principles curriculum, `nn-zero-to-hero` = Karpathy track, more to come).
- **The hub knows everything** — it carries the master plan, status, and connective tissue.
- **Children are gitignored in the parent** — their contents stay invisible to the hub's git; the hub never tracks their files.

## 2. How the parent stays current (hybrid sync)

The parent must "know everything" without tracking child contents. Two mechanisms combine:

1. **GitHub Project (the spine)** — an org-level Project v2 holds cross-repo work items / epics. Source of truth for *what to do next*.
2. **Snapshot script (the roll-up)** — a local script reads each gitignored child repo and regenerates a `STATUS.md` in the hub. Source of truth for *where things stand right now*.

The hub stitches both into one guiding view.

## 3. GitHub topology

- **Org:** `learn-ml-nn-ai` (already created, empty, owned by `mehdisalescale`).
- **Hub repo:** `learn-ml-nn-ai/hub`. Local working copy stays at `~/ML` (the remote is named `hub`).
- **Identity:** re-pin the hub from `mbaneshi` → `mehdisalescale` (rewrite `~/ML/.sid-identity` + `.envrc`, run `direnv allow`). `mehdisalescale` owns the org, so it can create the repo, transfer children in, and manage the Project.
- **Child repos migrate into the org over time.** `3brown1blue` first — a same-owner transfer (`mehdisalescale/3brown1blue` → `learn-ml-nn-ai/3brown1blue`) via `gh api -X POST /repos/mehdisalescale/3brown1blue/transfer -f new_owner=learn-ml-nn-ai`. Remotes are updated afterward. Migration is **not** a prerequisite for the hub to function.
- **Cross-repo Project:** one org-level Project v2 spanning every repo in the fleet.

## 4. Repo structure — the three co-equal pillars

```
ML/                       # local working copy of learn-ml-nn-ai/hub
├── README.md             # entry point: what the journey is, how to read the hub
├── STATUS.md             # GENERATED compass view — roll-up of every child repo
├── meta/                 # THE MAP
│   └── registry.md       #   table of every child: purpose · account · path · link · status
├── decisions/            # THE COMPASS
│   ├── README.md         #   index of decision records
│   ├── strategy.md       #   master journey narrative / north star
│   └── NNNN-<slug>.md     #   ADR-style decision records
├── operational/          # THE NEXT STEP
│   ├── runbooks/         #   how to set up / run each child repo
│   └── snapshot.py       #   reads children → regenerates STATUS.md
├── docs/superpowers/     # specs + plans (this file lives here)
├── justfile              # `just snapshot`, `just status`
├── .gitignore            # ignores child repo dirs + identity files
└── 3brown1blue/, nn-zero-to-hero/, Resources/   # gitignored
```

Pillar → directory mapping:
- **meta/** = the map — what each child repo is and how it fits the superset goal.
- **decisions/** = the compass — why the journey is shaped this way; ADRs + strategy.
- **operational/** = the next step — runbooks and the snapshot tooling.

## 5. Snapshot mechanism (the only real "software")

`just snapshot` walks each gitignored child directory and, per repo, reads:

- `ROADMAP.md` checkboxes — count `- [x]` vs total → percent complete per phase.
- Last commit — hash, date, subject.
- Current git branch.
- (Optional) open-issue count via `gh`.

It writes `STATUS.md`: one table — repo · phase progress · last activity · link.

**Constraints:**
- Run **manually** to start (YAGNI — no cron, no git hooks yet).
- **Python** over shell (checkbox parsing is cleaner).
- Single-purpose and testable; lives in `operational/`.

## 6. GitHub Project (the spine)

- Org-level **Project v2** under `learn-ml-nn-ai`, with fields for cross-repo epics (e.g. "Finish phase-04 transformers", "Port nanoGPT").
- Work items are filed as **issues in the relevant child repo**, then added to the org Project.
- Hub `README.md` + `STATUS.md` link to the Project URL.
- Created via `gh project create --owner learn-ml-nn-ai`; field tweaks via `gh api graphql`.

## 7. Cleanup folded into the move

- **Delete `ai-lab/`** — dead scaffold (16 empty dirs, `.gitkeep` only); a competing taxonomy to the phase structure already committed in `3brown1blue`.
- **Consolidate `Resources/`** — dissolve the current split-brain (PDFs at top level, notes inside `3brown1blue`). Shared/general reading (e.g. `mml-book`) lives in a **hub-level `Resources/`** under the existing **linked-only policy**: gitignore the binaries, track the markdown notes. Repo-specific resources stay in their own repo.
- **Outer `.gitignore`** grows to ignore each child repo dir explicitly.

## 8. Non-goals (YAGNI)

- No git **submodules** (contradicts the gitignored-children intent).
- No cross-repo **CLI** beyond the `snapshot` script.
- No **cron / scheduled** snapshotting initially.
- No **dashboard UI**.

## 9. Success criteria

1. `~/ML` is pinned to `mehdisalescale` and pushes to `learn-ml-nn-ai/hub`.
2. The three pillars (`meta/`, `decisions/`, `operational/`) exist with real seed content.
3. `just snapshot` regenerates a `STATUS.md` that correctly reports `3brown1blue`'s ROADMAP progress and last activity.
4. An org-level Project exists and is linked from the hub README.
5. `ai-lab/` is gone; `Resources/` has one canonical home; `git status` reads clean.

## 10. Suggested sequencing (for the implementation plan)

1. Re-pin hub identity to `mehdisalescale`; commit this spec.
2. Scaffold the three pillars + README + justfile.
3. Build + test `snapshot.py`; generate first `STATUS.md`.
4. Cleanup: delete `ai-lab/`, consolidate `Resources/`, update `.gitignore`.
5. Create `learn-ml-nn-ai/hub` remote; push.
6. Create the org Project; link it from the hub.
7. (Later, optional) transfer `3brown1blue` into the org; update remotes.
