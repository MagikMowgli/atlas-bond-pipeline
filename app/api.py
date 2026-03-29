from datetime import datetime
from app.schemas import BondResponse, PortfolioSummary, BondCreate
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, BondTable

app = FastAPI(title="Atlas Trade API")

def get_db():
    # This connects us to the postgres database
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/portfolio", response_model=PortfolioSummary)
def read_all_portfolio(db: Session = Depends(get_db)) -> PortfolioSummary:
    all_bonds = db.query(BondTable).all()

    total_val = sum(bond.market_value for bond in all_bonds)

    return {
        "total_market_value": total_val,
        "bond_count": len(all_bonds),
        "bonds": all_bonds
    }

@app.get("/portfolio/{ticker}", response_model=BondResponse)
def read_bond_by_ticker(ticker: str, db: Session = Depends(get_db)) -> BondResponse:
    """Endpoint to retrieve a bond by its ticker."""
    bond = db.query(BondTable).filter(BondTable.ticker == ticker).first()

    if not bond:
        raise HTTPException(status_code=404, detail=f"Bond with ticker {ticker} not found")
    return bond

@app.post("/portfolio/trade", response_model=BondResponse)
def create_trade(bond_data: BondCreate, db: Session = Depends(get_db)):
    new_bond_row = BondTable(
        isin=bond_data.isin,
        ticker=bond_data.ticker,
        face_value=bond_data.face_value,
        clean_price=bond_data.clean_price,
        market_value=bond_data.face_value * (bond_data.clean_price / 100.0),
        currency="USD",
        valuation_timestamp=datetime.now()
    )

    db.add(new_bond_row)
    db.commit()
    db.refresh(new_bond_row)
    
    return new_bond_row
