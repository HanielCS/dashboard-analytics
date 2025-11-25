from fastapi import APIRouter, Query, UploadFile, File, status
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Optional
import base64
from services import (
    criar_venda, listar_vendas, atualizar_venda, deletar_venda, 
    gerar_excel, gerar_pdf, gerar_predicao, gerar_kpis
)
from tasks import processar_importacao_csv
from models import VendaCreate, VendaDiaria

router = APIRouter()

# VENDAS (CRUD)

@router.post(
    "/dados", 
    response_model=VendaDiaria, 
    status_code=status.HTTP_201_CREATED,
    tags=["Vendas"],
    summary="Criar nova venda",
    description="Registra uma nova venda no banco de dados com os detalhes fornecidos."
)
def post_venda(venda: VendaCreate):
    return criar_venda(venda)

@router.get(
    "/dados", 
    tags=["Vendas"],
    summary="Listar vendas",
    description="Retorna a lista de vendas. Suporta filtros por data e paginação."
)
def get_dados(
    inicio: Optional[str] = Query(None, description="Data inicial (YYYY-MM-DD)"), 
    fim: Optional[str] = Query(None, description="Data final (YYYY-MM-DD)"),
    page: Optional[int] = Query(None, ge=1, description="Número da página"),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Itens por página")
):
    """
    * Se `page` e `limit` forem fornecidos, retorna objeto paginado.
    * Se `inicio` e `fim` forem fornecidos, filtra por data.
    * Caso contrário, retorna a lista completa.
    """
    return listar_vendas(inicio, fim, page, limit)

@router.put(
    "/dados/{venda_id}", 
    response_model=VendaDiaria,
    tags=["Vendas"],
    summary="Atualizar venda",
    description="Atualiza os dados de uma venda existente pelo ID."
)
def put_venda(venda_id: int, venda: VendaCreate):
    resultado = atualizar_venda(venda_id, venda)
    if resultado:
        return resultado
    return JSONResponse(status_code=404, content={"error": "Venda não encontrada"})

@router.delete(
    "/dados/{venda_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Vendas"],
    summary="Excluir venda",
    description="Remove permanentemente uma venda do banco de dados."
)
def delete_venda(venda_id: int):
    sucesso = deletar_venda(venda_id)
    if not sucesso:
        return JSONResponse(status_code=404, content={"error": "Venda não encontrada"})
    return 

# BI & ANALYTICS

@router.get(
    "/kpis", 
    tags=["BI & Analytics"],
    summary="Obter KPIs",
    description="Retorna totais (Vendas, Pedidos, Ticket Médio) e a variação percentual em relação ao período anterior."
)
def get_kpis(
    inicio: Optional[str] = Query(None, description="Data inicial"), 
    fim: Optional[str] = Query(None, description="Data final")
):
    return gerar_kpis(inicio, fim)

@router.get(
    "/predicao", 
    tags=["BI & Analytics"],
    summary="Previsão de Vendas (IA)",
    description="Utiliza o algoritmo ARIMA para projetar as vendas dos próximos 7 dias."
)
def get_predicao():
    return gerar_predicao()

# GRUPO: ARQUIVOS

@router.get(
    "/export/excel", 
    tags=["Arquivos"],
    summary="Download Excel",
    description="Gera e baixa um arquivo .xlsx com as vendas do período selecionado."
)
def export_excel(inicio: str = Query(...), fim: str = Query(...)):
    arquivo = gerar_excel(inicio, fim)
    headers = {'Content-Disposition': 'attachment; filename="relatorio_vendas.xlsx"'}
    return StreamingResponse(arquivo, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers=headers)

@router.get(
    "/export/pdf", 
    tags=["Arquivos"],
    summary="Download PDF",
    description="Gera e baixa um arquivo .pdf com o relatório de vendas do período."
)
def export_pdf(inicio: str = Query(...), fim: str = Query(...)):
    arquivo = gerar_pdf(inicio, fim)
    headers = {'Content-Disposition': 'attachment; filename="relatorio_vendas.pdf"'}
    return StreamingResponse(arquivo, media_type='application/pdf', headers=headers)

@router.post(
    "/import/csv", 
    tags=["Arquivos"],
    summary="Importar CSV (Background Task)",
    description="Recebe um arquivo CSV, converte para Base64 e envia para processamento assíncrono no Celery.",
    status_code=status.HTTP_202_ACCEPTED
)
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        return JSONResponse(status_code=400, content={"erro": "Apenas arquivos .csv são permitidos"})
    
    conteudo_bytes = await file.read()
    conteudo_b64 = base64.b64encode(conteudo_bytes).decode('utf-8')
    
    # Envia para a fila (Retorna instantaneamente)
    task = processar_importacao_csv.delay(conteudo_b64)
    
    return {
        "mensagem": "Arquivo recebido! O processamento iniciou em segundo plano.",
        "task_id": task.id,
        "status": "processando"
    }