import React, { useState } from 'react'
import config from '../config'

const Agent1Simple = () => {
  const [vagas, setVagas] = useState('')
  const [resultado, setResultado] = useState(null)
  const [carregando, setCarregando] = useState(false)
  const [erro, setErro] = useState(null)

  const analisarVagas = async () => {
    setCarregando(true)
    setErro(null)
    
    try {
      // Pega o texto das vagas e manda pra IA
      const response = await fetch(`${config.baseURL}/api/agent1/analyze-simple`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          texto_vagas: vagas,
          cargo: 'Desenvolvedor' // Valor fixo por enquanto
        })
      })

      if (!response.ok) {
        throw new Error('Erro na API')
      }

      const data = await response.json()
      setResultado(data)
    } catch (err) {
      setErro(err.message)
    } finally {
      setCarregando(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Análise Simples de Vagas</h1>
        
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <label className="block text-sm font-medium mb-2">
            Cole o texto das vagas aqui:
          </label>
          <textarea
            value={vagas}
            onChange={(e) => setVagas(e.target.value)}
            className="w-full h-64 p-3 border rounded-md"
            placeholder="Cole as descrições das vagas aqui..."
          />
          
          <button
            onClick={analisarVagas}
            disabled={!vagas.trim() || carregando}
            className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400"
          >
            {carregando ? 'Analisando...' : 'Analisar Vagas'}
          </button>
        </div>

        {erro && (
          <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-md mb-6">
            Erro: {erro}
          </div>
        )}

        {resultado && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4">Resultado da Análise</h2>
            <pre className="whitespace-pre-wrap text-sm">
              {JSON.stringify(resultado, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  )
}

export default Agent1Simple