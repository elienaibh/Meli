# Guia Rápido de Teste - MeliAutoProfit

Este guia simplificado ajudará você a testar rapidamente o sistema MeliAutoProfit que desenvolvemos até agora.

## Configuração Inicial

1. **Crie o arquivo .env com suas credenciais**:
   
   ```bash
   # Copie o arquivo de exemplo
   cp .env.example .env
   
   # Edite o arquivo com suas credenciais reais
   # Você precisará das credenciais do Mercado Livre, Mercado Pago, 
   # CJ Dropshipping ou Spocket, e um bot do Telegram
   ```

2. **Configure seu ambiente virtual e instale as dependências**:
   
   ```bash
   # Crie um ambiente virtual
   python -m venv venv
   
   # Ative o ambiente virtual (Windows)
   venv\Scripts\activate
   
   # OU Ative o ambiente virtual (Linux/Mac)
   source venv/bin/activate
   
   # Instale as dependências
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Configure o banco de dados**:
   
   ```bash
   # Execute o script de configuração do banco de dados
   python setup_database.py
   ```

## Testes por Fase

### Fase 1: Planejamento e Configuração

Verifique se todos os arquivos de configuração estão presentes:

```bash
# Verifique os arquivos essenciais
ls .env.example
ls requirements.txt
ls gerar_estrutura.py
```

### Fase 2: Desenvolvimento

Teste a estrutura básica do projeto:

```bash
# Verifique se os diretórios principais existem
ls app/
ls database/
```

### Fase 3: Testes e Depuração

Execute os testes unitários:

```bash
# Execute todos os testes
python run_tests.py --verbose

# OU teste apenas um serviço específico
python run_tests.py --verbose --module test_listagem_service
```

### Fase 4: Lançamento e Monitoramento

Teste a geração de relatórios:

```bash
# Execute o script de monitoramento
python -c "from app.services.monitoramento import MonitoramentoService; from database import get_db; MonitoramentoService(next(get_db())).gerar_relatorio_diario()"
```

### Fase 5: Manutenção e Escalabilidade

Teste a execução dos testes de cobertura:

```bash
# Gere relatório de cobertura
python run_tests.py --cov --html
```

## Testes Rápidos por Componente

### Serviço de Preparação

```bash
# Teste a criação de produtos de teste
python -c "from app.services.preparacao import PreparacaoService; from database import get_db; PreparacaoService(next(get_db())).criar_produtos_teste(10)"
```

### Serviço de Listagem

```bash
# Teste a busca de tendências
python -c "from app.services.listagem import ListagemService; from database import get_db; print(ListagemService(next(get_db())).buscar_tendencias(5))"
```

### Serviço de Monitoramento

```bash
# Teste o monitoramento de pedidos pendentes
python -c "from app.services.monitoramento import MonitoramentoService; from database import get_db; print(MonitoramentoService(next(get_db())).monitorar_pedidos_pendentes())"
```

## Execução da API FastAPI

```bash
# Inicie o servidor FastAPI
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Acesse no navegador: http://localhost:8000/docs
# Você verá a documentação interativa da API
```

## Resolução de Problemas Comuns

### Erro: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'app'
```

**Solução**: Você precisa estar no diretório raiz do projeto (meliautoprofit). Verifique seu diretório atual e mude se necessário:

```bash
cd meliautoprofit
```

### Erro: Database connection failed

```
ERROR: Database connection failed
```

**Solução**: Verifique se suas configurações de banco de dados estão corretas no arquivo `.env`.

### Erro: Authentication failed with API

```
ERROR: Authentication failed with API
```

**Solução**: Verifique se suas credenciais de API estão corretas no arquivo `.env`.

## Próximos Passos

Após testar os componentes individuais, você pode começar a testar fluxos completos:

1. Criação de produtos de teste
2. Listagem de produtos no Mercado Livre
3. Simulação de pedidos
4. Geração de relatórios diários

Para uma análise mais detalhada, consulte o `GUIA_TESTE_COMPLETO.md`. 