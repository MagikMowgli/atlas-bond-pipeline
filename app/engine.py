import polars as pl
from datetime import datetime

def run_valuation_pipeline(file_path: str):

    lf = pl.scan_csv(file_path)

    lf = lf.with_columns([
        (pl.col("face_value") * (pl.col("clean_price") / 100)).alias("market_value"),

        pl.lit(datetime.now()).alias("valuation_timestamp")
    ])

    print("--- Optimised query plan ---")
    print(lf.explain())

    return lf.collect()


