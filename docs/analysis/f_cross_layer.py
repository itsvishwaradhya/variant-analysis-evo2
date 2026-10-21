"""
Analysis F: cross-layer agreement between the two request validators.

The Next.js route handler validates with Zod; the Modal FastAPI endpoint
validates with Pydantic.  The two schemas are written independently.  This
script joins the two verdict sets produced by
docs/analysis/d_validation_conformance.py and
docs/analysis/e_clinvar_conformance.mjs on the canonical case list and
reports where the two layers disagree.

A disagreement is a defect that a user can trigger from the browser: the
request either passes the first gate and fails the second, or the reverse.

Run:
    evo2-backend/venv/Scripts/python.exe docs/analysis/f_cross_layer.py
"""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
D = json.loads((REPO / "docs/analysis/d_pydantic_cases.json").read_text("utf-8"))
E = json.loads((REPO / "docs/analysis/e_zod_cases.json").read_text("utf-8"))

py = {r["name"]: r for r in D["verdicts"]}
zo = {r["name"]: r for r in E["verdicts"]}
names = [r["name"] for r in D["verdicts"]]

rows = []
for n in names:
    a, b = py[n], zo.get(n)
    if b is None:
        continue
    rows.append({
        "name": n,
        "expect": a["expect"],
        "pydantic": a["got"],
        "zod": b["got"],
        "pydantic_ok": a["ok"],
        "zod_ok": b["ok"],
        "agree": a["got"] == b["got"],
        "both_wrong": (not a["ok"]) and (not b["ok"]),
        "pydantic_detail": a["detail"],
        "zod_detail": b["detail"],
    })

n = len(rows)
agree = sum(r["agree"] for r in rows)
disagree = [r for r in rows if not r["agree"]]
both_wrong = [r for r in rows if r["both_wrong"]]
py_only_wrong = [r for r in rows if not r["pydantic_ok"] and r["zod_ok"]]
zod_only_wrong = [r for r in rows if r["pydantic_ok"] and not r["zod_ok"]]
neither = [r for r in rows if r["pydantic_ok"] and r["zod_ok"]]

print("=" * 78)
print("F.1  Cross-layer agreement (Zod vs Pydantic)")
print("=" * 78)
print(f"cases executed        : {n}")
print(f"layers agree          : {agree}/{n} ({agree/n*100:.1f}%)")
print(f"layers disagree       : {len(disagree)}")
print(f"both layers conform   : {len(neither)}")
print(f"Pydantic only wrong   : {len(py_only_wrong)}")
print(f"Zod only wrong        : {len(zod_only_wrong)}")
print(f"both layers wrong     : {len(both_wrong)}")

print("\ncases where the two layers disagree:")
for r in disagree:
    print(f"  {r['name']:<50} expected {r['expect']:<7} "
          f"pydantic={r['pydantic']:<7} zod={r['zod']}")

print("\ncases where both layers violate the intended contract:")
for r in both_wrong:
    print(f"  {r['name']:<50} expected {r['expect']}")

print("\ncases where the layers agree but both are wrong:")
for r in both_wrong:
    print(f"  {r['name']}")

# Effect of each disagreement on the user-visible outcome
print("\n" + "=" * 78)
print("F.2  User-visible effect of each disagreement")
print("=" * 78)
for r in disagree:
    if r["pydantic"] == "accept" and r["zod"] == "reject":
        effect = ("browser rejects the request with HTTP 400 before the "
                  "scoring endpoint is reached")
    elif r["pydantic"] == "reject" and r["zod"] == "accept":
        effect = ("browser forwards the request, the endpoint answers HTTP 422 "
                  "after the request has already been accepted by the route")
    else:
        effect = "both layers accept, so the request is scored"
    print(f"  {r['name']:<50} {effect}")

out = {
    "cases": n,
    "layers_agree": agree,
    "layers_disagree": len(disagree),
    "both_conform": len(neither),
    "pydantic_only_wrong": len(py_only_wrong),
    "zod_only_wrong": len(zod_only_wrong),
    "both_wrong": len(both_wrong),
    "rows": rows,
}
dest = REPO / "docs/analysis/f_cross_layer.json"
dest.write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"\nwrote {dest}")
