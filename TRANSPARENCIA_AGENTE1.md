# 🔍 TRANSPARÊNCIA TOTAL - AGENTE 1 (MPC)

## Visão Geral
Este documento explica como acessar **todos** os dados de transparência do Agente 1, permitindo visualizar cada vaga coletada, cada palavra-chave extraída e todo o processo de análise.

## Endpoints de Transparência

### 1. Executar Coleta (como sempre)
```bash
POST /api/agent1/collect-keywords
```

**Payload:**
```json
{
  "area_interesse": "tecnologia",
  "cargo_objetivo": "desenvolvedor python", 
  "localizacao": "São Paulo, SP",
  "total_vagas_desejadas": 50
}
```

**Resposta inclui agora:**
- Dados normais (estatísticas, palavras categorizadas, fontes)
- Seção `transparencia` com dados completos

### 2. Obter Transparência Completa (NOVO)
```bash
GET /api/agent1/transparency/{result_id}
```

**Retorna:**
- **`vagas_individuais`**: Array com todas as vagas coletadas
- **`palavras_brutas`**: Array com todas as palavras antes da categorização
- **`logs_processo`**: Array com logs detalhados do processo
- **`processo_extracao`**: Informações sobre o método usado
- **`resumo_coleta`**: Resumo executivo da coleta

### 3. Listar Análises Disponíveis (NOVO)
```bash
GET /api/agent1/results
```

**Retorna:**
- Lista de todas as análises feitas
- ID de cada análise para acessar transparência
- Informações básicas (vagas, palavras, fontes, data)

## Exemplo de Uso

### Passo 1: Executar Coleta
```bash
curl -X POST http://localhost:5001/api/agent1/collect-keywords \
  -H "Content-Type: application/json" \
  -d '{
    "area_interesse": "marketing",
    "cargo_objetivo": "analista de marketing",
    "total_vagas_desejadas": 30
  }'
```

### Passo 2: Obter ID da Resposta
```json
{
  "id": "mpc_20250105_104530_xyz",
  "estatisticas": { ... },
  "transparencia": { ... }
}
```

### Passo 3: Acessar Transparência Completa
```bash
curl http://localhost:5001/api/agent1/transparency/mpc_20250105_104530_xyz
```

## Dados de Transparência Disponíveis

### Vagas Individuais
Cada vaga coletada com:
- **titulo**: Título da vaga
- **empresa**: Nome da empresa
- **fonte**: LinkedIn Jobs, Google Jobs, etc.
- **descricao**: Descrição completa da vaga
- **localizacao**: Localização
- **data_coleta**: Quando foi coletada

### Palavras Brutas
- Lista de todas as palavras extraídas antes da categorização
- Ordem de extração preservada
- Sem filtros ou limites aplicados

### Logs Detalhados
- Processo passo a passo
- Quantidade de vagas por fonte
- Estatísticas de extração
- Validação com IA

### Processo de Extração
- **total_descricoes_processadas**: Quantas descrições foram processadas
- **texto_completo_tamanho**: Tamanho total do texto analisado
- **metodo_usado**: Método técnico usado para extração

## Script de Teste

Execute o script de teste para ver tudo funcionando:

```bash
python3 test_transparencia_agente1.py
```

Este script:
1. Executa uma coleta completa
2. Obtém os dados de transparência
3. Mostra as vagas coletadas
4. Mostra as palavras extraídas
5. Salva tudo em um arquivo JSON

## Benefícios da Transparência

### Para Validação
- ✅ Verificar se as vagas são reais
- ✅ Confirmar fontes utilizadas (LinkedIn, Google Jobs)
- ✅ Validar palavras-chave extraídas

### Para Debugging
- ✅ Identificar problemas na coleta
- ✅ Verificar qualidade das descrições
- ✅ Analisar eficácia da extração

### Para Auditoria
- ✅ Rastrear processo completo
- ✅ Documentar metodologia aplicada
- ✅ Comprovar conformidade com Carolina Martins

## Exemplo de Resposta de Transparência

```json
{
  "id": "mpc_20250105_104530_xyz",
  "timestamp": "2025-01-05T10:45:30",
  "logs_processo": [
    "🎯 Iniciando coleta para: analista de marketing em marketing",
    "📊 Meta de coleta: 30 vagas",
    "✅ Coletadas: 28 vagas reais",
    "📂 Fontes utilizadas: ['linkedin_jobs', 'google_jobs']",
    "🔤 Palavras extraídas: 145",
    "📋 Categorizadas: 42",
    "🤖 Validação IA: 38 aprovadas"
  ],
  "vagas_individuais": [
    {
      "titulo": "Analista de Marketing Digital",
      "empresa": "Tech Corp",
      "fonte": "linkedin_jobs",
      "descricao": "Responsável por campanhas digitais, análise de métricas...",
      "localizacao": "São Paulo, SP",
      "data_coleta": "2025-01-05T10:45:30"
    }
  ],
  "palavras_brutas": [
    "marketing", "digital", "campanhas", "google analytics", "facebook ads", ...
  ],
  "resumo_coleta": {
    "total_vagas": 28,
    "total_palavras": 145,
    "fontes_utilizadas": {"linkedin_jobs": 15, "google_jobs": 13},
    "metodo_extracao": "document_processor.extrair_palavras_chave_curriculo"
  }
}
```

## Integração com Frontend

Para integrar no frontend, adicione botões/seções para:

1. **"Ver Vagas Coletadas"** → Chama `/api/agent1/transparency/{id}`
2. **"Ver Logs do Processo"** → Mostra `logs_processo`
3. **"Palavras Extraídas"** → Mostra `palavras_brutas`
4. **"Histórico de Análises"** → Chama `/api/agent1/results`

## Conclusão

Agora você tem **transparência total** sobre:
- ✅ Quais vagas foram coletadas
- ✅ De quais fontes vieram
- ✅ Que palavras foram extraídas
- ✅ Como o processo funcionou
- ✅ Logs detalhados de cada etapa

**Nenhum dado é mais "misterioso" ou "mocado"** - tudo está visível e auditável!