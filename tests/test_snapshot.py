from snapshot import PhaseProgress, parse_roadmap


def test_parse_roadmap_empty():
    assert parse_roadmap("") == []


def test_parse_roadmap_counts_per_phase():
    text = (
        "# Roadmap\n\n"
        "## Phase 01 — Math\n\n"
        "- [x] done one\n"
        "- [ ] not yet\n"
        "- [x] done two\n\n"
        "## Phase 02 — NN\n\n"
        "- [ ] a\n"
        "- [ ] b\n"
    )
    phases = parse_roadmap(text)
    assert len(phases) == 2
    assert phases[0] == PhaseProgress(name="Phase 01 — Math", done=2, total=3)
    assert phases[1] == PhaseProgress(name="Phase 02 — NN", done=0, total=2)
