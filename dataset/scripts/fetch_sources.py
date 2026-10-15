"""Download source texts that could not be collected verbatim in the cloud session.

Run locally:
    pip install requests beautifulsoup4
    export SEC_USER_AGENT="Your Name your@email"   # SEC requires a contact in User-Agent
    python scripts/fetch_sources.py               # press releases + verbatim Form 4
    python scripts/fetch_sources.py --only pr     # only press releases
    python scripts/fetch_sources.py --only form4  # only re-download Form 4

Writes:
    data/raw/press_releases.jsonl
    data/raw/form4.jsonl (text replaced by the exact sec.gov text, verbatim=true)
"""
import argparse
import csv
import json
import os
import re
import sys
import time
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
URLS = ROOT / "data" / "sources" / "press_release_urls.csv"
HTML_DIR = ROOT / "data" / "sources" / "html"
MAX_CHARS = 9000

BROWSER_UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

# CSS selectors for the release body on each wire site, tried in order
BODY_SELECTORS = [
    "div[itemprop='articleBody']",       # GlobeNewswire
    "div.main-body-container",            # GlobeNewswire (alt)
    "section.release-body",               # PR Newswire
    "div.release-body",                   # PR Newswire (alt)
    "div.bw-release-story",               # Business Wire
    "article",
]


def get(url: str, ua: str) -> str:
    r = requests.get(url, headers={"User-Agent": ua}, timeout=30)
    r.raise_for_status()
    r.encoding = "utf-8"  # sec.gov sends no charset -> requests falls back to latin-1 ("Â" garbage)
    return r.text


def html_to_text(node) -> str:
    # keep table rows on one line, cells separated by " | "
    for tr in node.find_all("tr"):
        cells = [c.get_text(" ", strip=True) for c in tr.find_all(["td", "th"])]
        tr.replace_with(" | ".join(cells) + "\n")
    text = node.get_text("\n", strip=True)
    return re.sub(r"\n{3,}", "\n\n", text)


def fetch_press_releases() -> None:
    out = []
    with URLS.open() as f:
        for row in csv.DictReader(f):
            try:
                # pages saved from a browser (for sites that block scripts) take priority
                local = HTML_DIR / f"{row['id']}.html"
                html = local.read_text(encoding="utf-8", errors="replace") if local.exists() \
                    else get(row["url"], BROWSER_UA)
                soup = BeautifulSoup(html, "html.parser")
                title = soup.find("h1").get_text(" ", strip=True) if soup.find("h1") else ""
                body = next((soup.select_one(s) for s in BODY_SELECTORS if soup.select_one(s)), None)
                if body is None:
                    raise ValueError("release body not found")
                text = html_to_text(body)
                truncated = len(text) > MAX_CHARS
                if truncated:
                    text = text[:MAX_CHARS].rsplit("\n", 1)[0]
                out.append({
                    "id": row["id"], "source_type": "press_release", "source_name": row["wire"],
                    "url": row["url"], "retrieved_at": date.today().isoformat(),
                    "title": title, "text": f"{title}\n\n{text}" if title else text,
                    "notes": f"event: {row['event_type']}; tickers: {row['ticker'] or 'n/a'}"
                             + ("; truncated" if truncated else ""),
                    "verbatim": True,
                })
                print(f"ok   {row['id']}  {len(text):>6} chars  {title[:70]}")
            except Exception as e:  # keep going, report at the end
                print(f"FAIL {row['id']}  {e}", file=sys.stderr)
            time.sleep(1)
    (RAW / "press_releases.jsonl").write_text(
        "".join(json.dumps(d, ensure_ascii=False) + "\n" for d in out), encoding="utf-8")
    print(f"saved {len(out)} press releases -> data/raw/press_releases.jsonl")


def fetch_form4() -> None:
    ua = os.environ.get("SEC_USER_AGENT")
    if not ua:
        sys.exit("Set SEC_USER_AGENT='Your Name your@email' (SEC rejects requests without it)")
    path = RAW / "form4.jsonl"
    rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    for d in rows:
        try:
            soup = BeautifulSoup(get(d["url"], ua), "html.parser")
            d["text"] = html_to_text(soup.body or soup)
            d["verbatim"] = True
            d["paraphrased_footnotes"] = 0
            d["notes"] = d.get("notes", "").split(" Footnotes longer than")[0]  # drop stale paraphrase note
            print(f"ok   {d['id']}  {len(d['text'])} chars")
        except Exception as e:
            print(f"FAIL {d['id']}  {e} (kept previous text)", file=sys.stderr)
        time.sleep(0.5)  # SEC limit is 10 req/s
    path.write_text("".join(json.dumps(d, ensure_ascii=False) + "\n" for d in rows), encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["pr", "form4"])
    a = ap.parse_args()
    if a.only in (None, "pr"):
        fetch_press_releases()
    if a.only in (None, "form4"):
        fetch_form4()
    print("next: python scripts/build_dataset.py")
