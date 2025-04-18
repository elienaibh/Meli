"""
Mocks para os testes
"""
from unittest.mock import MagicMock
from app.config import setup_logger

# Configuração de logger
logger = setup_logger(__name__)

class MockMercadoLivreAPI:
    """Mock da API do Mercado Livre para testes"""
    
    def __init__(self):
        """Inicializa o mock"""
        self.token = "mock-token-123456"
        logger.debug("Inicializando MockMercadoLivreAPI")
    
    def refresh_token(self):
        """Mock para atualizar token"""
        logger.debug("Mock: Atualizando token do Mercado Livre")
        return True
    
    def get_trends(self, limit=10):
        """Mock para obter tendências"""
        logger.debug(f"Mock: Obtendo {limit} tendências do Mercado Livre")
        
        trends = []
        for i in range(1, limit + 1):
            trends.append({
                "keyword": f"Produto Tendência {i}",
                "url": f"https://exemplo.com/trend{i}",
                "price": 100 + (i * 10),
                "position": i
            })
        
        return trends
    
    def get_item(self, item_id):
        """Mock para obter um item"""
        logger.debug(f"Mock: Obtendo item {item_id}")
        
        return {
            "id": item_id,
            "title": f"Produto {item_id}",
            "price": 150.0,
            "available_quantity": 10,
            "status": "active"
        }
    
    def create_item(self, item_data):
        """Mock para criar um item"""
        logger.debug(f"Mock: Criando item: {item_data.get('title')}")
        
        # Simula criação bem sucedida
        return {
            "id": f"MLB{hash(item_data.get('title')) % 1000000}",
            "title": item_data.get("title"),
            "price": item_data.get("price"),
            "status": "active",
            "permalink": f"https://produto.mercadolivre.com.br/{hash(item_data.get('title'))}"
        }
    
    def update_item(self, item_id, item_data):
        """Mock para atualizar um item"""
        logger.debug(f"Mock: Atualizando item {item_id}")
        
        # Simula atualização bem sucedida
        return {
            "id": item_id,
            "title": item_data.get("title"),
            "price": item_data.get("price"),
            "status": "active"
        }
    
    def get_orders(self, status="paid", limit=50, offset=0):
        """Mock para obter pedidos"""
        logger.debug(f"Mock: Obtendo pedidos com status '{status}'")
        
        orders = []
        for i in range(1, 11):  # Simula 10 pedidos
            orders.append({
                "id": f"ORDER{i}",
                "status": status,
                "date_created": "2025-04-15T10:30:00.000-03:00",
                "total_amount": 150.0 + (i * 10),
                "buyer": {
                    "id": f"BUYER{i}",
                    "nickname": f"Comprador Teste {i}"
                },
                "items": [
                    {
                        "item": {
                            "id": f"MLB{i}",
                            "title": f"Produto Teste {i}",
                            "variation_id": None
                        },
                        "quantity": 1,
                        "unit_price": 150.0 + (i * 10)
                    }
                ]
            })
        
        return {
            "results": orders,
            "paging": {
                "total": len(orders),
                "limit": limit,
                "offset": offset
            }
        }

class MockFornecedorAPI:
    """Mock da API de fornecedores para testes"""
    
    def __init__(self, fornecedor_type=None):
        """Inicializa o mock"""
        self.fornecedor_type = fornecedor_type
        logger.debug(f"Inicializando MockFornecedorAPI: {fornecedor_type}")
    
    def set_fornecedor(self, fornecedor_type):
        """Define o tipo de fornecedor a ser usado"""
        logger.debug(f"Mock: Definindo fornecedor para {fornecedor_type}")
        self.fornecedor_type = fornecedor_type
    
    def search_products(self, keyword, page=1, limit=20):
        """Mock para buscar produtos no fornecedor"""
        logger.debug(f"Mock: Buscando produtos com keyword '{keyword}' no fornecedor {self.fornecedor_type}")
        
        products = []
        for i in range(1, limit + 1):
            products.append({
                "id": f"{self.fornecedor_type}-{i}",
                "name": f"{keyword} {i}",
                "description": f"Descrição do produto {keyword} {i}",
                "price": 50.0 + (i * 5),
                "stock": 100 - (i * 2),
                "rating": 4.5 - (i * 0.1),
                "category": "Categoria Teste",
                "sku": f"SKU-{self.fornecedor_type}-{i}",
                "images": [
                    f"https://exemplo.com/imagem{i}_1.jpg",
                    f"https://exemplo.com/imagem{i}_2.jpg"
                ]
            })
        
        return products
    
    def get_product_details(self, product_id):
        """Mock para obter detalhes de um produto"""
        logger.debug(f"Mock: Obtendo detalhes do produto {product_id}")
        
        return {
            "id": product_id,
            "name": f"Produto {product_id}",
            "description": f"Descrição detalhada do produto {product_id}",
            "price": 75.0,
            "stock": 50,
            "rating": 4.2,
            "category": "Categoria Teste",
            "sku": f"SKU-{product_id}",
            "images": [
                "https://exemplo.com/imagem_detalhe_1.jpg",
                "https://exemplo.com/imagem_detalhe_2.jpg"
            ]
        }
    
    def create_order(self, **kwargs):
        """Mock para criar um pedido no fornecedor"""
        logger.debug(f"Mock: Criando pedido no fornecedor {self.fornecedor_type}")
        
        # Simula criação bem sucedida
        return {
            "order_id": f"ORDER-{self.fornecedor_type}-{hash(str(kwargs)) % 1000000}",
            "status": "processing",
            "tracking_number": f"TRACK-{hash(str(kwargs)) % 1000000}",
            "created_at": "2025-04-15T10:45:00Z"
        }

class MockTelegramAPI:
    """Mock da API do Telegram para testes"""
    
    def __init__(self):
        """Inicializa o mock"""
        logger.debug("Inicializando MockTelegramAPI")
    
    def _test_connection(self):
        """Mock para testar conexão"""
        logger.debug("Mock: Testando conexão com o Telegram")
        return True
    
    def send_message(self, text, chat_id=None):
        """Mock para enviar mensagem"""
        logger.debug(f"Mock: Enviando mensagem para o Telegram: {text[:30]}...")
        
        # Simula envio bem sucedido
        return {
            "message_id": hash(text) % 1000000,
            "date": "2025-04-15T10:50:00Z",
            "text": text
        }
    
    def send_notification(self, title, message, is_error=False):
        """Mock para enviar notificação"""
        logger.debug(f"Mock: Enviando notificação: {title}")
        
        emoji = "🔴" if is_error else "ℹ️"
        formatted_message = f"<b>{emoji} {title}</b>\n\n{message}"
        
        return self.send_message(formatted_message)
    
    def send_daily_report(self, pedidos, lucro, estoque_baixo=None):
        """Mock para enviar relatório diário"""
        logger.debug(f"Mock: Enviando relatório diário: {pedidos} pedidos, R${lucro} lucro")
        
        # Simula envio bem sucedido
        return {
            "message_id": hash(f"{pedidos}-{lucro}") % 1000000,
            "date": "2025-04-15T20:00:00Z",
            "text": f"Relatório: {pedidos} pedidos, R${lucro} lucro"
        }
    
    def send_order_notification(self, order):
        """Mock para enviar notificação de pedido"""
        logger.debug(f"Mock: Enviando notificação de pedido: {order.get('id')}")
        
        message = f"""
<b>🛒 Novo Pedido Recebido</b>

<b>ID:</b> {order.get('id')}
<b>Cliente:</b> {order.get('buyer', {}).get('nickname', 'N/A')}
<b>Valor Total:</b> R$ {order.get('total_amount', 0):.2f}
<b>Data:</b> {order.get('date_created', 'N/A')}
<b>Status:</b> {order.get('status', 'N/A')}
"""
        
        return self.send_message(message)

def get_mock_apis():
    """Retorna instâncias de todas as APIs mockadas"""
    return {
        "mercado_livre": MockMercadoLivreAPI(),
        "fornecedor": MockFornecedorAPI(),
        "telegram": MockTelegramAPI()
    } 