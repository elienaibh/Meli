"""
Testes para o serviço de monitoramento
"""
import os
import pytest
import json
import tempfile
from datetime import datetime
from unittest.mock import patch, MagicMock

from app.services.monitoramento import MonitoramentoService
from database.models import Produto, Pedido, StatusPedido, StatusProduto

class TestMonitoramentoService:
    """Testes para o serviço de monitoramento"""
    
    @pytest.fixture
    def service(self, test_db):
        """Fixture para criar o serviço de monitoramento com mocks"""
        with patch('app.services.monitoramento.TelegramAPI') as mock_telegram:
            # Configura o mock do Telegram
            telegram_instance = MagicMock()
            mock_telegram.return_value = telegram_instance
            
            # Cria o serviço com o banco de dados de teste
            service = MonitoramentoService(test_db)
            
            # Define atributos mockados
            service.bot_token = "mock-token"
            service.chat_id = "mock-chat-id"
            
            yield service
    
    def test_gerar_relatorio_diario(self, service):
        """Testa a geração de relatório diário"""
        # Executa o método
        relatorio = service.gerar_relatorio_diario()
        
        # Verifica se o relatório foi gerado corretamente
        assert relatorio is not None
        assert "data_geracao" in relatorio
        assert "vendas" in relatorio
        assert "produtos" in relatorio
        assert "pedidos" in relatorio
        assert "financeiro" in relatorio
        
        # Verifica valores específicos
        assert relatorio["vendas"]["total"] > 0
        assert relatorio["vendas"]["quantidade"] > 0
        assert relatorio["pedidos"]["novos"] >= 0
        assert relatorio["financeiro"]["lucro_liquido"] > 0
    
    def test_monitorar_pedidos_pendentes(self, service):
        """Testa o monitoramento de pedidos pendentes"""
        # Executa o método
        resultado = service.monitorar_pedidos_pendentes()
        
        # Verifica se o resultado é válido
        assert resultado is not None
        assert "data_verificacao" in resultado
        assert "total_pendentes" in resultado
        assert "pendentes_24h" in resultado
        assert "alertas" in resultado
        
        # Verifica se os alertas tem o formato esperado
        for alerta in resultado["alertas"]:
            assert "id" in alerta
            assert "data_criacao" in alerta
            assert "valor" in alerta
    
    def test_salvar_relatorio_json(self, service, tmp_path):
        """Testa o salvamento de relatório em JSON"""
        # Gera um relatório para salvar
        relatorio = service.gerar_relatorio_diario()
        
        # Caminho para o arquivo
        json_path = tmp_path / "relatorio_teste.json"
        
        # Executa o método
        resultado = service.salvar_relatorio_json(relatorio, str(json_path))
        
        # Verifica se o salvamento foi bem sucedido
        assert resultado is True
        assert os.path.exists(json_path)
        
        # Verifica o conteúdo do arquivo
        with open(json_path, "r", encoding="utf-8") as f:
            conteudo = json.load(f)
            
            # Verifica se o conteúdo corresponde ao relatório
            assert conteudo["data_geracao"] == relatorio["data_geracao"]
            assert conteudo["vendas"]["total"] == relatorio["vendas"]["total"]
            assert conteudo["pedidos"]["novos"] == relatorio["pedidos"]["novos"]
    
    def test_salvar_relatorio_json_diretorio_inexistente(self, service, tmp_path):
        """Testa o salvamento de relatório em diretório que não existe"""
        # Gera um relatório para salvar
        relatorio = service.gerar_relatorio_diario()
        
        # Caminho para o arquivo em um subdiretório que não existe
        diretorio = tmp_path / "subdir" / "relatorios"
        json_path = diretorio / "relatorio_teste.json"
        
        # Executa o método
        resultado = service.salvar_relatorio_json(relatorio, str(json_path))
        
        # Verifica se o salvamento foi bem sucedido
        assert resultado is True
        assert os.path.exists(json_path)
    
    @patch('app.services.monitoramento.telegram.Bot')
    def test_enviar_relatorio_telegram(self, mock_bot, service):
        """Testa o envio de relatório via Telegram"""
        # Configura o mock do Bot do Telegram
        bot_instance = MagicMock()
        mock_bot.return_value = bot_instance
        
        # Executa o método
        resultado = service.enviar_relatorio_telegram()
        
        # Verifica se o envio foi bem sucedido
        assert resultado is True
        
        # Verifica se os métodos do Bot foram chamados
        bot_instance.send_message.assert_called_once()
    
    @patch('app.services.monitoramento.telegram.Bot')
    def test_enviar_relatorio_telegram_sem_token(self, mock_bot, service):
        """Testa o envio de relatório sem token configurado"""
        # Remove as configurações
        service.bot_token = None
        service.chat_id = None
        
        # Executa o método
        resultado = service.enviar_relatorio_telegram()
        
        # Deve retornar False indicando falha
        assert resultado is False
        
        # Verifica que o bot não foi criado
        mock_bot.assert_not_called()
    
    @patch('app.services.monitoramento.telegram.Bot')
    def test_enviar_alerta_telegram(self, mock_bot, service):
        """Testa o envio de alerta via Telegram"""
        # Configura o mock do Bot do Telegram
        bot_instance = MagicMock()
        mock_bot.return_value = bot_instance
        
        # Executa o método privado
        resultado = service._enviar_alerta_telegram("Alerta de teste")
        
        # Verifica se o envio foi bem sucedido
        assert resultado is True
        
        # Verifica se os métodos do Bot foram chamados
        bot_instance.send_message.assert_called_once()
    
    def test_formatar_mensagem_telegram(self, service):
        """Testa a formatação de mensagem para o Telegram"""
        # Gera um relatório para formatar
        relatorio = service.gerar_relatorio_diario()
        
        # Executa o método privado
        mensagem = service._formatar_mensagem_telegram(relatorio)
        
        # Verifica se a mensagem foi formatada corretamente
        assert mensagem is not None
        assert mensagem.startswith("📊 *RELATÓRIO DIÁRIO")
        assert "💰 VENDAS" in mensagem
        assert "📦 PEDIDOS" in mensagem
        assert "💵 FINANCEIRO" in mensagem 