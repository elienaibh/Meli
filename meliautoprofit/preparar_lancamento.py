#!/usr/bin/env python
"""
Script para preparar o lançamento da loja
"""
import os
import sys
import argparse
import logging
from datetime import datetime

# Configura o caminho para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.config import setup_logger
from database import SessionLocal
from app.services.preparacao import PreparacaoService

# Configuração de logger
logger = setup_logger(__name__)

def main():
    """Função principal para preparar o lançamento"""
    # Configuração dos argumentos de linha de comando
    parser = argparse.ArgumentParser(description="Prepara o lançamento da loja MeliAutoProfit")
    parser.add_argument('--csv', type=str, help='Caminho para o arquivo CSV com produtos')
    parser.add_argument('--quantidade', type=int, default=50, help='Quantidade de produtos de teste a serem criados')
    parser.add_argument('--backup', type=str, help='Caminho para salvar o backup dos produtos')
    parser.add_argument('--apenas-backup', action='store_true', help='Apenas faz o backup sem inserir produtos')
    args = parser.parse_args()
    
    # Obtém a sessão do banco de dados
    db = SessionLocal()
    
    try:
        # Cria uma instância do serviço de preparação
        servico = PreparacaoService(db)
        
        # Faz backup dos produtos existentes
        if args.backup or args.apenas_backup:
            caminho_backup = args.backup or f"backup_produtos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            logger.info(f"Fazendo backup dos produtos para {caminho_backup}")
            sucesso = servico.fazer_backup_produtos(caminho_backup)
            
            if sucesso:
                logger.info(f"Backup salvo em {caminho_backup}")
            else:
                logger.error("Falha ao fazer backup")
        
        # Se for apenas backup, não insere produtos
        if args.apenas_backup:
            return
        
        # Importa produtos do CSV se fornecido
        if args.csv:
            logger.info(f"Importando produtos do arquivo {args.csv}")
            produtos_inseridos = servico.importar_produtos_csv(args.csv)
            logger.info(f"Importação concluída: {produtos_inseridos} produtos inseridos")
        
        # Cria produtos de teste
        else:
            quantidade = args.quantidade
            logger.info(f"Criando {quantidade} produtos de teste")
            produtos_inseridos = servico.criar_produtos_teste(quantidade)
            logger.info(f"Criação concluída: {produtos_inseridos} produtos inseridos")
        
        logger.info("Preparação de lançamento concluída com sucesso")
    
    except Exception as e:
        logger.error(f"Erro durante a preparação do lançamento: {str(e)}")
    
    finally:
        # Fecha a sessão do banco de dados
        db.close()

if __name__ == "__main__":
    logger.info("Iniciando preparação do lançamento")
    main()
    logger.info("Preparação de lançamento finalizada") 