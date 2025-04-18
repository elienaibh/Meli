Roadmap MeliAutoProfit - Fase 3: Testes e Depuração (Semana 7-8, 14 Dias)
Visão do Projeto
Sistema de e-commerce automatizado para renda passiva via dropshipping no Mercado Livre, usando APIs para listar produtos, processar pedidos, pagar fornecedores e monitorar lucros via app Flask e Telegram. Meta: R$15.000/mês em 6 meses, sem intervenção manual.
System Prompt
Analise visao_geral.txt e estrutura_projeto.json. Confirme entendimento, sugira otimizações e pergunte se quero código. Indique arquivo, função e local para mudanças, com comentários (#). Siga arquitetura MVC, foque em automação passiva e conformidade com APIs do Mercado Livre. Inclua logs de debug.

Tarefas
1. Planejar Testes

Criar documento no Google Docs:
Listagem: 20 anúncios via /trends.
Pedidos: 10 pedidos simulados.
Erros: API 429, fornecedor rejeitado.


Atualizar visao_geral.txt com plano.
Tempo Estimado: 2 horas.

2. Executar Testes

Listagem:
# app/services/listagem.py
def criar_anuncios_diarios(self):
    print("DEBUG: Testando 20 anúncios")  # Debug do PDF
    trends = self.ml_api.get_trends()
    for trend in trends[:20]:
        self.ml_api.create_item({"title": trend["keyword"], "price": trend["price"] * 1.3})


Pedidos:

Simular via Postman:
POST https://api.mercadolibre.com/orders
Authorization: Bearer SEU_TOKEN
{"item": {"id": "MLB123"}, "quantity": 1}




Tempo Estimado: 12 horas.


3. Depurar

Configurar logs:
import logging
logging.basicConfig(filename="meliautoprofit.log", level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Iniciando listagem")


Corrigir API 429:
# app/api/mercado_livre.py
def retry_api_call(self, func):
    for _ in range(3):
        try:
            logger.debug("DEBUG: Tentando API")  # Debug do PDF
            return func()
        except:
            logger.debug("DEBUG: Retry após erro 429")
            sleep(60)


Tempo Estimado: 8 horas.


Entregáveis

Documento de testes.
meliautoprofit.log.
Sistema testado (20 anúncios, 10 pedidos).

Tempo Total

22 horas.

