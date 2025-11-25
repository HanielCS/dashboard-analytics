from sqlmodel import Session, select
from models import VendaDiaria, VendaCreate
from database import engine, redis_client
from datetime import datetime, timedelta
import random
import json
import math

# Configurações do Cache
CACHE_KEY = "todas_vendas"
CACHE_EXPIRE = 300 # 5 minutos

def limpar_cache():
    try:
        print("🧹 Limpando cache do Redis...")
        redis_client.delete(CACHE_KEY)
    except Exception as e:
        print(f"⚠️ Aviso: Cache redis: {e}")

def criar_dados_iniciais():
    with Session(engine) as session:
        results = session.exec(select(VendaDiaria)).first()
        if not results:
            print("Criando dados iniciais REALISTAS...")
            categorias = ['Eletrônicos', 'Roupas', 'Casa', 'Livros', 'Jogos']
            hoje = datetime.now()
            
            for i in range(30, -1, -1):
                data_loop = hoje - timedelta(days=i)
                base = 500 + (30 - i) * 10 
                venda = VendaDiaria(
                    data=data_loop.strftime("%d/%m"),
                    vendas=float(max(50, base + random.randint(-100, 300))),
                    categoria=random.choice(categorias),
                    qtd_pedidos=random.randint(3, 15)
                )
                session.add(venda)
            session.commit()
            limpar_cache()

def listar_vendas(inicio: str = None, fim: str = None, page: int = None, limit: int = None):
    # 1. Cache
    lista_completa = []
    usou_cache = False

    if not inicio and not fim:
        try:
            dados = redis_client.get(CACHE_KEY)
            if dados:
                lista_completa = [VendaDiaria(**i) for i in json.loads(dados)]
                usou_cache = True
        except: pass

    if not usou_cache:
        with Session(engine) as session:
            lista_completa = list(session.exec(select(VendaDiaria)).all())
            if not inicio and not fim:
                try:
                    redis_client.set(CACHE_KEY, json.dumps([v.model_dump() for v in lista_completa]), ex=CACHE_EXPIRE)
                except: pass

    # 2. Filtros
    vendas_filtradas = []
    ano = datetime.now().year
    dt_ini, dt_fim = None, None

    if inicio and fim:
        try:
            dt_ini = datetime.strptime(inicio, "%Y-%m-%d").date()
            dt_fim = datetime.strptime(fim, "%Y-%m-%d").date()
        except: pass

    for v in lista_completa:
        try:
            dt_venda = datetime.strptime(f"{v.data}/{ano}", "%d/%m/%Y").date()
            if dt_ini and dt_fim:
                if dt_ini <= dt_venda <= dt_fim: vendas_filtradas.append(v)
            else:
                vendas_filtradas.append(v)
        except: continue

    # 3. Ordenação
    vendas_ordenadas = sorted(vendas_filtradas, key=lambda v: datetime.strptime(v.data, "%d/%m"))

    # 4. Paginação
    if page is not None and limit is not None:
        total = len(vendas_ordenadas)
        return {
            "data": vendas_ordenadas[(page-1)*limit : (page-1)*limit + limit],
            "total": total,
            "pages": math.ceil(total / limit),
            "current_page": page
        }

    return vendas_ordenadas

def criar_venda(dados: VendaCreate):
    with Session(engine) as session:
        db_venda = VendaDiaria.model_validate(dados)
        session.add(db_venda)
        session.commit()
        session.refresh(db_venda)
        limpar_cache()
        return db_venda

def atualizar_venda(id: int, dados: VendaCreate):
    with Session(engine) as session:
        db_venda = session.get(VendaDiaria, id)
        if not db_venda: return None
        
        for key, value in dados.model_dump(exclude_unset=True).items():
            setattr(db_venda, key, value)
            
        session.add(db_venda)
        session.commit()
        session.refresh(db_venda)
        limpar_cache()
        return db_venda

def deletar_venda(id: int):
    with Session(engine) as session:
        venda = session.get(VendaDiaria, id)
        if venda:
            session.delete(venda)
            session.commit()
            limpar_cache()
            return True
        return False