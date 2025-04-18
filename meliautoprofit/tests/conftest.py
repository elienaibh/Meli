"""
Fixtures e configurações para testes
"""
import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Adiciona o diretório raiz ao caminho para importar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import Base
from database.models import Fornecedor, Produto, StatusProduto
from app.config import setup_logger

# Configuração de logger
logger = setup_logger(__name__)

# Banco de dados em memória para testes
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def test_db():
    """Fixture para criar um banco de dados de teste em memória"""
    engine = create_engine(TEST_DATABASE_URL)
    
    # Cria todas as tabelas no banco de dados de teste
    Base.metadata.create_all(bind=engine)
    
    # Cria uma sessão de teste
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    
    try:
        # Adiciona dados de teste
        _criar_dados_teste(db)
        
        # Retorna a sessão para os testes
        yield db
    finally:
        # Limpa os dados e fecha a sessão após o teste
        db.close()
        Base.metadata.drop_all(bind=engine)

def _criar_dados_teste(db):
    """Cria dados de teste no banco de dados"""
    # Cria fornecedores
    fornecedores = [
        Fornecedor(
            nome="CJ Dropshipping (Test)",
            api_type="cj_dropshipping"
        ),
        Fornecedor(
            nome="Spocket (Test)",
            api_type="spocket"
        )
    ]
    
    # Adiciona fornecedores ao banco
    for fornecedor in fornecedores:
        db.add(fornecedor)
    
    db.commit()
    
    # Cria produtos de teste
    produtos = [
        Produto(
            titulo="Produto Teste 1",
            descricao="Descrição do produto teste 1",
            preco_custo=50.0,
            preco_venda=99.0,
            margem=0.98,
            estoque=10,
            categoria="Testes",
            sku="TESTE-001",
            fornecedor_id=1,
            fornecedor_product_id="CJ123456-TESTE",
            status=StatusProduto.ATIVO
        ),
        Produto(
            titulo="Produto Teste 2",
            descricao="Descrição do produto teste 2",
            preco_custo=75.0,
            preco_venda=149.0,
            margem=0.98,
            estoque=5,
            categoria="Testes",
            sku="TESTE-002",
            fornecedor_id=2,
            fornecedor_product_id="SP123456-TESTE",
            status=StatusProduto.PENDENTE
        )
    ]
    
    # Adiciona produtos ao banco
    for produto in produtos:
        db.add(produto)
    
    db.commit()
    
    logger.info("Dados de teste criados com sucesso") 