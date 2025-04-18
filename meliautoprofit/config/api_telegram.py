"""
Configuração da API do Telegram
"""
import requests
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Credenciais
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# URLs da API
TELEGRAM_API_BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
TELEGRAM_SEND_MESSAGE_URL = f"{TELEGRAM_API_BASE_URL}/sendMessage"

def send_message(text, chat_id=None):
    """Envia mensagem para o canal ou chat"""
    if not chat_id:
        chat_id = TELEGRAM_CHAT_ID
        
    print(f"DEBUG: Enviando mensagem para {chat_id}")
    
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    
    response = requests.post(TELEGRAM_SEND_MESSAGE_URL, json=data)
    if response.status_code == 200:
        return response.json()
    
    print(f"DEBUG: Erro ao enviar mensagem: {response.text}")
    return None

def send_daily_report(pedidos, lucro, estoque_baixo=None):
    """Envia relatório diário formatado"""
    print("DEBUG: Gerando relatório diário")
    
    if estoque_baixo is None:
        estoque_baixo = []
    
    message = f"""
<b>📊 Relatório Diário MeliAutoProfit</b>

🛒 <b>Pedidos:</b> {pedidos}
💰 <b>Lucro:</b> R$ {lucro:.2f}
"""

    if estoque_baixo:
        message += "\n<b>⚠️ Produtos com estoque baixo:</b>\n"
        for produto in estoque_baixo:
            message += f"- {produto}\n"
    
    return send_message(message)

# Exemplo de teste da API
if __name__ == "__main__":
    # Teste simples
    result = send_message("Teste de conexão com a API do Telegram.")
    if result:
        print("DEBUG: Mensagem enviada com sucesso!")
    
    # Teste de relatório
    report = send_daily_report(5, 150.50, ["Fone JBL", "Carregador Portátil"])
    if report:
        print("DEBUG: Relatório enviado com sucesso!") 