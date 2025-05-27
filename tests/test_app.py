from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
from decimal import Decimal
import main # To manipulate main.dia for forcing refresh

client = TestClient(app)


def test_get_main():
    response = client.get("/")
    assert response.status_code == 200
    # Ensure some JSON response is returned, structure might vary
    assert response.json() is not None


@patch('main.fg_get_data')
def test_get_ticker(mock_fg_get_data):
    mock_data = {'ABEV3': {'Cotacao': Decimal('12.34'), 'P/L': Decimal('15.67')}}
    mock_fg_get_data.return_value = mock_data
    
    main.dia = "previous_day" # Force refresh to use mocked data

    response = client.get("/ticker/abev3")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response['Cotacao'] == '12.34'
    assert json_response['P/L'] == '15.67'
    assert isinstance(json_response['Cotacao'], str)


@patch('main.fg_get_data')
def test_get_tickers(mock_fg_get_data):
    mock_data = {
        'ABEV3': {'Cotacao': Decimal('12.34'), 'P/L': Decimal('15.67')},
        'MGLU3': {'Cotacao': Decimal('2.50'), 'P/L': Decimal('10.00')}
    }
    mock_fg_get_data.return_value = mock_data

    main.dia = "previous_day" # Force refresh

    response = client.get("/tickers")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response['ABEV3']['Cotacao'] == '12.34'
    assert json_response['MGLU3']['Cotacao'] == '2.50'
    assert isinstance(json_response['ABEV3']['Cotacao'], str)


@patch('main.fg_get_data')
def test_get_ticker_not_found(mock_fg_get_data):
    # Ensure lista is populated but without the requested ticker
    mock_fg_get_data.return_value = {'XYZ1': {'Cotacao': Decimal('1.00')}}
    main.dia = "previous_day" # Force refresh

    response = client.get("/ticker/ABEV99") # Non-existent ticker
    assert response.status_code == 404
    assert response.json()['detail'] == "Ticker: ABEV99 não encontrado!"


@patch('main.fg_get_data')
def test_get_ticker_data_unavailable(mock_fg_get_data):
    mock_fg_get_data.return_value = {} # Simulate data fetching error
    main.dia = "previous_day" # Force refresh, main.lista will become {}

    response = client.get("/ticker/abev3")
    assert response.status_code == 503
    assert response.json()['detail'] == "Data currently unavailable. Please try again later."


@patch('main.fg_get_data')
def test_get_tickers_data_unavailable(mock_fg_get_data):
    mock_fg_get_data.return_value = {} # Simulate data fetching error
    main.dia = "previous_day" # Force refresh, main.lista will become {}

    response = client.get("/tickers")
    assert response.status_code == 200 # Returns empty dict, which is valid
    assert response.json() == {}
