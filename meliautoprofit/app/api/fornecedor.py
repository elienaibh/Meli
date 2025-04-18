"""
Integração com APIs de fornecedores
"""
import logging
from fastapi import HTTPException
from enum import Enum
from ..config import setup_logger
from config.api_cjdropshipping import search_products as cj_search, create_order as cj_create_order
from config.api_spocket import search_products as spocket_search, get_product_details, create_order as spocket_create_order

# Configuração de logger
logger = setup_logger(__name__)

class FornecedorType(str, Enum):
    """Tipos de fornecedores suportados"""
    CJ_DROPSHIPPING = "cj_dropshipping"
    SPOCKET = "spocket"

class FornecedorAPI:
    """Classe para integração com APIs de fornecedores"""
    
    def __init__(self, fornecedor_type=None):
        """Inicializa a API do fornecedor"""
        self.fornecedor_type = fornecedor_type
    
    def set_fornecedor(self, fornecedor_type):
        """Define o tipo de fornecedor a ser usado"""
        if fornecedor_type not in [ft.value for ft in FornecedorType]:
            raise HTTPException(
                status_code=400, 
                detail=f"Tipo de fornecedor não suportado: {fornecedor_type}"
            )
        
        self.fornecedor_type = fornecedor_type
    
    def search_products(self, keyword, page=1, limit=20):
        """Busca produtos no catálogo do fornecedor"""
        logger.debug(f"Buscando produtos com keyword '{keyword}' no fornecedor {self.fornecedor_type}")
        
        if not self.fornecedor_type:
            raise HTTPException(status_code=400, detail="Tipo de fornecedor não definido")
        
        if self.fornecedor_type == FornecedorType.CJ_DROPSHIPPING:
            return cj_search(keyword, page, limit)
        elif self.fornecedor_type == FornecedorType.SPOCKET:
            return spocket_search(keyword, page, limit)
        else:
            raise HTTPException(
                status_code=400, 
                detail=f"Tipo de fornecedor não suportado: {self.fornecedor_type}"
            )
    
    def get_product_details(self, product_id):
        """Obtém detalhes de um produto específico"""
        logger.debug(f"Obtendo detalhes do produto {product_id} do fornecedor {self.fornecedor_type}")
        
        if not self.fornecedor_type:
            raise HTTPException(status_code=400, detail="Tipo de fornecedor não definido")
        
        if self.fornecedor_type == FornecedorType.SPOCKET:
            return get_product_details(product_id)
        else:
            raise HTTPException(
                status_code=400, 
                detail=f"Operação não suportada para o fornecedor: {self.fornecedor_type}"
            )
    
    def create_order(self, **kwargs):
        """Cria um pedido no fornecedor"""
        logger.debug(f"Criando pedido no fornecedor {self.fornecedor_type}")
        
        if not self.fornecedor_type:
            raise HTTPException(status_code=400, detail="Tipo de fornecedor não definido")
        
        if self.fornecedor_type == FornecedorType.CJ_DROPSHIPPING:
            # Verifica parâmetros esperados
            required_params = ["product_id", "quantity", "shipping_address"]
            for param in required_params:
                if param not in kwargs:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Parâmetro obrigatório ausente: {param}"
                    )
            
            return cj_create_order(
                kwargs["product_id"],
                kwargs["quantity"],
                kwargs["shipping_address"]
            )
        
        elif self.fornecedor_type == FornecedorType.SPOCKET:
            # Verifica parâmetros esperados
            required_params = ["variant_id", "quantity", "shipping_address"]
            for param in required_params:
                if param not in kwargs:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Parâmetro obrigatório ausente: {param}"
                    )
            
            return spocket_create_order(
                kwargs["variant_id"],
                kwargs["quantity"],
                kwargs["shipping_address"]
            )
        
        else:
            raise HTTPException(
                status_code=400, 
                detail=f"Tipo de fornecedor não suportado: {self.fornecedor_type}"
            ) 