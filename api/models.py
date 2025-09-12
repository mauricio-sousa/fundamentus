from pydantic import BaseModel, Field, ConfigDict
from typing import Dict

class Indicadores(BaseModel):
    cotacao: float = Field(alias="Cotação", description="Preço atual da ação.")
    p_l: float = Field(alias="P/L", description="Preço/Lucro: Preço da ação dividido pelo lucro por ação.")
    p_vp: float = Field(alias="P/VP", description="Preço/Valor Patrimonial: Preço da ação dividido pelo valor patrimonial por ação.")
    psr: float = Field(alias="PSR", description="Price to Sales Ratio: Preço da ação dividido pela receita por ação.")
    dy: float = Field(alias="Div.Yield", description="Dividend Yield: Rendimento do dividendo.")
    p_ativo: float = Field(alias="P/Ativo", description="Preço/Ativo: Preço da ação dividido pelo valor dos ativos por ação.")
    p_cap_giro: float = Field(alias="P/Cap.Giro", description="Preço/Capital de Giro: Preço da ação dividido pelo capital de giro por ação.")
    p_ebit: float = Field(alias="P/EBIT", description="Preço/EBIT: Preço da ação dividido pelo EBIT por ação.")
    p_acl: float = Field(alias="P/Ativ Circ.Liq", description="Preço/Ativo Circulante Líquido: Preço da ação dividido pelo ativo circulante líquido por ação.")
    ev_ebit: float = Field(alias="EV/EBIT", description="EV/EBIT: Valor da empresa dividido pelo EBIT.")
    ev_ebitda: float = Field(alias="EV/EBITDA", description="EV/EBITDA: Valor da empresa dividido pelo EBITDA.")
    mrg_ebit: float = Field(alias="Mrg Ebit", description="Margem EBIT: Margem de lucro antes dos juros e impostos.")
    mrg_liq: float = Field(alias="Mrg. Líq.", description="Margem Líquida: Margem de lucro líquido.")
    liq_corr: float = Field(alias="Liq. Corr.", description="Liquidez Corrente: Ativo circulante dividido pelo passivo circulante.")
    roic: float = Field(alias="ROIC", description="Return on Invested Capital: Retorno sobre o capital investido.")
    roe: float = Field(alias="ROE", description="Return on Equity: Retorno sobre o patrimônio líquido.")
    liq_2meses: float = Field(alias="Liq.2meses", description="Liquidez em 2 meses: Volume de negociação médio dos últimos 2 meses.")
    patrim_liq: float = Field(alias="Patrim. Líq", description="Patrimônio Líquido: Ativos totais menos passivos totais.")
    div_brut_patrim: float = Field(alias="Dív.Brut/ Patrim.", description="Dívida Bruta/Patrimônio: Dívida bruta dividida pelo patrimônio líquido.")
    cresc_rec_5a: float = Field(alias="Cresc. Rec.5a", description="Crescimento da Receita (média de 5 anos): Crescimento médio da receita nos últimos 5 anos.")

    model_config = ConfigDict(populate_by_name=True)

TickerData = Dict[str, Indicadores]
