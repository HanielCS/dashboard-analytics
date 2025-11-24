from fastapi.testclient import TestClient
from models import VendaCreate

def test_criar_e_listar_venda(client: TestClient):
    payload = {
        "data": "25/12",
        "categoria": "Teste",
        "vendas": 500,
        "qtd_pedidos": 10
    }
    response = client.post("/api/dados", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["categoria"] == "Teste"
    assert "id" in data

    response = client.get("/api/dados")
    assert response.status_code == 200
    lista = response.json()
    
    assert len(lista) > 0
    assert lista[0]["categoria"] == "Teste"

def test_atualizar_e_deletar_venda(client: TestClient):
    payload = {
        "data": "01/01",
        "categoria": "Original",
        "vendas": 100,
        "qtd_pedidos": 1
    }
    res_create = client.post("/api/dados", json=payload)
    venda_id = res_create.json()["id"]

    novo_payload = {
        "data": "01/01",
        "categoria": "Atualizado",
        "vendas": 200,
        "qtd_pedidos": 2
    }
    res_update = client.put(f"/api/dados/{venda_id}", json=novo_payload)
    
    assert res_update.status_code == 200
    assert res_update.json()["categoria"] == "Atualizado"
    assert res_update.json()["vendas"] == 200

    res_delete = client.delete(f"/api/dados/{venda_id}")
    assert res_delete.status_code == 200
    
    res_list = client.get("/api/dados")
    vendas = res_list.json()
    assert not any(v["id"] == venda_id for v in vendas)