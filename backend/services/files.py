import pandas as pd
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlmodel import Session
from database import engine
from models import VendaDiaria
from .crud import listar_vendas, limpar_cache

def importar_csv(conteudo: bytes):
    try:
        df = pd.read_csv(io.BytesIO(conteudo))
        cols = {'data', 'categoria', 'vendas', 'qtd_pedidos'}
        if not cols.issubset(df.columns):
            return {"erro": f"Colunas inválidas. Necessário: {cols}"}

        with Session(engine) as session:
            objs = []
            for _, row in df.iterrows():
                try:
                    objs.append(VendaDiaria(
                        data=str(row['data']),
                        categoria=str(row['categoria']),
                        vendas=float(row['vendas']),
                        qtd_pedidos=int(row['qtd_pedidos'])
                    ))
                except: continue
            
            if not objs: return {"erro": "Nenhum dado válido."}
            
            session.add_all(objs)
            session.commit()
            limpar_cache()
            
        return {"mensagem": f"{len(objs)} vendas importadas!"}
    except Exception as e:
        return {"erro": str(e)}

def gerar_excel(inicio: str, fim: str):
    vendas = listar_vendas(inicio, fim)
    df = pd.DataFrame([v.dict(exclude={'id'}) for v in vendas])
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Vendas')
    output.seek(0)
    return output

def gerar_pdf(inicio: str, fim: str):
    vendas = listar_vendas(inicio, fim)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, "Relatório de Vendas")
    p.setFont("Helvetica", 10)
    p.drawString(50, 730, f"Período: {inicio} a {fim}")
    
    y = 700
    total = 0
    for v in vendas:
        if y < 50: p.showPage(); y = 750
        p.drawString(50, y, f"{v.data} | {v.categoria} | Qtd: {v.qtd_pedidos} | R$ {v.vendas:.2f}")
        total += v.vendas
        y -= 20
        
    p.drawString(50, y-10, f"TOTAL: R$ {total:.2f}")
    p.save()
    buffer.seek(0)
    return buffer