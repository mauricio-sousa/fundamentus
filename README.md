# Fundamentus

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c745b5b501ed41a79f52ceee58edd37b)](https://app.codacy.com/gh/mauricio-sousa/fundamentus?utm_source=github.com&utm_medium=referral&utm_content=mauricio-sousa/fundamentus&utm_campaign=Badge_Grade_Settings)
[![codecov](https://codecov.io/gh/mauricio-sousa/fundamentus/branch/master/graph/badge.svg?token=D74I99F0LU)](https://codecov.io/gh/mauricio-sousa/fundamentus)
[![Tests](https://github.com/mauricio-sousa/fundamentus/actions/workflows/python-tests.yml/badge.svg)](https://github.com/mauricio-sousa/fundamentus/actions/workflows/python-tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/mauricio-sousa/fundamentus/badge.svg?branch=master)](https://coveralls.io/github/mauricio-sousa/fundamentus?branch=master)

Esta é uma pequena API feita em python3 para análise de ações da BOVESPA utilizando o site fundamentus (www.fundamentus.com.br), que retorna os principais indicadores fundamentalistas em formato JSON.
A API utiliza o microframework [fastAPI](https://fastapi.tiangolo.com).
## Visão geral

Pequena API que faz scraping do site fundamentus e expõe indicadores fundamentalistas
em JSON. O projeto foi atualizado para usar requisições assíncronas (`httpx`) e
`BeautifulSoup` para parsing, além de cache em memória via `aiocache`.

## Pré-requisitos

- Python 3.11+ (este projeto usa 3.13 no ambiente de desenvolvimento)
- virtualenv ou venv recomendados

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate.fish  # se você usa fish shell
pip install -r requirements.txt
```

## Executando o servidor

```bash
uvicorn main:app --reload
```

O serviço ficará disponível em http://127.0.0.1:8000.

## Endpoints

- `GET /` - lista rotas disponíveis
- `GET /tickers` - retorna um dicionário com todos os tickers e seus indicadores
- `GET /ticker/{ticker_name}` - retorna os indicadores do ticker especificado (ex.: `ABEV3`)

Exemplos rápidos:

```bash
curl http://127.0.0.1:8000/tickers
curl http://127.0.0.1:8000/ticker/ABEV3
http http://127.0.0.1:8000/
```

## Cache

A função de scraping usa `aiocache` com TTL padrão de 3600 segundos (1 hora)
para reduzir chamadas ao site fundamentus. Ajuste `@cached(ttl=...)` em
`api/fundamentus.py` se desejar outro comportamento.

## Testes

Para executar a suíte de testes:

```bash
source .venv/bin/activate.fish
pytest -q
```

Os testes foram atualizados para usar mocks e executar com `TestClient`.

## Notas sobre mudanças

- Refatorado scraping para `httpx` + `BeautifulSoup` (assíncrono).
- Endpoint e inicialização migrados para lifespan (handler de ciclo de vida) do FastAPI.
- Adicionado cache via `aiocache`.
- Testes atualizados e docstrings em pt-BR adicionadas.

## Contribuição

Fique à vontade para abrir issues ou pull requests com melhorias.

