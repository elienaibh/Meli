Roadmap MeliAutoProfit - Fase 1: Planejamento e Configuração (Semana 1-2, 14 Dias)
Visão do Projeto
Sistema de e-commerce automatizado para renda passiva via dropshipping no Mercado Livre, usando APIs para listar produtos, processar pedidos, pagar fornecedores e monitorar lucros via app Flask e Telegram. Meta: R$15.000/mês em 6 meses, sem intervenção manual.
System Prompt
Analise visao_geral.txt e estrutura_projeto.json. Confirme entendimento, sugira otimizações e pergunte se quero código. Indique arquivo, função e local para mudanças, com comentários (#). Siga arquitetura MVC, foque em automação passiva e conformidade com APIs do Mercado Livre. Inclua prints de debug.

Tarefas
1. Criar visao_geral.txt

Criar arquivo no diretório raiz:
MeliAutoProfit - Visão Geral
Objetivo: Loja automatizada no Mercado Livre, meta R$15.000/mês.
Stack: Python 3.10, FastAPI, PostgreSQL, APIs (Mercado Livre, Mercado Pago, CJ Dropshipping, Telegram).
Arquitetura: MVC (controllers: listagem/pedidos, models: Produto/Pedido, services: APIs).
Público: Consumidores brasileiros, produtos R$50-500.
GUI: Dashboard Flask (lucros, pedidos, erros).
Estado: Fase 1 - Planejamento e configuração.


Salvar backup no Google Drive.

Tempo Estimado: 1 hora.


2. Definir Objetivo e Estratégia

Criar documento no Google Docs:
Objetivo: Loja com 50 produtos iniciais, escalando para 500.
Estratégia:
Listagem: 5 anúncios/dia via /trends/MLB.
Pedidos: Enviar ao fornecedor via API após /orders.
Pagamentos: Transferir via Mercado Pago.
Monitoramento: Relatórios diários no Telegram e app Flask.


Metas:
Mês 1: 20 pedidos, R$600.
Mês 6: 300 pedidos, R$15.000.




Tempo Estimado: 2 horas.

3. Pesquisar Mercado

Criar planilha no Google Sheets:

Colunas: Produto, Categoria, Custo, Venda, Margem, Fornecedor.
Exemplo: “Fone JBL”, Eletrônicos, R$80, R$120, 33%, CJ Dropshipping.


Selecionar 20 produtos via /trends/MLB:
GET https://api.mercadolibre.com/trends/MLB
Authorization: Bearer SEU_TOKEN


Escolher 2 fornecedores (ex.: CJ Dropshipping, Spocket) com API, entrega <15 dias.

Tempo Estimado: 8 horas.


4. Configurar APIs

Mercado Livre:

Criar app no DevCenter (escopos: read, write).

Testar OAuth:
POST https://api.mercadolibre.com/oauth/token
Content-Type: application/x-www-form-urlencoded
client_id=SEU_CLIENT_ID&client_secret=SEU_SECRET_KEY&grant_type=client_credentials




Mercado Pago:

Obter credenciais /v1/payments.


Fornecedor:

Configurar CJ Dropshipping API:
POST https://api.cjdropshipping.com/orders
Authorization: Bearer SEU_TOKEN
{"product_id": "CJ123", "quantity": 1}




Telegram:

Criar bot via BotFather, canal @MeliAutoProfit.

Testar:
import requests
print("DEBUG: Testando Telegram")  # Debug do PDF
requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": "Fase 1 OK"})




Tempo Estimado: 8 horas.


5. Criar estrutura_projeto.json

Criar script gerar_estrutura.py:
import json
structure = {
    "projectName": "MeliAutoProfit",
    "rootDirectory": "app",
    "structure": [
        {
            "name": "app",
            "type": "directory",
            "description": "Backend MeliAutoProfit",
            "children": [
                {"name": "main.py", "type": "file", "description": "# FastAPI backend"},
                {"name": "listagem.py", "type": "file", "description": "# Serviço de listagem"}
            ]
        }
    ]
}
with open("estrutura_projeto.json", "w", encoding="utf-8") as f:
    json.dump(structure, f, indent=2)
print("DEBUG: Estrutura gerada")  # Debug do PDF


Executar: python3 gerar_estrutura.py.

Tempo Estimado: 2 horas.


Entregáveis

visao_geral.txt.
Documento de estratégia.
Planilha com 20 produtos, 2 fornecedores.
APIs configuradas.
estrutura_projeto.json.

Tempo Total

21 horas.

