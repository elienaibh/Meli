"""
Serviço de monitoramento da loja
"""
import logging
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from pathlib import Path
import telegram
from dotenv import load_dotenv

from ..config import setup_logger
from ..api.telegram import TelegramAPI
from ...database.models import Produto, Pedido, PedidoItem, StatusPedido, StatusProduto
from ...database.repository import ProdutoRepository, PedidoRepository

# Carregar variáveis de ambiente
load_dotenv()

# Configuração de logger
logger = setup_logger(__name__)

class MonitoramentoService:
    """
    Serviço responsável pelo monitoramento de métricas da loja e geração de relatórios
    """
    
    def __init__(self, db: Session):
        """
        Inicializa o serviço de monitoramento com uma sessão de banco de dados
        
        Args:
            db: Sessão do banco de dados
        """
        self.db = db
        self.produto_repo = ProdutoRepository(db)
        self.pedido_repo = PedidoRepository(db)
        self.telegram = TelegramAPI()
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    def gerar_relatorio_diario(self) -> Dict[str, Any]:
        """
        Gera um relatório diário com métricas de desempenho da loja
        
        Returns:
            Um dicionário contendo o relatório diário
        """
        try:
            logger.info("Iniciando geração de relatório diário")
            
            # Data atual e ontem para comparações
            hoje = datetime.now()
            ontem = hoje - timedelta(days=1)
            
            # TODO: Obter dados reais do banco de dados
            # Dados são simulados para este exemplo
            relatorio = {
                "data_geracao": hoje.isoformat(),
                "periodo": {
                    "inicio": ontem.isoformat(),
                    "fim": hoje.isoformat()
                },
                "vendas": {
                    "total": 1250.00,
                    "quantidade": 5,
                    "ticket_medio": 250.00,
                    "variacao_dia_anterior": 15.0  # em porcentagem
                },
                "produtos": {
                    "mais_vendidos": [
                        {"id": "P001", "nome": "Produto A", "quantidade": 3, "valor_total": 750.00},
                        {"id": "P002", "nome": "Produto B", "quantidade": 2, "valor_total": 500.00}
                    ],
                    "sem_estoque": 2,
                    "estoque_baixo": 5
                },
                "pedidos": {
                    "novos": 6,
                    "em_processamento": 4,
                    "enviados": 3,
                    "entregues": 5,
                    "cancelados": 1,
                    "pendentes_ha_mais_de_24h": 2
                },
                "financeiro": {
                    "receita_bruta": 1250.00,
                    "taxas_ml": 125.00,
                    "custos_produtos": 625.00,
                    "custos_frete": 75.00,
                    "lucro_liquido": 425.00,
                    "margem_lucro": 34.0  # em porcentagem
                }
            }
            
            logger.info("Relatório diário gerado com sucesso")
            return relatorio
            
        except Exception as e:
            logger.exception("Erro ao gerar relatório diário")
            return {"erro": str(e)}
    
    def monitorar_pedidos_pendentes(self) -> Dict[str, Any]:
        """
        Monitora pedidos pendentes e identifica aqueles com mais de 24h
        
        Returns:
            Dicionário com o status do monitoramento e alertas
        """
        try:
            logger.info("Verificando pedidos pendentes")
            
            # TODO: Implementar consulta real ao banco de dados
            # Simulação de pedidos pendentes
            pedidos_pendentes = [
                {"id": "O001", "data_criacao": (datetime.now() - timedelta(hours=26)).isoformat(), "valor": 250.00},
                {"id": "O002", "data_criacao": (datetime.now() - timedelta(hours=25)).isoformat(), "valor": 320.00},
                {"id": "O003", "data_criacao": (datetime.now() - timedelta(hours=6)).isoformat(), "valor": 180.00}
            ]
            
            # Filtra pedidos com mais de 24h
            alertas = [p for p in pedidos_pendentes if 
                      (datetime.now() - datetime.fromisoformat(p["data_criacao"])).total_seconds() >= 24*3600]
            
            resultado = {
                "data_verificacao": datetime.now().isoformat(),
                "total_pendentes": len(pedidos_pendentes),
                "pendentes_24h": len(alertas),
                "alertas": alertas
            }
            
            # Se houver alertas, tenta enviar notificação
            if alertas and self.bot_token and self.chat_id:
                self._enviar_alerta_telegram(f"⚠️ ALERTA: {len(alertas)} pedidos pendentes há mais de 24h!")
            
            logger.info(f"Verificação concluída. {len(alertas)} pedidos pendentes há mais de 24h")
            return resultado
            
        except Exception as e:
            logger.exception("Erro ao monitorar pedidos pendentes")
            return {"erro": str(e)}
    
    def salvar_relatorio_json(self, relatorio: Dict[str, Any], caminho: str) -> bool:
        """
        Salva o relatório em um arquivo JSON
        
        Args:
            relatorio: Dicionário contendo o relatório
            caminho: Caminho onde o arquivo será salvo
            
        Returns:
            True se o arquivo foi salvo com sucesso, False caso contrário
        """
        try:
            # Cria o diretório se não existir
            diretorio = os.path.dirname(caminho)
            if diretorio and not os.path.exists(diretorio):
                os.makedirs(diretorio)
                
            # Salva o arquivo
            with open(caminho, 'w', encoding='utf-8') as f:
                json.dump(relatorio, f, indent=4, ensure_ascii=False)
                
            logger.info(f"Relatório salvo com sucesso em {caminho}")
            return True
            
        except Exception as e:
            logger.exception(f"Erro ao salvar relatório em {caminho}")
            return False
    
    def enviar_relatorio_telegram(self) -> bool:
        """
        Envia o relatório diário via Telegram
        
        Returns:
            True se o relatório foi enviado com sucesso, False caso contrário
        """
        try:
            if not self.bot_token or not self.chat_id:
                logger.error("Token do bot ou ID do chat não configurados")
                return False
                
            # Gera o relatório
            relatorio = self.gerar_relatorio_diario()
            
            # Verifica se houve erro na geração
            if "erro" in relatorio:
                logger.error(f"Erro ao gerar relatório para envio: {relatorio['erro']}")
                return False
            
            # Formata a mensagem
            mensagem = self._formatar_mensagem_telegram(relatorio)
            
            # Envia a mensagem
            resultado = self._enviar_mensagem_telegram(mensagem)
            
            return resultado
            
        except Exception as e:
            logger.exception("Erro ao enviar relatório via Telegram")
            return False
    
    def _formatar_mensagem_telegram(self, relatorio: Dict[str, Any]) -> str:
        """
        Formata o relatório para envio via Telegram
        
        Args:
            relatorio: Dicionário contendo o relatório
            
        Returns:
            Texto formatado para envio
        """
        try:
            data = datetime.fromisoformat(relatorio["data_geracao"]).strftime("%d/%m/%Y %H:%M")
            
            mensagem = f"📊 *RELATÓRIO DIÁRIO - {data}*\n\n"
            
            # Seção de vendas
            vendas = relatorio["vendas"]
            mensagem += f"*💰 VENDAS*\n"
            mensagem += f"Total: R$ {vendas['total']:.2f}\n"
            mensagem += f"Quantidade: {vendas['quantidade']}\n"
            mensagem += f"Ticket médio: R$ {vendas['ticket_medio']:.2f}\n"
            mensagem += f"Variação: {'+' if vendas['variacao_dia_anterior'] >= 0 else ''}{vendas['variacao_dia_anterior']:.1f}%\n\n"
            
            # Seção de pedidos
            pedidos = relatorio["pedidos"]
            mensagem += f"*📦 PEDIDOS*\n"
            mensagem += f"Novos: {pedidos['novos']}\n"
            mensagem += f"Em processamento: {pedidos['em_processamento']}\n"
            mensagem += f"Enviados: {pedidos['enviados']}\n"
            mensagem += f"Entregues: {pedidos['entregues']}\n"
            
            # Alertas se houver pedidos pendentes há mais de 24h
            if pedidos["pendentes_ha_mais_de_24h"] > 0:
                mensagem += f"⚠️ *Pendentes > 24h: {pedidos['pendentes_ha_mais_de_24h']}*\n\n"
            else:
                mensagem += "\n"
            
            # Seção financeira
            financeiro = relatorio["financeiro"]
            mensagem += f"*💵 FINANCEIRO*\n"
            mensagem += f"Receita bruta: R$ {financeiro['receita_bruta']:.2f}\n"
            mensagem += f"Custos: R$ {financeiro['custos_produtos'] + financeiro['custos_frete'] + financeiro['taxas_ml']:.2f}\n"
            mensagem += f"Lucro líquido: R$ {financeiro['lucro_liquido']:.2f}\n"
            mensagem += f"Margem: {financeiro['margem_lucro']:.1f}%\n\n"
            
            # Alerta de estoque
            produtos = relatorio["produtos"]
            if produtos["sem_estoque"] > 0 or produtos["estoque_baixo"] > 0:
                mensagem += f"*⚠️ ALERTAS DE ESTOQUE*\n"
                if produtos["sem_estoque"] > 0:
                    mensagem += f"Sem estoque: {produtos['sem_estoque']}\n"
                if produtos["estoque_baixo"] > 0:
                    mensagem += f"Estoque baixo: {produtos['estoque_baixo']}\n"
            
            return mensagem
            
        except Exception as e:
            logger.exception("Erro ao formatar mensagem para Telegram")
            return f"Erro ao formatar relatório: {str(e)}"
    
    def _enviar_mensagem_telegram(self, mensagem: str) -> bool:
        """
        Envia uma mensagem via Telegram
        
        Args:
            mensagem: Texto da mensagem a ser enviada
            
        Returns:
            True se a mensagem foi enviada com sucesso, False caso contrário
        """
        try:
            bot = telegram.Bot(token=self.bot_token)
            bot.send_message(
                chat_id=self.chat_id,
                text=mensagem,
                parse_mode="Markdown"
            )
            
            logger.info("Mensagem enviada com sucesso via Telegram")
            return True
            
        except Exception as e:
            logger.exception("Erro ao enviar mensagem via Telegram")
            return False
    
    def _enviar_alerta_telegram(self, mensagem: str) -> bool:
        """
        Envia um alerta via Telegram
        
        Args:
            mensagem: Texto do alerta a ser enviada
            
        Returns:
            True se o alerta foi enviado com sucesso, False caso contrário
        """
        try:
            return self._enviar_mensagem_telegram(mensagem)
        except Exception as e:
            logger.exception("Erro ao enviar alerta via Telegram")
            return False 