"""
Main module for the Fundamentus FastAPI application.

Provides API endpoints to access financial data for Brazilian stocks.
Manages data fetching, caching, and daily refresh logic.
"""
from fastapi import FastAPI, HTTPException
from api.fundamentus import get_data as fg_get_data # Use an alias to avoid confusion
from datetime import datetime

app = FastAPI()

lista = {} # Initialize as empty
dia = ""   # Initialize as empty

def get_fresh_data():
    """
    Fetches fresh stock data from `api.fundamentus.fg_get_data()` and updates globals.

    This function updates the global `lista` with the new stock data and
    the global `dia` with the current day of the month.
    If `fg_get_data()` fails (returns an empty dictionary), `lista` will be
    set to an empty dictionary, and an error message is printed.
    The `dia` variable is updated regardless of fetch success to prevent
    continuous refetch attempts on a failing source for the same day.
    """
    global lista, dia
    current_day = datetime.strftime(datetime.today(), "%d")
    data_from_fundamentus = fg_get_data() # Renamed import
    if not data_from_fundamentus: # Check if get_data returned empty (error)
        # If there was an error fetching new data, we have a choice:
        # 1. Return old data (if available) - might be too stale.
        # 2. Raise an error.
        # 3. Return an empty dict or a specific error response.
        # For now, let's clear existing data and log that fresh data couldn't be fetched.
        print(f"Error fetching fresh data on day {current_day}. Old data cleared if any.")
        lista = {} # Clear potentially stale data
    else:
        # Store Decimal objects directly, removing the float conversion
        lista = data_from_fundamentus
    dia = current_day # Update the day regardless of success to prevent constant retries on failure
    print(f"Data (re)loaded for day: {dia}")

# Call it once at startup
get_fresh_data()


@app.get("/")
def get_all_urls():
    """Lists all available API endpoints."""
    url_list = [{"path": route.path, "name": route.name} for route in app.routes]
    return url_list


@app.get("/ticker/{ticker_name}")
def get_ticker(ticker_name: str):
    "Retorna os indicadores da empresa consultada"
    global lista, dia # Ensure you're referencing the globals

    current_day = datetime.strftime(datetime.today(), "%d")
    if current_day != dia:
        print(f"Day changed from {dia} to {current_day}. Refreshing data.")
        get_fresh_data()

    ticker_name = ticker_name.upper()
    if not lista: # Check if lista is empty (either initial load failed or refresh failed)
         raise HTTPException(
             status_code=503, detail="Data currently unavailable. Please try again later."
         )
    if ticker_name not in lista:
        raise HTTPException(
            status_code=404, detail="Ticker: {} não encontrado!".format(ticker_name)
        )
    return lista[ticker_name]


@app.get("/tickers")
def get_all_tickers():
    "Retorna os indicadores de todas as empresas cadastradas na Bovespa"
    global lista, dia # Ensure you're referencing the globals

    current_day = datetime.strftime(datetime.today(), "%d")
    if current_day != dia:
        print(f"Day changed from {dia} to {current_day}. Refreshing data.")
        get_fresh_data()
    
    if not lista: # Check if lista is empty
         # Consistent with returning an empty list/dict if data is unavailable
         return {} 
    return lista
