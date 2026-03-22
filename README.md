# Atlas Bond Pipeline 📈
### High-Performance Fixed Income ETL & Risk Engine

A professional-grade data pipeline designed to ingest global bond positions, perform multi-core currency normalization, and store validated trade data for real-time risk analysis.

## 🏗️ Architecture & Design Decisions

This project is built to solve the common "Python Bottleneck" in financial data processing:

* **Extract (Async I/O):** Built with **FastAPI** and **httpx**. It utilizes Python's `asyncio` event loop to handle concurrent market data fetches without blocking the execution thread—crucial for high-throughput trading environments.
* **Transform (Parallel Processing):** Powered by **Polars**. By utilizing a Rust-backed engine, the pipeline drops the **GIL (Global Interpreter Lock)** to perform vectorized bond-math and FX-joins across all available CPU cores.
* **Validation (Type Safety):** Implements **Pydantic** models to enforce "Bank-Grade" data integrity, ensuring ISINs, yields, and prices meet strict schemas before ingestion.
* **Load (Persistent Storage):** Integrated with **PostgreSQL** using **SQLAlchemy**. Optimized with **B-Tree Indexing** on high-cardinality columns (Ticker/Date) to ensure sub-second query latency for analysts.

## 🚀 Key Features
- **Predicate Pushdown:** Lazy evaluation optimizes memory usage by filtering data at the source.
- **Concurrency vs. Parallelism:** Demonstrates a hybrid approach using `async` for I/O and multi-threading for CPU-bound tasks.
- **RESTful Interface:** Provides a Swagger-documented API for automated trade reporting.

## 🛠️ Tech Stack
- **Language:** Python 3.12+
- **Framework:** FastAPI
- **Data Science:** Polars (Rust-based)
- **Database:** PostgreSQL / SQLAlchemy
- **Infrastructure:** Docker / Kubernetes-ready

## 📖 Setup
1. `pip install -r requirements.txt`
2. `uvicorn main:app --reload`
