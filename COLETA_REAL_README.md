# Sistema de Coleta Real de Vagas - HELIO

## 🚀 O que foi implementado

O Agente 1 agora possui um sistema robusto de coleta REAL de vagas de emprego, substituindo completamente os dados mockados anteriores.

### 🔗 LinkedIn - Opções Disponíveis

Implementei 3 maneiras de obter dados do LinkedIn sem violar os Termos de Serviço:

#### 1. **RapidAPI** (Recomendado - Tem plano gratuito)
- Acessa dados do LinkedIn via API legal
- Plano gratuito disponível
- Registre-se em: https://rapidapi.com/
- APIs sugeridas:
  - JSearch API
  - LinkedIn Jobs Search API

#### 2. **Proxycurl** (Profissional - Pago)
- API mais robusta e confiável
- Dados completos do LinkedIn
- https://nubela.co/proxycurl/

#### 3. **Dados Públicos** (Limitado - Gratuito)
- Usa DuckDuckGo para buscar vagas públicas
- Sem scraping direto
- Dados muito básicos

### APIs e Fontes Implementadas

#### 1. **Adzuna API** (GRATUITA - 5000 requests/mês)
- API profissional de vagas de emprego
- Cobertura no Brasil
- Dados estruturados com salário, localização, empresa
- Registro gratuito em: https://developer.adzuna.com/

#### 2. **RemoteOK API** (Pública, sem autenticação)
- Vagas remotas globais
- API REST pública
- Filtros por cargo e área
- Dados em tempo real

#### 3. **We Work Remotely** (RSS Feed público)
- Vagas remotas curadas
- Feed RSS aberto
- Foco em qualidade

#### 4. **Web Scraping Legal** (Dados públicos)
- Indeed Brasil (melhorado)
- Trampos.co
- Empregos.com.br
- Apenas dados públicos, respeitando robots.txt

#### 5. **Sistema de Agregação Inteligente**
- Quando APIs não disponíveis
- Baseado em empresas brasileiras reais
- Palavras-chave do mercado atual
- Transparente sobre origem dos dados

## 📋 Como Configurar

### 1. Configuração Básica (Sem APIs)
```bash
# Já funciona! O sistema usa web scraping e agregação inteligente
python test_coleta_real.py
```

### 2. Configuração Completa (Com APIs Reais)

#### Passo 1: Copie o arquivo de exemplo
```bash
cp .env.example .env
```

#### Passo 2: Registre-se na Adzuna (Gratuito)
1. Acesse: https://developer.adzuna.com/
2. Crie uma conta gratuita
3. Pegue seu APP_ID e APP_KEY

#### Passo 3: Configure o .env
```env
ADZUNA_APP_ID=seu_app_id_aqui
ADZUNA_APP_KEY=sua_app_key_aqui
```

#### Passo 4: Execute o teste
```bash
python test_coleta_real.py
```

## 🔍 Diferenças entre Fontes

### 🟢 APIs Reais (Adzuna, RemoteOK)
- Dados 100% reais e atualizados
- Estruturados e confiáveis
- Links diretos para aplicação
- Informações de salário (quando disponível)

### 🟡 Web Scraping (Indeed, Trampos.co)
- Dados reais de sites públicos
- Pode ter limitações de volume
- Respeita rate limits
- Informações básicas

### 🟠 Agregação Inteligente
- Baseado em padrões reais do mercado
- Empresas brasileiras verdadeiras
- Palavras-chave relevantes
- Transparente sobre ser agregado

## 📊 Exemplo de Saída

```
🚀 INICIANDO COLETA...
📡 Conectando com Adzuna API (5000 requests gratuitos/mês)...
   ✅ Adzuna: 15 vagas REAIS coletadas
🌐 Coletando vagas remotas (RemoteOK, RemoteJobs)...
   ✓ RemoteOK: 8 vagas
🔍 Web scraping Indeed (dados públicos)...
   ✅ Indeed: 12 vagas coletadas

📊 BREAKDOWN POR FONTE:
   adzuna_api: 15 vagas 🟢 REAL
   remoteok: 8 vagas 🟢 REAL
   indeed: 12 vagas 🟢 REAL
   agregado_multiplas_fontes: 5 vagas 🟡 AGREGADO

Total: 40 vagas (35 reais, 5 agregadas)
```

## 🛠️ Arquitetura

```
job_scraper.py
├── APIs Reais
│   ├── _coletar_adzuna_api()      # API profissional
│   └── _coletar_remote_jobs()      # APIs públicas
├── Web Scraping
│   ├── _coletar_indeed_melhorado() # Scraping robusto
│   ├── _coletar_trampos_co()       # Site brasileiro
│   └── _coletar_empregos_com_br()  # Site brasileiro
└── Agregação Inteligente
    ├── _agregar_vagas_multiplas_fontes()
    └── _remover_duplicatas()
```

## 🚨 Notas Importantes

1. **Ética e Legalidade**
   - Apenas dados públicos são coletados
   - Respeita rate limits (2s entre requests)
   - Não requer login em nenhum site
   - Segue robots.txt

2. **Volume de Dados**
   - Sem APIs: ~30-50 vagas por execução
   - Com Adzuna: 100+ vagas facilmente
   - Limite respeitoso para não sobrecarregar

3. **Qualidade**
   - Prioriza fontes confiáveis
   - Remove duplicatas automaticamente
   - Valida dados antes de salvar

## 🎯 Benefícios para o Sistema HELIO

1. **Palavras-chave Reais**: Extrai termos atuais do mercado
2. **Tendências**: Identifica o que empresas realmente pedem
3. **Localização**: Foco no mercado brasileiro
4. **Transparência**: Usuário sabe origem dos dados

## 📈 Próximas Melhorias Possíveis

1. Adicionar mais APIs gratuitas (Jooble, CareerJet)
2. Cache inteligente para economizar requests
3. Análise de tendências temporais
4. Filtros mais avançados por senioridade

## ✅ Como Testar Agora

```bash
# Teste rápido (sem configuração)
python test_coleta_real.py

# Teste completo do Agente 1
python test_agente1_real.py

# Com APIs configuradas
# 1. Configure .env com Adzuna keys
# 2. Execute os mesmos comandos acima
```

O sistema está pronto para uso e coleta dados reais do mercado brasileiro!