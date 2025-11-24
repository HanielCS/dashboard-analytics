from typing import Optional
from sqlmodel import SQLModel, Field

class VendaBase(SQLModel):
    data: str
    vendas: float
    categoria: str
    qtd_pedidos: int

class VendaDiaria(VendaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class VendaCreate(VendaBase):
    pass