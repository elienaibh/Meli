"""
Aplicação principal MeliAutoProfit
"""
import logging
import os
from datetime import datetime
from fastapi import FastAPI, Request, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import requests

# Configuração de logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("meliautoprofit.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="MeliAutoProfit",
    description="Sistema automatizado de e-commerce para Mercado Livre",
    version="1.0.0"
)

# Configuração de CORS para permitir requisições de origens diferentes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração de templates Jinja2
templates = Jinja2Templates(directory="app/templates")

# Rota principal
@app.get("/")
async def root():
    """
    Endpoint principal da API
    """
    logger.info("Acessando endpoint principal")
    return {"status": "active", "message": "MeliAutoProfit API está funcionando!"}

# Rota para dashboard
@app.get("/dashboard")
async def dashboard(request: Request):
    """
    Endpoint para renderizar o dashboard
    """
    logger.info("Acessando dashboard")
    return templates.TemplateResponse("dashboard.html", {"request": request})

# Rota para callback do OAuth do Mercado Livre
@app.get("/auth/callback")
async def auth_callback(code: str = None, error: str = None):
    """
    Endpoint de callback para o processo de autenticação do Mercado Livre
    
    Args:
        code: Código de autorização fornecido pelo Mercado Livre
        error: Mensagem de erro, se houver
    
    Returns:
        Resposta JSON com status da autenticação
    """
    logger.info(f"Recebido callback de autenticação. Code: {code}, Error: {error}")
    
    if error:
        logger.error(f"Erro na autenticação: {error}")
        return {"status": "error", "message": f"Erro na autenticação: {error}"}
    
    if not code:
        logger.error("Código de autorização não fornecido")
        return {"status": "error", "message": "Código de autorização não fornecido"}
    
    try:
        # Troca o código de autorização por um token de acesso
        client_id = os.getenv("ML_CLIENT_ID")
        client_secret = os.getenv("ML_CLIENT_SECRET")
        redirect_uri = os.getenv("ML_REDIRECT_URI")
        
        response = requests.post(
            "https://api.mercadolibre.com/oauth/token",
            data={
                "grant_type": "authorization_code",
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "redirect_uri": redirect_uri
            },
            headers={"Accept": "application/json"}
        )
        
        if response.status_code == 200:
            token_data = response.json()
            logger.info("Token obtido com sucesso")
            
            # Aqui você pode salvar o token no banco de dados
            # Por exemplo: save_token_to_db(token_data)
            
            return {"status": "success", "message": "Autenticação concluída com sucesso"}
        else:
            logger.error(f"Erro ao obter token: {response.text}")
            return {"status": "error", "message": f"Erro ao obter token: {response.status_code}"}
            
    except Exception as e:
        logger.exception(f"Erro no processo de autenticação: {str(e)}")
        return {"status": "error", "message": f"Erro no processo de autenticação: {str(e)}"}

# Rota de webhook para receber notificações de pedidos
@app.post("/webhook/orders")
async def handle_order(request: Request, background_tasks: BackgroundTasks):
    """Recebe notificações de novos pedidos"""
    logger.debug("Recebendo webhook de pedido")
    try:
        data = await request.json()
        logger.info(f"Webhook recebido: {data}")
        
        # Processa o webhook em background
        # background_tasks.add_task(process_order_notification, data)
        
        return {"status": "received"}
    except Exception as e:
        logger.exception(f"Erro ao processar webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Health check
@app.get("/health")
async def health():
    """
    Endpoint para verificar a saúde da aplicação
    """
    return {"status": "healthy"}

# Inicialização da aplicação
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 