from pydantic import BaseModel
from datetime import datetime

class BondResponse(BaseModel):
    isin: str
    ticker: str
    face_value: float
    clean_price: float
    market_value: float
    valuation_timestamp: datetime

    class Config:
        from_attributes = True # This is the "bridge" between SQLAlchemy and Pydantic

class PortfolioSummary(BaseModel):
    total_market_value: float
    bond_count: int
    bonds: list[BondResponse]

class BondCreate(BaseModel):
    isin: str
    ticker: str
    face_value: float
    clean_price: float
    currency: str = "USD"