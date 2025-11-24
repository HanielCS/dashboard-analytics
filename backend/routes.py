from fastapi import APIRouter, Query, UploadFile, File
from fastapi.responses import StreamingResponse
from typing import Optional
import time
import base64

from tasks import processar_importacao_csv 

from services import (
    criar_venda, 
    listar_vendas, 
    atualizar_venda, 
    deletar_venda, 
    gerar_excel, 
    gerar_pdf, 
    gerar_predicao, 
    gerar_kpis
)
from models import VendaCreate

router = APIRouter()

# ROTA DE CRIAÇÃO (POST)
@router.post("/dados")
def post_venda(venda: VendaCreate):
    return criar_venda(venda)

# ROTA DE LISTAGEM (GET)
@router.get("/dados")
def get_dados(
    inicio: Optional[str] = Query(None), 
    fim: Optional[str] = Query(None),
    page: Optional[int] = Query(None),
    limit: Optional[int] = Query(None)
):
    return listar_vendas(inicio, fim, page, limit)

# ROTA DE ATUALIZAÇÃO (PUT)
@router.put("/dados/{venda_id}")
def put_venda(venda_id: int, venda: VendaCreate):
    resultado = atualizar_venda(venda_id, venda)
    if resultado:
        return resultado
    return {"error": "Venda não encontrada"}

# ROTA DE DELEÇÃO (DELETE)
@router.delete("/dados/{venda_id}")
def delete_venda(venda_id: int):
    sucesso = deletar_venda(venda_id)
    if sucesso:
        return {"message": "Deletado com sucesso"}
    return {"error": "Venda não encontrada"}

# ROTA DE KPIS (BI)
@router.get("/kpis")
def get_kpis(inicio: Optional[str] = Query(None), fim: Optional[str] = Query(None)):
    return gerar_kpis(inicio, fim)

# ROTA DE PREDIÇÃO (IA)
@router.get("/predicao")
def get_predicao():
    return gerar_predicao()

# ROTAS DE EXPORTAÇÃO
@router.get("/export/excel")
def export_excel(inicio: str = Query(...), fim: str = Query(...)):
    arquivo = gerar_excel(inicio, fim)
    headers = {'Content-Disposition': 'attachment; filename="relatorio_vendas.xlsx"'}
    return StreamingResponse(arquivo, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers=headers)

@router.get("/export/pdf")
def export_pdf(inicio: str = Query(...), fim: str = Query(...)):
    arquivo = gerar_pdf(inicio, fim)
    headers = {'Content-Disposition': 'attachment; filename="relatorio_vendas.pdf"'}
    return StreamingResponse(arquivo, media_type='application/pdf', headers=headers)

# ROTA DE IMPORTAÇÃO (CELERY / BACKGROUND TASK)
@router.post("/import/csv")
async def upload_csv(file: UploadFile = File(...)):
    """
    Recebe o arquivo, converte para Base64 e envia para o Celery processar em segundo plano.
    """
    if not file.filename.endswith('.csv'):
        return {"erro": "Apenas arquivos .csv são permitidos"}
    
    conteudo_bytes = await file.read()
    
    conteudo_b64 = base64.b64encode(conteudo_bytes).decode('utf-8')
    
    task = processar_importacao_csv.delay(conteudo_b64)
    
    return {
        "mensagem": "Arquivo recebido! O processamento iniciou em segundo plano.",
        "task_id": task.id,
        "status": "processando"
    }