import os
from app.engine import run_valuation_pipeline
from app.database import engine as db_engine, init_db
import polars as pl

# 1. SETUP: Configuration
CSV_FILE_PATH = "bonds_market_data.csv"
TARGET_TABLE = "bonds"

def run_full_etl():
    """The main entry point for our Hedge Fund Pipeline."""
    
    # Check if the CSV exists before starting (Ingestion Check)
    if not os.path.exists(CSV_FILE_PATH):
        print(f"❌ Error: {CSV_FILE_PATH} not found. Please add the file to the root directory.")
        return

    # --- PHASE 1: intialising the persistence Layer aka our load phase of etl pipeline ---
    print("🛠️  Step 1: Initializing Database Schema...")
    init_db() 

    # --- PHASE 2: Transformation Layer ---
    print(f"🧪 Step 2: Running Valuation Engine on {CSV_FILE_PATH}...")
    try:
        # We run our Polars math. This returns a DataFrame
        df_results = run_valuation_pipeline(CSV_FILE_PATH)
        print(f"✅ Transformation Complete. Calculated {len(df_results)} valuations.")
    except Exception as e:
        print(f"❌ Transformation Failed: {e}")
        return

    # --- PHASE 3: LOAD (Persistence Layer) ---
    print(f"📥 Step 3: Loading results into '{TARGET_TABLE}' table...")
    try:
        # Polars 'write_database' is the high-speed bridge to SQL
        df_results.write_database(
            table_name=TARGET_TABLE,
            connection=db_engine,
            if_table_exists="append"  # Adds new runs to the history
        )
        print("🚀 Success! Data is now persistent in the database.")
    except Exception as e:
        print(f"❌ Database Load Failed: {e}")

if __name__ == "__main__":
    run_full_etl()