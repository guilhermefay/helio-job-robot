// Configuração da API
const config = {
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