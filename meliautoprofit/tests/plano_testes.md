# Plano de Testes - MeliAutoProfit

## Objetivo

Este plano de testes define a estratégia para validar o funcionamento do sistema MeliAutoProfit, com foco em garantir que a listagem automática de produtos e o processamento de pedidos funcionem corretamente, além de verificar a resiliência do sistema para lidar com falhas nas APIs externas.

## Escopo

### Componentes a serem testados

1. **Serviço de Listagem Automática**
   - Busca de tendências no Mercado Livre
   - Busca de produtos nos fornecedores
   - Seleção do melhor produto
   - Criação de anúncios no Mercado Livre

2. **Controlador de Listagem**
   - Endpoints de API para iniciar listagem automática
   - Busca de tendências
   - Processamento em background

3. **Integrações com APIs externas**
   - API do Mercado Livre
   - APIs de fornecedores (CJ Dropshipping, Spocket)
   - API do Telegram

### Tipos de Testes

1. **Testes Unitários**
   - Verificação isolada das funções dos serviços
   - Validação da lógica de negócio

2. **Testes de Integração**
   - Comunicação entre os componentes internos
   - Validação do ciclo completo de listagem

3. **Testes Funcionais**
   - Simulação da criação automática de anúncios
   - Verificação do comportamento esperado do sistema

4. **Testes de Resiliência**
   - Resposta a falhas nas APIs externas
   - Tratamento de erros como rate limiting (429)

## Estratégia de Teste

### Mocks e Fixtures

- Utilização de mocks para APIs externas (Mercado Livre, fornecedores, Telegram)
- Banco de dados em memória para testes isolados
- Fixtures para configurar o ambiente de teste

### Casos de Teste Principais

#### 1. Serviço de Listagem

| ID | Descrição | Resultado Esperado |
|----|-----------|-------------------|
| LS01 | Buscar tendências | Lista de tendências retornada com sucesso |
| LS02 | Buscar produtos no fornecedor | Lista de produtos retornada conforme a palavra-chave |
| LS03 | Selecionar melhor produto | Produto com melhor score é selecionado |
| LS04 | Criar anúncio no ML | Anúncio criado e salvo no banco de dados |
| LS05 | Criar anúncios diários | Quantidade configurada de anúncios é criada |
| LS06 | Lidar com lista vazia de tendências | Processo finalizado sem erro |
| LS07 | Lidar com lista vazia de fornecedores | Processo finalizado sem erro |

#### 2. Controlador de Listagem

| ID | Descrição | Resultado Esperado |
|----|-----------|-------------------|
| LC01 | Criar anúncios automáticos via endpoint | Tarefa adicionada ao background e resposta 200 |
| LC02 | Buscar tendências via endpoint | Lista de tendências retornada na resposta |
| LC03 | Processar listagem em background | Anúncios criados e notificação enviada |
| LC04 | Lidar com erro no processamento | Erro capturado e notificação de erro enviada |

#### 3. API do Mercado Livre

| ID | Descrição | Resultado Esperado |
|----|-----------|-------------------|
| ML01 | Atualizar token de acesso | Token atualizado com sucesso |
| ML02 | Buscar tendências | Lista de tendências retornada |
| ML03 | Criar item no Mercado Livre | Item criado e ID retornado |
| ML04 | Lidar com erro de rate limiting (429) | Retry após o tempo de espera |
| ML05 | Lidar com token expirado | Token atualizado e operação reexecutada |

## Métricas de Cobertura

- **Cobertura de código:** Mínimo de 80% de cobertura para os serviços principais
- **Cobertura de casos de uso:** 100% dos fluxos críticos cobertos por testes

## Ambiente de Teste

- Banco de dados SQLite em memória para testes
- Mocks para todas as APIs externas
- Configurações específicas para testes em arquivo `.env.test`

## Relatórios

Os relatórios de teste serão gerados utilizando:
- Saída padrão do pytest
- Relatório de cobertura do coverage
- Exportação de relatório HTML para análise detalhada

## Critérios de Aceitação

- Todos os testes passando
- Cobertura mínima de 80% atingida
- Todos os cenários de erro testados
- Implementação da funcionalidade de retry para erros 429 