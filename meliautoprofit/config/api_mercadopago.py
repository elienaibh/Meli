"""
Configuração da API do Mercado Pago
"""
import requests
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Credenciais
MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")

# URLs da API
MP_API_BASE_URL = "https://api.mercadopago.com/v1"
MP_PAYMENTS_URL = f"{MP_API_BASE_URL}/payments"
MP_TRANSFERS_URL = f"{MP_API_BASE_URL}/transfers"

def get_payment_info(payment_id):
    """Obtém informações sobre um pagamento"""
    print(f"DEBUG: Obtendo info do pagamento {payment_id}")
    
    headers = {
        "Authorization": f"Bearer {MP_ACCESS_TOKEN}"
    }
    
    response = requests.get(f"{MP_PAYMENTS_URL}/{payment_id}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"DEBUG: Erro ao obter pagamento: {response.text}")
        return None

def create_transfer(user_id, amount, description="Pagamento de fornecedor"):
    """Cria uma transferência para conta de terceiros"""
    print(f"DEBUG: Transferindo R${amount} para {user_id}")
    
    headers = {
        "Authorization": f"Bearer {MP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "user_id": user_id,
        "amount": amount,
        "description": description
    }
    
    response = requests.post(MP_TRANSFERS_URL, headers=headers, json=data)
    if response.status_code in (200, 201):
        return response.json()
    else:
        print(f"DEBUG: Erro ao transferir: {response.text}")
        return None

# Exemplo de teste da API
if __name__ == "__main__":
    # Simula consulta de pagamento
    payment_info = get_payment_info("12345678")
    if payment_info:
        print(f"DEBUG: Pagamento encontrado: R${payment_info.get('transaction_amount')}") 