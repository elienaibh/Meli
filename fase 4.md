Roadmap MeliAutoProfit - Fase 4: Lançamento e Monitoramento (Semana 9-10, 14 Dias)
Visão do Projeto
Sistema de e-commerce automatizado para renda passiva via dropshipping no Mercado Livre, usando APIs para listar produtos, processar pedidos, pagar fornecedores e monitorar lucros via app Flask e Telegram. Meta: R$15.000/mês em 6 meses, sem intervenção manual.
System Prompt
Analise visao_geral.txt e estrutura_projeto.json. Confirme entendimento, sugira otimizações e pergunte se quero código. Indique arquivo, função e local para mudanças, com comentários (#). Siga arquitetura MVC, foque em automação passiva e conformidade com APIs do Mercado Livre. Inclua logs de debug.

Tarefas
1. Preparar Lançamento

Inserir 50 produtos:# app/models/produto.py
produto = Produto(titulo="Fone JBL", preco=120)
session.add(produto)
session.commit()
print("DEBUG: Produto inserido")  # Debug do PDF


Fazer backup:pg_dump -U user meliautoprofit > backup.sql


Tempo Estimado: 6 horas.

2. Lançar Loja

Listar 50 produtos:# app/services/listagem.py
def criar_anuncios_diarios(self):
    logger.debug("DEBUG: 50 anúncios")  # Debug do PDF
    trends = self.ml_api.get_trends()
    for trend in trends[:50]:
        self.ml_api.create_item({"title": trend["keyword"], "price": trend["price"] * 1.3})


Configurar webhook:# app/main.py
@app.post("/webhook/orders")
async def handle_order(data: dict):
    logger.debug(f"DEBUG: Pedido {data['order_id']}")  # Debug do PDF
    order_processor.process_order(data["order_id"])


Tempo Estimado: 8 horas.

3. Configurar Monitoramento

Relatórios Telegram:# app/services/monitoramento.py
def relatorio_diario():
    logger.debug("DEBUG: Relatório")  # Debug do PDF
    telegram_bot.send_message("Lucro: R$150, 5 pedidos")


Tempo Estimado: 4 horas.

Entregáveis

50 produtos listados.
5 pedidos processados.
7 relatórios Telegram.

Tempo Total

18 horas.

