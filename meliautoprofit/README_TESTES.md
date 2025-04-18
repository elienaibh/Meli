# Testes Automatizados - MeliAutoProfit

Este documento contém informações sobre os testes automatizados do sistema MeliAutoProfit.

## Estrutura de Testes

Os testes estão organizados na pasta `tests` e seguem a seguinte estrutura:

- `conftest.py`: Configurações e fixtures do pytest
- `mocks.py`: Classes para mockagem de serviços externos
- `test_*_service.py`: Testes para os serviços
- `test_*_controller.py`: Testes para os controladores
- `plano_testes.md`: Plano de testes detalhado

## Componentes Testados

1. **Serviço de Listagem**
   - Busca de tendências
   - Busca de produtos no fornecedor
   - Seleção do melhor produto
   - Criação de anúncios no Mercado Livre
   - Criação de anúncios diários

2. **Serviço de Monitoramento**
   - Geração de relatórios diários
   - Monitoramento de pedidos pendentes
   - Salvamento de relatórios em JSON
   - Envio de relatórios e alertas via Telegram

3. **Serviço de Preparação**
   - Importação de produtos de arquivos CSV
   - Criação de produtos de teste
   - Backup de produtos em CSV

4. **Controladores**
   - Controlador de listagem automática

## Execução dos Testes

Para executar os testes, você pode usar o script `run_tests.py`:

```bash
# Executar todos os testes
python run_tests.py

# Executar testes em modo verboso
python run_tests.py --verbose

# Gerar relatório de cobertura de código
python run_tests.py --cov

# Gerar relatório de cobertura HTML
python run_tests.py --cov --html

# Testar apenas um módulo específico
python run_tests.py --module test_preparacao_service
```

Alternativamente, você pode usar o pytest diretamente:

```bash
# Na raiz do projeto
pytest tests/

# Com cobertura de código
pytest --cov=app --cov=database tests/

# Para um teste específico
pytest tests/test_listagem_service.py::TestListagemService::test_buscar_tendencias
```

## Mocks

Os testes utilizam mocks para simular as interações com APIs externas:

- **MockMercadoLivreAPI**: Simula as interações com a API do Mercado Livre
- **MockFornecedorAPI**: Simula as interações com as APIs dos fornecedores
- **MockTelegramAPI**: Simula o envio de mensagens via Telegram

## Banco de Dados para Testes

Os testes utilizam um banco de dados SQLite em memória, configurado no arquivo `conftest.py`. Este banco é recriado para cada sessão de teste, garantindo o isolamento entre os testes.

## Cobertura de Código

O relatório de cobertura de código mostra quais partes do código estão sendo testadas. Para gerar um relatório detalhado, execute:

```bash
python run_tests.py --cov --html
```

O relatório HTML será gerado na pasta `htmlcov/`.

## Integração Contínua

Estes testes podem ser integrados a um pipeline de CI/CD para garantir que as alterações no código não quebrem a funcionalidade existente.

## Requisitos para Testes

Os testes dependem dos seguintes pacotes:

- pytest
- pytest-cov
- coverage
- freezegun (para testes que manipulam datas)

Estes pacotes estão incluídos no arquivo `requirements-dev.txt`. 