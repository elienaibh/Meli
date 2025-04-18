from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
import traceback
import json
from typing import Dict, Any

# Configurar logging para console (compatível com Vercel)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = FastAPI(title="MeliAutoProfit")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware para logging de requisições e tratamento de erros"""
    logger.info(f"Request: {request.method} {request.url}")
    try:
        # Log do corpo da requisição se for POST/PUT
        if request.method in ["POST", "PUT"]:
            body = await request.body()
            if body:
                try:
                    body_json = json.loads(body)
                    logger.debug(f"Request body: {json.dumps(body_json, indent=2)}")
                except json.JSONDecodeError:
                    logger.debug(f"Request body (raw): {body}")

        response = await call_next(request)
        
        logger.info(f"Response status: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Error in request: {str(e)}\n{traceback.format_exc()}")
        return HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Endpoint de teste/healthcheck"""
    return {"status": "ok", "message": "MeliAutoProfit API is running"}

@app.post("/webhook/mercadolivre")
async def handle_order(request: Request):
    """Handler para webhooks do Mercado Livre"""
    try:
        data = await request.json()
        order_id = data.get("order_id", "N/A")
        logger.info(f"Pedido recebido: {order_id}")
        logger.debug(f"Dados do pedido: {json.dumps(data, indent=2)}")
        
        # Aqui você pode adicionar a lógica de processamento do pedido
        
        return {
            "status": "received",
            "order_id": order_id,
            "message": "Pedido recebido com sucesso"
        }
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=400, detail="JSON inválido")
    except Exception as e:
        logger.error(f"Erro no webhook: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar notificação: {str(e)}")

@app.get("/auth/callback")
async def auth_callback(request: Request):
    """Handler para callback de autenticação do Mercado Livre"""
    try:
        # Extrair parâmetros da query string
        params = dict(request.query_params)
        logger.info("Callback de autenticação recebido")
        logger.debug(f"Parâmetros: {json.dumps(params, indent=2)}")
        
        # Aqui você pode adicionar a lógica de autenticação
        
        return {
            "status": "success",
            "message": "Autenticação processada com sucesso",
            "params": params
        }
    except Exception as e:
        logger.error(f"Erro no callback de autenticação: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar autenticação: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Isso permite que o Vercel encontre a aplicação FastAPI
# como uma função serverless simples 