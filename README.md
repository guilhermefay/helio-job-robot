# 🤖 Robô de Empregos - Trocando de Emprego

## 📋 Visão Geral

Sistema de IA com agentes autônomos que automatiza o método **Trocando de Emprego** da Carolina Martins, ajudando profissionais a conquistarem novas oportunidades de trabalho através de estratégia inteligente no LinkedIn.

## 🎯 Objetivo

Transformar as etapas centrais do método validado por **13 mil alunos** em uma experiência assistida por IA, executando ou sugerindo ações baseadas em dados reais.

## 🏗️ Arquitetura do Sistema

### Agentes Autônomos (MVP)

1. **Agente 0: Diagnóstico e Onboarding**
   - Upload e análise de currículo
   - Análise do perfil LinkedIn
   - Questionário sobre objetivos profissionais
   - Geração de perfil unificado

2. **Agente 1: Extração de Palavras-chave**
   - Busca automática de vagas relevantes
   - Análise de frequência e relevância
   - Lista personalizada baseada em dados reais

3. **Agente 2: Otimização de Currículo**
   - Reestruturação seguindo método da Carol
   - Storytelling focado em resultados
   - Integração de palavras-chave

4. **Agente 3: Otimização do LinkedIn**
   - Otimização de headline e seção "sobre"
   - Aprimoramento de experiências
   - Aumento de visibilidade

5. **Agente 4: Geração de Conteúdo**
   - Roteiro editorial personalizado
   - Templates de postagens estratégicas
   - Construção de autoridade

## 📁 Estrutura do Projeto

```
robo-empregos/
├── agents/                 # Agentes autônomos
│   ├── agent_0_diagnostic/ # Diagnóstico e onboarding
│   ├── agent_1_keywords/   # Extração de palavras-chave
│   ├── agent_2_resume/     # Otimização de currículo
│   ├── agent_3_linkedin/   # Otimização LinkedIn
│   └── agent_4_content/    # Geração de conteúdo
├── core/                   # Funcionalidades compartilhadas
│   ├── models/            # Modelos de dados
│   ├── services/          # Serviços comuns
│   └── utils/             # Utilitários
├── api/                    # API REST
├── web/                    # Interface web
├── tests/                  # Testes automatizados
└── docs/                   # Documentação
```

## 🛠️ Stack Tecnológico

- **Backend:** Python + FastAPI
- **Frontend:** React + TypeScript
- **Banco de Dados:** PostgreSQL
- **Cache:** Redis
- **Containerização:** Docker
- **Cloud:** AWS/GCP
- **IA/ML:** OpenAI API, Hugging Face
- **Scraping:** BeautifulSoup, Selenium

## 🚀 Próximos Passos

1. ✅ **Configuração Inicial** (Em andamento)
   - [x] Estrutura de pastas
   - [x] Setup do ambiente Python
   - [ ] Configuração Docker
   - [ ] Setup banco de dados
   - [ ] Configuração de logging
   - [ ] Testes automatizados

2. 🔍 **Pesquisa de APIs**
   - [ ] LinkedIn API (limitações)
   - [ ] APIs de job boards
   - [ ] APIs de NLP
   - [ ] Análise de documentos

3. 🏗️ **Arquitetura dos Agentes**
   - [ ] Interfaces comuns
   - [ ] Sistema de comunicação
   - [ ] Estrutura de dados
   - [ ] Logs e monitoramento

## 📊 Métricas de Sucesso

- Palavras-chave geradas por sessão
- Currículos otimizados
- Perfis LinkedIn atualizados
- Posts publicados
- **Entrevistas agendadas** (métrica principal)

## 🔒 Privacidade e Segurança

- Criptografia de dados sensíveis
- Conformidade LGPD/GDPR
- Controle de acesso rigoroso
- Política de retenção de dados

## 🏆 Diferenciais

- ✅ Método validado com 13 mil alunos
- ✅ Autoridade da marca Carolina Martins
- ✅ IA que executa, não só conversa
- ✅ Base em dados reais, não teoria
- ✅ Aplicação prática e mensurável

---

**Desenvolvido com 💙 para revolucionar transições de carreira** # Railway deploy trigger
# Force Railway deploy
