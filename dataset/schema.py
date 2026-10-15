"""Extraction schema for financial news / insider-trade texts (draft v1).

Rules the golden set follows (put them in the prompt too):
- Use only what is in the text. Missing -> null (or empty list). Never guess a year.
- Brokers/analyst firms go to analyst_action, not to companies.
- Insider-trade numbers go to insider_transactions only, not to key_figures.
- Money in absolute units: "$117.68M" -> 117680000; EPS "(42c)" -> -0.42.
- Person names in "First Middle Last" order ("Cole Matthew Ryan" -> "Matthew Ryan Cole").
- Ticker only if it is written in the text; do not infer it from the company name.
- is_confirmed=true for official statements, including a company's denial of a rumor.
- Target of takeover interest/approach -> sentiment positive for that target.
"""
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EventType(str, Enum):
    earnings = "earnings"
    guidance = "guidance"
    m_and_a = "m_and_a"
    ipo = "ipo"
    offering = "offering"
    dividend = "dividend"
    buyback = "buyback"
    analyst_rating = "analyst_rating"
    insider_trade = "insider_trade"
    executive_change = "executive_change"
    contract = "contract"
    regulatory = "regulatory"          # regulators, FDA, government action, delisting
    other = "other"


class Sentiment(str, Enum):
    # for the subject company; insider buy (P) -> positive, other insider codes -> neutral
    positive = "positive"
    negative = "negative"
    neutral = "neutral"
    mixed = "mixed"


class Language(str, Enum):
    en = "en"
    uk = "uk"
    pl = "pl"
    mixed = "mixed"
    other = "other"


class CompanyRole(str, Enum):
    subject = "subject"            # the company the news is about
    counterparty = "counterparty"  # buyer/target/partner
    other = "other"


class Company(BaseModel):
    name: Optional[str] = Field(None, description="Company name as written; null if only a ticker is given")
    ticker: Optional[str] = Field(None, description="Ticker without exchange prefix, e.g. NVDA")
    role: CompanyRole


class Metric(str, Enum):
    eps = "eps"
    revenue = "revenue"
    price_change = "price_change"
    valuation = "valuation"
    deal_value = "deal_value"
    offering_size = "offering_size"
    dividend_per_share = "dividend_per_share"
    buyback_amount = "buyback_amount"
    other = "other"


class Unit(str, Enum):
    usd = "usd"
    usd_per_share = "usd_per_share"
    percent = "percent"
    shares = "shares"
    other = "other"


class ComparisonBasis(str, Enum):
    consensus = "consensus"
    guidance = "guidance"
    prior_period = "prior_period"


class KeyFigure(BaseModel):
    metric: Metric
    value: float
    unit: Unit
    period: Optional[str] = Field(None, description="Fiscal period if stated, e.g. 'Q2'")
    comparison_value: Optional[float] = None
    comparison_basis: Optional[ComparisonBasis] = None


class TransactionCode(str, Enum):
    P = "P"  # open-market purchase
    S = "S"  # sale
    F = "F"  # tax withholding
    G = "G"  # gift
    M = "M"  # option / RSU exercise or conversion
    A = "A"  # grant
    J = "J"  # other
    other = "other"


class Ownership(str, Enum):
    direct = "direct"
    indirect = "indirect"


class InsiderTransaction(BaseModel):
    person: str
    role: Optional[str] = Field(None, description="e.g. 'CEO, Director', '10% Owner'")
    code: TransactionCode
    date: Optional[str] = Field(None, description="YYYY-MM-DD; null if the year is not in the text")
    shares: float
    price: Optional[float] = Field(None, description="Price per share; null if absent or only a range is given")
    ownership: Optional[Ownership] = None
    under_10b5_1: Optional[bool] = Field(None, description="true/false from the 10b5-1 checkbox or footnote; null if not mentioned")


class AnalystAction(str, Enum):
    initiate = "initiate"
    upgrade = "upgrade"
    downgrade = "downgrade"
    reiterate = "reiterate"
    price_target_change = "price_target_change"


class Analyst(BaseModel):
    firm: str
    action: Optional[AnalystAction] = Field(None, description="null if the text does not say what kind of move it is")
    rating: Optional[str] = None
    price_target: Optional[float] = None


class NewsExtraction(BaseModel):
    event_type: EventType = Field(description="Main event of the text")
    is_confirmed: bool = Field(description="false for rumors, 'said to', 'reportedly', chatter")
    sentiment: Sentiment
    language: Language
    companies: list[Company]
    key_figures: list[KeyFigure] = []
    insider_transactions: list[InsiderTransaction] = []
    analyst_action: Optional[Analyst] = None
