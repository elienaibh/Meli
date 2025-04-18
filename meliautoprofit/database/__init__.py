"""
Pacote de banco de dados
"""
from .database import Base, engine, SessionLocal, get_db, init_db
from .models import (
    Produto, 
    Fornecedor, 
    Cliente, 
    Endereco, 
    Pedido, 
    PedidoItem, 
    Relatorio, 
    StatusProduto, 
    StatusPedido
)
from .repository import (
    ProdutoRepository,
    FornecedorRepository,
    PedidoRepository,
    ClienteRepository
)

"""
Inicialização do banco de dados
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Base para os modelos SQLAlchemy
Base = declarative_base()

# URL do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./meliautoprofit.db")

# Cria o engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Configuração da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Função para obter uma sessão do banco de dados.
    Deve ser usada como uma dependência no FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Inicializa o banco de dados criando todas as tabelas definidas nos modelos.
    """
    from . import models  # Importação circular, então importamos aqui
    Base.metadata.create_all(bind=engine) 