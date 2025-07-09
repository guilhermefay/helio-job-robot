// Configuração de API
const config = {
  // URL base da API - Railway em produção, localhost em desenvolvimento  
  baseURL: process.env.NODE_ENV === 'production' 
    ? 'https://helio-job-robot-production.up.railway.app'
    : 'http://localhost:8080',
  
  endpoints: {
    agent1: {
      collectKeywords: '/api/agent1/collect-keywords',
      collectKeywordsStream: '/api/agent1/collect-keywords',
      collectJobsDemo: '/api/agent1/collect-keywords'
    },
    health: '/api/health'
  }
};

export default config;