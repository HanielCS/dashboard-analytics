from celery_worker import celery_app
from sqlmodel import Session
from database import engine
from models import VendaDiaria
from services import limpar_cache
import pandas as pd
import io
import base64

@celery_app.task(name="tasks.processar_importacao_csv")
def processar_importacao_csv(conteudo_base64: str):
    """
    Recebe o arquivo em Base64 (Celery não gosta de bytes puros),
    decodifica e insere no banco.
    """
    print("🐇 Celery: Iniciando processamento do CSV...")
    
    try:
        conteudo = base64.b64decode(conteudo_base64)
        
        df = pd.read_csv(io.BytesIO(conteudo))
        
        required_cols = {'data', 'categoria', 'vendas', 'qtd_pedidos'}
        if not required_cols.issubset(df.columns):
            return {"status": "erro", "msg": "Colunas incorretas"}

        with Session(engine) as session:
            novas_vendas = []
            for _, row in df.iterrows():
                try:
                    venda = VendaDiaria(
                        data=str(row['data']),
                        categoria=str(row['categoria']),
                        vendas=float(row['vendas']),
                        qtd_pedidos=int(row['qtd_pedidos'])
                    )
                    novas_vendas.append(venda)
                except: continue

            session.add_all(novas_vendas)
            session.commit()
            
            limpar_cache()
            
        print(f"✅ Celery: {len(novas_vendas)} vendas importadas!")
        return {"status": "sucesso", "qtd": len(novas_vendas)}

    except Exception as e:
        print(f"❌ Celery Erro: {e}")
        return {"status": "erro", "msg": str(e)}