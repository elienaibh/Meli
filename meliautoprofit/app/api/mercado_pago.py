"""
Integração com a API do Mercado Pago
"""
import requests
import logging
from fastapi import HTTPException
from ..config import setup_logger
from config.api_mercadopago import get_payment_info, create_transfer

# Configuração de logger
logger = setup_logger(__name__)

class MercadoPagoAPI:
    """Classe para integração com o Mercado Pago"""
    
    def __init__(self):
        """Inicializa a API do Mercado Pago"""
        self.access_token = None
        self._load_access_token()
    
    def _load_access_token(self):
        """Carrega o token de acesso das variáveis de ambiente"""
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        self.access_token = os.getenv("MP_ACCESS_TOKEN")
        return self.access_token is not None
    
    def get_payment(self, payment_id):
        """Obtém detalhes de um pagamento específico"""
        logger.debug(f"Obtendo detalhes do pagamento {payment_id}")
        if not self.access_token:
            if not self._load_access_token():
                raise HTTPException(status_code=500, detail="Token de acesso do Mercado Pago não encontrado")
        
        result = get_payment_info(payment_id)
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail=f"Pagamento {payment_id} não encontrado")
    
    def make_transfer(self, user_id, amount, description=None):
        """Realiza uma transferência para outro usuário"""
        logger.debug(f"Transferindo R${amount} para usuário {user_id}")
        if not self.access_token:
            if not self._load_access_token():
                raise HTTPException(status_code=500, detail="Token de acesso do Mercado Pago não encontrado")
        
        if description is None:
            description = f"Pagamento MeliAutoProfit: R${amount}"
        
        result = create_transfer(user_id, amount, description)
        if result:
            return result
        else:
            raise HTTPException(status_code=500, detail=f"Erro ao transferir para usuário {user_id}")
    
    def get_transaction_history(self, limit=10, offset=0):
        """Obtém o histórico de transações"""
        logger.debug(f"Obtendo histórico de transações (limit={limit}, offset={offset})")
        if not self.access_token:
            if not self._load_access_token():
                raise HTTPException(status_code=500, detail="Token de acesso do Mercado Pago não encontrado")
        
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        params = {
            "limit": limit,
            "offset": offset
        }
        
        response = requests.get(
            "https://api.mercadopago.com/v1/payments/search",
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Erro ao obter histórico de transações: {response.text}")
            raise HTTPException(status_code=response.status_code, detail=response.text)
    
    def refund_payment(self, payment_id):
        """Reembolsa um pagamento"""
        logger.debug(f"Reembolsando pagamento {payment_id}")
        if not self.access_token:
            if not self._load_access_token():
                raise HTTPException(status_code=500, detail="Token de acesso do Mercado Pago não encontrado")
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"https://api.mercadopago.com/v1/payments/{payment_id}/refunds",
            headers=headers
        )
        
        if response.status_code in (200, 201):
            return response.json()
        else:
            logger.error(f"Erro ao reembolsar pagamento {payment_id}: {response.text}")
            raise HTTPException(status_code=response.status_code, detail=response.text) 