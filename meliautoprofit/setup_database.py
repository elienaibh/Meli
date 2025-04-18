"""
Script para inicializar o banco de dados
"""
import os
import sys
import logging
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("meliautoprofit.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Adiciona o diretório atual ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importa os módulos do projeto
from database import Base, engine, SessionLocal, init_db
from database.models import Fornecedor, Produto, StatusProduto, Cliente, Endereco

# Carrega variáveis de ambiente
load_dotenv()

def create_tables():
    """Cria as tabelas no banco de dados"""
    logger.info("Criando tabelas no banco de dados")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tabelas criadas com sucesso")
        return True
    except Exception as e:
        logger.error(f"Erro ao criar tabelas: {str(e)}")
        return False

def insert_initial_data():
    """Insere dados iniciais no banco de dados"""
    logger.info("Inserindo dados iniciais")
    
    try:
        db = SessionLocal()
        
        # Verifica se já existem fornecedores
        if db.query(Fornecedor).count() == 0:
            logger.info("Inserindo fornecedores")
            
            # Cria fornecedores
            fornecedores = [
                Fornecedor(
                    nome="CJ Dropshipping",
                    api_type="cj_dropshipping"
                ),
                Fornecedor(
                    nome="Spocket",
                    api_type="spocket"
                )
            ]
            
            # Adiciona fornecedores ao banco
            for fornecedor in fornecedores:
                db.add(fornecedor)
            
            db.commit()
            logger.info(f"{len(fornecedores)} fornecedores inseridos")
        else:
            logger.info("Fornecedores já existem no banco")
        
        # Verifica se já existem produtos
        if db.query(Produto).count() == 0:
            logger.info("Inserindo produtos de exemplo")
            
            # Obtém os fornecedores
            cj_dropshipping = db.query(Fornecedor).filter_by(api_type="cj_dropshipping").first()
            spocket = db.query(Fornecedor).filter_by(api_type="spocket").first()
            
            # Cria produtos
            produtos = [
                Produto(
                    titulo="Fone JBL T110",
                    descricao="Fone de ouvido com fio JBL T110, preto, com microfone",
                    preco_custo=80.0,
                    preco_venda=120.0,
                    margem=0.33,
                    estoque=10,
                    categoria="Eletrônicos",
                    sku="FN-JBL-T110",
                    fornecedor_id=cj_dropshipping.id,
                    fornecedor_product_id="CJ123456",
                    status=StatusProduto.PENDENTE
                ),
                Produto(
                    titulo="Smartwatch X7",
                    descricao="Relógio inteligente X7, monitor cardíaco, resistente à água",
                    preco_custo=95.0,
                    preco_venda=159.0,
                    margem=0.40,
                    estoque=5,
                    categoria="Eletrônicos",
                    sku="SW-X7-BLK",
                    fornecedor_id=cj_dropshipping.id,
                    fornecedor_product_id="CJ789012",
                    status=StatusProduto.PENDENTE
                ),
                Produto(
                    titulo="Carregador Portátil 10000mAh",
                    descricao="Power bank 10000mAh, 2 portas USB, carregamento rápido",
                    preco_custo=45.0,
                    preco_venda=89.0,
                    margem=0.49,
                    estoque=15,
                    categoria="Eletrônicos",
                    sku="PB-10K-BLK",
                    fornecedor_id=spocket.id,
                    fornecedor_product_id="SP123456",
                    status=StatusProduto.PENDENTE
                )
            ]
            
            # Adiciona produtos ao banco
            for produto in produtos:
                db.add(produto)
            
            db.commit()
            logger.info(f"{len(produtos)} produtos inseridos")
        else:
            logger.info("Produtos já existem no banco")
        
        # Verifica se já existem clientes
        if db.query(Cliente).count() == 0:
            logger.info("Inserindo cliente de exemplo")
            
            # Cria cliente
            cliente = Cliente(
                ml_user_id="ML12345678",
                nome="Cliente Teste",
                email="cliente@teste.com",
                telefone="(11) 98765-4321"
            )
            
            db.add(cliente)
            db.commit()
            
            # Cria endereço para o cliente
            endereco = Endereco(
                cliente_id=cliente.id,
                rua="Avenida Paulista",
                numero="1000",
                complemento="Apto 123",
                bairro="Bela Vista",
                cidade="São Paulo",
                estado="SP",
                cep="01310-100",
                is_principal=True
            )
            
            db.add(endereco)
            db.commit()
            
            logger.info("Cliente e endereço inseridos")
        else:
            logger.info("Clientes já existem no banco")
        
        db.close()
        logger.info("Dados iniciais inseridos com sucesso")
        return True
    
    except Exception as e:
        logger.error(f"Erro ao inserir dados iniciais: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("Inicializando banco de dados")
    
    if not init_db():
        logger.error("Falha ao inicializar banco de dados")
        sys.exit(1)
    
    if not create_tables():
        logger.error("Falha ao criar tabelas")
        sys.exit(1)
    
    if not insert_initial_data():
        logger.error("Falha ao inserir dados iniciais")
        sys.exit(1)
    
    logger.info("Banco de dados inicializado com sucesso")
    sys.exit(0) 