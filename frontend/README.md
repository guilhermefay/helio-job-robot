# HELIO Frontend

Frontend do sistema HELIO - Jornada IA para recolocação profissional.

## 🚀 Como executar

### Pré-requisitos
- Node.js (versão 16 ou superior)
- npm ou yarn

### Instalação e execução

1. **Instalar dependências:**
```bash
npm install
```

2. **Executar em desenvolvimento:**
```bash
npm start
```

3. **Abrir no navegador:**
- O aplicativo será executado em: http://localhost:3000
- A página será recarregada automaticamente quando você fizer alterações

## 🎯 Funcionalidades

### Agentes Funcionais
- **Agente 0 - Diagnóstico:** Análise completa de CV
- **Agente 1 - Palavras-chave:** Coleta de vagas e extração de palavras-chave

### Agentes em Desenvolvimento
- **Agente 2 - Currículo:** Otimização seguindo metodologia Carolina Martins
- **Agente 3 - LinkedIn:** Otimização de perfil em 10 passos
- **Agente 4 - Conteúdo:** Geração automatizada de conteúdo

## 🛠️ Tecnologias

- React 18
- React Router DOM
- TailwindCSS
- Heroicons
- Metodologia Carolina Martins

## 📁 Estrutura

```
src/
├── App.jsx              # Componente principal e roteamento
├── components/
│   └── AgentCard.jsx    # Componente de card dos agentes
├── pages/
│   ├── Agent0.jsx       # Página do Agente 0 (funcional)
│   └── Agent1.jsx       # Página do Agente 1 (funcional)
├── data/
│   └── agents.js        # Dados dos agentes
├── assets/
│   └── theme.js         # Configuração de tema
└── index.js             # Ponto de entrada
```

## 🎨 Design System

Baseado nas cores do LinkedIn:
- **Azul principal:** #0077B5
- **Fundo:** #F3F6F9  
- **Texto:** #1D1D1F
- **Interface limpa e profissional**

## 📱 Responsividade

- Mobile-first design
- Breakpoints otimizados para todas as telas
- Componentes adaptativos