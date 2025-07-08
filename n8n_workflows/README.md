# N8N Workflows - Agentes IA (Metodologia Carol Martins)

Este diretório contém os workflows N8N para os Agentes 0 e 1 do sistema de IA baseado na Metodologia Carol Martins.

## 📁 Arquivos

- `agent0_diagnostic_workflow.json` - Agente 0: Diagnóstico Curricular
- `agent1_keywords_workflow.json` - Agente 1: Mapa de Palavras-Chave (MPC)

## 🚀 Como Importar no N8N

### Passo 1: Acesse seu N8N
- Abra sua instância do N8N
- Vá para a página de Workflows

### Passo 2: Importe os Workflows
1. Clique em **"Import from File"** ou **"Import Workflow"**
2. Selecione o arquivo JSON do agente desejado
3. O workflow será carregado automaticamente

### Passo 3: Configure as Credenciais

#### Para Agent 0 (Diagnóstico):
- **Google API Key** (Gemini): Adicione em Settings → Credentials
- **Anthropic API Key** (Claude): Opcional, como fallback
- **OpenAI API Key** (GPT-4): Opcional, como fallback
- **Convertio API Key**: Para extração de texto de PDFs (ou substitua por outro serviço)

#### Para Agent 1 (Palavras-chave):
- **Apify API Token**: Para coletar vagas reais do LinkedIn
- **Google API Key** (Gemini): Para validação de palavras-chave com IA
- As mesmas APIs de IA do Agent 0 como fallback

### Passo 4: Configure as Variáveis de Ambiente

No N8N, vá em **Settings → Environment Variables** e adicione:

```
GOOGLE_API_KEY=sua_chave_google
ANTHROPIC_API_KEY=sua_chave_anthropic
OPENAI_API_KEY=sua_chave_openai
APIFY_API_TOKEN=seu_token_apify
```

## 📋 Descrição dos Workflows

### Agent 0 - Diagnóstico Curricular

**Objetivo**: Analisar currículos seguindo a metodologia Carolina Martins

**Fluxo**:
1. Recebe CV via webhook (arquivo ou texto)
2. Extrai texto do documento
3. Analisa com IA (Gemini/Claude/OpenAI)
4. Valida 10 elementos da metodologia
5. Calcula score de 0 a 100
6. Retorna análise completa com recomendações

**Entrada (POST para webhook)**:
```json
{
  "cv_text": "texto do currículo",
  "motivationData": {
    "cargoObjetivo": "Desenvolvedor Full Stack",
    "empresaSonho": "Google",
    "valoresImportantes": ["inovação", "flexibilidade"]
  }
}
```

### Agent 1 - Mapa de Palavras-Chave

**Objetivo**: Coletar vagas e extrair palavras-chave estratégicas

**Fluxo**:
1. Recebe parâmetros de busca via webhook
2. Expande queries e localizações
3. Coleta vagas do LinkedIn (Apify) ou usa demo
4. Extrai palavras-chave das descrições
5. Categoriza (técnicas, comportamentais, digitais)
6. Valida com IA
7. Aplica metodologia Carolina Martins (essencial >70%, importante 40-69%, complementar <40%)

**Entrada (POST para webhook)**:
```json
{
  "area_interesse": "Tecnologia",
  "cargo_objetivo": "Desenvolvedor Backend",
  "localizacao": "São Paulo",
  "total_vagas_desejadas": 50,
  "tipo_vaga": "remoto"
}
```

## 🔧 Customizações Recomendadas

### Substituir Serviços

1. **PDF para Texto**: O workflow usa Convertio, mas você pode substituir por:
   - N8N PDF nodes nativos
   - Outro serviço de OCR/extração

2. **Web Scraping**: Apify pode ser substituído por:
   - Bright Data
   - ScraperAPI
   - Playwright/Puppeteer nodes

3. **IA**: Ordem de preferência configurável:
   - Gemini (padrão)
   - Claude (fallback 1)
   - OpenAI (fallback 2)

### Adicionar Notificações

Adicione nodes de notificação após o processamento:
- Email (Send Email node)
- Slack (Slack node)
- Webhook para outro sistema

### Integrar com Banco de Dados

Adicione nodes para salvar resultados:
- PostgreSQL/MySQL nodes
- MongoDB nodes
- Google Sheets nodes

## 📊 Monitoramento

### Logs e Debugging
- Ative execução manual para testar
- Use o painel de execuções para ver detalhes
- Configure error workflows para capturar falhas

### Métricas Sugeridas
- Taxa de sucesso das análises
- Tempo médio de processamento
- Quantidade de palavras-chave extraídas
- Score médio dos currículos

## 🔐 Segurança

1. **Webhooks**: Configure autenticação nos webhooks
2. **API Keys**: Use credenciais do N8N, nunca hardcode
3. **Rate Limits**: Configure delays entre chamadas de API
4. **Dados Sensíveis**: Não logue informações pessoais

## 📝 Notas Importantes

1. **Limites de API**:
   - Gemini: 60 requests/minuto
   - Apify: Depende do plano
   - Configure delays se necessário

2. **Processamento em Lote**:
   - Agent 1 processa múltiplas combinações
   - Use Split in Batches para grandes volumes

3. **Fallbacks**:
   - Todos os nodes de IA têm continueOnFail ativo
   - Sistema degrada graciosamente

4. **Demo Mode**:
   - Agent 1 funciona sem Apify (modo demo)
   - Útil para testes e desenvolvimento

## 🤝 Suporte

Para dúvidas sobre:
- **Metodologia Carolina Martins**: Consulte a documentação do projeto
- **N8N**: https://docs.n8n.io/
- **APIs**: Documentação de cada provedor

## 🚀 Próximos Passos

Após importar e configurar os workflows:

1. Teste com dados de exemplo
2. Ajuste os prompts de IA conforme necessário
3. Configure automações e triggers
4. Integre com seus sistemas existentes
5. Implemente os Agentes 2, 3 e 4 seguindo o mesmo padrão

---

**Desenvolvido seguindo a Metodologia Carolina Martins**  
*Transformando carreiras através de IA e dados*