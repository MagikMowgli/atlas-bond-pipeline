import asyncio
import os
from app.extract import run_network_extract 
from app.engine import run_valuation_pipeline 
from app.database import engine as db_engine, init_db
import polars as pl

# 1. SETUP: Configuration (The "Universe")
TICKERS_TO_PULL = ["AAPL_CORP", "TSLA_CORP", "MSFT_CORP", "GOOG_CORP"]
TARGET_TABLE = "bonds"

async def run_full_etl():
    """The Asynchronous Entry Point for the Atlas Pipeline."""
    
    # --- PHASE 0: Init Persistence Layer ---
    print("🛠️  Step 1: Initializing Database Schema...")
    init_db() 

    # --- PHASE 1: EXTRACT (Network Layer) ---
    print(f"📡 Step 2: Requesting {len(TICKERS_TO_PULL)} tickers via Asyncio...")
    try:
        # We 'await' the result here. The CPU is free to do other things during the wait.
        raw_df = await run_network_extract(TICKERS_TO_PULL)
        print(f"✅ Extraction Complete. Pulled {len(raw_df)} bonds from API.")
    except Exception as e:
        print(f"❌ Extraction Failed: {e}")
        return

    # --- PHASE 2: TRANSFORM (Engine Layer) ---
    print("🧪 Step 3: Running Valuation Engine in RAM...")
    try:
        # NOTICE: We pass the 'raw_df' directly, NOT a file path!
        df_results = run_valuation_pipeline(raw_df)
        print(f"✅ Transformation Complete. Calculated {len(df_results)} valuations.")
    except Exception as e:
        print(f"❌ Transformation Failed: {e}")
        return

    # --- PHASE 3: LOAD (Persistence Layer) ---
    print(f"📥 Step 4: Loading results into '{TARGET_TABLE}'...")
    try:
        df_results.write_database(
            table_name=TARGET_TABLE,
            connection=db_engine,
            if_table_exists="append"
        )
        print("🚀 Success! Data is now persistent in Postgres.")
    except Exception as e:
        print(f"❌ Database Load Failed: {e}")

if __name__ == "__main__":
    # We use the asyncio runner to turn on the Event Loop
    asyncio.run(run_full_etl())