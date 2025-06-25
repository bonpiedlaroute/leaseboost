from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime


class MarketComparable(BaseModel):
    address: str
    distance_km: float
    price_per_sqm: float
    transaction_date: str
    surface: float
    similarity_score: float

class MarketPosition(BaseModel):
    percentile_position: str
    market_median_price: str
    your_estimated_price: str
    immediate_opportunity: str
    confidence_level: str
    comparable_count: int
    comparables: List[MarketComparable]

class LegalAlert(BaseModel):
    severity: str # 'HIGH', 'MEDIUM', 'LOW'
    type: str
    description: str
    legal_reference: str
    action_required: str
    deadline: Optional[str] = None
    financial_impact: Optional[str] = None    


class CriticalDeadline(BaseModel):
    type: str
    date: str
    days_remaining: int
    urgency: str
    action_required: str
    potential_loss:str

class Opportunity(BaseModel):
    type: str
    description: str
    impact: str
    recommendation: str
    confidence: str
    legal_basis: Optional[str] = None
    comparables_count: Optional[int] = None

class FinancialMetrics(BaseModel):
    annual_rent: str
    operational_charges: str
    potential_savings: str
    optimized_rent: str
    market_position: Optional[str] = None

class LeaseAnalysisResponse(BaseModel):
    # 1/ market benchmark functionality
    market_intelligence: MarketPosition
    # 2/ legal alerts
    legal_alerts: List[LegalAlert]
    critical_deadlines: List[CriticalDeadline]

    # 3/ opportunities
    opportunities: List[Opportunity]
    financial_metrics: FinancialMetrics

    # summary
    executive_summary: str
    analysis_confidence: str


