// api/callback.js
// Função serverless para Vercel
export default async function handler(req, res) {
  // Permitir CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  try {
    const { code } = req.query;
    
    console.log('Callback recebido:', { code, query: req.query });
    
    if (!code) {
      return res.status(400).json({ 
        error: 'Código de autorização não encontrado',
        received: req.query 
      });
    }

    // Suas credenciais do Portal de Parceiros
    const APP_ID = process.env.NUVEMSHOP_APP_ID || '19190';
    const CLIENT_SECRET = process.env.NUVEMSHOP_CLIENT_SECRET || 'a2fd713e74bf1d526c7e0514774cbee5f390a8302c9195b0';

    console.log('Trocando código por access_token...');
    
    // Fazer requisição para obter access_token
    const tokenResponse = await fetch('https://www.tiendanube.com/apps/authorize/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        client_id: APP_ID,
        client_secret: CLIENT_SECRET,
        grant_type: 'authorization_code',
        code: code
      })
    });

    const tokenData = await tokenResponse.json();
    
    console.log('Resposta da API:', tokenData);
    
    if (!tokenResponse.ok) {
      throw new Error(`Erro da API Nuvemshop: ${JSON.stringify(tokenData)}`);
    }

    // Verificar se recebeu access_token
    if (!tokenData.access_token) {
      throw new Error(`Token não recebido: ${JSON.stringify(tokenData)}`);
    }

    const { access_token, user_id, scope } = tokenData;
    
    // TODO: Salvar no banco de dados em produção
    console.log('✅ Aplicativo instalado com sucesso:', {
      store_id: user_id,
      scope: scope,
      timestamp: new Date().toISOString()
    });

    // Página de sucesso
    const successPage = `
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Aplicativo Instalado - LatAm Treasure</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.1);
                text-align: center;
                max-width: 500px;
                width: 100%;
            }
            .success-icon {
                font-size: 64px;
                margin-bottom: 20px;
            }
            h1 {
                color: #333;
                margin-bottom: 10px;
                font-size: 28px;
            }
            .subtitle {
                color: #666;
                margin-bottom: 30px;
                font-size: 16px;
            }
            .info-box {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
                text-align: left;
                border-left: 4px solid #28a745;
            }
            .info-item {
                margin: 8px 0;
                font-family: 'Courier New', monospace;
                font-size: 14px;
            }
            .btn {
                background: #007bff;
                color: white;
                padding: 12px 24px;
                text-decoration: none;
                border-radius: 6px;
                display: inline-block;
                margin-top: 20px;
                transition: background 0.3s;
            }
            .btn:hover {
                background: #0056b3;
            }
            .timestamp {
                color: #999;
                font-size: 12px;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="success-icon">🎉</div>
            <h1>Instalação Concluída!</h1>
            <p class="subtitle">Seu aplicativo foi conectado com sucesso à loja Nuvemshop.</p>
            
            <div class="info-box">
                <strong>📋 Detalhes da Instalação:</strong>
                <div class="info-item"><strong>Store ID:</strong> ${user_id}</div>
                <div class="info-item"><strong>Permissões:</strong> ${scope}</div>
                <div class="info-item"><strong>Status:</strong> ✅ Ativo</div>
            </div>
            
            <p>Agora você pode aproveitar todas as funcionalidades do aplicativo LatAm Treasure.</p>
            
            <a href="https://latamtreasure.com" class="btn">🏠 Voltar para a Loja</a>
            
            <div class="timestamp">
                Instalado em: ${new Date().toLocaleString('pt-BR')}
            </div>
        </div>
    </body>
    </html>`;

    res.setHeader('Content-Type', 'text/html');
    return res.status(200).send(successPage);

  } catch (error) {
    console.error('❌ Erro no callback:', error);
    
    // Página de erro
    const errorPage = `
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Erro na Instalação - LatAm Treasure</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.1);
                text-align: center;
                max-width: 500px;
                width: 100%;
            }
            .error-icon {
                font-size: 64px;
                margin-bottom: 20px;
            }
            h1 {
                color: #333;
                margin-bottom: 10px;
            }
            .error-details {
                background: #f8d7da;
                color: #721c24;
                padding: 15px;
                border-radius: 6px;
                margin: 20px 0;
                border: 1px solid #f5c6cb;
                text-align: left;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                word-break: break-all;
            }
            .btn {
                background: #6c757d;
                color: white;
                padding: 12px 24px;
                text-decoration: none;
                border-radius: 6px;
                display: inline-block;
                margin-top: 20px;
            }
            .btn:hover {
                background: #545b62;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="error-icon">❌</div>
            <h1>Erro na Instalação</h1>
            <p>Ocorreu um problema ao conectar o aplicativo à sua loja.</p>
            
            <div class="error-details">
                <strong>Detalhes técnicos:</strong><br>
                ${error.message}
            </div>
            
            <p>Tente instalar novamente ou entre em contato com o suporte.</p>
            
            <a href="https://latamtreasure.com" class="btn">🏠 Voltar para a Loja</a>
        </div>
    </body>
    </html>`;

    res.setHeader('Content-Type', 'text/html');
    return res.status(500).send(errorPage);
  }
}
