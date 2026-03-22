from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

# Model for a bondposition (struct)
class Bondposition(BaseModel):
    isin: str = Field(..., min_length=12, max_length=12)
    ticker: str
    currency: str 

    face_value: float = Field(..., gt=0)
    clean_price: float = Field(..., gt=0)

    timestamp: datetime = Field(default_factory=datetime.now)

    @validator('currency')
    def currency_must_be_uppercase(cls,v):
        return v.upper()

# Model for the market data (fx rates struct)
class MarketState(BaseModel):
    currency: str
    fx_rate_to_usd: float