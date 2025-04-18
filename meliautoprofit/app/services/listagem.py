"""
Serviço de listagem automática de produtos
"""
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from ..config import setup_logger, ML_ITEMS_PER_DAY, ML_MARGIN_PERCENTAGE
from ..api.mercado_livre import MercadoLivreAPI
from ..api.fornecedor import FornecedorAPI, FornecedorType
from ...database.repository import ProdutoRepository, FornecedorRepository
from ...database.models import StatusProduto, Produto

# Configuração de logger
logger = setup_logger(__name__)

class ListagemService:
    """Serviço para listagem automática de produtos no Mercado Livre"""
    
    def __init__(self, db: Session):
        """Inicializa o serviço de listagem"""
        self.db = db
        self.ml_api = MercadoLivreAPI()
        self.fornecedor_api = FornecedorAPI()
        self.produto_repo = ProdutoRepository(db)
        self.fornecedor_repo = FornecedorRepository(db)
    
    def buscar_tendencias(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Busca as tendências de produtos no Mercado Livre"""
        logger.info(f"Buscando top {limit} tendências no Mercado Livre")
        
        try:
            # Obtém as tendências de busca do Mercado Livre
            trends = self.ml_api.get_trends(limit=limit)
            
            if not trends:
                logger.warning("Nenhuma tendência encontrada")
                return []
            
            logger.info(f"Encontradas {len(trends)} tendências")
            return trends
        
        except Exception as e:
            logger.error(f"Erro ao buscar tendências: {str(e)}")
            return []
    
    def buscar_produtos_fornecedor(self, keyword: str, fornecedor_type: FornecedorType) -> List[Dict[str, Any]]:
        """Busca produtos no fornecedor com base em uma palavra-chave"""
        logger.info(f"Buscando produtos com keyword '{keyword}' no fornecedor {fornecedor_type}")
        
        try:
            # Define o fornecedor a ser usado
            self.fornecedor_api.set_fornecedor(fornecedor_type)
            
            # Busca produtos no fornecedor
            produtos = self.fornecedor_api.search_products(keyword)
            
            if not produtos:
                logger.warning(f"Nenhum produto encontrado para '{keyword}' no fornecedor {fornecedor_type}")
                return []
            
            logger.info(f"Encontrados {len(produtos)} produtos para '{keyword}'")
            return produtos
        
        except Exception as e:
            logger.error(f"Erro ao buscar produtos no fornecedor: {str(e)}")
            return []
    
    def selecionar_melhor_produto(self, produtos: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Seleciona o melhor produto da lista baseado em critérios como preço, avaliação, etc."""
        if not produtos:
            return None
        
        # Implementação básica: seleciona o produto com melhor margem potencial
        # Em uma implementação real, consideraria outros fatores como avaliações, tempo de entrega, etc.
        melhor_produto = None
        melhor_score = -1
        
        for produto in produtos:
            preco = produto.get("price", 0)
            avaliacao = produto.get("rating", 0)
            estoque = produto.get("stock", 0)
            
            if preco <= 0 or estoque <= 0:
                continue
            
            # Cálculo simplificado de score
            score = (avaliacao * 0.6) + (estoque * 0.4)
            
            if score > melhor_score:
                melhor_score = score
                melhor_produto = produto
        
        if melhor_produto:
            logger.info(f"Melhor produto selecionado: {melhor_produto.get('name', 'Desconhecido')}")
        else:
            logger.warning("Nenhum produto adequado encontrado")
        
        return melhor_produto
    
    def criar_anuncio_ml(self, produto_fornecedor: Dict[str, Any], fornecedor_id: int) -> Optional[Dict[str, Any]]:
        """Cria um anúncio no Mercado Livre com base em um produto do fornecedor"""
        try:
            # Calcula preço de venda com margem
            preco_custo = produto_fornecedor.get("price", 0)
            if preco_custo <= 0:
                logger.warning("Produto com preço inválido")
                return None
            
            margem = ML_MARGIN_PERCENTAGE  # Percentual de margem definido na configuração
            preco_venda = preco_custo * (1 + margem)
            
            # Monta dados do anúncio
            item_data = {
                "title": produto_fornecedor.get("name", ""),
                "category_id": "MLB1051",  # Categoria padrão (deve ser adaptada)
                "price": preco_venda,
                "currency_id": "BRL",
                "available_quantity": min(produto_fornecedor.get("stock", 10), 50),  # Limita a 50 unidades
                "buying_mode": "buy_it_now",
                "condition": "new",
                "listing_type_id": "gold_special",  # Tipo de listagem
                "description": {
                    "plain_text": produto_fornecedor.get("description", "")
                },
                "pictures": [
                    {"source": url} for url in produto_fornecedor.get("images", [])
                ],
                "shipping": {
                    "mode": "me2",
                    "local_pick_up": False,
                    "free_shipping": preco_venda > 150,  # Frete grátis para produtos acima de R$150
                    "logistic_type": "cross_docking"
                }
            }
            
            # Cria o anúncio no Mercado Livre
            logger.info(f"Criando anúncio no ML: {item_data['title']}")
            resultado = self.ml_api.create_item(item_data)
            
            if not resultado or "id" not in resultado:
                logger.error(f"Falha ao criar anúncio: {resultado}")
                return None
            
            # Salva o produto no banco de dados
            logger.info(f"Salvando produto no banco: {item_data['title']}")
            produto_db = self.produto_repo.create({
                "titulo": item_data["title"],
                "descricao": item_data["description"]["plain_text"],
                "preco_custo": preco_custo,
                "preco_venda": preco_venda,
                "margem": margem,
                "estoque": item_data["available_quantity"],
                "categoria": produto_fornecedor.get("category", ""),
                "sku": produto_fornecedor.get("sku", ""),
                "ml_item_id": resultado["id"],
                "fornecedor_id": fornecedor_id,
                "fornecedor_product_id": produto_fornecedor.get("id", ""),
                "status": StatusProduto.ATIVO
            })
            
            logger.info(f"Anúncio criado com sucesso: {resultado['id']}")
            return resultado
        
        except Exception as e:
            logger.error(f"Erro ao criar anúncio no ML: {str(e)}")
            return None
    
    def criar_anuncios_diarios(self) -> int:
        """Cria anúncios diários com base nas tendências e configurações"""
        logger.info("Iniciando criação de anúncios diários")
        
        # Quantidade de anúncios a serem criados
        quantidade = ML_ITEMS_PER_DAY
        
        # Busca tendências
        tendencias = self.buscar_tendencias(limit=quantidade * 2)  # Busca o dobro para ter margem
        
        if not tendencias:
            logger.warning("Sem tendências para criar anúncios")
            return 0
        
        # Obtém fornecedores
        fornecedores = self.fornecedor_repo.list_all()
        if not fornecedores:
            logger.error("Nenhum fornecedor cadastrado")
            return 0
        
        # Mapa de fornecedores por tipo de API
        fornecedores_map = {f.api_type: f for f in fornecedores}
        
        # Lista de tipos de fornecedores suportados
        tipos_fornecedores = [FornecedorType.CJ_DROPSHIPPING, FornecedorType.SPOCKET]
        
        # Contador de anúncios criados
        anuncios_criados = 0
        
        # Para cada tendência, tenta criar um anúncio
        for tendencia in tendencias:
            if anuncios_criados >= quantidade:
                break
            
            keyword = tendencia.get("keyword", "")
            if not keyword:
                continue
            
            logger.info(f"Processando tendência: {keyword}")
            
            # Tenta cada fornecedor até conseguir criar o anúncio
            for tipo_fornecedor in tipos_fornecedores:
                if tipo_fornecedor.value not in fornecedores_map:
                    logger.warning(f"Fornecedor {tipo_fornecedor} não cadastrado")
                    continue
                
                fornecedor = fornecedores_map[tipo_fornecedor.value]
                
                # Busca produtos no fornecedor
                produtos_fornecedor = self.buscar_produtos_fornecedor(keyword, tipo_fornecedor)
                
                if not produtos_fornecedor:
                    logger.info(f"Nenhum produto encontrado para '{keyword}' no fornecedor {tipo_fornecedor}")
                    continue
                
                # Seleciona o melhor produto
                melhor_produto = self.selecionar_melhor_produto(produtos_fornecedor)
                
                if not melhor_produto:
                    logger.info(f"Nenhum produto adequado para '{keyword}' no fornecedor {tipo_fornecedor}")
                    continue
                
                # Cria o anúncio no Mercado Livre
                resultado = self.criar_anuncio_ml(melhor_produto, fornecedor.id)
                
                if resultado:
                    anuncios_criados += 1
                    logger.info(f"Anúncio {anuncios_criados}/{quantidade} criado com sucesso")
                    break  # Passa para a próxima tendência
        
        logger.info(f"Processo concluído. {anuncios_criados} anúncios criados.")
        return anuncios_criados 