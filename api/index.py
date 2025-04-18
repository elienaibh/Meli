from fastapi import FastAPI, Request, HTTPException
import logging

# Configurar logging para console (compatível com Vercel)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="MeliAutoProfit")

@app.post("/webhook/mercadolivre")
async def handle_order(request: Request):
    try:
        data = await request.json()
        order_id = data.get("order_id", "N/A")
        logger.debug(f"DEBUG: Pedido recebido: {order_id}")
        return {"status": "received"}
    except Exception as e:
        logger.error(f"DEBUG: Erro no webhook: {str(e)}")
        raise HTTPException(status_code=400, detail="Erro ao processar notificação")

@app.get("/auth/callback")
async def oauth_callback(code: str = None, state: str = None):
    try:
        logger.debug(f"DEBUG: Callback OAuth recebido: code={code}, state={state}")
        return {"message": "Callback recebido, autenticação pendente"}
    except Exception as e:
        logger.error(f"DEBUG: Erro no callback: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro no callback")

@app.get("/")
async def root():
    logger.debug("DEBUG: Acessando raiz")
    return {"message": "Loja Ativa!"}

# Isso permite que o Vercel encontre a aplicação FastAPI
# como uma função serverless simples 