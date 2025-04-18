"""
Testes para o controlador de listagem
"""
import pytest
from unittest.mock import patch, MagicMock
from fastapi import BackgroundTasks
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.controllers.listagem_controller import processar_listagem_automatica
from .mocks import MockMercadoLivreAPI, MockFornecedorAPI, MockTelegramAPI

# Cliente de teste para FastAPI
client = TestClient(app)

class TestListagemController:
    """Testes para o controlador de listagem"""
    
    @pytest.fixture
    def background_tasks(self):
        """Fixture para criar um objeto BackgroundTasks mockado"""
        tasks = BackgroundTasks()
        tasks.add_task = MagicMock()
        return tasks
    
    @patch('app.controllers.listagem_controller.ListagemService')
    def test_criar_anuncios_automaticos(self, mock_service, background_tasks, test_db):
        """Testa o endpoint de criação automática de anúncios"""
        # Configura a sessão de banco de dados mockada
        with patch('app.controllers.listagem_controller.get_db', return_value=lambda: test_db):
            # Executa a requisição para o endpoint
            response = client.post("/api/v1/listagem/automatica")
            
            # Verifica se a resposta foi bem-sucedida
            assert response.status_code == 200
            assert "message" in response.json()
            assert "background" in response.json()["message"]
    
    @patch('app.controllers.listagem_controller.ListagemService')
    def test_buscar_tendencias(self, mock_service, test_db):
        """Testa o endpoint de busca de tendências"""
        # Configura o serviço mockado
        service_instance = mock_service.return_value
        service_instance.buscar_tendencias.return_value = [
            {"keyword": "Produto 1", "url": "url1", "price": 100, "position": 1},
            {"keyword": "Produto 2", "url": "url2", "price": 150, "position": 2}
        ]
        
        # Configura a sessão de banco de dados mockada
        with patch('app.controllers.listagem_controller.get_db', return_value=lambda: test_db):
            # Executa a requisição para o endpoint
            response = client.get("/api/v1/listagem/tendencias")
            
            # Verifica se a resposta foi bem-sucedida
            assert response.status_code == 200
            
            # Verifica se retornou as tendências
            data = response.json()
            assert len(data) == 2
            assert data[0]["keyword"] == "Produto 1"
            assert data[1]["keyword"] == "Produto 2"
    
    @patch('app.controllers.listagem_controller.ListagemService')
    @patch('app.controllers.listagem_controller.TelegramAPI')
    def test_processar_listagem_automatica(self, mock_telegram, mock_service, test_db):
        """Testa o processamento de listagem automática"""
        # Configura o serviço mockado
        service_instance = mock_service.return_value
        service_instance.criar_anuncios_diarios.return_value = 5
        
        # Configura o telegram mockado
        telegram_instance = mock_telegram.return_value
        
        # Executa a função de processamento
        processar_listagem_automatica(test_db)
        
        # Verifica se os métodos foram chamados corretamente
        service_instance.criar_anuncios_diarios.assert_called_once()
        telegram_instance.send_message.assert_called()
    
    @patch('app.controllers.listagem_controller.ListagemService')
    @patch('app.controllers.listagem_controller.TelegramAPI')
    def test_processar_listagem_automatica_com_erro(self, mock_telegram, mock_service, test_db):
        """Testa o processamento de listagem automática com erro"""
        # Configura o serviço mockado para lançar uma exceção
        service_instance = mock_service.return_value
        service_instance.criar_anuncios_diarios.side_effect = Exception("Erro de teste")
        
        # Configura o telegram mockado
        telegram_instance = mock_telegram.return_value
        
        # Executa a função de processamento
        processar_listagem_automatica(test_db)
        
        # Verifica se os métodos foram chamados corretamente
        service_instance.criar_anuncios_diarios.assert_called_once()
        telegram_instance.send_notification.assert_called_with(
            "Erro na Listagem Automática",
            "Ocorreu um erro durante o processo de listagem automática: Erro de teste",
            is_error=True
        ) 