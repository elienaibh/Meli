"""
Controlador de listagem automática
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any, List

from ..config import setup_logger
from ..services.listagem import ListagemService
from ...database import get_db
from ..api.telegram import TelegramAPI

# Configuração de logger
logger = setup_logger(__name__)

# Roteador FastAPI
router = APIRouter(
    prefix="/listagem",
    tags=["listagem"],
    responses={404: {"description": "Not found"}},
)

@router.post("/automatica")
async def criar_anuncios_automaticos(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Inicia o processo de criação automática de anúncios em background"""
    logger.info("Iniciando processo de criação automática de anúncios")
    
    # Adiciona a tarefa ao processamento em background
    background_tasks.add_task(processar_listagem_automatica, db)
    
    return {"message": "Processo de listagem automática iniciado em background"}

@router.get("/tendencias")
async def buscar_tendencias(limit: int = 10, db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    """Busca as tendências atuais no Mercado Livre"""
    logger.info(f"Buscando top {limit} tendências")
    
    try:
        service = ListagemService(db)
        tendencias = service.buscar_tendencias(limit=limit)
        
        return tendencias
    
    except Exception as e:
        logger.error(f"Erro ao buscar tendências: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar tendências: {str(e)}")

def processar_listagem_automatica(db: Session):
    """Processa a listagem automática em background"""
    logger.info("Executando processamento de listagem automática")
    
    try:
        # Inicializa o serviço de listagem
        service = ListagemService(db)
        
        # Inicializa o API do Telegram para notificações
        telegram = TelegramAPI()
        
        # Hora inicial
        hora_inicio = datetime.now()
        
        # Cria anúncios automaticamente
        total_anuncios = service.criar_anuncios_diarios()
        
        # Hora final
        hora_fim = datetime.now()
        duracao = (hora_fim - hora_inicio).total_seconds() / 60  # Duração em minutos
        
        # Envia notificação pelo Telegram
        mensagem = f"""
🟢 Listagem Automática Concluída

📊 Resumo:
- Anúncios criados: {total_anuncios}
- Data: {hora_inicio.strftime('%d/%m/%Y')}
- Horário: {hora_inicio.strftime('%H:%M')}
- Duração: {duracao:.1f} minutos
        """
        
        telegram.send_message(mensagem)
        
        logger.info(f"Processo de listagem automática concluído. {total_anuncios} anúncios criados.")
    
    except Exception as e:
        logger.error(f"Erro durante processo de listagem automática: {str(e)}")
        
        # Tenta enviar notificação de erro
        try:
            telegram = TelegramAPI()
            telegram.send_notification(
                "Erro na Listagem Automática",
                f"Ocorreu um erro durante o processo de listagem automática: {str(e)}",
                is_error=True
            )
        except Exception as telegram_error:
            logger.error(f"Erro ao enviar notificação de erro pelo Telegram: {str(telegram_error)}") 