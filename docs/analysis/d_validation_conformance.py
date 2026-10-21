"""
Analysis D: request-validation conformance for the backend layer.

Evo2Serve validates every request twice: once with Zod in the Next.js route
handler and once with Pydantic on the Modal FastAPI endpoint.  The two
schemas are written independently and describe the same contract, so a
disagreement between them is a defect that a user can trigger from the
browser.

This script imports the real Pydantic model from evo2-backend/main.py and
executes the canonical case matrix in docs/analysis/validation_cases.json
against it.  The same matrix is executed against the Zod schema by
docs/analysis/e_clinvar_conformance.mjs, and the two verdicts are joined by
docs/analysis/f_cross_layer.py.

Run:
    evo2-backend/venv/Scripts/python.exe docs/analysis/d_validation_conformance.py
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from pydantic import ValidationError

REPO = Path(__file__).resolve().parents[2]
MAIN_PY = REPO / "evo2-backend/main.py"
CASES = REPO / "docs/analysis/validation_cases.json"

# --------------------------------------------------------------------------
# Load the real model without importing the whole Modal app.
# --------------------------------------------------------------------------
spec = importlib.util.spec_from_file_location("evo2_main", MAIN_PY)
mod = importlib.util.module_from_spec(spec)
sys.modules["evo2_main"] = mod
spec.loader.exec_module(mod)
VariantRequest = mod.VariantRequest

spec_json = json.loads(CASES.read_text(encoding="utf-8"))
base = spec_json["base"]
cases = spec_json["cases"]


def expand(value):
    """Expand a {"$repeat": {...}} placeholder into a literal string."""
    if isinstance(value, dict) and "$repeat" in value:
        r = value["$repeat"]
        return r.get("char", "A") * int(r.get("count", 0)) + r.get("suffix", "")
    return value


results = []
for c in cases:
    payload = {**base, **{k: expand(v) for k, v in c["payload"].items()}}
    try:
        VariantRequest(**payload)
        got = "accept"
        detail = ""
    except ValidationError as exc:
        got = "reject"
        detail = "; ".join(e["msg"] for e in exc.errors()[:2])
    results.append({
        "name": c["name"],
        "expect": c["expect"],
        "got": got,
        "ok": got == c["expect"],
        "detail": detail,
        "payload": payload,
    })

n = len(results)
ok = sum(r["ok"] for r in results)
by = {}
for r in results:
    by[f"{r['expect']}/{r['got']}"] = by.get(f"{r['expect']}/{r['got']}", 0) + 1

print("=" * 78)
print("D.1  Pydantic validation matrix (evo2-backend/main.py)")
print("=" * 78)
print(f"cases executed : {n}")
print(f"conforming    : {ok}/{n}")
for k in sorted(by):
    print(f"  expected/got {k}: {by[k]}")
print("\nnon-conforming cases:")
for r in results:
    if not r["ok"]:
        print(f"  {r['name']:<48} expected {r['expect']}, got {r['got']}")

out = {
    "layer": "pydantic",
    "cases": n,
    "conforming": ok,
    "verdicts": results,
}
dest = REPO / "docs/analysis/d_pydantic_cases.json"
dest.write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"\nwrote {dest}")
