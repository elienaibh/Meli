"""
Integração com a API do Telegram
"""
import logging
from fastapi import HTTPException
from ..config import setup_logger
from config.api_telegram import send_message, send_daily_report

# Configuração de logger
logger = setup_logger(__name__)

class TelegramAPI:
    """Classe para integração com o Telegram"""
    
    def __init__(self):
        """Inicializa a API do Telegram"""
        self._test_connection()
    
    def _test_connection(self):
        """Testa a conexão com a API do Telegram"""
        logger.debug("Testando conexão com a API do Telegram")
        try:
            result = send_message("Teste de conexão - MeliAutoProfit")
            return result is not None
        except Exception as e:
            logger.error(f"Erro ao conectar com Telegram: {str(e)}")
            return False
    
    def send_message(self, text, chat_id=None):
        """Envia uma mensagem para o chat ou canal"""
        logger.debug(f"Enviando mensagem para o Telegram: {text[:30]}...")
        
        try:
            result = send_message(text, chat_id)
            if result:
                return result
            else:
                raise HTTPException(status_code=500, detail="Erro ao enviar mensagem para o Telegram")
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    def send_notification(self, title, message, is_error=False):
        """Envia uma notificação formatada"""
        logger.debug(f"Enviando notificação: {title}")
        
        emoji = "🔴" if is_error else "ℹ️"
        formatted_message = f"<b>{emoji} {title}</b>\n\n{message}"
        
        return self.send_message(formatted_message)
    
    def send_daily_report(self, pedidos, lucro, estoque_baixo=None):
        """Envia o relatório diário"""
        logger.debug(f"Enviando relatório diário: {pedidos} pedidos, R${lucro} lucro")
        
        try:
            result = send_daily_report(pedidos, lucro, estoque_baixo)
            if result:
                return result
            else:
                raise HTTPException(status_code=500, detail="Erro ao enviar relatório para o Telegram")
        except Exception as e:
            logger.error(f"Erro ao enviar relatório: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    def send_order_notification(self, order):
        """Envia notificação de novo pedido"""
        logger.debug(f"Enviando notificação de pedido: {order.get('id')}")
        
        message = f"""
<b>🛒 Novo Pedido Recebido</b>

<b>ID:</b> {order.get('id')}
<b>Cliente:</b> {order.get('buyer', {}).get('nickname', 'N/A')}
<b>Valor Total:</b> R$ {order.get('total_amount', 0):.2f}
<b>Data:</b> {order.get('date_created', 'N/A')}
<b>Status:</b> {order.get('status', 'N/A')}
"""
        
        return self.send_message(message) 