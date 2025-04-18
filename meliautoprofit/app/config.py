"""
Configurações da aplicação MeliAutoProfit
"""
import os
from dotenv import load_dotenv
import logging

# Carrega variáveis de ambiente
load_dotenv()

# Configurações de aplicação
APP_NAME = "MeliAutoProfit"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

# Configurações de API
API_PREFIX = "/api/v1"
API_TAGS_METADATA = [
    {"name": "produtos", "description": "Operações com produtos"},
    {"name": "pedidos", "description": "Operações com pedidos"},
    {"name": "fornecedores", "description": "Operações com fornecedores"},
    {"name": "relatórios", "description": "Geração de relatórios"}
]

# Configurações de banco de dados
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./meliautoprofit.db")

# Configurações de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = "meliautoprofit.log"

# Configurações de Mercado Livre
ML_ITEMS_PER_DAY = int(os.getenv("ML_ITEMS_PER_DAY", "5"))
ML_MARGIN_PERCENTAGE = float(os.getenv("ML_MARGIN_PERCENTAGE", "0.3"))

# Configurações de relatórios
REPORT_DAILY_TIME = os.getenv("REPORT_DAILY_TIME", "20:00")  # Hora para envio do relatório diário
REPORT_RECIPIENTS = os.getenv("REPORT_RECIPIENTS", "").split(",")  # Lista de destinatários

# Configurações de monitoramento
MONITOR_INTERVAL_SECONDS = int(os.getenv("MONITOR_INTERVAL_SECONDS", "300"))  # 5 minutos

# Função para configurar o logger
def setup_logger(name):
    """Configuração de logger para os módulos da aplicação"""
    logger = logging.getLogger(name)
    
    # Define o nível de log
    level = getattr(logging, LOG_LEVEL)
    logger.setLevel(level)
    
    # Cria handlers se não existirem
    if not logger.handlers:
        # Handler de arquivo
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(file_handler)
        
        # Handler de console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(console_handler)
    
    return logger 