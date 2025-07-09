import React, { useState, useEffect, useRef } from 'react'
import config from '../config'
import { 
  ArrowPathIcon, 
  CheckCircleIcon, 
  ExclamationTriangleIcon 
} from '@heroicons/react/24/outline'

const ProgressStream = ({ isActive, onComplete, onError, requestData }) => {
  const [progress, setProgress] = useState(0)
  const [message, setMessage] = useState('Iniciando coleta de vagas...')
  const [status, setStatus] = useState('iniciando')
  const [fakeProgress, setFakeProgress] = useState(0)
  const [jokeIndex, setJokeIndex] = useState(0)
  const fakeProgressRef = useRef(0)
  
  // Frases estilo Carolina Martins 
  const frasesScraping = [
    "💼 Vasculhando o LinkedIn sem ativar o #OpenToWork. Não sou amadora.",
    "🚫 Ignorando panfletagem de currículo. 200 CVs por semana é desespero, não estratégia.",
    "✍️ Achei uma vaga pedindo 'perfil hands on'. Anotando pro seu MPC.",
    "📸 Pulando empresas que pedem foto 3x4. É crime e é feio.",
    "🎯 Hunting nas melhores vagas. As tops nem são divulgadas, sabia?",
    "💥 LinkedIn travou. Deve ser o peso dos egos inflados por lá.",
    "🔑 Coletando 20 palavras-chave. Com menos que isso você tá brincando.",
    "👻 Separando vagas reais das fake. RH adora postar vaga fantasma.",
    "✅ Checando se você tem 70% dos requisitos. 100% nem Jesus tinha.",
    "💰 Descartando 'salário a combinar'. Combinar com quem, com o capeta?"
  ]
  
  const frasesIA = [
    "🧘 Aplicando a Lei do Desapego nas suas experiências. Tchau, estágio de 2003.",
    "🚀 Transformando seu currículo bom em METEÓRICO. É tipo Thanos: inevitável.",
    "🦅 Matando o Zeca Urubu do seu resumo. Síndrome do impostor detected.",
    "📊 Procurando resultados tangíveis. 'Diminuí 2% do turnover' > 'sou esforçado'.",
    "💪 Verificando se você é executor ou espectador. Só executor consegue emprego.",
    "⚡ Processando... Mais rápido que você levou pra sair da cama hoje.",
    "🔄 Analisando suas experiências híbridas. Gestão é gestão, meu filho.",
    "👥 Contando suas recomendações no LinkedIn. Menos de 5? Amador.",
    "✨ Aplicando técnica meteórica. Seu currículo nunca mais será medíocre.",
    "🎯 Finalizando análise. Preparado pra parar de ser café com leite no mercado?"
  ]

  // Resetar progresso fake quando ativa
  useEffect(() => {
    if (isActive) {
      setFakeProgress(0)
      fakeProgressRef.current = 0
      setJokeIndex(0)
    }
  }, [isActive])

  // Efeito para progresso falso e frases
  useEffect(() => {
    if (!isActive) return
    
    // Atualiza progresso fake suavemente (2% por segundo = 1% a cada 500ms)
    const progressInterval = setInterval(() => {
      setFakeProgress(prev => {
        // Não ultrapassa o progresso real
        if (prev >= progress - 5) return prev
        // Incremento constante de 1% a cada 500ms = 2% por segundo
        const newProgress = Math.min(prev + 1, 95)
        fakeProgressRef.current = newProgress
        return newProgress
      })
    }, 500)
    
    // Troca as frases a cada 3 segundos
    const jokeInterval = setInterval(() => {
      setJokeIndex(prev => {
        const frases = status === 'processando_ia' ? frasesIA : frasesScraping
        return (prev + 1) % frases.length
      })
    }, 3000)
    
    return () => {
      clearInterval(progressInterval)
      clearInterval(jokeInterval)
    }
  }, [isActive, progress, status, frasesIA, frasesScraping])

  useEffect(() => {
    if (!isActive || !requestData) return

    // Não podemos usar EventSource com POST, então vamos usar fetch com ReadableStream
    const fetchStream = async () => {
      try {
        const response = await fetch(`${config.baseURL}${config.endpoints.agent1.collectKeywordsStream}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestData)
        })

        if (!response.ok) {
          throw new Error('Erro ao iniciar stream')
        }

        const reader = response.body.getReader()
        const decoder = new TextDecoder()

        while (true) {
          const { done, value } = await reader.read()
          
          if (done) break
          
          const chunk = decoder.decode(value)
          const lines = chunk.split('\n')
          
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.slice(6))
                
                setProgress(data.progress)
                setMessage(data.message)
                setStatus(data.status)
                
                // Se o progresso real pulou muito, ajusta o fake para acompanhar
                if (data.progress > 10 && fakeProgressRef.current < data.progress - 20) {
                  const newFakeProgress = data.progress - 10
                  setFakeProgress(newFakeProgress)
                  fakeProgressRef.current = newFakeProgress
                }

                if (data.status === 'concluido' && data.result_id) {
                  onComplete(data.result_id)
                  return
                } else if (data.status === 'erro') {
                  onError(data.message)
                  return
                }
              } catch (e) {
                console.error('Erro ao processar chunk:', e)
              }
            }
          }
        }
      } catch (error) {
        console.error('Erro no streaming:', error)
        onError('Erro de conexão com o servidor')
      }
    }

    fetchStream()

  }, [isActive, requestData, onComplete, onError])

  if (!isActive) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-2xl p-8 max-w-md w-full">
        <div className="text-center mb-6">
          {status === 'erro' ? (
            <ExclamationTriangleIcon className="w-16 h-16 text-red-500 mx-auto mb-4" />
          ) : status === 'concluido' ? (
            <CheckCircleIcon className="w-16 h-16 text-green-500 mx-auto mb-4" />
          ) : (
            <ArrowPathIcon className="w-16 h-16 text-blue-500 mx-auto mb-4 animate-spin" />
          )}
          
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            {status === 'erro' ? 'Erro na Análise' : 
             status === 'concluido' ? 'Análise Concluída!' : 
             'Analisando Vagas...'}
          </h3>
          
          <p className="text-gray-600 text-sm">
            {message}
          </p>
        </div>

        {/* Barra de progresso */}
        <div className="w-full bg-gray-200 rounded-full h-3 mb-4">
          <div 
            className={`h-3 rounded-full transition-all duration-500 ${
              status === 'erro' ? 'bg-red-500' :
              status === 'concluido' ? 'bg-green-500' :
              'bg-blue-500'
            }`}
            style={{ width: `${status === 'concluido' ? 100 : Math.max(fakeProgress, progress, 0)}%` }}
          />
        </div>

        <div className="text-center text-sm text-gray-500">
          {progress > 0 && progress < 100 && `${Math.round(Math.max(fakeProgress, progress))}% completo`}
        </div>
        
        {/* Frase cômica atual */}
        {(status === 'coletando' || status === 'processando_ia') && (
          <div className="mt-3 p-3 bg-gray-50 rounded-lg text-center">
            <p className="text-sm text-gray-700 font-medium animate-pulse">
              {status === 'processando_ia' ? frasesIA[jokeIndex] : frasesScraping[jokeIndex]}
            </p>
          </div>
        )}

        {/* Info adicional */}
        {status === 'coletando' && (
          <div className="mt-4 p-3 bg-blue-50 rounded-lg text-center">
            <p className="text-xs text-blue-600">
              ⏱️ Tempo estimado: 1-2 minutos | 🎯 Metodologia Carolina Martins
            </p>
          </div>
        )}

        {status === 'processando_ia' && (
          <div className="mt-4 p-3 bg-purple-50 rounded-lg text-center">
            <p className="text-xs text-purple-600">
              🤖 Gemini 2.5 Pro analisando | ✨ Gerando insights exclusivos
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

export default ProgressStream