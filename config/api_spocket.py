"""
Configuração da API do Spocket
"""
import requests
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Credenciais
SPOCKET_API_KEY = os.getenv("SPOCKET_API_KEY")

# URLs da API
SPOCKET_API_BASE_URL = "https://api.spocket.co/v1"
SPOCKET_SEARCH_URL = f"{SPOCKET_API_BASE_URL}/products/search"
SPOCKET_PRODUCT_URL = f"{SPOCKET_API_BASE_URL}/products"
SPOCKET_ORDER_URL = f"{SPOCKET_API_BASE_URL}/orders"

def search_products(keyword, page=1, per_page=20):
    """Busca produtos no catálogo"""
    print(f"DEBUG: Buscando produtos Spocket: {keyword}")
    
    headers = {
        "Authorization": f"Bearer {SPOCKET_API_KEY}",
        "Accept": "application/json"
    }
    
    params = {
        "query": keyword,
        "page": page,
        "per_page": per_page
    }
    
    response = requests.get(SPOCKET_SEARCH_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("products", [])
    
    print(f"DEBUG: Erro ao buscar produtos Spocket: {response.text}")
    return []

def get_product_details(product_id):
    """Obtém detalhes de um produto específico"""
    print(f"DEBUG: Obtendo detalhes do produto {product_id}")
    
    headers = {
        "Authorization": f"Bearer {SPOCKET_API_KEY}",
        "Accept": "application/json"
    }
    
    response = requests.get(f"{SPOCKET_PRODUCT_URL}/{product_id}", headers=headers)
    if response.status_code == 200:
        return response.json()
    
    print(f"DEBUG: Erro ao obter detalhes: {response.text}")
    return None

def create_order(variant_id, quantity, shipping_address):
    """Cria um pedido para o fornecedor"""
    print(f"DEBUG: Criando pedido para variante {variant_id}")
    
    headers = {
        "Authorization": f"Bearer {SPOCKET_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    data = {
        "variant_id": variant_id,
        "quantity": quantity,
        "shipping_address": shipping_address
    }
    
    response = requests.post(SPOCKET_ORDER_URL, headers=headers, json=data)
    if response.status_code in (200, 201):
        return response.json()
    
    print(f"DEBUG: Erro ao criar pedido Spocket: {response.text}")
    return None

# Exemplo de teste da API
if __name__ == "__main__":
    products = search_products("headphones")
    if products:
        print(f"DEBUG: {len(products)} produtos encontrados")
        for i, product in enumerate(products[:3]):
            print(f"DEBUG: Produto {i+1}: {product.get('title')}")
            
        # Obter detalhes do primeiro produto
        if products:
            details = get_product_details(products[0].get("id"))
            if details:
                print(f"DEBUG: Preço: {details.get('price')}, Estoque: {details.get('inventory_quantity')}") 