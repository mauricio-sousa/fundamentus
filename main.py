from fastapi import FastAPI, HTTPException
from api.fundamentus import get_data
from datetime import datetime
from typing import Dict
from fastapi import FastAPI, HTTPException
from api.fundamentus import get_data
from datetime import datetime
from typing import Dict

app = FastAPI()


async def fetch_and_convert():
    """Helper que chama `get_data()` e converte Decimal -> float.

    Retorna um dicionário pronto para serialização JSON. Em caso de erro ao
    buscar os dados externos, lança uma HTTPException(503).
    """

    try:
        raw = await get_data()
    except Exception as e:
        # Falha na consulta externa — retornar 503 para o cliente
        raise HTTPException(status_code=503, detail=f"Erro ao obter dados externos: {e}")

    converted = {
        outer_k: {inner_k: float(inner_v) for inner_k, inner_v in outer_v.items()}
        for outer_k, outer_v in raw.items()
    }
    return converted


@app.get("/")
async def get_all_urls() -> list:
    """Retorna a lista de rotas da API.

    Useful para descoberta rápida das rotas disponíveis.
    """

    url_list = [{"path": route.path, "name": route.name} for route in app.routes]
    return url_list


@app.get(
    "/ticker/{ticker_name}",
    responses={
        200: {
            "description": "Indicadores do ticker",
            "content": {
                "application/json": {
                    "example": {
                        "Cotacao": 7.23,
                        "P/L": 12.5,
                        "P/VP": 1.8,
                        "PSR": 2.3,
                        "DY": 0.035,
                        "ROE": 0.18
                    }
                }
            },
        },
        404: {"description": "Ticker não encontrado"},
    },
)
async def get_ticker(ticker_name: str) -> Dict[str, float]:
    """Retorna os indicadores para um ticker informado.

    Args:
        ticker_name (str): código do ativo (ex.: 'ABEV3').

    Returns:
        Dict[str, float]: dicionário com os indicadores do ticker.

    Raises:
        HTTPException: se o ticker não for encontrado (status 404).
    """

    ticker_name = ticker_name.upper()
    data = await fetch_and_convert()
    if ticker_name not in data:
        raise HTTPException(
            status_code=404, detail="Ticker: {} não encontrado!".format(ticker_name)
        )
    return data[ticker_name]




@app.get(
    "/tickers",
    responses={
        200: {
            "description": "Mapeamento ticker -> indicadores",
            "content": {
                "application/json": {
                    "example": {
                        "ABEV3": {
                            "Cotacao": 7.23,
                            "P/L": 12.5,
                            "P/VP": 1.8,
                            "PSR": 2.3,
                            "DY": 0.035,
                        },
                        "PETR4": {
                            "Cotacao": 28.4,
                            "P/L": 6.2,
                            "P/VP": 0.9,
                            "PSR": 1.1,
                            "DY": 0.012,
                        }
                    }
                }
            },
        }
    },
)
async def get_all_tickers() -> Dict[str, Dict[str, float]]:
    """Retorna os indicadores de todos os tickers disponíveis.

    Returns:
        Dict[str, Dict[str, float]]: mapeamento ticker -> indicadores.
    """

    data = await fetch_and_convert()
    return data
