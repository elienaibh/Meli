Roadmap MeliAutoProfit - Fase 2: Desenvolvimento (Semana 3-6, 28 Dias)
Visão do Projeto
Sistema de e-commerce automatizado para renda passiva via dropshipping no Mercado Livre, usando APIs para listar produtos, processar pedidos, pagar fornecedores e monitorar lucros via app Flask e Telegram. Meta: R$15.000/mês em 6 meses, sem intervenção manual.
System Prompt
Analise visao_geral.txt e estrutura_projeto.json. Confirme entendimento, sugira otimizações e pergunte se quero código. Indique arquivo, função e local para mudanças, com comentários (#). Siga arquitetura MVC, foque em automação passiva e conformidade com APIs do Mercado Livre. Inclua prints de debug.

Tarefas
1. Configurar Ambiente

Criar projeto:
mkdir meliautoprofit
cd meliautoprofit
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn psycopg2-binary python-telegram-bot requests


Criar dependencias.txt:
import subprocess
print("DEBUG: Gerando dependências")  # Debug do PDF
with open("dependencias.txt", "w") as f:
    subprocess.run(["pip", "freeze"], stdout=f)


Configurar Git:
git init
git add .
git commit -m "Setup inicial"


Tempo Estimado: 4 horas.


2. Estruturar Backend

Criar diretórios:
meliautoprofit/
├── app/
│   ├── api/
│   │   ├── mercado_livre.py
│   │   ├── fornecedor.py
│   ├── models/
│   │   ├── produto.py
│   ├── services/
│   │   ├── listagem.py
│   ├── main.py
├── dependencias.txt
├── estrutura_projeto.json


Configurar FastAPI:
# app/main.py
from fastapi import FastAPI
app = FastAPI(title="MeliAutoProfit")
@app.get("/")
async def root():
    print("DEBUG: Acessando raiz")  # Debug do PDF
    return {"message": "Loja Ativa!"}


Atualizar estrutura_projeto.json via gerar_estrutura.py.

Tempo Estimado: 6 horas.


3. Integrar APIs

Mercado Livre:
# app/api/mercado_livre.py
import requests
class MercadoLivreAPI:
    def __init__(self, client_id, secret):
        self.base_url = "https://api.mercadolibre.com"
        self.token = self.get_token(client_id, secret)
    def get_token(self, client_id, secret):
        print("DEBUG: Obtendo token")  # Debug do PDF
        data = {"grant_type": "client_credentials", "client_id": client_id, "client_secret": secret}
        response = requests.post(f"{self.base_url}/oauth/token", data=data)
        return response.json()["access_token"]


Fornecedor:
# app/api/fornecedor.py
class CJDropshippingAPI:
    def send_order(self, product_id, quantity):
        print(f"DEBUG: Pedido {product_id}")  # Debug do PDF
        return requests.post("https://api.cjdropshipping.com/orders", json={"product_id": product_id, "quantity": quantity}).json()


Telegram:
# app/api/telegram.py
class TelegramBot:
    def send_message(self, text):
        print(f"DEBUG: Mensagem: {text}")  # Debug do PDF
        return requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": text})


Tempo Estimado: 12 horas.


4. Configurar Banco

Criar tabelas:
CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255),
    preco DECIMAL
);


Modelo:
# app/models/produto.py
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    preco = Column(Float)
    def __repr__(self):
        print(f"DEBUG: Produto {self.titulo}")  # Debug do PDF
        return f"<Produto {self.titulo}>"


Tempo Estimado: 8 horas.


5. Implementar Listagem

Criar serviço:
# app/services/listagem.py
class ListagemService:
    def criar_anuncios_diarios(self):
        print("DEBUG: Buscando tendências")  # Debug do PDF
        trends = self.ml_api.get_trends()
        for trend in trends[:5]:
            self.ml_api.create_item({"title": trend["keyword"], "price": trend["price"] * 1.3})


Tempo Estimado: 10 horas.


Entregáveis

dependencias.txt.
Backend com MVC.
APIs integradas.
Banco com 1 produto.
1 anúncio criado.

Tempo Total

40 horas.

