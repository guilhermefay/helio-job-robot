// Configuração da API
const config = {
  // URL base da API - Railway em produção, localhost em desenvolvimento
  baseURL: process.env.NODE_ENV === 'production' 
    ? 'https://helio-job-robot-production.up.railway.app'
    : 'http://localhost:5000',
  
  endpoints: {
    agent0: {
      diagnostic: '/api/agent0/diagnostic',
      uploadFiles: '/api/agent0/upload-files'
    },
    agent1: {
      collectKeywords: '/api/agent1/collect-keywords',
      collectKeywordsStream: '/api/agent1/collect-keywords-stream',
      getResults: '/api/agent1/results'
    }
  }
}

export default config