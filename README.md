# Trade Monitor API

A lightweight FastAPI + Polars project for monitoring, querying, and summarising trade-style datasets.

This project was built to demonstrate practical Python skills around:
- API development with FastAPI
- tabular data processing with Polars
- filtering and aggregating trade data
- basic anomaly detection for operational monitoring

## Features

- Load trade-style data from CSV
- Query trades with optional filters
- Summarise trades by book
- Summarise trades by trader
- Flag suspicious records based on simple business rules
- Explore endpoints through FastAPI's auto-generated Swagger docs

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Polars

## Project Structure

```text
trade-monitor-api/
├── main.py
├── sample_trades.csv
└── README.md
