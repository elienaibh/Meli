"""
Configuração da API do Mercado Livre
"""
import requests
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Credenciais
ML_CLIENT_ID = os.getenv("ML_CLIENT_ID")
ML_CLIENT_SECRET = os.getenv("ML_CLIENT_SECRET")
ML_USER_ID = os.getenv("ML_USER_ID")

# URLs da API
ML_API_BASE_URL = "https://api.mercadolibre.com"
ML_AUTH_URL = f"{ML_API_BASE_URL}/oauth/token"
ML_ITEMS_URL = f"{ML_API_BASE_URL}/items"
ML_ORDERS_URL = f"{ML_API_BASE_URL}/orders"
ML_TRENDS_URL = f"{ML_API_BASE_URL}/trends/MLB"

def get_access_token():
    """Obtém token de acesso via OAuth"""
    print("DEBUG: Obtendo token do Mercado Livre")
    data = {
        "grant_type": "client_credentials",
        "client_id": ML_CLIENT_ID,
        "client_secret": ML_CLIENT_SECRET
    }
    
    response = requests.post(ML_AUTH_URL, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"DEBUG: Erro ao obter token: {response.text}")
        return None

def get_trends():
    """Obtém tendências de produtos"""
    token = get_access_token()
    if not token:
        return []
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(ML_TRENDS_URL, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"DEBUG: Erro ao obter tendências: {response.text}")
        return []

# Exemplo de teste da API
if __name__ == "__main__":
    token = get_access_token()
    print(f"DEBUG: Token obtido: {token[:10]}...")
    
    trends = get_trends()
    if trends:
        print(f"DEBUG: {len(trends)} tendências encontradas")
        for i, trend in enumerate(trends[:3]):
            print(f"DEBUG: Tendência {i+1}: {trend.get('keyword')}") 