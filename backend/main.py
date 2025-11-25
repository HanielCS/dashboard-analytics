from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes import router as vendas_router
from database import create_db_and_tables
from services.crud import criar_dados_iniciais
import time
from sqlalchemy.exc import OperationalError
from prometheus_fastapi_instrumentator import Instrumentator

@asynccontextmanager
async def lifespan(app: FastAPI):
    max_retries = 10
    for i in range(max_retries):
        try:
            print(f"Tentativa de conexão com o banco {i+1}/{max_retries}...")
            create_db_and_tables()
            criar_dados_iniciais()
            print("✅ Sucesso! Banco conectado e dados inicializados.")
            break
        except OperationalError:
            if i < max_retries - 1:
                print("⏳ Banco de dados ainda iniciando... aguardando 2 segundos.")
                time.sleep(2)
            else:
                print("❌ Erro: O Banco de dados demorou muito para responder.")
                raise
    
    yield
    
    print("🛑 Desligando aplicação...")

app = FastAPI(lifespan=lifespan)

# Configura Prometheus
Instrumentator().instrument(app).expose(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vendas_router, prefix="/api", tags=["Vendas"])