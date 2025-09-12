from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app


@patch("main.lazy_loader.get_data")
def test_get_main(mock_get_data):
    mock_get_data.return_value = {"ABEV3": {"Cotação": 15.0}}
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()


@patch("main.lazy_loader.get_data")
def test_get_ticker(mock_get_data):
    mock_get_data.return_value = {
        "ABEV3": {
            "Cotação": 15.0,
            "P/L": 12.5,
            "P/VP": 1.8,
            "PSR": 2.3,
            "Div.Yield": 0.035,
            "P/Ativo": 0.1,
            "P/Cap.Giro": 0.2,
            "P/EBIT": 0.3,
            "P/Ativ Circ.Liq": 0.4,
            "EV/EBIT": 0.5,
            "EV/EBITDA": 0.6,
            "Mrg Ebit": 0.7,
            "Mrg. Líq.": 0.8,
            "Liq. Corr.": 0.9,
            "ROIC": 1.0,
            "ROE": 1.1,
            "Liq.2meses": 1.2,
            "Patrim. Líq": 1.3,
            "Dív.Brut/ Patrim.": 1.4,
            "Cresc. Rec.5a": 1.5,
        }
    }
    with TestClient(app) as client:
        response = client.get("/ticker/ABEV3")
        assert response.status_code == 200
        assert response.json()["Cotação"] == 15.0


@patch("main.lazy_loader.get_data")
def test_get_tickers(mock_get_data):
    mock_get_data.return_value = {
        "ABEV3": {
            "Cotação": 15.0,
            "P/L": 12.5,
            "P/VP": 1.8,
            "PSR": 2.3,
            "Div.Yield": 0.035,
            "P/Ativo": 0.1,
            "P/Cap.Giro": 0.2,
            "P/EBIT": 0.3,
            "P/Ativ Circ.Liq": 0.4,
            "EV/EBIT": 0.5,
            "EV/EBITDA": 0.6,
            "Mrg Ebit": 0.7,
            "Mrg. Líq.": 0.8,
            "Liq. Corr.": 0.9,
            "ROIC": 1.0,
            "ROE": 1.1,
            "Liq.2meses": 1.2,
            "Patrim. Líq": 1.3,
            "Dív.Brut/ Patrim.": 1.4,
            "Cresc. Rec.5a": 1.5,
        },
        "VALE3": {
            "Cotação": 70.0,
            "P/L": 12.5,
            "P/VP": 1.8,
            "PSR": 2.3,
            "Div.Yield": 0.035,
            "P/Ativo": 0.1,
            "P/Cap.Giro": 0.2,
            "P/EBIT": 0.3,
            "P/Ativ Circ.Liq": 0.4,
            "EV/EBIT": 0.5,
            "EV/EBITDA": 0.6,
            "Mrg Ebit": 0.7,
            "Mrg. Líq.": 0.8,
            "Liq. Corr.": 0.9,
            "ROIC": 1.0,
            "ROE": 1.1,
            "Liq.2meses": 1.2,
            "Patrim. Líq": 1.3,
            "Dív.Brut/ Patrim.": 1.4,
            "Cresc. Rec.5a": 1.5,
        },
    }
    with TestClient(app) as client:
        response = client.get("/tickers")
        assert response.status_code == 200
        assert response.json()["ABEV3"]["Cotação"] == 15.0


@patch("main.lazy_loader.get_data")
def test_get_ticker_not_found(mock_get_data):
    mock_get_data.return_value = {"ABEV3": {"Cotação": 15.0}}
    with TestClient(app) as client:
        response = client.get("/ticker/abev")
        assert response.status_code == 404
        assert response.json()["detail"] == "Ticker: ABEV não encontrado!"
