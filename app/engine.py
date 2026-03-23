import polars as pl
from datetime import datetime

def run_valuation_pipeline(file_path: str) -> pl.DataFrame:
    """
    The High-Frequency Engine.
    Uses pure Polars LazyFrames for Predicate Pushdown (Filtering) 
    and high-speed vectorized math.
    """
    print("🚀 Spinning up pure Polars engine...")
    
    # 1. Scan the CSV (Lazy Mode - doesn't load into RAM yet)
    lf = pl.scan_csv(file_path)

    # 2. The Polars Bouncer (Predicate Filtering)
    # We drop bad rows instantly using C++ vectorisation
    lf = lf.filter(
        (pl.col("clean_price") > 0) & 
        (pl.col("face_value") > 0) & 
        (pl.col("isin").str.len_chars() == 12)
    )

    # 3. The Math Engine
    lf = lf.with_columns([
        (pl.col("face_value") * (pl.col("clean_price") / 100.0)).alias("market_value"),
        pl.lit(datetime.now()).alias("valuation_timestamp")
    ])

    # 4. Show the blueprint of what Polars is about to do
    print("--- Optimised query plan ---")
    print(lf.explain())

    # 5. Execute the plan and return the clean, calculated DataFrame
    return lf.collect()