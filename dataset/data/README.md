# Data

44 financial news and insider-trade texts (US markets plus a few non-US companies, mostly Sep–Oct 2026) for extracting structured JSON. The schema is in `../schema.py`.

## Contents

| File | Count | Source |
|---|---|---|
| `raw/press_releases.jsonl` | 11 | GlobeNewswire / PR Newswire (`sources/press_release_urls.csv`): earnings, guidance, M&A, dividend, buyback, offering, FDA, CEO change, contract, delisting |
| `raw/form4.jsonl` | 10 | SEC EDGAR, Form 4, exact text of the sec.gov pages |
| `raw/headlines.jsonl` | 18 | StreetInsider, TheFly/TipRanks, Investing.com, Reuters reprints: 14 rumors, 2 analyst moves, 2 other news items. Headline plus 1–2 sentences only |
| `raw/synthetic.jsonl` | 5 | Hand-made "messed up" versions of real items (field `based_on`): UA/PL/mixed languages, typos, CAPS. Facts come only from the original |
| `texts.jsonl` | 44 | Model input: everything from `raw/` after cleaning |
| `golden/golden.jsonl` | 17 | Hand labelling |

## Pipeline

```bash
python scripts/fetch_sources.py     # downloads press releases + Form 4 -> data/raw/
python scripts/build_dataset.py     # raw -> clean -> data/texts.jsonl
python scripts/build_golden.py      # golden labels -> data/golden/golden.jsonl (validated by the schema)
```

`raw/` stays exactly as downloaded. `clean_texts.py` removes only site artifacts:

- `Â` garbage from a wrong encoding;
- PR Newswire widgets ("Continue Reading", "Request a Demo");
- hidden e-mails;
- the standard SEC legal footer.

Flattened tables, CAPS, legal text and typos are kept on purpose.

## Golden set (17)

| Type | ids |
|---|---|
| press releases | pr_01 (earnings), pr_03 (M&A), pr_04 (dividend), pr_05 (buyback) |
| Form 4 | f4_01 (P), f4_09 (S that is really a tax withholding + G), f4_10 (F) |
| rumors / news | hl_01, hl_05, hl_07, hl_08, hl_10, hl_12 (denial), hl_16 |
| synthetic | syn_01 (UA, 2 events), syn_02 (PL), syn_05 (UA, no year in dates) |

## How to score

- **Single fields** (`event_type`, `is_confirmed`, `sentiment`, `language`): exact match.
- **`companies`:** match by ticker, or by name when the ticker is null. Report precision and recall.
- **`insider_transactions`:** match by (`code`, `shares`), then check `date`, `price`, `ownership` and `under_10b5_1`.
- **`key_figures`:** the golden set lists the **must-have** figures, so count recall by (`metric`, `value` ±1%). Long releases contain many numbers (premiums, guidance, cash flow), and extra numbers are not counted as errors.
- **`analyst_action`:** compare `firm`, `action` and `price_target`.

## Notes

- **Insider names** in Form 4 are public regulatory data (SEC filings).
- **Headlines** keep only the headline and a short teaser, never the full article.
- **Truncated texts:** pr_01, pr_03, pr_07 and pr_11 are cut at 9000 characters (`truncated` in notes).
- **Hard cases** for the error analysis:
  - f4_09: a sale coded S that the footnote calls a tax withholding;
  - f4_07: a fractional share amount;
  - syn_05: dates without a year;
  - hl_16: no ticker in the text (MAT must not be made up);
  - pr_01: GAAP and non-GAAP EPS in the same text.
