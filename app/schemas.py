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