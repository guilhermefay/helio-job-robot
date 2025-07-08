# 🚀 Como Executar o Sistema HELIO

Sistema completo com **backend real** e **frontend React** integrados.

## 🎯 **Status Atual**
- ✅ **Agente 0** - Análise de CV: **FUNCIONAL COM BACKEND REAL**
- ✅ **Agente 1** - Palavras-chave: **FUNCIONAL COM BACKEND REAL**
- ⏳ **Agentes 2,3,4** - Em desenvolvimento

## 📋 **Pré-requisitos**

### Obrigatórios:
- **Python 3.8+** 
- **Node.js 16+** e **npm**
- **Chaves de API** configuradas no `.env`:
  - `OPENAI_API_KEY`
  - `ANTHROPIC_API_KEY`

### Verificar instalação:
```bash
python3 --version
node --version
npm --version
```

## 🚀 **Opção 1: Execução Completa (Recomendado)**

**Execute tudo automaticamente:**
```bash
python3 start_helio.py
```

Este script:
1. Verifica dependências
2. Oferece instalar pacotes
3. Inicia backend (porta 5000)
4. Inicia frontend (porta 3000)
5. Abre ambos automaticamente

## 🔧 **Opção 2: Execução Manual**

### 1. **Instalar Dependências**
```bash
# Backend Python
pip install -r requirements.txt

# Frontend React
cd frontend
npm install
cd ..
```

### 2. **Executar Backend** (Terminal 1)
```bash
python3 start_backend.py
# ou diretamente:
python3 api_server.py
```

### 3. **Executar Frontend** (Terminal 2)
```bash
cd frontend
python3 start_frontend.py
# ou diretamente:
npm start
```

## 🌐 **URLs de Acesso**

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **Frontend** | http://localhost:3000 | Interface principal |
| **Backend API** | http://localhost:5000 | API REST |
| **Health Check** | http://localhost:5000/api/health | Status da API |

## 🧪 **Como Testar**

### **Agente 0 - Análise de CV:**
1. Acesse http://localhost:3000
2. Clique em "Agente 0 - Diagnóstico"
3. **Opção A:** Faça upload de um PDF/DOCX
4. **Opção B:** Cole texto do currículo (min. 500 chars)
5. Clique "Analisar Currículo"
6. ✅ **Resultado real:** Score, estrutura, validações

### **Agente 1 - Palavras-chave:**
1. Acesse http://localhost:3000
2. Clique em "Agente 1 - Palavras-chave"
3. Preencha: área, cargo, localização
4. Escolha quantidade de vagas
5. Clique "Iniciar Coleta de Vagas"
6. ✅ **Resultado real:** Palavras-chave categorizadas

## 🔍 **Verificar Funcionamento**

### **Backend funcionando:**
```bash
curl http://localhost:5000/api/health
```
**Resposta esperada:** Status OK com serviços ativos

### **Frontend funcionando:**
- Navegue para http://localhost:3000
- Deve ver dashboard com 5 cards de agentes
- Agentes 0 e 1 clicáveis
- Agentes 2,3,4 com "Em breve"

## 🛠️ **Troubleshooting**

### **Erro "ECONNREFUSED" no frontend:**
- ✅ Backend não está rodando
- ✅ Execute `python3 start_backend.py` primeiro

### **Erro 500 na API:**
- ✅ Verifique chaves no `.env`
- ✅ Verifique logs do terminal do backend

### **"Module not found":**
- ✅ Execute `pip install -r requirements.txt`
- ✅ Execute `cd frontend && npm install`

### **Porta já em uso:**
- ✅ Backend: mude porta em `api_server.py`
- ✅ Frontend: escolha porta diferente quando perguntado

## ⚡ **Scripts Disponíveis**

| Script | Comando | Descrição |
|--------|---------|-----------|
| **Completo** | `python3 start_helio.py` | Frontend + Backend |
| **Só Backend** | `python3 start_backend.py` | Apenas API |
| **Só Frontend** | `cd frontend && npm start` | Apenas React |

## 🎉 **Funcionalidades Implementadas**

### ✅ **Integração Completa:**
- Frontend React responsivo
- Backend Flask com APIs reais
- Comunicação AJAX entre frontend/backend
- Upload de arquivos funcionando
- Análise real de documentos
- Coleta real de vagas de emprego
- Validação por IA (OpenAI/Anthropic)

### ✅ **Sem Simulações:**
- Processamento real de PDF/DOCX
- Web scraping real (Indeed, InfoJobs, Catho)
- Análise de IA real
- Armazenamento de resultados
- Tratamento de erros completo

## 📚 **APIs Disponíveis**

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/health` | GET | Status dos serviços |
| `/api/agent0/analyze-cv` | POST | Análise de currículo |
| `/api/agent1/collect-keywords` | POST | Coleta de palavras-chave |
| `/api/results/<id>` | GET | Obter resultado por ID |
| `/api/agents/status` | GET | Status dos agentes |

---

## 🎯 **Sistema 100% Funcional!**

O sistema HELIO está **completamente integrado** e **sem simulações**. 
Os Agentes 0 e 1 usam serviços reais e APIs reais para fornecer resultados precisos.

**Execute e teste agora!** 🚀