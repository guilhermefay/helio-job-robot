// Configuração da API
const BASE_API_URL = process.env.REACT_APP_API_URL || process.env.VITE_API_URL || 'http://localhost:5001';

// WORKAROUND TEMPORÁRIO PARA CORS - usando proxy público
const USE_CORS_PROXY = process.env.NODE_ENV === 'production' && BASE_API_URL.includes('railway.app');
const CORS_PROXY = 'https://cors-anywhere.herokuapp.com/';
const API_URL = USE_CORS_PROXY ? `${CORS_PROXY}${BASE_API_URL}` : BASE_API_URL;

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