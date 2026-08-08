#!/usr/bin/env python3

import httpx
from lxml import html
from aiocache import cached
from typing import Dict, List
from decimal import Decimal


@cached(ttl=10800)  # Cache por 3 horas
async def get_data(*args, **kwargs) -> Dict[str, Dict[str, Decimal]]:
    """Consulta o site Fundamentus e retorna um dicionário com os indicadores.

    Retorna um mapeamento de ticker -> indicadores, onde cada indicador é um
    Decimal. A função usa cache (TTL = 10800s) para reduzir chamadas ao site.
    (Argumentos *args e **kwargs são ignorados).
    """
    url = "https://www.fundamentus.com.br/resultado.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://www.fundamentus.com.br/",
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()

    page = html.fromstring(response.text)
    result = {}

    # Extrai os cabeçalhos da tabela
    header_elements = page.xpath(".//thead/tr/th")
    FIELDS: List[str] = [th.text_content().strip() for th in header_elements][1:]

    for tr in page.xpath(".//tbody/tr"):
        tds = tr.findall("td")
        if len(tds) < len(FIELDS) + 1:
            continue
        ticker = tds[0].text_content().strip()
        values = [td.text_content().strip() for td in tds]
        result[ticker] = {FIELDS[i]: to_decimal(values[i + 1]) for i in range(len(FIELDS))}

    return result


def to_decimal(string: str) -> Decimal:
    """Converte uma string numérica formatada para Decimal."""
    # Usa '.' como separador de milhares e ',' como separador decimal.
    # Exemplos aceitáveis: '1.234,56', '12,34', '5,6%'.
    # Valores não numéricos (como '-' ou '') retornam Decimal('0.0').
    string = string.strip().translate(str.maketrans({".": "", "%": "", ",": "."}))
    if not string or string == "-":
        return Decimal("0.0")
    return Decimal(string)
