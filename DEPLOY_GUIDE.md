# 🚀 Guia de Deploy - HELIO Job Robot

## ✅ Status Atual
- [x] Repositório criado: https://github.com/guilhermefay/helio-job-robot
- [x] Código enviado para GitHub
- [x] Arquivos de configuração prontos

## 🛠️ Deploy do Backend na Railway

### 1. Acesse a Railway
- Vá para [railway.app](https://railway.app)
- Faça login com sua conta GitHub

### 2. Criar Novo Projeto
1. Clique em "New Project"
2. Selecione "Deploy from GitHub repo"
3. Escolha o repositório: `guilhermefay/helio-job-robot`
4. A Railway detectará automaticamente que é um projeto Python

### 3. Configurar Variáveis de Ambiente
Na Railway, vá em **Variables** e adicione:

```env
# Environment
ENVIRONMENT=production

# Database (Railway fornecerá automaticamente)
DATABASE_URL=postgresql://...  # Railway auto-gera

# API Keys (OBRIGATÓRIAS - adicione suas chaves)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=ant-...

# Security
SECRET_KEY=sua_chave_secreta_super_forte_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs (opcional)
RAPIDAPI_KEY=sua_rapidapi_key

# Logging
LOG_LEVEL=INFO

# Frontend URL (será atualizado após deploy da Vercel)
FRONTEND_URL=https://seu-projeto.vercel.app
```

### 4. Adicionar Banco PostgreSQL
1. Na Railway, clique em "New" → "Database" → "PostgreSQL"
2. A variável `DATABASE_URL` será automaticamente criada
3. O Railway conectará o banco ao seu projeto

### 5. Deploy Automático
- O Railway detectará o `railway.json` e fará deploy automaticamente
- O projeto será executado com `python api_server.py`
- URL do backend: `https://seu-projeto.up.railway.app`

## 🌐 Deploy do Frontend na Vercel

### 1. Acesse a Vercel
- Vá para [vercel.com](https://vercel.com)
- Faça login com sua conta GitHub

### 2. Importar Projeto
1. Clique em "New Project"
2. Importe o repositório: `guilhermefay/helio-job-robot`
3. Configure as opções:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

### 3. Configurar Variáveis de Ambiente
Adicione a variável:

```env
REACT_APP_API_URL=https://seu-projeto.up.railway.app
```

### 4. Deploy Automático
- A Vercel detectará o `vercel.json` na raiz
- Fará build do frontend automaticamente
- URL do frontend: `https://seu-projeto.vercel.app`

## 🔄 Atualizar URLs Após Deploy

### 1. Atualizar CORS no Backend
Após obter a URL da Vercel, atualize na Railway:
```env
FRONTEND_URL=https://seu-projeto.vercel.app
```

### 2. Atualizar API URL no Frontend  
Na Vercel, atualize:
```env
REACT_APP_API_URL=https://seu-projeto.up.railway.app
```

## 📋 Checklist Pós-Deploy

### Backend (Railway)
- [ ] Deploy realizado com sucesso
- [ ] Banco PostgreSQL conectado
- [ ] Variáveis de ambiente configuradas
- [ ] API funcionando (teste: `GET /health`)
- [ ] Logs sem erros

### Frontend (Vercel)
- [ ] Deploy realizado com sucesso  
- [ ] Build executado sem erros
- [ ] Conectando com a API do backend
- [ ] Interface carregando corretamente

### Integração
- [ ] CORS configurado corretamente
- [ ] Frontend consegue acessar API
- [ ] Todas as funcionalidades testadas

## 🔑 Variáveis de Ambiente Obrigatórias

### Para Funcionamento Básico:
- `OPENAI_API_KEY` - Para análises de IA
- `SECRET_KEY` - Para segurança da aplicação
- `FRONTEND_URL` - Para configuração CORS

### Para Funcionalidades Avançadas:
- `ANTHROPIC_API_KEY` - Para Claude AI
- `RAPIDAPI_KEY` - Para scraping de vagas
- `LINKEDIN_CLIENT_ID/SECRET` - Para integração LinkedIn

## 🆘 Troubleshooting

### Erro de CORS
- Verifique se `FRONTEND_URL` no Railway está correto
- Aguarde alguns minutos para propagação

### Erro de Database
- Verifique se o PostgreSQL foi adicionado na Railway
- Confirme se `DATABASE_URL` foi gerada automaticamente

### Build Error no Frontend
- Verifique se `REACT_APP_API_URL` está configurado
- Confirme se não há erros de sintaxe no código

## 🎯 Próximos Passos

1. **Configurar Domínio Personalizado** (opcional)
2. **Configurar Monitoramento** 
3. **Configurar CI/CD** para deploys automáticos
4. **Configurar Backup do Banco**
5. **Configurar SSL/HTTPS** (automático na Railway/Vercel)

---

## 📞 URLs Finais

Após o deploy, você terá:

- **Frontend**: `https://seu-projeto.vercel.app`
- **Backend API**: `https://seu-projeto.up.railway.app` 
- **Documentação API**: `https://seu-projeto.up.railway.app/docs`

🎉 **Parabéns! Seu HELIO Job Robot está online!** 