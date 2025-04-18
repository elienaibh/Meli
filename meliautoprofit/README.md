# MeliAutoProfit

Sistema automatizado de e-commerce para renda passiva via dropshipping no Mercado Livre.

## Sobre o Projeto

MeliAutoProfit é um sistema que automatiza operações de e-commerce no Mercado Livre utilizando APIs para listar produtos, processar pedidos, pagar fornecedores e monitorar lucros. O objetivo é criar uma fonte de renda passiva através do dropshipping.

### Funcionalidades Principais

- Listagem automatizada de produtos baseada em tendências
- Processamento automático de pedidos
- Integração com fornecedores dropshipping
- Dashboard para monitoramento de métricas
- Alertas e relatórios via Telegram
- Testes automatizados para garantir a estabilidade

## Configuração e Execução

### Pré-requisitos

- Python 3.8+
- PostgreSQL
- Conta de desenvolvedor no Mercado Livre
- Contas nas plataformas de dropshipping (CJ Dropshipping, Spocket, etc)
- Bot do Telegram

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/elienaibh/MeliAutoProfit.git
cd MeliAutoProfit
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

5. Configure o banco de dados:
```bash
python setup_database.py
```

### Execução

Para iniciar o servidor:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Acesse o dashboard em: http://localhost:8000/dashboard

### Testes

Para executar os testes:
```bash
python run_tests.py --verbose
```

Para gerar relatório de cobertura:
```bash
python run_tests.py --cov --html
```

## Estrutura do Projeto

```
meliautoprofit/
├── app/                  # Aplicação principal
│   ├── api/              # Integrações com APIs externas
│   ├── controllers/      # Controladores de rotas
│   ├── models/           # Modelos de dados
│   ├── services/         # Serviços de negócio
│   ├── templates/        # Templates HTML
│   ├── config.py         # Configurações da aplicação
│   └── main.py           # Ponto de entrada da aplicação
├── database/             # Configuração e modelos do banco de dados
├── tests/                # Testes automatizados
├── .env.example          # Exemplo de variáveis de ambiente
├── requirements.txt      # Dependências do projeto
└── setup_database.py     # Script para configuração do banco de dados
```

## Deployment na Vercel

1. Garanta que tenha um arquivo `vercel.json` na raiz do projeto
2. Configure as variáveis de ambiente na Vercel
3. Configure a URL de callback no Mercado Livre para apontar para sua aplicação na Vercel
4. Faça o deploy através do dashboard da Vercel ou CLI

## Licença

Este projeto é licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.

## Contato

Seu Nome - elienaibh@gmail.com

Link do Projeto: [https://github.com/elienaibh/MeliAutoProfit](https://github.com/elienaibh/MeliAutoProfit) 