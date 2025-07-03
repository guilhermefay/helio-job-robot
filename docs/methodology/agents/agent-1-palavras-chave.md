# Agente 1: Metodologia de Palavras-Chave (MPC) - Carolina Martins

## 📋 Visão Geral

### Conceito da Ferramenta MPC
A ferramenta **MPC (Mapa de Palavras-Chave)** é mencionada extensivamente nas transcrições como um pré-requisito fundamental para construção do currículo meteórico. Esta ferramenta deve ser completada ANTES da construção do currículo.

### Referências nas Transcrições

**Aula 2 - Qualificações:**
> "você já fez a ferramenta MPC você já levantou as palavras-chave e agora aqui a gente vai começar a usar essas palavras-chave"

**Aula 6 - Resumo:**
> "Como eu sei, quais são as competências importantes, você já sabe porque você já fez a ferramenta do MPC"

**Aula 8 - Experiências:**
> "você já tem o seu guia de palavra-chave, então não seja irresponsável a ponto de não usar"

**Aula 12 - Tecnologia:**
> "para isso aquele guia que você fez o MPC a ferramenta das palavras-chave pode te ajudar"

## 🎯 Metodologia Inferida do MPC

### Processo de Pesquisa
1. **Busca por vagas** da área de interesse
2. **Extração de palavras-chave** das vagas
3. **Validação no ChatGPT**
4. **Pesquisa em perfis profissionais**
5. **Mapeamento de competências**

### Tipos de Palavras-Chave Identificadas

**Competências Técnicas:**
- Gestão de projetos
- Gestão de equipe
- Resolução de conflitos
- Planejamento e execução
- Estruturação de time
- Implantação de recursos

**Competências Digitais:**
- Excel (sempre presente)
- SAP (diversos módulos)
- CRM (Salesforce, etc.)
- ERP específicos
- Linguagens de programação

**Palavras-Chave por Contexto:**
- Segmentos de atuação
- Tipos de empresa
- Processos específicos
- Metodologias
- Certificações relevantes

## 🔍 Aplicação das Palavras-Chave

### No Resumo do Currículo
> "a gente começa a falar de palavra-chave e a gente começa a inserir as palavras-chave logo no campo de resumo"

**Estrutura de aplicação:**
```
Sólidos conhecimentos em [PALAVRA-CHAVE 1], [PALAVRA-CHAVE 2], 
vivência em [PALAVRA-CHAVE 3] com foco em [PALAVRA-CHAVE 4].
```

### Nas Experiências Profissionais
> "é essencial ter palavra-chave no seu resumo... Porém na experiência profissional é muito importante"

**Aplicação estratégica:**
- Integrar palavras-chave nas descrições de responsabilidades
- Usar em resultados obtidos
- Mencionar em atividades principais
- Aplicar em contexto natural

### Em Tecnologia/Softwares
> "Com base no MPC e você fez então a vaga pede e você tem cruzou essas informações"

**Processo de cruzamento:**
1. Palavras-chave tecnológicas do MPC
2. Competências que o profissional possui
3. Match entre demanda e oferta
4. Priorização por relevância

## 📊 Estrutura Inferida da Ferramenta MPC

### Seções Possíveis
1. **Competências Comportamentais**
2. **Competências Técnicas**
3. **Softwares e Tecnologias**
4. **Segmentos de Atuação**
5. **Tipos de Empresa**
6. **Processos e Metodologias**
7. **Certificações Relevantes**

### Validação Multi-Fonte
- **Vagas reais**: Análise de job descriptions
- **ChatGPT**: Validação de relevância
- **Perfis profissionais**: Benchmark de mercado
- **Recorrência**: Palavras mais frequentes

## 🎯 Implementação no Agente 1

### Input Necessário
- **Área de atuação** do usuário
- **Cargo objetivo** atual
- **Nível hierárquico** pretendido
- **Segmentos de interesse**
- **Localização geográfica**

### Processo Automatizado

#### 1. Coleta de Vagas
- **Job boards**: LinkedIn, Catho, InfoJobs, etc.
- **Sites corporativos**: Empresas target
- **Filtros**: Cargo, localização, senioridade
- **Volume**: Mínimo 50-100 vagas relevantes

#### 2. Extração de Palavras-Chave
- **NLP processing**: Análise de texto das vagas
- **Frequência**: Palavras mais recorrentes
- **Categorização**: Por tipo de competência
- **Priorização**: Por relevância e frequência

#### 3. Validação e Enriquecimento
- **IA validation**: ChatGPT/Claude para validar relevância
- **Profile matching**: Análise de perfis LinkedIn top performers
- **Market research**: Tendências da área
- **Competências emergentes**: Skills do futuro

#### 4. Organização e Entrega
- **Categorização clara** por tipo
- **Ranking de prioridade**
- **Contexto de uso** (onde aplicar)
- **Exemplos práticos** de aplicação

### Output Estruturado

```json
{
  "competencias_comportamentais": [
    {
      "palavra_chave": "gestão de equipe",
      "frequencia": 85,
      "contexto": "requisito essencial",
      "aplicacao": ["resumo", "experiencias"]
    }
  ],
  "competencias_tecnicas": [
    {
      "palavra_chave": "gestão de projetos",
      "frequencia": 78,
      "metodologias": ["Scrum", "Agile"],
      "aplicacao": ["resumo", "experiencias", "certificacoes"]
    }
  ],
  "tecnologias": [
    {
      "ferramenta": "Excel",
      "nivel_exigido": "avançado",
      "frequencia": 95,
      "modulos": ["VBA", "Power Query", "Tabelas Dinâmicas"]
    }
  ]
}
```

## 💡 Insights da Metodologia Carolina

### Importância Crítica
> "as palavras-chave, elas vão fazer com que o recrutador, identifique mais rápido e você é um profissional bem compatível com a vaga"

### Aplicação Natural
- Não forçar palavras-chave artificialmente
- Integrar naturalmente nas descrições
- Usar contexto profissional real
- Manter autenticidade

### Filtros de Triagem
> "o filtro de triagem do recrutador teria currículos por palavras-chave"

**Implicações:**
- ATS (Applicant Tracking Systems) fazem busca por keywords
- Palavras-chave corretas = passar na triagem inicial
- Localização estratégica nas seções certas
- Match com job description específica

## 🔄 Integração com Outros Agentes

### Com Agente 0 (Diagnóstico)
- Recebe área de atuação e objetivos
- Define parâmetros de busca
- Estabelece nível de senioridade

### Com Agente 2 (Currículo)
- Fornece palavras-chave estruturadas
- Guia aplicação em cada campo
- Valida otimização para ATS

### Com Agente 3 (LinkedIn)
- Mesmas palavras-chave para consistência
- Adaptação para formato LinkedIn
- SEO para busca de recrutadores

### Com Agente 4 (Conteúdo)
- Keywords para autoridade temática
- Hashtags relevantes
- Temas para posts

---

**Nota**: Esta metodologia foi inferida das múltiplas referências ao MPC nas transcrições do Módulo Currículo Meteórico. A ferramenta MPC é claramente fundamental para todo o método Carolina Martins.