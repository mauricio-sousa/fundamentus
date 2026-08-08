from fastapi_mcp import FastApiMCP
from fastapi import FastAPI, HTTPException, Query
from api.fundamentus import get_data
from api.models import Indicadores, TickerData

app = FastAPI()

mcp = FastApiMCP(
    app,
    name="API Fundamentus",
    description="Indicadores fundamentalistas das empresas listadas na B3.",
    describe_all_responses=True,        # Include all possible response schemas in tool descriptions
    describe_full_response_schema=True  # Include full JSON schema in tool descriptions
)

mcp.mount_http()

async def fetch_data():
    """Chama `get_data()` e lida com falhas.

    O retorno é um dicionário mapeando o código do ativo (ticker) para um
    dicionário de indicadores numéricos (floats).

    Erros:
    - Em caso de falha na requisição ao site externo, levanta
      HTTPException(status_code=503) para indicar indisponibilidade do
      serviço externo.
    """
    try:
        return await get_data()
    except Exception as e:
        # Falha na consulta externa — retornar 503 para o cliente
        raise HTTPException(status_code=503, detail=f"Erro ao obter dados externos: {e}")


@app.get("/")
async def get_all_urls() -> list:
    """Retorna a lista de rotas da API.

    Useful para descoberta rápida das rotas disponíveis.
    """
    # Filtrando para não exibir rotas internas do MCP na resposta raiz
    allowed_routes = {"/", "/tickers", "/ticker/{ticker_name}"}
    url_list = [{"path": route.path, "name": route.name} for route in app.routes if route.path in allowed_routes]
    return url_list

@app.get("/ticker/{ticker_name}", operation_id="get_ticker", response_model=Indicadores)
async def get_ticker(ticker_name: str) -> Indicadores:
    """Retorna os indicadores para um ticker (código do ativo) específico.

    Parâmetros:
    - ticker_name: código alfanumérico do ativo negociado na B3 (ex.: 'ABEV3',
      'VALE3'). A busca é feita em caixa alta; a entrada será normalizada.

    Retorno:
    - Um dicionário onde chaves são nomes de indicadores (por exemplo,
      'P/L', 'ROE') e valores são floats prontos para serialização JSON.

    Erros:
    - Se o ticker não existir no conjunto de dados, retorna 404 (HTTPException).
    - Se ocorrer falha ao obter dados externos, a função chamadora já mapeiará
      o erro para 503.
    """

    ticker_name = ticker_name.upper()
    data = await fetch_data()
    if ticker_name not in data:
        raise HTTPException(
            status_code=404, detail="Ticker: {} não encontrado!".format(ticker_name)
        )
    return data[ticker_name]

@app.get("/tickers", response_model=TickerData)
async def get_all_tickers(
    skip: int = Query(0, ge=0, description="Número de tickers a pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número de tickers a retornar")
) -> TickerData:
    """Retorna os indicadores para uma lista paginada de tickers.

    Parâmetros:
    - skip: número de tickers a pular (para paginação).
    - limit: número máximo de tickers a retornar.

    Retorno:
    - Dicionário mapeando cada ticker (código do ativo) para outro dicionário
      com indicadores numéricos (float).
    """

    data = await fetch_data()
    tickers = list(data.keys())[skip : skip + limit]
    return {ticker: data[ticker] for ticker in tickers}

# Refresh the MCP server to include the new endpoint
mcp.setup_server()