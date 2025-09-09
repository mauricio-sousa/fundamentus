from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app


@patch("main.get_data")
def test_get_main(mock_get_data):
    mock_get_data.return_value = {"ABEV3": {"Cotacao": 15.0}}
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()


@patch("main.get_data")
def test_get_ticker(mock_get_data):
    mock_get_data.return_value = {"ABEV3": {"Cotacao": 15.0}}
    with TestClient(app) as client:
        response = client.get("/ticker/ABEV3")
        assert response.status_code == 200
        assert response.json() == {"Cotacao": 15.0}


@patch("main.get_data")
def test_get_tickers(mock_get_data):
    mock_get_data.return_value = {
        "ABEV3": {"Cotacao": 15.0},
        "VALE3": {"Cotacao": 70.0},
    }
    with TestClient(app) as client:
        response = client.get("/tickers")
        assert response.status_code == 200
        assert response.json() == {
            "ABEV3": {"Cotacao": 15.0},
            "VALE3": {"Cotacao": 70.0},
        }


@patch("main.get_data")
def test_get_ticker_not_found(mock_get_data):
    mock_get_data.return_value = {"ABEV3": {"Cotacao": 15.0}}
    with TestClient(app) as client:
        response = client.get("/ticker/abev")
        assert response.status_code == 404
        assert response.json()["detail"] == "Ticker: ABEV não encontrado!"
