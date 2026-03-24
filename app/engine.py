import polars as pl
from datetime import datetime

def run_valuation_pipeline(df: pl.DataFrame) -> pl.DataFrame:
    """
    The High-Frequency Engine.
    Processes live data from RAM using Polars Lazy mode.
    """
    print("🚀 Spinning up pure Polars engine on live data...")
    
    # This creates a "Plan" instead of doing the math immediately using lazy framing aka a pre made plan of action
    lf = df.lazy()

    # 2. The Polars Bouncer (Filtering)
    # This drops invalid data instantly using C++ speed
    lf = lf.filter(
        (pl.col("clean_price") > 0) & 
        (pl.col("face_value") > 0)
    )

    # 3. Vectorised Math
    # We calculate Market Value for all 50 bonds at once.
    lf = lf.with_columns([
        (pl.col("face_value") * (pl.col("clean_price") / 100.0)).alias("market_value"),
        pl.lit(datetime.now()).alias("valuation_timestamp")
    ])

    # 4. The Execution
    # 'collect()' is the "Go" button that runs the optimized plan.
    return lf.collect()