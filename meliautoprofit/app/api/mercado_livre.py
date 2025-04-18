"""
Integração com a API do Mercado Livre
"""
import requests
import logging
import time
from fastapi import HTTPException
from functools import wraps
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from ..config import setup_logger
from config.api_mercadolivre import get_access_token, get_trends

# Configuração de logger
logger = setup_logger(__name__)

class MercadoLivreAPI:
    """Classe para integração com o Mercado Livre"""
    
    def __init__(self):
        """Inicializa a API do Mercado Livre"""
        self.token = None
        self.refresh_token()
    
    def refresh_token(self):
        """Obtém um novo token de acesso"""
        logger.debug("Atualizando token de acesso do Mercado Livre")
        self.token = get_access_token()
        return self.token is not None
    
    @retry(
        retry=retry_if_exception_type((requests.exceptions.HTTPError, ConnectionError)),
        stop=stop_after_attempt(3),
        wait=wait_fixed(60),
        before_sleep=lambda retry_state: logger.debug(
            f"Retry após erro de API. Tentativa {retry_state.attempt_number}/3"
        )
    )
    def _request_with_retry(self, method, url, **kwargs):
        """Faz uma requisição com retry em caso de erro 429"""
        logger.debug(f"Fazendo requisição {method} para {url}")
        
        response = requests.request(method, url, **kwargs)
        
        # Se for erro 429 (Too Many Requests), lança uma exceção que será capturada pelo retry
        if response.status_code == 429:
            logger.warning(f"API rate limit excedido: {response.text}")
            response.raise_for_status()
        
        return response
    
    def get_trends(self, limit=10):
        """Obtém as tendências de busca"""
        logger.debug(f"Obtendo top {limit} tendências do Mercado Livre")
        trends = get_trends()
        return trends[:limit] if trends else []
    
    def get_item(self, item_id):
        """Obtém detalhes de um item específico"""
        logger.debug(f"Obtendo detalhes do item {item_id}")
        if not self.token:
            if not self.refresh_token():
                raise HTTPException(status_code=500, detail="Falha ao obter token do Mercado Livre")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            response = self._request_with_retry(
                "GET",
                f"https://api.mercadolibre.com/items/{item_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                # Tenta renovar o token e tentar novamente
                if self.refresh_token():
                    return self.get_item(item_id)
                else:
                    raise HTTPException(status_code=401, detail="Não autorizado pelo Mercado Livre")
            else:
                logger.error(f"Erro ao obter item {item_id}: {response.text}")
                raise HTTPException(status_code=response.status_code, detail=response.text)
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de requisição ao obter item {item_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erro ao comunicar com API do Mercado Livre: {str(e)}")
    
    def create_item(self, item_data):
        """Cria um novo item/anúncio"""
        logger.debug(f"Criando novo item: {item_data.get('title')}")
        if not self.token:
            if not self.refresh_token():
                raise HTTPException(status_code=500, detail="Falha ao obter token do Mercado Livre")
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = self._request_with_retry(
                "POST",
                "https://api.mercadolibre.com/items",
                headers=headers,
                json=item_data
            )
            
            if response.status_code in (200, 201):
                return response.json()
            elif response.status_code == 401:
                # Tenta renovar o token e tentar novamente
                if self.refresh_token():
                    return self.create_item(item_data)
                else:
                    raise HTTPException(status_code=401, detail="Não autorizado pelo Mercado Livre")
            else:
                logger.error(f"Erro ao criar item: {response.text}")
                raise HTTPException(status_code=response.status_code, detail=response.text)
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de requisição ao criar item: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erro ao comunicar com API do Mercado Livre: {str(e)}")
    
    def update_item(self, item_id, item_data):
        """Atualiza um item existente"""
        logger.debug(f"Atualizando item {item_id}")
        if not self.token:
            if not self.refresh_token():
                raise HTTPException(status_code=500, detail="Falha ao obter token do Mercado Livre")
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = self._request_with_retry(
                "PUT",
                f"https://api.mercadolibre.com/items/{item_id}",
                headers=headers,
                json=item_data
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                # Tenta renovar o token e tentar novamente
                if self.refresh_token():
                    return self.update_item(item_id, item_data)
                else:
                    raise HTTPException(status_code=401, detail="Não autorizado pelo Mercado Livre")
            else:
                logger.error(f"Erro ao atualizar item {item_id}: {response.text}")
                raise HTTPException(status_code=response.status_code, detail=response.text)
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de requisição ao atualizar item {item_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erro ao comunicar com API do Mercado Livre: {str(e)}")
    
    def get_orders(self, status="paid", limit=50, offset=0):
        """Obtém pedidos com um determinado status"""
        logger.debug(f"Obtendo pedidos com status '{status}'")
        if not self.token:
            if not self.refresh_token():
                raise HTTPException(status_code=500, detail="Falha ao obter token do Mercado Livre")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {
            "status": status,
            "limit": limit,
            "offset": offset
        }
        
        try:
            response = self._request_with_retry(
                "GET",
                "https://api.mercadolibre.com/orders/search",
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                # Tenta renovar o token e tentar novamente
                if self.refresh_token():
                    return self.get_orders(status, limit, offset)
                else:
                    raise HTTPException(status_code=401, detail="Não autorizado pelo Mercado Livre")
            else:
                logger.error(f"Erro ao obter pedidos: {response.text}")
                raise HTTPException(status_code=response.status_code, detail=response.text)
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de requisição ao obter pedidos: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erro ao comunicar com API do Mercado Livre: {str(e)}")
    
    def get_order(self, order_id):
        """Obtém detalhes de um pedido específico"""
        logger.debug(f"Obtendo detalhes do pedido {order_id}")
        if not self.token:
            if not self.refresh_token():
                raise HTTPException(status_code=500, detail="Falha ao obter token do Mercado Livre")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            response = self._request_with_retry(
                "GET",
                f"https://api.mercadolibre.com/orders/{order_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                # Tenta renovar o token e tentar novamente
                if self.refresh_token():
                    return self.get_order(order_id)
                else:
                    raise HTTPException(status_code=401, detail="Não autorizado pelo Mercado Livre")
            else:
                logger.error(f"Erro ao obter pedido {order_id}: {response.text}")
                raise HTTPException(status_code=response.status_code, detail=response.text)
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de requisição ao obter pedido {order_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erro ao comunicar com API do Mercado Livre: {str(e)}")
    
    def get_shipping(self, shipping_id):
        """Obtém detalhes de uma entrega"""
        logger.debug(f"Obtendo detalhes da entrega {shipping_id}")
        if not self.token:
            if not self.refresh_token():
                raise HTTPException(status_code=500, detail="Falha ao obter token do Mercado Livre")
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            response = self._request_with_retry(
                "GET",
                f"https://api.mercadolibre.com/shipments/{shipping_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                # Tenta renovar o token e tentar novamente
                if self.refresh_token():
                    return self.get_shipping(shipping_id)
                else:
                    raise HTTPException(status_code=401, detail="Não autorizado pelo Mercado Livre")
            else:
                logger.error(f"Erro ao obter entrega {shipping_id}: {response.text}")
                raise HTTPException(status_code=response.status_code, detail=response.text)
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de requisição ao obter entrega {shipping_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Erro ao comunicar com API do Mercado Livre: {str(e)}") 