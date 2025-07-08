// Configuração dos agentes do sistema HELIO
// Baseado na metodologia Carolina Martins

export const agents = [
  {
    id: 0,
    name: "Diagnóstico",
    title: "Agente 0 - Diagnóstico e Onboarding",
    description: "Análise completa do seu perfil profissional, identificação de sabotadores e mapeamento da situação atual de carreira.",
    shortDesc: "Análise de perfil e identificação de sabotadores",
    status: "ativo",
    icon: "UserCircleIcon",
    color: "blue",
    features: [
      "Análise de currículo atual",
      "Identificação dos 10 sabotadores",
      "Mapeamento de experiência vs mercado",
      "Validação de expectativas (70%)",
      "Configuração personalizada"
    ],
    route: "/agent0",
    estimatedTime: "10-15 min",
    methodology: "13 passos Carolina Martins",
    inputs: [
      "Upload de currículo (PDF/DOCX)",
      "URL do LinkedIn",
      "Questionário de sabotadores",
      "Dados de experiência"
    ],
    outputs: [
      "Score de qualidade do currículo",
      "Sabotadores identificados",
      "Gaps e pontos fortes",
      "Recomendações personalizadas"
    ]
  },
  
  {
    id: 1,
    name: "Palavras-chave",
    title: "Agente 1 - Mapa de Palavras-Chave (MPC)",
    description: "Coleta de 50-100 vagas reais da sua área e extração das palavras-chave mais relevantes para otimizar seu currículo.",
    shortDesc: "Coleta de vagas e extração de palavras-chave",
    status: "ativo",
    icon: "MagnifyingGlassIcon",
    color: "green",
    features: [
      "Coleta de 50-100 vagas reais",
      "Extração automática de palavras-chave",
      "Categorização (técnica, comportamental, digital)",
      "Validação com IA (ChatGPT/Claude)",
      "Priorização por frequência"
    ],
    route: "/agent1",
    estimatedTime: "5-8 min",
    methodology: "Ferramenta MPC Carolina Martins",
    inputs: [
      "Área de interesse",
      "Cargo objetivo",
      "Localização preferida",
      "Segmentos de empresa"
    ],
    outputs: [
      "Lista priorizada de palavras-chave",
      "Análise de frequência no mercado",
      "Categorização por tipo",
      "Validação e sugestões de IA"
    ]
  },
  
  {
    id: 2,
    name: "Currículo",
    title: "Agente 2 - Otimização de Currículo",
    description: "Reestruturação completa do seu currículo seguindo os 13 passos da metodologia Carolina Martins.",
    shortDesc: "Reestruturação seguindo metodologia de 13 passos",
    status: "em_breve",
    icon: "DocumentTextIcon",
    color: "purple",
    features: [
      "Aplicação dos 13 passos metodológicos",
      "Currículo base vs personalizado",
      "Validações de honestidade",
      "Formatação Carolina Martins",
      "Score de qualidade (0-100)"
    ],
    route: "/agent2",
    estimatedTime: "15-20 min",
    methodology: "13 passos do currículo meteórico",
    comingSoonMessage: "Implementação dos 13 passos metodológicos em desenvolvimento"
  },
  
  {
    id: 3,
    name: "LinkedIn",
    title: "Agente 3 - Otimização LinkedIn",
    description: "Otimização completa do seu perfil LinkedIn seguindo os 10 passos para máxima visibilidade e autoridade.",
    shortDesc: "Otimização em 10 passos + estratégia de conteúdo",
    status: "em_breve",
    icon: "GlobeAltIcon",
    color: "blue",
    features: [
      "10 passos LinkedIn meteórico",
      "Estratégia de conteúdo 60/40",
      "SSI (Social Selling Index) tracking",
      "50 competências estratégicas",
      "Calendário editorial automatizado"
    ],
    route: "/agent3",
    estimatedTime: "12-18 min",
    methodology: "10 passos LinkedIn + estratégia 60/40",
    comingSoonMessage: "Integração com LinkedIn API e automações em desenvolvimento"
  },
  
  {
    id: 4,
    name: "Conteúdo",
    title: "Agente 4 - Geração de Conteúdo",
    description: "Criação automatizada de conteúdo estratégico para LinkedIn baseado no seu perfil e objetivos profissionais.",
    shortDesc: "Calendário editorial e posts automatizados",
    status: "em_breve",
    icon: "PencilSquareIcon",
    color: "orange",
    features: [
      "Calendário editorial estratégico",
      "Templates personalizados",
      "Personas da audiência",
      "Hashtags otimizadas",
      "KPIs e métricas de acompanhamento"
    ],
    route: "/agent4",
    estimatedTime: "8-12 min",
    methodology: "Estratégia de conteúdo 60/40",
    comingSoonMessage: "Sistema de geração automática de conteúdo em desenvolvimento"
  }
]

// Utility functions
export const getAgentById = (id) => {
  return agents.find(agent => agent.id === id)
}

export const getActiveAgents = () => {
  return agents.filter(agent => agent.status === 'ativo')
}

export const getComingSoonAgents = () => {
  return agents.filter(agent => agent.status === 'em_breve')
}

export const getAgentsByStatus = (status) => {
  return agents.filter(agent => agent.status === status)
}

// Status configurations
export const statusConfig = {
  ativo: {
    label: "Ativo",
    color: "text-green-600",
    bg: "bg-green-50",
    border: "border-green-200",
    icon: "CheckCircleIcon"
  },
  em_breve: {
    label: "Em Breve",
    color: "text-gray-500",
    bg: "bg-gray-50",
    border: "border-gray-200",
    icon: "ClockIcon"
  },
  processando: {
    label: "Processando",
    color: "text-blue-600",
    bg: "bg-blue-50",
    border: "border-blue-200",
    icon: "ArrowPathIcon"
  },
  erro: {
    label: "Erro",
    color: "text-red-600",
    bg: "bg-red-50",
    border: "border-red-200",
    icon: "ExclamationTriangleIcon"
  }
}