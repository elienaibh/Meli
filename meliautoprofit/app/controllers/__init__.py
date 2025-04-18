"""
Controladores da aplicação
"""
from fastapi import APIRouter
from .listagem_controller import router as listagem_router

# Roteador principal que agrupa todos os controladores
api_router = APIRouter()

# Registra os sub-roteadores
api_router.include_router(listagem_router)

# Função para registrar todos os controladores no aplicativo principal
def register_controllers(app):
    """Registra todos os controladores no aplicativo FastAPI"""
    app.include_router(api_router, prefix="/api/v1") 