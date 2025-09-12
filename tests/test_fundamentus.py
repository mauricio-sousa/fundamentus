import asyncio
from decimal import Decimal
from unittest.mock import AsyncMock, patch
from api.fundamentus import get_data, todecimal


def test_todecimal():
    assert todecimal("1.234,56") == Decimal("1234.56")
    assert todecimal("12,34") == Decimal("12.34")
    assert todecimal("5,6%") == Decimal("5.6")


def test_get_data():
    mock_html = """
    <table id="resultado">
        <thead>
            <tr>
                <th>Papel</th>
                <th>Cotação</th>
                <th>P/L</th>
                <th>P/VP</th>
                <th>PSR</th>
                <th>Div.Yield</th>
                <th>P/Ativo</th>
                <th>P/Cap.Giro</th>
                <th>P/EBIT</th>
                <th>P/Ativ Circ.Liq</th>
                <th>EV/EBIT</th>
                <th>EV/EBITDA</th>
                <th>Mrg Ebit</th>
                <th>Mrg. Líq.</th>
                <th>Liq. Corr.</th>
                <th>ROIC</th>
                <th>ROE</th>
                <th>Liq.2meses</th>
                <th>Patrim. Líq</th>
                <th>Dív.Brut/ Patrim.</th>
                <th>Cresc. Rec.5a</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>ABEV3</td>
                <td>15,00</td>
                <td>12,50</td>
                <td>1,80</td>
                <td>2,30</td>
                <td>0,035</td>
                <td>0,1</td>
                <td>0,2</td>
                <td>0,3</td>
                <td>0,4</td>
                <td>0,5</td>
                <td>0,6</td>
                <td>0,7</td>
                <td>0,8</td>
                <td>0,9</td>
                <td>1,0</td>
                <td>1,1</td>
                <td>1,2</td>
                <td>1,3</td>
                <td>1,4</td>
                <td>1,5</td>
            </tr>
        </tbody>
    </table>
    """

    async def fake_get(*args, **kwargs):
        class R:
            text = mock_html
            status_code = 200

            def raise_for_status(self):
                return None

        return R()

    with patch("api.fundamentus.httpx.AsyncClient.get", new=AsyncMock(side_effect=fake_get)):
        # chamamos a função original (por baixo do decorator) para evitar cache
        result = asyncio.run(get_data.__wrapped__())
        assert "ABEV3" in result
        # checa alguns campos
        assert result["ABEV3"]["Cotação"] == Decimal("15.00")
        assert result["ABEV3"]["P/L"] == Decimal("12.50")


def test_ignores_short_rows():
    # Uma linha com menos de 21 colunas deve ser ignorada (cobrir branch continue)
    mock_html = """
    <table id="resultado">
        <thead>
            <tr>
                <th>Papel</th>
                <th>Cotação</th>
                <th>P/L</th>
                <th>P/VP</th>
                <th>PSR</th>
                <th>Div.Yield</th>
                <th>P/Ativo</th>
                <th>P/Cap.Giro</th>
                <th>P/EBIT</th>
                <th>P/Ativ Circ.Liq</th>
                <th>EV/EBIT</th>
                <th>EV/EBITDA</th>
                <th>Mrg Ebit</th>
                <th>Mrg. Líq.</th>
                <th>Liq. Corr.</th>
                <th>ROIC</th>
                <th>ROE</th>
                <th>Liq.2meses</th>
                <th>Patrim. Líq</th>
                <th>Dív.Brut/ Patrim.</th>
                <th>Cresc. Rec.5a</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>SHORT</td>
                <td>1,00</td>
                <td>2,00</td>
            </tr>
            <tr>
                <td>ABEV3</td>
                <td>15,00</td>
                <td>12,50</td>
                <td>1,80</td>
                <td>2,30</td>
                <td>0,035</td>
                <td>0,1</td>
                <td>0,2</td>
                <td>0,3</td>
                <td>0,4</td>
                <td>0,5</td>
                <td>0,6</td>
                <td>0,7</td>
                <td>0,8</td>
                <td>0,9</td>
                <td>1,0</td>
                <td>1,1</td>
                <td>1,2</td>
                <td>1,3</td>
                <td>1,4</td>
                <td>1,5</td>
            </tr>
        </tbody>
    </table>
    """

    async def fake_get(*args, **kwargs):
        class R:
            text = mock_html

            def raise_for_status(self):
                return None

        return R()

    with patch("api.fundamentus.httpx.AsyncClient.get", new=AsyncMock(side_effect=fake_get)):
        result = asyncio.run(get_data())
        # garante que a linha SHORT foi ignorada e ABEV3 processada
        assert "SHORT" not in result
        assert "ABEV3" in result
