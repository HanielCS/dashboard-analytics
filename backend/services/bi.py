from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import math
from .crud import listar_vendas

def gerar_kpis(inicio: str = None, fim: str = None):
    if not inicio or not fim:
        hoje = datetime.now().date()
        inicio = datetime(hoje.year, hoje.month, 1).strftime("%Y-%m-%d")
        fim = hoje.strftime("%Y-%m-%d")

    dt_ini = datetime.strptime(inicio, "%Y-%m-%d")
    dt_fim = datetime.strptime(fim, "%Y-%m-%d")
    duracao = (dt_fim - dt_ini).days + 1
    
    prev_fim = (dt_ini - timedelta(days=1)).strftime("%Y-%m-%d")
    prev_ini = (dt_ini - timedelta(days=duracao)).strftime("%Y-%m-%d")

    atuais = listar_vendas(inicio, fim)
    anteriores = listar_vendas(prev_ini, prev_fim)

    def somar(lista):
        d = lista['data'] if isinstance(lista, dict) else lista
        vendas = sum(v.vendas for v in d)
        pedidos = sum(v.qtd_pedidos for v in d)
        return { "vendas": vendas, "pedidos": pedidos, "ticket": (vendas/pedidos) if pedidos > 0 else 0 }

    tot_at = somar(atuais)
    tot_ant = somar(anteriores)

    def delta(a, b): return ((a - b) / b * 100) if b != 0 else (0 if a == 0 else 100)

    return {
        "totais": tot_at,
        "variacao": { k: delta(tot_at[k], tot_ant[k]) for k in tot_at }
    }

def gerar_predicao():
    vendas = listar_vendas()
    if isinstance(vendas, dict): vendas = vendas['data']
    if len(vendas) < 5: return []

    try:
        df = pd.DataFrame([v.dict() for v in vendas])
        ano = datetime.now().year
        df['data'] = pd.to_datetime(df['data'] + f"/{ano}", format="%d/%m/%Y")
        
        df = df.groupby('data')['vendas'].sum().reset_index()
        df = df.set_index('data').resample('D').mean().interpolate()

        model = ARIMA(df['vendas'], order=(1,1,1))
        res = model.fit().forecast(steps=7)
        
        return [{
            "data": dt.strftime("%d/%m"),
            "vendas": round(max(0, val), 2),
            "tipo": "previsao"
        } for dt, val in res.items()]

    except Exception as e:
        print(f"Erro ARIMA: {e}")
        return []