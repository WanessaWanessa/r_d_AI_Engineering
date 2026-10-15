"""Merge data/raw/*.jsonl into data/texts.jsonl (the input set for extraction runs).

Texts are passed through clean_texts.clean() to drop scraping artifacts.
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clean_texts import clean

DATA = Path(__file__).resolve().parent.parent / "data"
RAW = DATA / "raw"
ORDER = ["press_releases", "form4", "headlines", "synthetic"]

rows = []
for name in ORDER:
    p = RAW / f"{name}.jsonl"
    if not p.exists():
        print(f"skip {p.name} (not downloaded yet: python scripts/fetch_sources.py)")
        continue
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip():
            d = json.loads(line)
            row = {k: d.get(k) for k in ["id", "source_type", "source_name", "url", "verbatim"]}
            row["text"] = clean(d["text"])
            rows.append(row)

ids = [r["id"] for r in rows]
dupes = [i for i, c in Counter(ids).items() if c > 1]
if dupes:
    sys.exit(f"duplicate ids: {dupes}")

out = DATA / "texts.jsonl"
out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")

golden = {json.loads(l)["id"] for l in (DATA / "golden" / "golden.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
missing = golden - set(ids)
lengths = sorted(len(r["text"]) for r in rows)
print(f"{len(rows)} texts -> {out}")
print("by type:", dict(Counter(r["source_type"] for r in rows)))
print(f"length chars: min {lengths[0]}, median {lengths[len(lengths)//2]}, max {lengths[-1]}")
print(f"golden: {len(golden)} ids, missing from texts: {missing or 'none'}")
