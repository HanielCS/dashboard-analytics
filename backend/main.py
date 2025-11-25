from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes import router as vendas_router
from database import create_db_and_tables
from services.crud import criar_dados_iniciais
import time
from sqlalchemy.exc import OperationalError
from prometheus_fastapi_instrumentator import Instrumentator

# CONFIGURAÇÃO DE METADADOS DA API
description = """
API do Dashboard Executivo de Vendas. 🚀

## Funcionalidades
* **CRUD de Vendas**: Criar, ler, atualizar e deletar registros.
* **Dashboard & KPIs**: Cálculos de totais e variações percentuais.
* **Predição (IA)**: Previsão de vendas futuras usando ARIMA.
* **Importação/Exportação**: Suporte a CSV, Excel e PDF.

## Autores
* **Haniel Carvalho** - *Desenvolvedor Full Stack*
"""

tags_metadata = [
    {
        "name": "Vendas",
        "description": "Operações de CRUD para gestão de vendas diárias.",
    },
    {
        "name": "BI & Analytics",
        "description": "Endpoints de inteligência de dados, KPIs e predições.",
    },
    {
        "name": "Arquivos",
        "description": "Upload de CSV e download de relatórios (PDF/Excel).",
    },
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    max_retries = 10
    for i in range(max_retries):
        try:
            print(f"Tentativa de conexão com o banco {i+1}/{max_retries}...")
            create_db_and_tables()
            criar_dados_iniciais()
            print("✅ Sucesso! Banco conectado.")
            break
        except OperationalError:
            if i < max_retries - 1:
                print("⏳ Aguardando banco...")
                time.sleep(2)
            else:
                print("❌ Erro: Banco indisponível.")
                raise
    yield
    print("🛑 Desligando...")

# INICIALIZAÇÃO COM DOCUMENTAÇÃO
app = FastAPI(
    title="Dashboard Analytics API",
    description=description,
    version="1.0.0",
    openapi_tags=tags_metadata,
    lifespan=lifespan,
    contact={
        "name": "Haniel Carvalho",
        "email": "carvalho.hanielx@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
)

Instrumentator().instrument(app).expose(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vendas_router, prefix="/api")