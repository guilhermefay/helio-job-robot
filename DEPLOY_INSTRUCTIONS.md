# Instruções de Deploy - Agentes IA (Metodologia Carol Martins)

## 🚀 Deploy Rápido - Railway + Vercel

### Passo 1: Deploy do Backend no Railway

1. **Acesse Railway.app** e faça login
2. **Crie um novo projeto** → "Deploy from GitHub repo"
3. **Conecte este repositório**
4. **Configure as variáveis de ambiente** (Settings → Variables):

```bash
# COPIE E COLE TODAS ESTAS VARIÁVEIS NO RAILWAY:

# APIs de IA (pelo menos uma é obrigatória)
GOOGLE_API_KEY=your_google_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key

# Para coleta real de vagas (opcional, funciona sem)
APIFY_API_TOKEN=your_apify_token

# Configuração do servidor
FLASK_ENV=production
PORT=5001
```

5. **Deploy será automático!** Railway vai detectar que é um app Python e fazer tudo
6. **Copie a URL do seu backend** (algo como: https://seu-app.railway.app)

### Passo 2: Deploy do Frontend na Vercel

1. **Faça commit e push** de todas as alterações:
```bash
git add .
git commit -m "Preparar para deploy"
git push origin main
```

2. **Acesse vercel.com** e faça login
3. **Import Git Repository** → Selecione este repositório
4. **Configure o Root Directory**: `frontend`
5. **Configure a variável de ambiente**:
```bash
REACT_APP_API_URL=https://seu-backend.railway.app
```
(Use a URL do Railway do passo anterior)

6. **Deploy!** A Vercel vai fazer build e deploy automaticamente

## ✅ Pronto!

Seu sistema estará disponível em:
- **Frontend**: https://seu-app.vercel.app
- **Backend**: https://seu-app.railway.app

## 🔧 Variáveis de Ambiente - Referência Completa

### Backend (Railway)

```bash
# APIs de IA - Pelo menos uma é necessária
GOOGLE_API_KEY=sk-...          # Para Gemini (recomendado)
ANTHROPIC_API_KEY=sk-ant-...   # Para Claude
OPENAI_API_KEY=sk-...          # Para GPT-4

# Scraping (Opcional - sistema funciona sem)
APIFY_API_TOKEN=apify_api_...  # Para coletar vagas reais do LinkedIn

# Configuração
FLASK_ENV=production
PORT=5001
```

### Frontend (Vercel)

```bash
# URL do Backend (obrigatório)
REACT_APP_API_URL=https://seu-backend.railway.app
```

## 📝 Notas Importantes

1. **Sem Apify?** O sistema detecta automaticamente e usa o modo demo com vagas de exemplo
2. **Sem API de IA?** Você precisa de pelo menos uma API (Google, Anthropic ou OpenAI)
3. **CORS**: Já está configurado para aceitar requisições da Vercel
4. **Custos**: 
   - Railway: Grátis até $5/mês de uso
   - Vercel: Grátis para projetos pessoais
   - APIs de IA: Têm planos gratuitos limitados

## 🆘 Troubleshooting

**Backend não inicia no Railway?**
- Verifique se adicionou pelo menos uma API key de IA
- Cheque os logs no Railway

**Frontend não conecta com backend?**
- Verifique se a variável REACT_APP_API_URL está correta
- A URL deve ser HTTPS e sem barra no final

**Erro de CORS?**
- O backend já está configurado, mas se precisar, adicione seu domínio Vercel no api_server.py

## 🎉 Sucesso!

Após o deploy, você terá:
- Sistema completo de 5 agentes IA
- Coleta de vagas (real com Apify ou demo)
- Análise com IA (Gemini, Claude ou GPT)
- Interface moderna e responsiva
- Tudo baseado na Metodologia Carol Martins