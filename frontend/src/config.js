// Configuração da API
const API_URL = process.env.REACT_APP_API_URL || process.env.VITE_API_URL || 'https://helio-backend-v2-production.up.railway.app';

export default {
  API_URL,
  endpoints: {
    health: `${API_URL}/api/health`,
    agent0: {
      analyzeCV: `${API_URL}/api/agent0/analyze-cv`
    },
    agent1: {
      collectJobs: `${API_URL}/api/agent1/collect-jobs`,
      collectJobsDemo: `${API_URL}/api/agent1/collect-jobs-demo`,
      analyzeKeywords: `${API_URL}/api/agent1/analyze-keywords`,
      collectKeywordsStream: `${API_URL}/api/agent1/collect-keywords-stream`
    },
    results: `${API_URL}/api/results`
  }
};