#!/usr/bin/env python3

import re
import httpx
from bs4 import BeautifulSoup
from decimal import Decimal
from aiocache import cached
from typing import Dict


@cached(ttl=3600)  # Cache por 1 hora
async def get_data(*args, **kwargs) -> Dict[str, Dict[str, Decimal]]:
    """Consulta o site Fundamentus e retorna um dicionário com os indicadores.

    Retorna um mapeamento de ticker -> indicadores, onde cada indicador é um
    Decimal. A função usa cache (TTL = 3600s) para reduzir chamadas ao site.

    Args:
        *args: argumentos posicionais (ignorados).
        **kwargs: argumentos nomeados (ignorados).

    Returns:
        Dict[str, Dict[str, Decimal]]: dicionário com os dados dos tickers.
    """

    url = "https://www.fundamentus.com.br/resultado.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "resultado"})
    result = {}

    for row in table.find("tbody").find_all("tr"):
        columns = row.find_all("td")
        ticker = columns[0].text.strip()
        result[ticker] = {
            "Cotacao": todecimal(columns[1].text),
            "P/L": todecimal(columns[2].text),
            "P/VP": todecimal(columns[3].text),
            "PSR": todecimal(columns[4].text),
            "DY": todecimal(columns[5].text),
            "P/Ativo": todecimal(columns[6].text),
            "P/Cap.Giro": todecimal(columns[7].text),
            "P/EBIT": todecimal(columns[8].text),
            "P/ACL": todecimal(columns[9].text),
            "EV/EBIT": todecimal(columns[10].text),
            "EV/EBITDA": todecimal(columns[11].text),
            "Mrg.Ebit": todecimal(columns[12].text),
            "Mrg.Liq.": todecimal(columns[13].text),
            "Liq.Corr.": todecimal(columns[14].text),
            "ROIC": todecimal(columns[15].text),
            "ROE": todecimal(columns[16].text),
            "Liq.2meses": todecimal(columns[17].text),
            "Pat.Liq": todecimal(columns[18].text),
            "Div.Brut/Pat.": todecimal(columns[19].text),
            "Cresc.5anos": todecimal(columns[20].text),
        }

    return result


def todecimal(string: str) -> Decimal:
    """Converte uma string numérica formatada (com '.' como separador de milhares
    e ',' como separador decimal) para Decimal.

    Exemplos aceitáveis: '1.234,56', '12,34', '5,6%'.

    Args:
        string (str): string a ser convertida.

    Returns:
        Decimal: valor convertido.
    """

    string = string.translate(str.maketrans({".": "", "%": "", ",": "."}))
    return Decimal(string)
