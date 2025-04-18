"""
Testes para o serviço de listagem
"""
import pytest
from unittest.mock import patch, MagicMock

from app.services.listagem import ListagemService
from app.api.fornecedor import FornecedorType
from database.models import StatusProduto
from .mocks import MockMercadoLivreAPI, MockFornecedorAPI, MockTelegramAPI

class TestListagemService:
    """Testes para o serviço de listagem"""
    
    @pytest.fixture
    def service(self, test_db):
        """Fixture para criar o serviço de listagem com mocks"""
        with patch('app.services.listagem.MercadoLivreAPI') as mock_ml, \
             patch('app.services.listagem.FornecedorAPI') as mock_fornecedor:
            # Configura os mocks
            mock_ml.return_value = MockMercadoLivreAPI()
            mock_fornecedor.return_value = MockFornecedorAPI()
            
            # Cria o serviço com o banco de dados de teste
            service = ListagemService(test_db)
            
            yield service
    
    def test_buscar_tendencias(self, service):
        """Testa a busca de tendências"""
        # Executa o método
        tendencias = service.buscar_tendencias(limit=5)
        
        # Verifica se retornou o número correto de tendências
        assert len(tendencias) == 5
        
        # Verifica se as tendências têm o formato esperado
        for i, tendencia in enumerate(tendencias, 1):
            assert tendencia["keyword"] == f"Produto Tendência {i}"
            assert tendencia["price"] > 0
    
    def test_buscar_produtos_fornecedor(self, service):
        """Testa a busca de produtos no fornecedor"""
        # Executa o método
        produtos = service.buscar_produtos_fornecedor("Smartphone", FornecedorType.CJ_DROPSHIPPING)
        
        # Verifica se retornou produtos
        assert len(produtos) > 0
        
        # Verifica se os produtos têm o formato esperado
        for produto in produtos:
            assert "name" in produto
            assert "price" in produto
            assert "stock" in produto
    
    def test_selecionar_melhor_produto(self, service):
        """Testa a seleção do melhor produto"""
        # Produtos de teste
        produtos = [
            {"name": "Produto 1", "price": 100, "stock": 5, "rating": 4.5},
            {"name": "Produto 2", "price": 120, "stock": 10, "rating": 4.2},
            {"name": "Produto 3", "price": 80, "stock": 15, "rating": 3.8}
        ]
        
        # Executa o método
        melhor_produto = service.selecionar_melhor_produto(produtos)
        
        # Verifica se retornou um produto
        assert melhor_produto is not None
        
        # O produto com melhor score deve ser o primeiro (por causa do rating alto)
        assert melhor_produto["name"] == "Produto 1"
    
    def test_selecionar_melhor_produto_lista_vazia(self, service):
        """Testa a seleção do melhor produto com lista vazia"""
        # Executa o método com lista vazia
        melhor_produto = service.selecionar_melhor_produto([])
        
        # Deve retornar None
        assert melhor_produto is None
    
    def test_criar_anuncio_ml(self, service, test_db):
        """Testa a criação de anúncio no Mercado Livre"""
        # Produto do fornecedor
        produto_fornecedor = {
            "id": "CJ-123456",
            "name": "Smartphone X12",
            "description": "Smartphone de última geração",
            "price": 500.0,
            "stock": 50,
            "category": "Eletrônicos",
            "sku": "SM-X12",
            "images": ["https://exemplo.com/imagem1.jpg"]
        }
        
        # Fornecedor ID do banco de dados de teste
        fornecedor_id = 1
        
        # Executa o método
        resultado = service.criar_anuncio_ml(produto_fornecedor, fornecedor_id)
        
        # Verifica se retornou um resultado
        assert resultado is not None
        assert "id" in resultado
        assert resultado["status"] == "active"
        
        # Verifica se o produto foi salvo no banco
        produto = test_db.query(service.produto_repo.get_by_ml_item_id(resultado["id"]))
        assert produto is not None
    
    @patch('app.services.listagem.ML_ITEMS_PER_DAY', 3)  # Limita a 3 anúncios para o teste
    def test_criar_anuncios_diarios(self, service, test_db):
        """Testa a criação de anúncios diários"""
        # Executa o método
        total = service.criar_anuncios_diarios()
        
        # Deve criar 3 anúncios
        assert total == 3
        
        # Verifica se os produtos foram salvos no banco
        produtos = test_db.query(service.produto_repo.list_by_status(StatusProduto.ATIVO))
        assert len(produtos) >= 3  # Já existiam alguns produtos teste
    
    def test_criar_anuncios_diarios_sem_fornecedores(self, service, test_db):
        """Testa a criação de anúncios diários sem fornecedores"""
        # Remove os fornecedores do banco de teste
        for fornecedor in test_db.query(service.fornecedor_repo.list_all()):
            test_db.delete(fornecedor)
        test_db.commit()
        
        # Executa o método
        total = service.criar_anuncios_diarios()
        
        # Não deve criar nenhum anúncio
        assert total == 0 