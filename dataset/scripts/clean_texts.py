"""Remove scraping artifacts from raw texts. Raw files stay untouched; cleaning happens in build_dataset.py.

Only site junk is removed. Real "dirt" (tables flattened to text, caps, legal boilerplate,
typos in synthetic texts) is kept on purpose: that is what the model has to cope with.
"""
import re

RULES = [
    # wrong decoding of non-breaking spaces on sec.gov pages: "Â\xa0" / "Â "
    (re.compile("Â[  ]"), " "),
    (re.compile("Â"), ""),
    # PR Newswire page widgets
    (re.compile(r"\n?\d+\s*\n%\s*\nmore press release views with\s*\nRequest a Demo\s*$"), ""),
    (re.compile(r"^Continue Reading$\n?", re.M), ""),
    # Cloudflare-hidden e-mails on PR Newswire
    (re.compile(r"\[email\s*protected\]"), "[email]"),
    # SEC form legal footer (identical in every Form 4, carries no data)
    (re.compile(r"\nReminder: Report on a separate line.*$", re.S), ""),
]


def clean(text: str) -> str:
    for pattern, repl in RULES:
        text = pattern.sub(repl, text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


if __name__ == "__main__":
    sample = ("Â Â | Â Â | Check this box\nContinue Reading\nInvestors\n[email protected]\n"
              "SOURCE MongoDB, Inc.\n21\n%\nmore press release views with\nRequest a Demo")
    print(clean(sample))
