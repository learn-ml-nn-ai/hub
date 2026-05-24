import subprocess

from snapshot import PhaseProgress, RepoStatus, discover_repos, parse_roadmap, read_repo, render_status


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


def test_repostatus_aggregates():
    r = RepoStatus(name="x", phases=[PhaseProgress("p1", 1, 4), PhaseProgress("p2", 1, 1)])
    assert r.done == 2
    assert r.total == 5
    assert r.pct == 40


def test_repostatus_pct_zero_when_empty():
    assert RepoStatus(name="x").pct == 0


def test_render_status_table():
    r = RepoStatus(
        name="demo",
        phases=[PhaseProgress("p", 1, 2)],
        last_commit="abc123 2026-05-20 hello",
        branch="main",
    )
    out = render_status([r], "2026-05-24 10:00 UTC")
    assert "Do not edit by hand" in out
    assert "| demo | 50% (1/2) | abc123 2026-05-20 hello | main |" in out


def _init_repo(path):
    path.mkdir()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.email", "t@t.io"], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.name", "tester"], check=True)


def test_read_repo_reads_roadmap_and_commit(tmp_path):
    repo = tmp_path / "child"
    _init_repo(repo)
    (repo / "ROADMAP.md").write_text("## Phase 01\n\n- [x] a\n- [ ] b\n")
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "initial"], check=True)

    status = read_repo(repo)
    assert status.name == "child"
    assert status.done == 1
    assert status.total == 2
    assert "initial" in status.last_commit


def test_discover_repos_finds_only_git_dirs(tmp_path):
    _init_repo(tmp_path / "a")
    (tmp_path / "b").mkdir()
    found = discover_repos(tmp_path)
    assert [p.name for p in found] == ["a"]


def test_read_repo_handles_no_commits(tmp_path):
    repo = tmp_path / "empty"
    _init_repo(repo)
    status = read_repo(repo)
    assert status.last_commit == "(no commits)"
