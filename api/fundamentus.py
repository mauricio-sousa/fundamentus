#!/usr/bin/env python3
"""
Scrapes financial data for Brazilian stocks from www.fundamentus.com.br.
"""

import requests
from lxml import html # Import html for fromstring
from decimal import Decimal
# Removed 're' and 'fragment_fromstring' as they are no longer needed


def get_data(*args, **kwargs) -> dict:
    """
    Fetches and parses stock data from the Fundamentus website.

    The data is scraped from http://www.fundamentus.com.br/resultado.php.
    
    Args:
        *args: Not used.
        **kwargs: Not used.

    Returns:
        dict: A dictionary where keys are stock tickers (str) and values are
              dictionaries of financial indicators. Financial indicators are
              keyed by their names (str) and values are Decimal objects.
              Returns an empty dictionary if any error occurs during fetching
              or parsing (e.g., network issues, unexpected HTML structure,
              table not found).
    """
    url = "http://www.fundamentus.com.br/resultado.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10) # Added timeout
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        content = response.text
    except requests.exceptions.RequestException as e:
        print(f"Error during requests to {url}: {e}") # Modified error message slightly
        return {}

    try:
        doc = html.fromstring(content) # Parse the full HTML content
        tables = doc.xpath('//table[@id="resultado"]') # Find the table by ID

        if not tables:
            print(f"Error: Table with id='resultado' not found on {url}") # Added url to message
            return {}
        
        page = tables[0] # The 'page' is now the table element itself
        result = {}

        tbody_list = page.xpath("tbody") # This should work on the table element
        if not tbody_list:
            print(f"Error: tbody element not found in table from {url}")
            return {}

        for rows in tbody_list[0].findall("tr"):
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

    except html.etree.LxmlError as e: # Catch potential lxml parsing errors
        print(f"Error parsing HTML from {url}: {e}")
        return {}


def todecimal(string_value: str) -> Decimal:
    """
    Converts a string value to a Decimal object.

    The string can contain Brazilian Portuguese number formatting (',' as decimal separator)
    and percentage signs, which are removed before conversion.

    Args:
        string_value (str): The string to convert.

    Returns:
        Decimal: The converted Decimal object.
    """
    string_value = string_value.translate(str.maketrans({".": "", "%": "", ",": "."}))
    return Decimal(string_value)
