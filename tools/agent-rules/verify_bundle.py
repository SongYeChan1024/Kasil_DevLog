"""CI check independent of machine-local installation state. Author: 송예찬."""
from pathlib import Path
from rules_core import PROJECT_FILES, SOURCE, render_project
import runtime

root = Path(__file__).resolve().parents[2]
existing = {name: (root / name).read_bytes() if (root / name).is_file() else None for name in PROJECT_FILES}
# GitHub Actions may use a different checkout folder name.
desired = render_project(root.parent / "Kasil_DevLog", SOURCE.read_bytes(), existing)
bad = [name for name, content in desired.items() if existing.get(name) != content]
bad += runtime.static_checks(root, list(desired))
if bad:
    raise SystemExit("Generated bundle mismatch: " + ", ".join(bad))
print(f"PASS: {len(desired)} generated files match RULES.md and the shared runtime.")
