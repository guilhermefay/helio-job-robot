# Agent 1 - Arquivos Completos e Status de Funcionalidade

## 🟢 ARQUIVOS PRINCIPAIS DO AGENT 1

### 1. **`/core/services/agente_1_palavras_chave.py`** ✅ REAL
- **Status**: Funcional, sem dados mockados
- **Classe**: `MPCCarolinaMartins`
- **Funcionalidades**:
  - `executar_mpc_completo()` - Processo completo do MPC
  - `coletar_vagas_reais()` - Chama o JobScraper
  - `extrair_palavras_chave()` - Extração via AI
  - `categorizar_palavras()` - Categorização automática
  - `validar_com_ia()` - Validação com GPT/Claude/Gemini

### 2. **`/core/services/job_scraper.py`** ⚠️ PARCIALMENTE MOCKADO
- **Status**: Contém métodos reais E simulados
- **Métodos REAIS**:
  - `_coletar_linkedin_selenium_real()` - USA APIFY! ✅
  - `_coletar_indeed()` - Web scraping real
  - `_coletar_linkedin_via_rapidapi()` - API real (se configurada)
  - `_coletar_adzuna_api()` - API real (se configurada)
  
- **Métodos MOCKADOS/SIMULADOS** ❌:
  - `_gerar_vagas_product_management_linkedin()`
  - `_gerar_vagas_marketing_linkedin()`
  - `_gerar_vagas_analista_linkedin()`
  - `_gerar_vagas_genericas_linkedin()`
  - `_gerar_templates_metodologicos()`
  - `_gerar_demo_honesto()`

### 3. **`/core/services/ai_keyword_extractor.py`** ✅ REAL
- **Status**: 100% funcional, sem mocks
- **Funcionalidades**:
  - Usa Gemini 2.5 Pro (preferencial)
  - Fallback para Claude 3 ou GPT-4
  - Extração inteligente com prompt sofisticado
  - SEM FALLBACK RUIM (removido conforme solicitado)

### 4. **`/core/services/linkedin_apify_scraper.py`** ✅ REAL
- **Status**: Funcional com Apify configurado
- **Actor**: `misceres/linkedin-jobs-scraper`
- **Métodos**:
  - `coletar_vagas_linkedin()` - Coleta real via Apify
  - `verificar_credenciais()` - Verifica token
  - `_processar_resultados_apify()` - Processa resultados

### 5. **`/core/services/query_expander.py`** ✅ REAL (NOVO)
- **Status**: 100% funcional
- **Funcionalidades**:
  - Expande queries genéricas
  - Gera múltiplas combinações cargo/localização
  - Melhora significativamente a coleta

### 6. **`/api_server.py`** ✅ REAL
- **Endpoints**:
  - `/api/agent1/collect-keywords` - Endpoint principal
  - `/api/agent1/collect-keywords-stream` - Com progresso via SSE
  - `/api/agent1/transparency/<id>` - Dados de transparência

### 7. **`/core/models/palavras_chave.py`** ✅ REAL
- **Status**: Modelos de banco de dados reais
- **Tabelas**:
  - `MapaPalavrasChave`
  - `VagaAnalisada`
  - `PalavraChave`
  - `ProcessamentoMPC`
  - `ValidacaoIA`

## 🔴 PROBLEMAS IDENTIFICADOS

### 1. **Métodos Simulados no job_scraper.py**
Os métodos `_gerar_*` retornam dados falsos. Eles são chamados quando:
- LinkedIn scraping falha
- APIs não estão configuradas
- Como fallback

### 2. **Dependência de APIs**
Para funcionar 100% real, precisa:
- ✅ `APIFY_API_TOKEN` - Configurado!
- ❌ `RAPIDAPI_KEY` - Não configurado
- ❌ `PROXYCURL_API_KEY` - Não configurado
- ❌ `ADZUNA_API_ID/KEY` - Não configurado

## 🛠️ CORREÇÕES NECESSÁRIAS

### 1. Remover/Desativar Métodos Simulados
```python
# Em job_scraper.py, substituir chamadas para:
# _gerar_vagas_* → retornar lista vazia []
# OU lançar exceção clara
```

### 2. Melhorar Fallbacks
```python
# Ao invés de gerar dados falsos:
if not vagas_reais:
    raise Exception("Não foi possível coletar vagas reais. Configure as APIs necessárias.")
```

### 3. Forçar Uso do Apify
```python
# Já está configurado, mas pode melhorar:
# - Adicionar retry logic
# - Tentar múltiplos actors se um falhar
# - Melhor tratamento de erros
```

## ✅ O QUE ESTÁ FUNCIONANDO

1. **Apify está configurado** e deve funcionar
2. **AI Keyword Extractor** com Gemini 2.5 Pro
3. **Query Expander** para melhorar buscas
4. **Modelos de banco** estruturados
5. **API endpoints** funcionais

## 📊 FLUXO ATUAL DO AGENT 1

```
1. API recebe request → /api/agent1/collect-keywords
2. JobScraper.coletar_vagas_multiplas_fontes()
   → Tenta LinkedIn via Apify ✅
   → Tenta Indeed scraping ✅
   → APIs complementares ❌ (não configuradas)
3. AIKeywordExtractor.extrair_palavras_chave_ia()
   → Usa Gemini 2.5 Pro ✅
4. Retorna palavras categorizadas
```

## 🚨 RECOMENDAÇÃO

Para garantir 0% dados mockados:
1. Desabilitar TODOS os métodos `_gerar_*`
2. Retornar erro claro quando não conseguir coletar
3. Focar no Apify que está configurado
4. Adicionar mais actors do Apify como backup