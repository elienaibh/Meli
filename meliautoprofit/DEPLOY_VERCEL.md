# Deploy no Vercel

Este documento contém instruções para o deploy do projeto MeliAutoProfit no Vercel.

## Arquivos importantes

- `vercel.json`: Configuração principal do Vercel (definindo runtime Python 3.9)
- `api/index.py`: Ponto de entrada para o Vercel
- `requirements.txt`: Dependências do projeto
- `runtime.txt`: Versão específica do Python (3.9.16)

## Problemas conhecidos e soluções

### Versões de bibliotecas

Este projeto usa versões específicas das bibliotecas que são compatíveis com Python 3.9 no Vercel:

- A biblioteca aiohttp 3.8.5 é usada para evitar problemas de compilação com Python 3.12
- O FastAPI está na versão 0.95.2 por compatibilidade com outras dependências
- A versão do pydantic é 1.10.8 para garantir compatibilidade

### Variáveis de ambiente

Certifique-se de configurar todas as variáveis de ambiente necessárias no dashboard do Vercel:

- `DATABASE_URL`: URL do banco de dados (SQLite ou outro)
- `DEBUG`: Definido como "False" para produção
- `TELEGRAM_BOT_TOKEN`: Token do bot do Telegram para notificações
- `TELEGRAM_CHAT_ID`: ID do chat para notificações
- `ML_ITEMS_PER_DAY`: Número de itens a serem listados por dia
- `ML_MARGIN_PERCENTAGE`: Porcentagem de margem para produtos

## Deploy manual

Para fazer deploy manualmente:

1. Instale a CLI do Vercel: `npm install -g vercel`
2. Faça login: `vercel login`
3. Execute: `vercel --prod`

## Troubleshooting

- Se ocorrerem erros relacionados a bibliotecas, verifique a compatibilidade das versões no `requirements.txt`
- Para problemas com o tamanho da função Lambda, aumente o `maxLambdaSize` no `vercel.json`
- Consulte os logs de build no dashboard do Vercel para detalhes sobre erros específicos 