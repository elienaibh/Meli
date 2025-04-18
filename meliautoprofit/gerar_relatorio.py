#!/usr/bin/env python
"""
Script para gerar e enviar relatórios diários do MeliAutoProfit
"""
import os
import sys
import argparse
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meliautoprofit.app.services.monitoramento import MonitoramentoService
from meliautoprofit.database.session import SessionLocal
from meliautoprofit.app.config import setup_logger

# Configuração de logger
logger = setup_logger("gerar_relatorio")

def main():
    """Função principal para geração e envio de relatórios"""
    parser = argparse.ArgumentParser(description="Gera e envia relatórios diários")
    parser.add_argument("-s", "--salvar", action="store_true", help="Salvar relatório em arquivo JSON")
    parser.add_argument("-d", "--diretorio", type=str, default="relatorios", 
                        help="Diretório para salvar relatórios (padrão: 'relatorios')")
    parser.add_argument("-t", "--telegram", action="store_true", help="Enviar relatório via Telegram")
    parser.add_argument("-m", "--monitorar", action="store_true", help="Monitorar pedidos pendentes")
    
    args = parser.parse_args()
    
    # Se nenhuma opção for fornecida, assume telegram e salvamento
    if not (args.salvar or args.telegram or args.monitorar):
        args.salvar = True
        args.telegram = True
    
    logger.info("Iniciando geração de relatório")
    
    # Verifica se o diretório existe
    if args.salvar:
        dir_path = Path(args.diretorio)
        if not dir_path.exists():
            logger.info(f"Criando diretório de relatórios: {args.diretorio}")
            dir_path.mkdir(parents=True, exist_ok=True)
    
    # Cria a sessão do banco de dados
    db: Session = SessionLocal()
    
    try:
        # Instancia o serviço de monitoramento
        monitoramento = MonitoramentoService(db)
        
        # Gera o relatório diário
        logger.info("Gerando relatório diário")
        relatorio = monitoramento.gerar_relatorio_diario()
        
        # Verifica se o relatório tem erro
        if "erro" in relatorio:
            logger.error(f"Erro ao gerar relatório: {relatorio['erro']}")
            if args.telegram:
                # Envia notificação de erro pelo Telegram
                monitoramento.enviar_relatorio_telegram(relatorio)
            return 1
        
        # Salva o relatório em arquivo
        if args.salvar:
            # Gera nome do arquivo com a data atual
            nome_arquivo = f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            caminho_arquivo = os.path.join(args.diretorio, nome_arquivo)
            
            logger.info(f"Salvando relatório em {caminho_arquivo}")
            monitoramento.salvar_relatorio_json(relatorio, caminho_arquivo)
        
        # Envia o relatório pelo Telegram
        if args.telegram:
            logger.info("Enviando relatório pelo Telegram")
            monitoramento.enviar_relatorio_telegram(relatorio)
        
        # Monitora pedidos pendentes
        if args.monitorar:
            logger.info("Monitorando pedidos pendentes")
            monitoramento.monitorar_pedidos_pendentes()
        
        logger.info("Geração e envio de relatório concluídos com sucesso")
        return 0
    
    except Exception as e:
        logger.error(f"Erro ao processar relatório: {str(e)}")
        return 1
    
    finally:
        # Fecha a sessão do banco de dados
        db.close()

if __name__ == "__main__":
    sys.exit(main()) 