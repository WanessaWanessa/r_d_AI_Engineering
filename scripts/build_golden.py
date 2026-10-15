"""Draft golden labels (to be reviewed by hand). Validates each against schema.NewsExtraction."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from schema import NewsExtraction

G = {
"hl_01": dict(event_type="m_and_a", is_confirmed=False, sentiment="neutral", language="en",
    companies=[dict(name="Starbucks", ticker="SBUX", role="subject"),
               dict(name="Chipotle Mexican Grill", ticker="CMG", role="counterparty")]),
"hl_05": dict(event_type="analyst_rating", is_confirmed=True, sentiment="positive", language="en",
    companies=[dict(name="Nvidia", ticker="NVDA", role="subject")],
    analyst_action=dict(firm="Citi", action="reiterate", rating="Buy", price_target=315.0)),
"hl_07": dict(event_type="earnings", is_confirmed=True, sentiment="positive", language="en",
    companies=[dict(name="FireFly Aerospace", ticker=None, role="subject")],
    key_figures=[dict(metric="eps", value=-0.42, unit="usd_per_share", period="Q2", comparison_value=-0.57, comparison_basis="consensus"),
                 dict(metric="revenue", value=117680000, unit="usd", period="Q2", comparison_value=88520000, comparison_basis="consensus")]),
"hl_08": dict(event_type="regulatory", is_confirmed=True, sentiment="negative", language="en",
    companies=[dict(name="Fair Isaac Corporation", ticker="FICO", role="subject")],
    key_figures=[dict(metric="price_change", value=-8.0, unit="percent")]),
"f4_01": dict(event_type="insider_trade", is_confirmed=True, sentiment="positive", language="en",
    companies=[dict(name="Ellsworth Growth & Income Fund Ltd", ticker="ECF", role="subject")],
    insider_transactions=[dict(person="Saba Capital Management, L.P.", role="10% Owner", code="P", date="2026-10-12",
        shares=14600, price=12.03, ownership="indirect", under_10b5_1=False)]),
"f4_09": dict(event_type="insider_trade", is_confirmed=True, sentiment="neutral", language="en",
    companies=[dict(name="Strive, Inc.", ticker="ASST", role="subject")],
    insider_transactions=[
        dict(person="Matthew Ryan Cole", role="CEO, Director", code="S", date="2026-10-05", shares=58789, price=31.3343, ownership="direct", under_10b5_1=False),
        dict(person="Matthew Ryan Cole", role="CEO, Director", code="G", date="2026-10-05", shares=81783, price=None, ownership="direct", under_10b5_1=False)]),
"f4_10": dict(event_type="insider_trade", is_confirmed=True, sentiment="neutral", language="en",
    companies=[dict(name="NVIDIA Corp", ticker="NVDA", role="subject")],
    insider_transactions=[dict(person="Scott Gawel", role="Principal Accounting Officer", code="F", date="2026-09-16",
        shares=2932, price=212.17, ownership="direct", under_10b5_1=False)]),
"hl_10": dict(event_type="m_and_a", is_confirmed=False, sentiment="neutral", language="en",
    companies=[dict(name="AAR Corp", ticker="AIR", role="subject"),
               dict(name="MRO Holdings", ticker=None, role="counterparty")],
    key_figures=[dict(metric="deal_value", value=1800000000, unit="usd"),
                 dict(metric="other", value=65.0, unit="percent")]),
"hl_12": dict(event_type="m_and_a", is_confirmed=True, sentiment="neutral", language="en",
    companies=[dict(name="Nu Holdings", ticker=None, role="subject"),
               dict(name="Monzo", ticker=None, role="counterparty")]),
"hl_16": dict(event_type="m_and_a", is_confirmed=False, sentiment="positive", language="en",
    companies=[dict(name="Mattel", ticker=None, role="subject"),
               dict(name="Authentic Brands Group", ticker=None, role="counterparty")],
    key_figures=[dict(metric="valuation", value=6000000000, unit="usd")]),
"pr_01": dict(event_type="earnings", is_confirmed=True, sentiment="positive", language="en",
    companies=[dict(name="Synopsys, Inc.", ticker="SNPS", role="subject")],
    key_figures=[dict(metric="revenue", value=2477000000, unit="usd", period="Q3 FY2026", comparison_value=1740000000, comparison_basis="prior_period"),
                 dict(metric="eps", value=2.84, unit="usd_per_share", period="Q3 FY2026", comparison_value=1.50, comparison_basis="prior_period"),
                 dict(metric="eps", value=3.91, unit="usd_per_share", period="Q3 FY2026", comparison_value=3.39, comparison_basis="prior_period")]),
"pr_03": dict(event_type="m_and_a", is_confirmed=True, sentiment="positive", language="en",
    companies=[dict(name="MISTRAS Group, Inc.", ticker="MG", role="subject"),
               dict(name="H.I.G. Capital", ticker=None, role="counterparty")],
    key_figures=[dict(metric="deal_value", value=866000000, unit="usd"),
                 dict(metric="other", value=20.35, unit="usd_per_share")]),
"pr_04": dict(event_type="dividend", is_confirmed=True, sentiment="neutral", language="en",
    companies=[dict(name="ONEOK, Inc.", ticker="OKE", role="subject")],
    key_figures=[dict(metric="dividend_per_share", value=1.07, unit="usd_per_share", comparison_value=1.07, comparison_basis="prior_period")]),
"pr_05": dict(event_type="buyback", is_confirmed=True, sentiment="positive", language="en",
    companies=[dict(name="Ollie's Bargain Outlet Holdings, Inc.", ticker="OLLI", role="subject")],
    key_figures=[dict(metric="buyback_amount", value=500000000, unit="usd")]),
"syn_01": dict(event_type="earnings", is_confirmed=True, sentiment="mixed", language="uk",
    companies=[dict(name=None, ticker="FLY", role="subject")],
    key_figures=[dict(metric="eps", value=-0.42, unit="usd_per_share", period="Q2", comparison_value=-0.57, comparison_basis="consensus"),
                 dict(metric="revenue", value=117680000, unit="usd", period="Q2", comparison_value=88520000, comparison_basis="consensus")],
    analyst_action=dict(firm="Barclays", action=None, rating="Equal Weight", price_target=34.0)),
"syn_02": dict(event_type="regulatory", is_confirmed=True, sentiment="negative", language="pl",
    companies=[dict(name="FICO", ticker="FICO", role="subject")],
    key_figures=[dict(metric="price_change", value=-8.0, unit="percent")]),
"syn_05": dict(event_type="insider_trade", is_confirmed=True, sentiment="neutral", language="uk",
    companies=[dict(name=None, ticker="NVDA", role="subject")],
    insider_transactions=[
        dict(person="Colette Kress", role="CFO", code="S", date=None, shares=34900, price=None, ownership=None, under_10b5_1=True),
        dict(person="Colette Kress", role="CFO", code="F", date=None, shares=40747, price=None, ownership=None, under_10b5_1=None)]),
}
# ids checked by hand against the verbatim texts (2026-10-15); new labels stay reviewed=false until checked
REVIEWED = {"hl_01", "hl_05", "hl_07", "hl_08", "hl_10", "hl_12", "hl_16", "f4_01", "f4_09", "f4_10",
            "syn_01", "syn_02", "syn_05", "pr_01", "pr_03", "pr_04", "pr_05"}
out = Path(__file__).resolve().parent.parent / "data" / "golden" / "golden.jsonl"
with out.open("w", encoding="utf-8") as f:
    for i, g in G.items():
        m = NewsExtraction.model_validate(g)
        f.write(json.dumps({"id": i, "expected": m.model_dump(mode="json"), "reviewed": i in REVIEWED}, ensure_ascii=False) + "\n")
print(f"{len(G)} golden records valid -> {out}")
