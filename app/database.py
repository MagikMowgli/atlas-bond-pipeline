from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
# creates the physical connection to the database but not yet calling the db
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("CRITICAL ERROR: DATABASE_URL not found in environment!")

# this connects our python code to the sql database aka postgres
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# import to create sessions before we add to our database to keep things neat and orderly
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# allows us to model against a modelled pre written table
Base = declarative_base()

# builds the blueprint to the table we want
class BondTable(Base):
    __tablename__ = "bonds"

    id = Column(Integer, primary_key=True, index=True)
    isin = Column(String, index=True)
    ticker = Column(String)
    currency = Column(String)
    face_value = Column(Float)
    clean_price = Column(Float)
    market_value = Column(Float)
    valuation_timestamp = Column(DateTime)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# the "Builder" Function essnetially builds the db in psql
def init_db():
    Base.metadata.create_all(bind=engine)