from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from decimal import Decimal


@patch("main.get_data")
def test_get_main(mock_get_data):
    mock_get_data.return_value = {"ABEV3": {"Cotação": Decimal("15.0")}}
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()


@patch("main.get_data")
def test_get_ticker(mock_get_data):
    mock_get_data.return_value = {
        "ABEV3": {
            "Cotação": Decimal("15.0"),
            "P/L": Decimal("12.5"),
            "P/VP": Decimal("1.8"),
            "PSR": Decimal("2.3"),
            "Div.Yield": Decimal("0.035"),
            "P/Ativo": Decimal("0.1"),
            "P/Cap.Giro": Decimal("0.2"),
            "P/EBIT": Decimal("0.3"),
            "P/Ativ Circ.Liq": Decimal("0.4"),
            "EV/EBIT": Decimal("0.5"),
            "EV/EBITDA": Decimal("0.6"),
            "Mrg Bruta": Decimal("0.65"),
            "Mrg Ebit": Decimal("0.7"),
            "Mrg. Líq.": Decimal("0.8"),
            "Liq. Corr.": Decimal("0.9"),
            "ROIC": Decimal("1.0"),
            "ROE": Decimal("1.1"),
            "Liq.2meses": Decimal("1.2"),
            "Patrim. Líq": Decimal("1.3"),
            "Dív.Líq/ Patrim.": Decimal("1.4"),
            "Cresc. Rec.5a": Decimal("1.5"),
        }
    }
    with TestClient(app) as client:
        response = client.get("/ticker/ABEV3")
        assert response.status_code == 200
        assert response.json()["Cotação"] == "15.0"


@patch("main.get_data")
def test_get_tickers(mock_get_data):
    mock_get_data.return_value = {
        "ABEV3": {
            "Cotação": Decimal("15.0"),
            "P/L": Decimal("12.5"),
            "P/VP": Decimal("1.8"),
            "PSR": Decimal("2.3"),
            "Div.Yield": Decimal("0.035"),
            "P/Ativo": Decimal("0.1"),
            "P/Cap.Giro": Decimal("0.2"),
            "P/EBIT": Decimal("0.3"),
            "P/Ativ Circ.Liq": Decimal("0.4"),
            "EV/EBIT": Decimal("0.5"),
            "EV/EBITDA": Decimal("0.6"),
            "Mrg Bruta": Decimal("0.65"),
            "Mrg Ebit": Decimal("0.7"),
            "Mrg. Líq.": Decimal("0.8"),
            "Liq. Corr.": Decimal("0.9"),
            "ROIC": Decimal("1.0"),
            "ROE": Decimal("1.1"),
            "Liq.2meses": Decimal("1.2"),
            "Patrim. Líq": Decimal("1.3"),
            "Dív.Líq/ Patrim.": Decimal("1.4"),
            "Cresc. Rec.5a": Decimal("1.5"),
        },
        "VALE3": {
            "Cotação": Decimal("70.0"),
            "P/L": Decimal("12.5"),
            "P/VP": Decimal("1.8"),
            "PSR": Decimal("2.3"),
            "Div.Yield": Decimal("0.035"),
            "P/Ativo": Decimal("0.1"),
            "P/Cap.Giro": Decimal("0.2"),
            "P/EBIT": Decimal("0.3"),
            "P/Ativ Circ.Liq": Decimal("0.4"),
            "EV/EBIT": Decimal("0.5"),
            "EV/EBITDA": Decimal("0.6"),
            "Mrg Bruta": Decimal("0.65"),
            "Mrg Ebit": Decimal("0.7"),
            "Mrg. Líq.": Decimal("0.8"),
            "Liq. Corr.": Decimal("0.9"),
            "ROIC": Decimal("1.0"),
            "ROE": Decimal("1.1"),
            "Liq.2meses": Decimal("1.2"),
            "Patrim. Líq": Decimal("1.3"),
            "Dív.Líq/ Patrim.": Decimal("1.4"),
            "Cresc. Rec.5a": Decimal("1.5"),
        },
    }
    with TestClient(app) as client:
        response = client.get("/tickers")
        assert response.status_code == 200
        assert response.json()["ABEV3"]["Cotação"] == "15.0"


@patch("main.get_data")
def test_get_ticker_not_found(mock_get_data):
    mock_get_data.return_value = {"ABEV3": {"Cotação": Decimal("15.0")}}
    with TestClient(app) as client:
        response = client.get("/ticker/abev")
        assert response.status_code == 404
        assert response.json()["detail"] == "Ticker: ABEV não encontrado!"
