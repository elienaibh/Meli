"""
Script para gerar a estrutura do projeto MeliAutoProfit
"""
import json

print("DEBUG: Gerando estrutura do projeto")  # Debug do PDF

structure = {
    "projectName": "MeliAutoProfit",
    "rootDirectory": "meliautoprofit",
    "structure": [
        {
            "name": "meliautoprofit",
            "type": "directory",
            "description": "Diretório raiz do projeto",
            "children": [
                {
                    "name": "app",
                    "type": "directory",
                    "description": "Aplicação principal",
                    "children": [
                        {
                            "name": "api",
                            "type": "directory",
                            "description": "Módulos de integração com APIs externas",
                            "children": [
                                {"name": "mercado_livre.py", "type": "file", "description": "# Integração com Mercado Livre"},
                                {"name": "mercado_pago.py", "type": "file", "description": "# Integração com Mercado Pago"},
                                {"name": "fornecedor.py", "type": "file", "description": "# Integração com fornecedores"},
                                {"name": "telegram.py", "type": "file", "description": "# Integração com Telegram"}
                            ]
                        },
                        {
                            "name": "controllers",
                            "type": "directory",
                            "description": "Controladores da aplicação",
                            "children": [
                                {"name": "listagem_controller.py", "type": "file", "description": "# Controlador de listagem de produtos"},
                                {"name": "pedido_controller.py", "type": "file", "description": "# Controlador de pedidos"},
                                {"name": "pagamento_controller.py", "type": "file", "description": "# Controlador de pagamentos"}
                            ]
                        },
                        {
                            "name": "models",
                            "type": "directory",
                            "description": "Modelos de dados",
                            "children": [
                                {"name": "produto.py", "type": "file", "description": "# Modelo de produto"},
                                {"name": "pedido.py", "type": "file", "description": "# Modelo de pedido"},
                                {"name": "fornecedor.py", "type": "file", "description": "# Modelo de fornecedor"},
                                {"name": "base.py", "type": "file", "description": "# Base para os modelos"}
                            ]
                        },
                        {
                            "name": "services",
                            "type": "directory",
                            "description": "Serviços da aplicação",
                            "children": [
                                {"name": "listagem.py", "type": "file", "description": "# Serviço de listagem de produtos"},
                                {"name": "pedido.py", "type": "file", "description": "# Serviço de processamento de pedidos"},
                                {"name": "pagamento.py", "type": "file", "description": "# Serviço de processamento de pagamentos"},
                                {"name": "monitoramento.py", "type": "file", "description": "# Serviço de monitoramento"}
                            ]
                        },
                        {
                            "name": "templates",
                            "type": "directory",
                            "description": "Templates para interface web",
                            "children": [
                                {"name": "dashboard.html", "type": "file", "description": "# Template principal do dashboard"},
                                {"name": "relatorios.html", "type": "file", "description": "# Template de relatórios"}
                            ]
                        },
                        {"name": "main.py", "type": "file", "description": "# Ponto de entrada da aplicação FastAPI"},
                        {"name": "config.py", "type": "file", "description": "# Configurações da aplicação"}
                    ]
                },
                {
                    "name": "config",
                    "type": "directory",
                    "description": "Configurações e integrações com APIs",
                    "children": [
                        {"name": "api_mercadolivre.py", "type": "file", "description": "# Configuração da API Mercado Livre"},
                        {"name": "api_mercadopago.py", "type": "file", "description": "# Configuração da API Mercado Pago"},
                        {"name": "api_cjdropshipping.py", "type": "file", "description": "# Configuração da API CJ Dropshipping"},
                        {"name": "api_spocket.py", "type": "file", "description": "# Configuração da API Spocket"},
                        {"name": "api_telegram.py", "type": "file", "description": "# Configuração da API Telegram"}
                    ]
                },
                {
                    "name": "database",
                    "type": "directory",
                    "description": "Configuração de banco de dados",
                    "children": [
                        {"name": "models.py", "type": "file", "description": "# Modelos SQL Alchemy"},
                        {"name": "database.py", "type": "file", "description": "# Configuração do banco de dados"}
                    ]
                },
                {
                    "name": "tests",
                    "type": "directory",
                    "description": "Testes da aplicação",
                    "children": [
                        {"name": "test_api.py", "type": "file", "description": "# Testes das integrações com APIs"},
                        {"name": "test_services.py", "type": "file", "description": "# Testes dos serviços"}
                    ]
                },
                {"name": ".env.example", "type": "file", "description": "# Exemplo de variáveis de ambiente"},
                {"name": "requirements.txt", "type": "file", "description": "# Dependências do projeto"},
                {"name": "README.md", "type": "file", "description": "# Documentação do projeto"}
            ]
        }
    ]
}

# Salvar a estrutura em JSON
with open("estrutura_projeto.json", "w", encoding="utf-8") as f:
    json.dump(structure, f, indent=2)

print("DEBUG: Estrutura gerada com sucesso")  # Debug do PDF 