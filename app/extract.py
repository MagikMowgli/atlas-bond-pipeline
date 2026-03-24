import asyncio
import httpx
import polars as pl

async def fetch_bond(client: httpx.AsyncClient, ticker: str) -> dict:
    """
    Task 1: The individual worker. 
    It goes to the internet, waits for the data, and brings it back.
    """
    # using a free public dummy API just to test that the network connection works
    url = "https://jsonplaceholder.typicode.com/posts/1" 
    
    try:
        response = await client.get(url)
        response.raise_for_status() # Raises an error if the website is down (is our failsafe)
        
        # Simulate formatting the response into a hedge fund dictionary
        return {
            "ticker": ticker,
            "isin": f"US12345{ticker[:4]}", # Generates a fake 12-char ISIN
            "face_value": 1000.0,
            "clean_price": 95.50,
            "currency": "USD"
        }
    except Exception as e:
        print(f"⚠️ Network error for {ticker}: {e}")
        return None

async def run_network_extract(tickers: list[str]) -> pl.DataFrame:
    """
    Task 2: The Switchboard.
    Fires all workers at the exact same time.
    """
    print(f"📡 Requesting {len(tickers)} bonds over the network...")
    
    # Open ONE highly efficient network connection for all requests
    async with httpx.AsyncClient() as client:
        
        # 1. Line up the tasks (Don't run them yet)
        tasks = [fetch_bond(client, ticker) for ticker in tickers]
        
        # 2. Fire them ALL simultaneously!
        results = await asyncio.gather(*tasks)
        
    # Clean up any failed network calls and convert to Polars
    valid_results = [res for res in results if res is not None]
    return pl.DataFrame(valid_results)