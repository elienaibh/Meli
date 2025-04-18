# Guia Completo de Teste - MeliAutoProfit

Este guia fornece instruções detalhadas para testar o sistema MeliAutoProfit em todas as suas fases, desde a configuração inicial até a execução dos testes automatizados.

## Pré-requisitos

1. **Ambiente Python**:
   - Python 3.8+ instalado
   - Pip atualizado
   - Ambiente virtual (recomendado)

2. **Banco de Dados**:
   - PostgreSQL (para produção)
   - SQLite (para testes)

3. **APIs Externas**:
   - Credenciais do Mercado Livre
   - Credenciais do Mercado Pago
   - Credenciais de fornecedores (CJ Dropshipping, Spocket)
   - Token do Telegram Bot

## 1. Configuração Inicial (Fase 1)

### 1.1. Configurar Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Windows)
venv\Scripts\activate

# Ativar ambiente virtual (Linux/Mac)
source venv/bin/activate
```

### 1.2. Instalar Dependências

```bash
# Instalar dependências de produção
pip install -r requirements.txt

# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt
```

### 1.3. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar o arquivo .env com suas credenciais
# Substitua os valores "seu_*_aqui" pelos valores reais
```

### 1.4. Configurar Banco de Dados

```bash
# Executar script de configuração do banco de dados
python setup_database.py
```

## 2. Preparação do Lançamento (Fase 2)

### 2.1. Testar Importação de Produtos

```bash
# Executar script de preparação de lançamento
python preparar_lancamento.py --importar produtos_pesquisa.csv
```

### 2.2. Criar Produtos de Teste

```bash
# Criar produtos de teste (50 produtos)
python preparar_lancamento.py --gerar-teste 50
```

### 2.3. Verificar Banco de Dados

```bash
# Verificar se os produtos foram adicionados
# (Use uma ferramenta SQL como DBeaver ou pgAdmin)
# Ou execute uma consulta SQL diretamente
```

## 3. Listagem de Produtos (Fase 3)

### 3.1. Executar Listagem Manual

```bash
# Executar listagem manual de produtos (teste)
python -c "from meliautoprofit.app.services.listagem import ListagemService; from meliautoprofit.database import get_db; ListagemService(next(get_db())).criar_anuncios_diarios()"
```

### 3.2. Verificar Logs

```bash
# Verificar logs de listagem
cat meliautoprofit.log | grep "DEBUG: Listagem"
```

### 3.3. Verificar API do Mercado Livre

```bash
# (Acesse o painel de desenvolvedor do Mercado Livre para verificar se os anúncios foram criados)
# https://developers.mercadolivre.com.br/
```

## 4. Monitoramento (Fase 4)

### 4.1. Gerar Relatório

```bash
# Executar geração de relatório
python gerar_relatorio.py
```

### 4.2. Enviar Relatório via Telegram

```bash
# Enviar relatório via Telegram
python gerar_relatorio.py --enviar-telegram
```

### 4.3. Verificar Alerta de Pedidos Pendentes

```bash
# Verificar pedidos pendentes
python -c "from meliautoprofit.app.services.monitoramento import MonitoramentoService; from meliautoprofit.database import get_db; MonitoramentoService(next(get_db())).monitorar_pedidos_pendentes()"
```

## 5. Testes Automatizados (Fase 5)

### 5.1. Executar Todos os Testes

```bash
# Executar todos os testes
python run_tests.py --verbose
```

### 5.2. Executar Testes Específicos

```bash
# Testar serviço de preparação
python run_tests.py --verbose --module test_preparacao_service

# Testar serviço de listagem
python run_tests.py --verbose --module test_listagem_service

# Testar serviço de monitoramento
python run_tests.py --verbose --module test_monitoramento_service
```

### 5.3. Verificar Cobertura de Código

```bash
# Gerar relatório de cobertura
python run_tests.py --cov --html
```

## 6. API e Interface Web

### 6.1. Iniciar Servidor

```bash
# Iniciar servidor da API
python -m uvicorn meliautoprofit.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 6.2. Testar Endpoints

```bash
# Testar endpoint de status
curl http://localhost:8000/

# Testar dashboard
# (Acesse http://localhost:8000/dashboard no navegador)

# Testar API de listagem
curl http://localhost:8000/api/v1/listagem/tendencias
```

## 7. Manutenção e Escalabilidade

### 7.1. Verificar Backup Automático

```bash
# Verificar backup do banco de dados
ls -la backup_*.sql
```

### 7.2. Testar Ajuste de Preço

```bash
# Ajustar preço de um produto específico
python -c "from meliautoprofit.app.services.listagem import ListagemService; from meliautoprofit.database import get_db; ListagemService(next(get_db())).ajustar_preco('MLB123456789')"
```

## Resolução de Problemas Comuns

### Problema 1: Erro de Autenticação com APIs Externas

```
ERROR: Authentication failed with Mercado Livre API
```

**Solução**: Verifique se as credenciais no arquivo `.env` estão corretas. Talvez o token tenha expirado e precise ser renovado.

### Problema 2: Banco de Dados Não Conecta

```
ERROR: Database connection failed
```

**Solução**: Verifique se o PostgreSQL está rodando e se as credenciais de banco de dados estão corretas no arquivo `.env`.

### Problema 3: Testes Falham

```
FAILED tests/test_*.py::Test*::test_* - AssertionError
```

**Solução**: Verifique os logs detalhados para entender o motivo da falha. Pode ser necessário atualizar os mocks ou ajustar as expectativas do teste.

### Problema 4: Servidor Não Inicia

```
ERROR: Uvicorn failed to start
```

**Solução**: Verifique se a porta 8000 não está sendo usada por outro processo. Tente usar uma porta diferente com `--port 8080`.

## Conclusão

Este guia deve ajudar a testar todas as funcionalidades do sistema MeliAutoProfit. Lembre-se de que, para um ambiente de produção, seria necessário configurar também:

1. **Segurança**: Certificados SSL, proteção contra ataques, etc.
2. **Monitoramento**: Prometheus, Grafana, alertas, etc.
3. **Backup**: Rotina automática de backup.
4. **CI/CD**: Pipeline de integração e entrega contínua.

Para mais detalhes sobre o desenvolvimento futuro, consulte o arquivo `PROXIMOS_PASSOS.md`. 