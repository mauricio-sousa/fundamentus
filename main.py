from fastapi_mcp import FastApiMCP
from fastapi import FastAPI, HTTPException
from api.fundamentus import get_data
from typing import Dict

app = FastAPI()

# Criar o servidor MCP antes de definir as rotas


async def fetch_and_convert():
    """Chama `get_data()` e prepara o resultado para resposta JSON.

    O retorno é um dicionário mapeando o código do ativo (ticker) para um
    dicionário de indicadores numéricos. "Ticker" aqui significa o código
    alfanumérico que identifica um ativo negociado na B3 (por exemplo
    'ABEV3' ou 'PETR4').

    Conversões:
    - Decimal -> float para serialização JSON.

    Erros:
    - Em caso de falha na requisição ao site externo, levanta
      HTTPException(status_code=503) para indicar indisponibilidade do
      serviço externo.
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
    "/ticker/{ticker_name}", operation_id="get_ticker",
    responses={
        200: {
            "description": "Indicadores fundamentalistas do ticker",
            "content": {
                "application/json": {
                    "example": {
                        "Cotacao": 34.41,
                        "P/L": 5.73,
                        "P/VP": 1.11,
                        "PSR": 0.899,
                        "DY": 15.13,
                        "P/Ativo": 0.377,
                        "P/Cap.Giro": -10.24,
                        "P/EBIT": 2.16,
                        "P/ACL": -0.7,
                        "EV/EBIT": 3.71,
                        "EV/EBITDA": 2.73,
                        "Mrg.Ebit": 41.67,
                        "Mrg.Liq.": 15.78,
                        "Liq.Corr.": 0.76,
                        "ROIC": 18.87,
                        "ROE": 19.38,
                        "Liq.2meses": 311662000.0,
                        "Pat.Liq": 399222000000.0,
                        "Div.Brut/Pat.": 0.93,
                        "Cresc.5anos": 6.17
                    }
                }
            },
        },
        404: {"description": "Ticker não encontrado"},
    },
)
async def get_ticker(ticker_name: str) -> Dict[str, float]:
    """Retorna os indicadores para um ticker (código do ativo) específico.

    Parâmetros:
    - ticker_name: código alfanumérico do ativo negociado na B3 (ex.: 'ABEV3',
      'VALE3'). A busca é feita em caixa alta; a entrada será normalizada.

    Retorno:
    - Um dicionário onde chaves são nomes de indicadores (por exemplo,
      'P/L', 'ROE') e valores são floats prontos para serialização JSON.

    Exemplo de resposta:
    {
        "Cotacao": 34.41,
        "P/L": 5.73,
        "P/VP": 1.11,
        "PSR": 0.899,
        "DY": 15.13,
        "P/Ativo": 0.377,
        "P/Cap.Giro": -10.24,
        "P/EBIT": 2.16,
        "P/ACL": -0.7,
        "EV/EBIT": 3.71,
        "EV/EBITDA": 2.73,
        "Mrg.Ebit": 41.67,
        "Mrg.Liq.": 15.78,
        "Liq.Corr.": 0.76,
        "ROIC": 18.87,
        "ROE": 19.38,
        "Liq.2meses": 311662000.0,
        "Pat.Liq": 399222000000.0,
        "Div.Brut/Pat.": 0.93,
        "Cresc.5anos": 6.17
    }

    Erros:
    - Se o ticker não existir no conjunto de dados, retorna 404 (HTTPException).
    - Se ocorrer falha ao obter dados externos, a função chamadora já mapeiará
      o erro para 503.
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
                        "CSTB3": {
                            "Cotacao": 150.0,
                            "P/L": 0.0,
                            "P/VP": 0.0,
                            "PSR": 0.0,
                            "DY": 0.0,
                            "P/Ativo": 0.0,
                            "P/Cap.Giro": 0.0,
                            "P/EBIT": 0.0,
                            "P/ACL": 0.0,
                            "EV/EBIT": 0.0,
                            "EV/EBITDA": 0.0,
                            "Mrg.Ebit": 40.85,
                            "Mrg.Liq.": 28.98,
                            "Liq.Corr.": 2.6,
                            "ROIC": 22.4,
                            "ROE": 20.11,
                            "Liq.2meses": 0.0,
                            "Pat.Liq": 8420670000.0,
                            "Div.Brut/Pat.": 0.14,
                            "Cresc.5anos": 31.91
                        },
                        "MNSA4": {
                            "Cotacao": 0.47,
                            "P/L": 0.0,
                            "P/VP": 0.0,
                            "PSR": 0.0,
                            "DY": 0.0,
                            "P/Ativo": 0.0,
                            "P/Cap.Giro": 0.0,
                            "P/EBIT": 0.0,
                            "P/ACL": 0.0,
                            "EV/EBIT": 0.0,
                            "EV/EBITDA": 0.0,
                            "Mrg.Ebit": -208.15,
                            "Mrg.Liq.": -362.66,
                            "Liq.Corr.": 3.63,
                            "ROIC": -13.5,
                            "ROE": 145.7,
                            "Liq.2meses": 0.0,
                            "Pat.Liq": -9105000.0,
                            "Div.Brut/Pat.": -6.52,
                            "Cresc.5anos": -41.11
                        }
                    }
                }
            },
        }
    },
)
async def get_all_tickers() -> Dict[str, Dict[str, float]]:
    """Retorna os indicadores dos dois primeiros tickers encontrados.

    Retorno:
    - Dicionário mapeando cada ticker (código do ativo) para outro dicionário
      com indicadores numéricos (float). Exemplo:

      {
        "CSTB3": {...},
        "MNSA4": {...}
      }

    Observações:
    - Os dados são obtidos sob demanda (fetch ondemand) na primeira requisição
      e em seguida servidos a partir do cache por 1 hora (TTL). Se o serviço
      externo estiver indisponível, a requisição retornará 503 (via
      fetch_and_convert).
    """

    data = await fetch_and_convert()
    return data

mcp = FastApiMCP(
    app,
    name="API Fundamentus",
    description="Indicadores fundamentalistas das empresas listadas na B3.",
    describe_all_responses=True,        # Include all possible response schemas in tool descriptions
    describe_full_response_schema=True  # Include full JSON schema in tool descriptions
)

# Mount the MCP server to your FastAPI app
mcp.mount()

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)