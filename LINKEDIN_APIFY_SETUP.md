# 🔗 Configuração do LinkedIn com Apify

## Por que Apify?

- ✅ **Mais confiável** que Selenium (sem bloqueios)
- ✅ **Mais barato** que outras APIs pagas
- ✅ **Mais rápido** e escalável
- ✅ **Sem necessidade** de gerenciar proxies

## 🚀 Configuração Rápida

### 1. Criar conta no Apify

1. Acesse [apify.com](https://apify.com)
2. Clique em "Sign up" (conta gratuita)
3. Confirme seu email

### 2. Obter API Token

1. No dashboard, clique no seu avatar (canto superior direito)
2. Vá em "Settings" → "Integrations"
3. Copie seu "Personal API token"

### 3. Configurar no HELIO

Adicione ao arquivo `.env`:

```bash
APIFY_API_TOKEN=apify_api_seu_token_aqui
```

### 4. Reiniciar o servidor

```bash
# Pare o servidor (Ctrl+C)
# Reinicie
python api_server.py
```

## 💰 Custos

### Actor Recomendado: curious_coder/linkedin-jobs-scraper

- **Custo**: ~$0.04 por execução (100 vagas)
- **Créditos gratuitos**: $5 mensais (125 execuções)
- **Link**: [curious_coder/linkedin-jobs-scraper](https://apify.com/curious_coder/linkedin-jobs-scraper)

### Comparação de custos:

| Serviço | Custo por 100 vagas | Observações |
|---------|---------------------|-------------|
| Apify (curious_coder) | $0.04 | Mais barato |
| Apify (bebity) | $0.10 | Mais features |
| ScraperAPI | $0.10 | Precisa Selenium |
| Proxycurl | $0.49 | API profissional |

## 🧪 Testar Configuração

### Via Python:

```python
from core.services.linkedin_apify_scraper import LinkedInApifyScraper

scraper = LinkedInApifyScraper()
if scraper.verificar_credenciais():
    print("✅ Apify configurado!")
else:
    print("❌ Verifique o token")
```

### Via API:

```bash
curl -X POST http://localhost:5001/api/agent1/collect-keywords \
  -H "Content-Type: application/json" \
  -d '{
    "area_interesse": "tecnologia",
    "cargo_objetivo": "desenvolvedor python",
    "localizacao": "São Paulo, SP",
    "total_vagas_desejadas": 10
  }'
```

## 📊 Dados Coletados

O Apify retorna dados ricos do LinkedIn:

- ✅ Título da vaga
- ✅ Empresa e logo
- ✅ Localização
- ✅ Descrição completa
- ✅ Link direto da vaga
- ✅ Data de publicação
- ✅ Número de candidatos
- ✅ Nível de experiência
- ✅ Tipo de emprego
- ✅ Salário (quando disponível)

## 🔍 Monitoramento

No dashboard do Apify você pode:

- Ver histórico de execuções
- Monitorar custos
- Debugar erros
- Configurar webhooks

## ⚠️ Limites e Boas Práticas

1. **Rate limits**: Máximo 100 vagas por execução
2. **Localização**: Use formato "Cidade, Estado" ou "Cidade, País"
3. **Keywords**: Seja específico (ex: "python backend" não apenas "python")
4. **Créditos**: Monitor seus créditos mensais gratuitos

## 🆘 Troubleshooting

### Token inválido
- Verifique se copiou o token completo
- Confirme que adicionou ao `.env`
- Reinicie o servidor

### Sem resultados
- Verifique a localização (use inglês para global)
- Tente keywords mais genéricas
- Verifique se tem créditos disponíveis

### Erro de execução
- Verifique os logs no dashboard Apify
- Tente com menos vagas (limite 50)
- Use localizações válidas do LinkedIn

## 📚 Recursos Adicionais

- [Documentação do Actor](https://apify.com/curious_coder/linkedin-jobs-scraper)
- [API Reference](https://docs.apify.com/api/v2)
- [Exemplos de código](https://github.com/apify/actor-templates)