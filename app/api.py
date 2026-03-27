from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal, BondTable

app = FastAPI(title="Atlas Trade API")

def get_db():
    # This connects us to the postgres database
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/portfolio")
def read_all_bonds(db: Session = Depends(get_db)):
    """Endpoint to retrieve all bonds in the portfolio."""
    bonds = db.query(BondTable).all()
    return bonds

@app.get("/portfolio/{ticker}")
def read_bond_by_ticker(ticker: str, db: Session = Depends(get_db)):
    """Endpoint to retrieve a bond by its ticker."""
    bond = db.query(BondTable).filter(BondTable.ticker == ticker).first()

    if not bond:
        raise HTTPException(status_code=404, detail=f"Bond with ticker {ticker} not found")
    return bond