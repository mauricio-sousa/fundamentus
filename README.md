[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c745b5b501ed41a79f52ceee58edd37b)](https://app.codacy.com/gh/mauricio-sousa/fundamentus?utm_source=github.com&utm_medium=referral&utm_content=mauricio-sousa/fundamentus&utm_campaign=Badge_Grade_Settings)
[![codecov](https://codecov.io/gh/mauricio-sousa/fundamentus/branch/master/graph/badge.svg?token=D74I99F0LU)](https://codecov.io/gh/mauricio-sousa/fundamentus)
[![Python package](https://github.com/mauricio-sousa/fundamentus/actions/workflows/python-package.yml/badge.svg)](https://github.com/mauricio-sousa/fundamentus/actions/workflows/python-package.yml)
[![Coverage Status](https://coveralls.io/repos/github/mauricio-sousa/fundamentus/badge.svg?branch=master)](https://coveralls.io/github/mauricio-sousa/fundamentus?branch=master)
# Fundamentus
Esta é uma pequena API feita em python3 para análise de ações da BOVESPA utilizando o site fundamentus (www.fundamentus.com.br), que retorna os 
principais indicadores fundamentalistas em formato JSON.
A API utiliza o microframework Flask.
Também é possível utilizar via linha de comando.

# Instalando
    $ pip3 install -r requirements.txt

# Executando o WebServer
    $ uvicorn main:app --reload

# Acessando a API
Conecte no endereço (ex.: http://127.0.0.1:8000/tickers) 
