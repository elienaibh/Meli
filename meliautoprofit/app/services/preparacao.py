"""
Serviço para preparação do lançamento
"""
import csv
import os
import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from ..config import setup_logger
from ...database.models import Produto, Fornecedor, StatusProduto
from ...database.repository import ProdutoRepository, FornecedorRepository

# Configuração de logger
logger = setup_logger(__name__)

class PreparacaoService:
    """Serviço para preparação do lançamento"""
    
    def __init__(self, db: Session):
        """Inicializa o serviço de preparação"""
        self.db = db
        self.produto_repo = ProdutoRepository(db)
        self.fornecedor_repo = FornecedorRepository(db)
    
    def importar_produtos_csv(self, caminho_arquivo: str) -> int:
        """Importa produtos de um arquivo CSV"""
        logger.info(f"Importando produtos do arquivo {caminho_arquivo}")
        
        if not os.path.exists(caminho_arquivo):
            logger.error(f"Arquivo não encontrado: {caminho_arquivo}")
            return 0
        
        # Obtém os fornecedores
        fornecedores = {f.api_type: f.id for f in self.fornecedor_repo.list_all()}
        
        if not fornecedores:
            logger.error("Nenhum fornecedor cadastrado")
            return 0
        
        produtos_inseridos = 0
        
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    # Verifica se o produto já existe
                    if row.get('sku') and self.produto_repo.get_by_sku(row['sku']):
                        logger.warning(f"Produto com SKU '{row['sku']}' já existe. Pulando.")
                        continue
                    
                    # Verifica se o fornecedor existe
                    fornecedor_type = row.get('fornecedor')
                    if fornecedor_type not in fornecedores:
                        logger.warning(f"Fornecedor '{fornecedor_type}' não encontrado. Pulando produto '{row.get('titulo')}'")
                        continue
                    
                    # Cria o produto
                    try:
                        preco_custo = float(row.get('preco_custo', 0))
                        preco_venda = float(row.get('preco_venda', 0))
                        
                        # Calcula margem se não for informada
                        if row.get('margem'):
                            margem = float(row['margem'])
                        else:
                            margem = (preco_venda - preco_custo) / preco_custo if preco_custo > 0 else 0
                        
                        # Cria o produto
                        produto = {
                            "titulo": row.get('titulo', ''),
                            "descricao": row.get('descricao', ''),
                            "preco_custo": preco_custo,
                            "preco_venda": preco_venda,
                            "margem": margem,
                            "estoque": int(row.get('estoque', 10)),
                            "categoria": row.get('categoria', ''),
                            "sku": row.get('sku', ''),
                            "fornecedor_id": fornecedores[fornecedor_type],
                            "fornecedor_product_id": row.get('fornecedor_product_id', ''),
                            "status": StatusProduto.PENDENTE
                        }
                        
                        # Salva o produto
                        self.produto_repo.create(produto)
                        produtos_inseridos += 1
                        logger.debug(f"Produto '{row.get('titulo')}' inserido com sucesso")
                    
                    except Exception as e:
                        logger.error(f"Erro ao inserir produto '{row.get('titulo')}': {str(e)}")
                
                logger.info(f"{produtos_inseridos} produtos inseridos com sucesso")
                return produtos_inseridos
        
        except Exception as e:
            logger.error(f"Erro ao importar produtos: {str(e)}")
            return 0
    
    def criar_produtos_teste(self, quantidade: int = 50) -> int:
        """Cria produtos de teste para o lançamento"""
        logger.info(f"Criando {quantidade} produtos de teste")
        
        # Obtém os fornecedores
        fornecedores = self.fornecedor_repo.list_all()
        
        if not fornecedores:
            logger.error("Nenhum fornecedor cadastrado")
            return 0
        
        produtos_inseridos = 0
        
        try:
            # Distribuir os produtos entre os fornecedores
            for i in range(1, quantidade + 1):
                fornecedor = fornecedores[i % len(fornecedores)]
                
                # Varia preços para ter diversidade
                preco_base = 50 + (i % 10) * 15
                preco_custo = preco_base
                preco_venda = preco_base * 1.8
                margem = (preco_venda - preco_custo) / preco_custo
                
                # Categorias alternadas
                categorias = ["Eletrônicos", "Casa", "Esportes", "Saúde", "Beleza"]
                categoria = categorias[i % len(categorias)]
                
                # Cria o produto
                produto = {
                    "titulo": f"Produto Teste {i} - {categoria}",
                    "descricao": f"Descrição detalhada do produto {i} na categoria {categoria}. Produto de alta qualidade para testar a plataforma.",
                    "preco_custo": preco_custo,
                    "preco_venda": preco_venda,
                    "margem": margem,
                    "estoque": 10 + (i % 20),
                    "categoria": categoria,
                    "sku": f"TESTE-{i:04d}",
                    "fornecedor_id": fornecedor.id,
                    "fornecedor_product_id": f"{fornecedor.api_type.upper()}-{i:04d}",
                    "status": StatusProduto.PENDENTE
                }
                
                # Salva o produto
                self.produto_repo.create(produto)
                produtos_inseridos += 1
                
                if i % 10 == 0:
                    logger.debug(f"Inseridos {i} produtos de {quantidade}")
            
            logger.info(f"{produtos_inseridos} produtos de teste inseridos com sucesso")
            return produtos_inseridos
        
        except Exception as e:
            logger.error(f"Erro ao criar produtos de teste: {str(e)}")
            return produtos_inseridos
    
    def fazer_backup_produtos(self, caminho_arquivo: str) -> bool:
        """Exporta produtos para um arquivo CSV como backup"""
        logger.info(f"Exportando produtos para {caminho_arquivo}")
        
        try:
            produtos = self.produto_repo.list_all(limit=1000)
            
            with open(caminho_arquivo, 'w', encoding='utf-8', newline='') as f:
                # Define os campos
                fieldnames = ['id', 'titulo', 'descricao', 'preco_custo', 'preco_venda', 
                             'margem', 'estoque', 'categoria', 'sku', 'ml_item_id', 
                             'fornecedor_id', 'fornecedor_product_id', 'status']
                
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for produto in produtos:
                    writer.writerow({
                        'id': produto.id,
                        'titulo': produto.titulo,
                        'descricao': produto.descricao,
                        'preco_custo': produto.preco_custo,
                        'preco_venda': produto.preco_venda,
                        'margem': produto.margem,
                        'estoque': produto.estoque,
                        'categoria': produto.categoria,
                        'sku': produto.sku,
                        'ml_item_id': produto.ml_item_id,
                        'fornecedor_id': produto.fornecedor_id,
                        'fornecedor_product_id': produto.fornecedor_product_id,
                        'status': produto.status.value if produto.status else None
                    })
            
            logger.info(f"Backup de {len(produtos)} produtos realizado com sucesso")
            return True
        
        except Exception as e:
            logger.error(f"Erro ao fazer backup dos produtos: {str(e)}")
            return False 