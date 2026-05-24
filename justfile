# ML Hub tasks

# Regenerate STATUS.md from all child repos
snapshot:
    uv run python operational/snapshot.py

# Print the current STATUS.md
status:
    cat STATUS.md
