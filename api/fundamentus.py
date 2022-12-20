#!/usr/bin/env python3

import re
import requests
from lxml.html import fragment_fromstring
from decimal import Decimal


def get_data(*args, **kwargs):
    url = "http://www.fundamentus.com.br/resultado.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    }
    content = requests.get(url, headers=headers).text

    pattern = re.compile('<table id="resultado".*</table>', re.DOTALL)
    page = fragment_fromstring(re.findall(pattern, content)[0])
    result = {}

    for rows in page.xpath("tbody")[0].findall("tr"):
        result.update(
            {
                rows.getchildren()[0][0]
                .getchildren()[0]
                .text: {
                    "Cotacao": todecimal(rows.getchildren()[1].text),
                    "P/L": todecimal(rows.getchildren()[2].text),
                    "P/VP": todecimal(rows.getchildren()[3].text),
                    "PSR": todecimal(rows.getchildren()[4].text),
                    "DY": todecimal(rows.getchildren()[5].text),
                    "P/Ativo": todecimal(rows.getchildren()[6].text),
                    "P/Cap.Giro": todecimal(rows.getchildren()[7].text),
                    "P/EBIT": todecimal(rows.getchildren()[8].text),
                    "P/ACL": todecimal(rows.getchildren()[9].text),
                    "EV/EBIT": todecimal(rows.getchildren()[10].text),
                    "EV/EBITDA": todecimal(rows.getchildren()[11].text),
                    "Mrg.Ebit": todecimal(rows.getchildren()[12].text),
                    "Mrg.Liq.": todecimal(rows.getchildren()[13].text),
                    "Liq.Corr.": todecimal(rows.getchildren()[14].text),
                    "ROIC": todecimal(rows.getchildren()[15].text),
                    "ROE": todecimal(rows.getchildren()[16].text),
                    "Liq.2meses": todecimal(rows.getchildren()[17].text),
                    "Pat.Liq": todecimal(rows.getchildren()[18].text),
                    "Div.Brut/Pat.": todecimal(rows.getchildren()[19].text),
                    "Cresc.5anos": todecimal(rows.getchildren()[20].text),
                }
            }
        )
    return result


def todecimal(string):
    string = string.translate(str.maketrans({".": "", "%": "", ",": "."}))
    return Decimal(string)
