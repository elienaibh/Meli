"""
Configuração da API do CJ Dropshipping
"""
import requests
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Credenciais
CJ_API_KEY = os.getenv("CJ_API_KEY")
CJ_EMAIL = os.getenv("CJ_EMAIL")

# URLs da API
CJ_API_BASE_URL = "https://api.cjdropshipping.com"
CJ_AUTH_URL = f"{CJ_API_BASE_URL}/api/auth/token"
CJ_PRODUCT_URL = f"{CJ_API_BASE_URL}/api/product/list"
CJ_ORDER_URL = f"{CJ_API_BASE_URL}/api/order/create"

def get_access_token():
    """Obtém token de acesso da API"""
    print("DEBUG: Obtendo token CJ Dropshipping")
    
    data = {
        "email": CJ_EMAIL,
        "password": CJ_API_KEY
    }
    
    response = requests.post(CJ_AUTH_URL, json=data)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == 200:
            return result.get("data", {}).get("accessToken")
    
    print(f"DEBUG: Erro ao obter token CJ: {response.text}")
    return None

def search_products(keyword, page=1, page_size=20):
    """Busca produtos no catálogo"""
    token = get_access_token()
    if not token:
        return []
    
    print(f"DEBUG: Buscando produtos com keyword: {keyword}")
    
    headers = {
        "CJ-Access-Token": token
    }
    
    params = {
        "productNameEn": keyword,
        "pageNum": page,
        "pageSize": page_size
    }
    
    response = requests.get(CJ_PRODUCT_URL, headers=headers, params=params)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == 200:
            return result.get("data", {}).get("list", [])
    
    print(f"DEBUG: Erro ao buscar produtos: {response.text}")
    return []

def create_order(product_id, quantity, shipping_address):
    """Cria um pedido para o fornecedor"""
    token = get_access_token()
    if not token:
        return None
    
    print(f"DEBUG: Criando pedido para produto {product_id}")
    
    headers = {
        "CJ-Access-Token": token,
        "Content-Type": "application/json"
    }
    
    data = {
        "productId": product_id,
        "quantity": quantity,
        "shippingAddress": shipping_address
    }
    
    response = requests.post(CJ_ORDER_URL, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == 200:
            return result.get("data")
    
    print(f"DEBUG: Erro ao criar pedido: {response.text}")
    return None

# Exemplo de teste da API
if __name__ == "__main__":
    token = get_access_token()
    print(f"DEBUG: Token obtido: {token[:10]}...") if token else print("DEBUG: Falha ao obter token")
    
    products = search_products("phone case")
    if products:
        print(f"DEBUG: {len(products)} produtos encontrados")
        for i, product in enumerate(products[:3]):
            print(f"DEBUG: Produto {i+1}: {product.get('productNameEn')}") 