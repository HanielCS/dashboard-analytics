import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

import database
from services import crud, files 
from models import VendaDiaria, VendaCreate

from main import app


# 1. CONFIGURAÇÃO DO BANCO DE DADOS DE TESTE (SQLite na Memória)
engine_test = create_engine(
    "sqlite://", 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

# Sobrescreve a engine do banco de dados para usar o banco de teste
database.engine = engine_test
crud.engine = engine_test
files.engine = engine_test

from main import app

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine_test)
    with Session(engine_test) as session:
        yield session
    SQLModel.metadata.drop_all(engine_test)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[database.get_session] = get_session_override
    
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()