from fastapi import FastAPI, Request, HTTPException
import logging
import sys
import traceback

# Configurar logging para console (compatível com Vercel)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = FastAPI(title="MeliAutoProfit")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Error: {str(e)}\n{traceback.format_exc()}")
        raise

@app.post("/webhook/mercadolivre")
async def handle_order(request: Request):
    try:
        data = await request.json()
        order_id = data.get("order_id", "N/A")
        logger.info(f"Pedido recebido: {order_id}")
        return {"status": "received", "order_id": order_id}
    except Exception as e:
        logger.error(f"Erro no webhook: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=400, detail="Erro ao processar notificação")

@app.get("/auth/callback")
async def oauth_callback(code: str = None, state: str = None):
    try:
        logger.info(f"Callback OAuth recebido: code={code}, state={state}")
        return {"message": "Callback recebido, autenticação pendente", "code": code, "state": state}
    except Exception as e:
        logger.error(f"Erro no callback: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Erro no callback")

@app.get("/")
async def root():
    logger.info("Acessando raiz")
    return {"message": "Loja Ativa!", "status": "online"}

# Isso permite que o Vercel encontre a aplicação FastAPI
# como uma função serverless simples 