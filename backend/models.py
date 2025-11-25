from typing import Optional
from sqlmodel import SQLModel, Field

# MODELO BASE
class VendaBase(SQLModel):
    data: str = Field(
        description="Data da venda no formato DD/MM", 
        schema_extra={"example": "25/12"}
    )
    vendas: float = Field(
        description="Valor monetário total das vendas", 
        schema_extra={"example": 1500.50}
    )
    categoria: str = Field(
        description="Categoria do produto vendido", 
        schema_extra={"example": "Eletrônicos"}
    )
    qtd_pedidos: int = Field(
        description="Quantidade de pedidos realizados no dia", 
        schema_extra={"example": 15}
    )

# MODELO DE TABELA (DB)
class VendaDiaria(VendaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

# MODELO DE CRIAÇÃO (DTO)
class VendaCreate(VendaBase):
    class Config:
        json_schema_extra = {
            "example": {
                "data": "01/01",
                "categoria": "Jogos",
                "vendas": 299.90,
                "qtd_pedidos": 3
            }
        }