Roadmap MeliAutoProfit - Fase 5: Manutenção e Escalabilidade (Semana 11+, Contínuo)
Visão do Projeto
Sistema de e-commerce automatizado para renda passiva via dropshipping no Mercado Livre, usando APIs para listar produtos, processar pedidos, pagar fornecedores e monitorar lucros via app Flask e Telegram. Meta: R$15.000/mês em 6 meses, sem intervenção manual.
System Prompt
Analise visao_geral.txt e estrutura_projeto.json. Confirme entendimento, sugira otimizações e pergunte se quero código. Indique arquivo, função e local para mudanças, com comentários (#). Siga arquitetura MVC, foque em automação passiva e conformidade com APIs do Mercado Livre. Inclua logs de debug.

Tarefas
1. Configurar Manutenção

Configurar alertas:sudo apt install prometheus


Backup semanal:pg_dump -U user meliautoprofit > backup_$(date +%F).sql


Atualizar dependencias.txt:with open("dependencias.txt", "w") as f:
    print("DEBUG: Atualizando dependências")  # Debug do PDF
    subprocess.run(["pip", "freeze"], stdout=f)


Tempo Estimado: 4 horas iniciais, 5min/mês.

2. Escalar Produtos

Listar 200 produtos:# app/services/listagem.py
def criar_anuncios_diarios(self):
    logger.debug("DEBUG: 30 novos produtos")  # Debug do PDF
    trends = self.ml_api.get_trends()
    for trend in trends[:30]:
        self.ml_api.create_item({"title": trend["keyword"], "price": trend["price"] * 1.3})


Tempo Estimado: 6 horas.

3. Otimizar Preços

Ajustar preços:# app/services/listagem.py
def ajustar_preco(self, item_id):
    logger.debug(f"DEBUG: Ajustando {item_id}")  # Debug do PDF
    new_price = ml_api.get_competitors(item_id)["lowest_price"] * 0.95
    ml_api.update_item(item_id, {"price": new_price})


Tempo Estimado: 4 horas.

4. Documentar Progresso

Criar resumo mensal:Mês 1: 200 produtos, R$1.800 lucro.


Tempo Estimado: 1 hora/mês.

Entregáveis

Alertas e backups configurados.
200 produtos listados.
10 preços ajustados.
Resumo mensal.

Tempo Total

15 horas iniciais, 1h/mês.

