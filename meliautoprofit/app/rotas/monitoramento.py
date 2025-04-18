from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import logging
from datetime import datetime, timedelta

from meliautoprofit.app.services.monitoramento import MonitoramentoService
from meliautoprofit.database.session import get_db

# Configuração de logger
logger = logging.getLogger(__name__)

# Criação do router
router = APIRouter(
    prefix="/monitoramento",
    tags=["monitoramento"],
    responses={404: {"description": "Não encontrado"}}
)

@router.get("/relatorio", response_model=Dict[str, Any])
async def gerar_relatorio(
    db: Session = Depends(get_db)
):
    """
    Gera um relatório diário com métricas de desempenho da loja
    """
    try:
        # Inicializa o serviço de monitoramento
        servico = MonitoramentoService(db)
        
        # Gera o relatório
        relatorio = servico.gerar_relatorio_diario()
        
        # Verifica se houve erro
        if "erro" in relatorio:
            logger.error(f"Erro ao gerar relatório: {relatorio['erro']}")
            raise HTTPException(status_code=500, detail=relatorio["erro"])
        
        return relatorio
    except Exception as e:
        logger.exception("Erro ao gerar relatório via API")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/enviar/telegram")
async def enviar_telegram(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Envia o relatório diário via Telegram em uma tarefa em segundo plano
    """
    try:
        # Inicializa o serviço de monitoramento
        servico = MonitoramentoService(db)
        
        # Adiciona a tarefa de envio ao background
        background_tasks.add_task(servico.enviar_relatorio_telegram)
        
        return {"mensagem": "Solicitação de envio de relatório via Telegram em processamento"}
    except Exception as e:
        logger.exception("Erro ao agendar envio de relatório via Telegram")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pedidos-pendentes")
async def monitorar_pedidos_pendentes(
    db: Session = Depends(get_db)
):
    """
    Verifica pedidos pendentes e retorna alertas para pedidos com mais de 24h
    """
    try:
        # Inicializa o serviço de monitoramento
        servico = MonitoramentoService(db)
        
        # Monitora pedidos pendentes
        resultado = servico.monitorar_pedidos_pendentes()
        
        return resultado
    except Exception as e:
        logger.exception("Erro ao verificar pedidos pendentes")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/gerar-salvar")
async def gerar_e_salvar_relatorio(
    background_tasks: BackgroundTasks,
    nome_arquivo: str = None,
    db: Session = Depends(get_db)
):
    """
    Gera e salva um relatório em um arquivo JSON
    """
    try:
        # Inicializa o serviço de monitoramento
        servico = MonitoramentoService(db)
        
        # Gera o relatório
        relatorio = servico.gerar_relatorio_diario()
        
        # Verifica se houve erro
        if "erro" in relatorio:
            logger.error(f"Erro ao gerar relatório: {relatorio['erro']}")
            raise HTTPException(status_code=500, detail=relatorio["erro"])
        
        # Prepara o nome do arquivo se não for fornecido
        if not nome_arquivo:
            data_atual = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"relatorios/relatorio_{data_atual}.json"
        
        # Salva o relatório em segundo plano
        background_tasks.add_task(servico.salvar_relatorio_json, relatorio, nome_arquivo)
        
        return {
            "mensagem": f"Relatório sendo salvo em {nome_arquivo}",
            "relatorio": relatorio
        }
    except Exception as e:
        logger.exception("Erro ao gerar e salvar relatório")
        raise HTTPException(status_code=500, detail=str(e)) 