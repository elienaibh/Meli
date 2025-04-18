"""
Configuração do banco de dados
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import logging

# Configuração de logging
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

# URL de conexão com o banco
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./meliautoprofit.db")

# Cria engine do SQLAlchemy
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith('sqlite') else {},
    echo=os.getenv("SQL_ECHO", "False").lower() in ("true", "1", "t")
)

# Sessão para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

def get_db():
    """Função para obter uma sessão do banco"""
    db = SessionLocal()
    try:
        logger.debug("Iniciando sessão de banco de dados")
        yield db
    finally:
        logger.debug("Fechando sessão de banco de dados")
        db.close()

def init_db():
    """Inicializa o banco de dados com as tabelas"""
    logger.info("Inicializando banco de dados")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Banco de dados inicializado com sucesso")
        return True
    except Exception as e:
        logger.error(f"Erro ao inicializar banco de dados: {str(e)}")
        return False 