import React, { useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import config from '../config'
import {
  CloudArrowUpIcon,
  DocumentTextIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  ChartBarIcon,
  UserCircleIcon,
  SparklesIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline'

// Header Component
const Header = () => {
  const navigate = useNavigate()
  
  return (
    <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => navigate('/')}
              className="flex items-center text-gray-600 hover:text-gray-900 transition-colors"
            >
              <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              <span className="text-sm font-medium">Voltar</span>
            </button>
            
            <div className="flex items-center space-x-3">
              <div className="flex items-center justify-center w-8 h-8 bg-blue-600 rounded-lg">
                <UserCircleIcon className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">
                  Agente 0 - Diagnóstico
                </h1>
                <p className="text-sm text-gray-600">
                  Análise completa do seu perfil profissional
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

// Upload Component
const FileUpload = ({ onFileSelect, selectedFile, isProcessing }) => {
  const [dragOver, setDragOver] = useState(false)

  const handleDragOver = useCallback((e) => {
    e.preventDefault()
    setDragOver(true)
  }, [])

  const handleDragLeave = useCallback((e) => {
    e.preventDefault()
    setDragOver(false)
  }, [])

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    setDragOver(false)
    
    const files = e.dataTransfer.files
    if (files.length > 0) {
      const file = files[0]
      if (file.type === 'application/pdf' || file.name.endsWith('.docx') || file.name.endsWith('.doc')) {
        onFileSelect(file)
      }
    }
  }, [onFileSelect])

  const handleFileInput = (e) => {
    const file = e.target.files[0]
    if (file) {
      onFileSelect(file)
    }
  }

  return (
    <div className="w-full">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Upload do Currículo
      </label>
      
      <div
        className={`
          relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200
          ${dragOver ? 'border-blue-400 bg-blue-50' : 'border-gray-300 hover:border-gray-400'}
          ${isProcessing ? 'opacity-50 pointer-events-none' : 'cursor-pointer'}
        `}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input
          type="file"
          accept=".pdf,.docx,.doc"
          onChange={handleFileInput}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          disabled={isProcessing}
        />
        
        <div className="space-y-4">
          {selectedFile ? (
            <div className="flex items-center justify-center space-x-3">
              <DocumentTextIcon className="w-8 h-8 text-green-600" />
              <div className="text-left">
                <p className="text-sm font-medium text-gray-900">{selectedFile.name}</p>
                <p className="text-xs text-gray-500">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
              <CheckCircleIcon className="w-6 h-6 text-green-600" />
            </div>
          ) : (
            <>
              <CloudArrowUpIcon className="mx-auto w-12 h-12 text-gray-400" />
              <div>
                <p className="text-lg font-medium text-gray-900">
                  Arraste seu currículo aqui
                </p>
                <p className="text-sm text-gray-600">
                  ou clique para selecionar
                </p>
              </div>
            </>
          )}
          
          <div className="text-xs text-gray-500">
            Formatos suportados: PDF, DOCX, DOC (máx. 10MB)
          </div>
        </div>
      </div>
    </div>
  )
}

// Text Input Alternative
const TextInput = ({ value, onChange, disabled }) => {
  return (
    <div className="w-full">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Ou cole o texto do seu currículo
      </label>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        placeholder="Cole aqui o conteúdo completo do seu currículo..."
        className="w-full h-48 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none disabled:bg-gray-50"
      />
      <p className="mt-1 text-xs text-gray-500">
        Mínimo 500 caracteres para uma análise adequada
      </p>
    </div>
  )
}

// Progress Indicator
const ProgressIndicator = ({ currentStep, steps }) => {
  return (
    <div className="w-full bg-gray-200 rounded-full h-2 mb-6">
      <div 
        className="bg-blue-600 h-2 rounded-full transition-all duration-500 ease-out"
        style={{ width: `${(currentStep / steps) * 100}%` }}
      />
    </div>
  )
}

// Results Display
const ResultsDisplay = ({ results }) => {
  if (!results) return null

  const { estrutura, honestidade, palavrasChave, score, motivacaoUsuario, sabotadoresIdentificados } = results

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600 bg-green-50 border-green-200'
    if (score >= 60) return 'text-yellow-600 bg-yellow-50 border-yellow-200'
    return 'text-red-600 bg-red-50 border-red-200'
  }

  const getScoreLabel = (score) => {
    if (score >= 80) return 'Excelente'
    if (score >= 60) return 'Bom'
    return 'Necessita melhorias'
  }

  return (
    <div className="space-y-6">
      {/* Dados de Motivação */}
      {motivacaoUsuario && (
        <div className="bg-blue-50 rounded-xl border border-blue-200 p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-4 flex items-center">
            <UserCircleIcon className="w-5 h-5 mr-2" />
            Contexto da Análise
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <span className="font-medium text-blue-900">Cargo Objetivo:</span>
              <p className="text-blue-800 mt-1">{motivacaoUsuario.cargoObjetivo}</p>
            </div>
            <div>
              <span className="font-medium text-blue-900">Empresa Ideal:</span>
              <p className="text-blue-800 mt-1">{motivacaoUsuario.empresaSonho}</p>
            </div>
          </div>
        </div>
      )}

      {/* Score Principal */}
      <div className={`rounded-xl border-2 p-6 ${getScoreColor(score)}`}>
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold">Score de Qualidade</h3>
            <p className="text-sm opacity-80">Baseado na metodologia Carolina Martins</p>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold">{score}%</div>
            <div className="text-sm font-medium">{getScoreLabel(score)}</div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Análise Estrutural */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <ChartBarIcon className="w-5 h-5 mr-2 text-blue-600" />
            Análise Estrutural
          </h3>
          
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Elementos presentes:</span>
              <span className="font-medium">{estrutura.presentes}/{estrutura.total}</span>
            </div>
            
            <div className="space-y-2">
              {estrutura.elementos.map((elemento, index) => (
                <div key={index} className="flex items-center space-x-2">
                  {elemento.presente ? (
                    <CheckCircleIcon className="w-4 h-4 text-green-500" />
                  ) : (
                    <ExclamationTriangleIcon className="w-4 h-4 text-red-500" />
                  )}
                  <span className="text-sm text-gray-700">
                    {elemento.nome}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Validação de Honestidade */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <SparklesIcon className="w-5 h-5 mr-2 text-purple-600" />
            Validação de Honestidade
          </h3>
          
          <div className="space-y-3">
            {honestidade.validacoes.map((validacao, index) => (
              <div key={index} className="flex items-center space-x-2">
                {validacao.status ? (
                  <CheckCircleIcon className="w-4 h-4 text-green-500" />
                ) : (
                  <ExclamationTriangleIcon className="w-4 h-4 text-red-500" />
                )}
                <span className="text-sm text-gray-700">
                  {validacao.nome}
                </span>
              </div>
            ))}
            
            {honestidade.alertas.length > 0 && (
              <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                <h4 className="text-sm font-medium text-yellow-800 mb-1">Alertas:</h4>
                {honestidade.alertas.map((alerta, index) => (
                  <p key={index} className="text-sm text-yellow-700">• {alerta}</p>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Sabotadores Identificados */}
      {sabotadoresIdentificados && sabotadoresIdentificados.length > 0 && (
        <div className="bg-orange-50 rounded-xl border border-orange-200 p-6">
          <h3 className="text-lg font-semibold text-orange-900 mb-4 flex items-center">
            <ExclamationTriangleIcon className="w-5 h-5 mr-2" />
            Sabotadores Identificados
          </h3>
          
          <div className="space-y-3">
            {sabotadoresIdentificados.map((sabotador, index) => {
              const nomeFormatado = sabotador.nome
                .replace(/_/g, ' ')
                .replace(/\b\w/g, l => l.toUpperCase())
              
              return (
                <div key={index} className="flex items-center justify-between p-3 bg-white rounded-lg border border-orange-200">
                  <div>
                    <h4 className="font-medium text-orange-900">{nomeFormatado}</h4>
                    <p className="text-sm text-orange-700">
                      Nível: {sabotador.nivel} (Média: {sabotador.media.toFixed(1)}/5)
                    </p>
                  </div>
                  <div className={`px-3 py-1 rounded-full text-xs font-medium ${
                    sabotador.nivel === 'alto' ? 'bg-red-100 text-red-800' :
                    sabotador.nivel === 'médio' ? 'bg-orange-100 text-orange-800' :
                    'bg-yellow-100 text-yellow-800'
                  }`}>
                    {sabotador.nivel.toUpperCase()}
                  </div>
                </div>
              )
            })}
          </div>
          
          <div className="mt-4 p-3 bg-orange-100 rounded-lg">
            <p className="text-sm text-orange-800">
              <strong>Recomendação:</strong> Trabalhe esses padrões mentais limitantes para aumentar suas chances de sucesso na transição de carreira.
            </p>
          </div>
        </div>
      )}

      {/* Palavras-chave */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Palavras-chave Identificadas
        </h3>
        
        <div className="flex flex-wrap gap-2">
          {palavrasChave.map((palavra, index) => (
            <span
              key={index}
              className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800"
            >
              {palavra}
            </span>
          ))}
        </div>
        
        {palavrasChave.length === 0 && (
          <p className="text-gray-500 text-sm">
            Nenhuma palavra-chave identificada automaticamente.
          </p>
        )}
      </div>

      {/* Caminho para 100% - Metodologia Carolina Martins */}
      {results?.caminho_para_100 && (
        <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl border border-purple-200 p-6">
          <h3 className="text-lg font-bold text-purple-900 mb-4 flex items-center">
            <SparklesIcon className="w-5 h-5 mr-2" />
            Caminho para Score 100% - Metodologia Carolina Martins
          </h3>
          
          {/* Por que este score? */}
          <div className="mb-4">
            <h4 className="font-semibold text-purple-800 mb-2">Por que você recebeu {score}%?</h4>
            <div className="bg-white/70 rounded-lg p-3 space-y-1">
              {results.caminho_para_100.penalizacoes_detalhadas?.map((penalizacao, idx) => (
                <p key={idx} className="text-sm text-red-700">• {penalizacao}</p>
              ))}
              <p className="text-sm font-semibold text-purple-900 mt-2">
                Total de penalizações: -{results.caminho_para_100.total_penalizacoes || 0} pontos
              </p>
            </div>
          </div>
          
          {/* O que falta para 100%? */}
          <div className="mb-4">
            <h4 className="font-semibold text-purple-800 mb-2">O que falta para alcançar 100%?</h4>
            <div className="bg-white/70 rounded-lg p-3 space-y-1">
              {results.caminho_para_100.o_que_falta_para_100?.map((item, idx) => (
                <p key={idx} className="text-sm text-green-700">✓ {item}</p>
              ))}
            </div>
          </div>
          
          {/* Conceitos da Metodologia */}
          <div>
            <h4 className="font-semibold text-purple-800 mb-2">Conceitos-chave da Metodologia:</h4>
            <div className="bg-white/70 rounded-lg p-3 space-y-1">
              {results.caminho_para_100.metodologia_carolina_martins?.map((conceito, idx) => (
                <p key={idx} className="text-sm text-purple-700">📌 {conceito}</p>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Recomendações */}
      <div className="bg-blue-50 rounded-xl border border-blue-200 p-6">
        <h3 className="text-lg font-semibold text-blue-900 mb-3">
          Próximos Passos Recomendados
        </h3>
        <div className="space-y-2">
          <p className="text-sm text-blue-800">• Execute o Agente 1 para mapear palavras-chave do mercado</p>
          <p className="text-sm text-blue-800">• Identifique gaps entre seu perfil atual e as demandas do mercado</p>
          <p className="text-sm text-blue-800">• Prepare-se para otimização do currículo com base nos resultados</p>
        </div>
      </div>
    </div>
  )
}

// Sabotadores Questionnaire Component
const SabotadoresQuestionnaire = ({ onComplete }) => {
  const [responses, setResponses] = useState({})
  const [currentPage, setCurrentPage] = useState(0)
  const questionsPerPage = 10

  // Definição das perguntas dos sabotadores
  const questions = [
    // Hiper-racional
    { id: 'q1', text: 'Tendo dificuldade para tomar decisões porque sempre quero analisar mais dados?', sabotador: 'hiper_racional' },
    { id: 'q2', text: 'Costumo adiar ações importantes porque quero ter certeza absoluta?', sabotador: 'hiper_racional' },
    { id: 'q3', text: 'Prefiro analisar a situação do que partir para a ação?', sabotador: 'hiper_racional' },
    // Hiper-realizador
    { id: 'q4', text: 'Sinto que meu trabalho nunca está bom o suficiente?', sabotador: 'hiper_realizador' },
    { id: 'q5', text: 'Prefiro fazer tudo sozinho para garantir que seja feito corretamente?', sabotador: 'hiper_realizador' },
    { id: 'q6', text: 'Fico estressado quando não posso controlar todos os detalhes?', sabotador: 'hiper_realizador' },
    // Controlador
    { id: 'q7', text: 'Tenho dificuldade em delegar tarefas importantes?', sabotador: 'controlador' },
    { id: 'q8', text: 'Fico ansioso quando não sei como uma situação vai se desenrolar?', sabotador: 'controlador' },
    { id: 'q9', text: 'Prefiro liderar a ser liderado?', sabotador: 'controlador' },
    // Hipervigilante
    { id: 'q10', text: 'Costumo pensar primeiro nos riscos e problemas de uma situação?', sabotador: 'hipervigilante' },
    { id: 'q11', text: 'Tenho dificuldade em confiar totalmente nas pessoas?', sabotador: 'hipervigilante' },
    { id: 'q12', text: 'Estou sempre alerta para possíveis ameaças ou problemas?', sabotador: 'hipervigilante' },
    // Inquieto
    { id: 'q13', text: 'Tenho dificuldade em manter foco em uma tarefa por muito tempo?', sabotador: 'inquieto' },
    { id: 'q14', text: 'Gosto de ter várias atividades acontecendo ao mesmo tempo?', sabotador: 'inquieto' },
    { id: 'q15', text: 'Fico entediado facilmente com rotinas?', sabotador: 'inquieto' },
    // Complacente
    { id: 'q16', text: 'Evito conflitos mesmo quando sei que estou certo?', sabotador: 'complacente' },
    { id: 'q17', text: 'Prefiro manter a paz do que expressar minha opinião?', sabotador: 'complacente' },
    { id: 'q18', text: 'Tenho dificuldade em dizer "não" para pedidos dos outros?', sabotador: 'complacente' },
    // Juiz
    { id: 'q19', text: 'Sou muito crítico comigo mesmo quando cometo erros?', sabotador: 'juiz' },
    { id: 'q20', text: 'Noto facilmente os defeitos e falhas nas pessoas?', sabotador: 'juiz' },
    { id: 'q21', text: 'Tenho padrões muito altos para mim e para os outros?', sabotador: 'juiz' },
    // Vítima
    { id: 'q22', text: 'Sinto que as coisas ruins sempre acontecem comigo?', sabotador: 'vitima' },
    { id: 'q23', text: 'Acredito que fatores externos são responsáveis pelos meus problemas?', sabotador: 'vitima' },
    { id: 'q24', text: 'Sinto que não tenho controle sobre os resultados da minha vida?', sabotador: 'vitima' },
    // Agradador
    { id: 'q25', text: 'Preciso que todos gostem de mim?', sabotador: 'agradador' },
    { id: 'q26', text: 'Mudo meu comportamento dependendo de com quem estou?', sabotador: 'agradador' },
    { id: 'q27', text: 'Fico muito incomodado quando alguém não gosta de mim?', sabotador: 'agradador' },
    // Evitador
    { id: 'q28', text: 'Deixo para depois tarefas que considero difíceis ou desagradáveis?', sabotador: 'evitador' },
    { id: 'q29', text: 'Evito situações onde posso ser rejeitado ou criticado?', sabotador: 'evitador' },
    { id: 'q30', text: 'Prefiro ficar na zona de conforto a arriscar coisas novas?', sabotador: 'evitador' }
  ]

  const scaleOptions = [
    { value: 1, label: 'Nunca' },
    { value: 2, label: 'Raramente' },
    { value: 3, label: 'Às vezes' },
    { value: 4, label: 'Frequentemente' },
    { value: 5, label: 'Sempre' }
  ]

  const handleResponseChange = (questionId, value) => {
    setResponses(prev => ({ ...prev, [questionId]: value }))
  }

  const getCurrentPageQuestions = () => {
    const start = currentPage * questionsPerPage
    const end = start + questionsPerPage
    return questions.slice(start, end)
  }

  const totalPages = Math.ceil(questions.length / questionsPerPage)
  const isLastPage = currentPage === totalPages - 1
  const isFirstPage = currentPage === 0
  const allAnswered = Object.keys(responses).length === questions.length

  const handleNext = () => {
    if (isLastPage && allAnswered) {
      // Calcular sabotadores identificados
      const sabotadoresScores = {}
      questions.forEach(q => {
        const score = responses[q.id] || 0
        if (!sabotadoresScores[q.sabotador]) {
          sabotadoresScores[q.sabotador] = { total: 0, count: 0 }
        }
        sabotadoresScores[q.sabotador].total += score
        sabotadoresScores[q.sabotador].count += 1
      })

      // Calcular médias e identificar sabotadores principais (média >= 3.5)
      const sabotadoresIdentificados = Object.entries(sabotadoresScores)
        .map(([sabotador, data]) => ({
          nome: sabotador,
          media: data.total / data.count,
          nivel: data.total / data.count >= 4 ? 'alto' : data.total / data.count >= 3 ? 'médio' : 'baixo'
        }))
        .filter(s => s.media >= 3.5)
        .sort((a, b) => b.media - a.media)

      onComplete({ responses, sabotadoresIdentificados })
    } else if (!isLastPage) {
      setCurrentPage(prev => prev + 1)
    }
  }

  const handlePrevious = () => {
    if (!isFirstPage) {
      setCurrentPage(prev => prev - 1)
    }
  }

  const progressPercentage = (Object.keys(responses).length / questions.length) * 100

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6">
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-2 flex items-center">
          <ExclamationTriangleIcon className="w-5 h-5 mr-2 text-orange-600" />
          Questionário de Sabotadores
        </h3>
        <p className="text-sm text-gray-600">
          Identifique os padrões mentais que podem estar limitando seu crescimento profissional.
        </p>
        
        {/* Progress Bar */}
        <div className="mt-4">
          <div className="flex justify-between text-xs text-gray-600 mb-1">
            <span>Progresso: {Object.keys(responses).length}/{questions.length} perguntas</span>
            <span>{Math.round(progressPercentage)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-orange-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progressPercentage}%` }}
            />
          </div>
          {/* Debug - remover depois */}
          {isLastPage && Object.keys(responses).length < questions.length && (
            <div className="mt-2 text-xs text-red-600">
              Perguntas não respondidas: {questions.filter(q => !responses[q.id]).map(q => q.id).join(', ')}
            </div>
          )}
        </div>
      </div>

      {/* Questions */}
      <div className="space-y-6">
        {getCurrentPageQuestions().map((question, index) => {
          const globalIndex = currentPage * questionsPerPage + index
          return (
            <div key={question.id} className="border-b border-gray-100 pb-6 last:border-0">
              <p className="text-sm font-medium text-gray-900 mb-3">
                {globalIndex + 1}. {question.text}
              </p>
              <div className="flex justify-between items-center space-x-2">
                {scaleOptions.map(option => (
                  <button
                    key={option.value}
                    onClick={() => handleResponseChange(question.id, option.value)}
                    className={`
                      flex-1 px-3 py-2 rounded-lg text-xs font-medium transition-all
                      ${responses[question.id] === option.value
                        ? 'bg-orange-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }
                    `}
                  >
                    {option.label}
                  </button>
                ))}
              </div>
            </div>
          )
        })}
      </div>

      {/* Navigation */}
      <div className="flex justify-between items-center mt-8">
        <button
          onClick={handlePrevious}
          disabled={isFirstPage}
          className={`
            flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-all
            ${!isFirstPage
              ? 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              : 'bg-gray-50 text-gray-400 cursor-not-allowed'
            }
          `}
        >
          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Anterior
        </button>

        <span className="text-sm text-gray-600">
          Página {currentPage + 1} de {totalPages}
        </span>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => onComplete({ responses: {}, sabotadoresIdentificados: [] })}
            className="px-4 py-2 rounded-lg text-sm font-medium text-gray-600 hover:text-gray-800 hover:bg-gray-100 transition-all"
          >
            Pular questionário completo
          </button>
          <button
            onClick={handleNext}
            disabled={isLastPage && !allAnswered}
            className={`
              flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-all
              ${(!isLastPage || (isLastPage && allAnswered))
                ? 'bg-orange-600 text-white hover:bg-orange-700'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              }
            `}
          >
            {isLastPage ? 'Concluir' : 'Próxima'}
            <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  )
}

// Motivation Questionnaire Component
const MotivationQuestionnaire = ({ onComplete }) => {
  const [formData, setFormData] = useState({
    cargoObjetivo: '',
    empresaSonho: '',
    motivoMudanca: '',
    estiloTrabalho: '',
    valoresImportantes: '',
    maioresDesafios: '',
    ondeMeVejo5Anos: ''
  })

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const isFormValid = Object.values(formData).every(value => value.trim().length >= 10)

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
        <UserCircleIcon className="w-5 h-5 mr-2 text-blue-600" />
        Questionário de Objetivos e Motivação
      </h3>
      <p className="text-sm text-gray-600 mb-6">
        Para uma análise mais precisa e personalizada, precisamos entender suas motivações e objetivos profissionais.
      </p>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Qual cargo você deseja conquistar?
          </label>
          <input
            type="text"
            value={formData.cargoObjetivo}
            onChange={(e) => handleChange('cargoObjetivo', e.target.value)}
            placeholder="Ex: Gerente de Marketing Digital"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Qual é sua empresa dos sonhos ou tipo de empresa ideal?
          </label>
          <input
            type="text"
            value={formData.empresaSonho}
            onChange={(e) => handleChange('empresaSonho', e.target.value)}
            placeholder="Ex: Startups de tecnologia com cultura inovadora"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Por que você quer mudar de emprego ou área?
          </label>
          <textarea
            value={formData.motivoMudanca}
            onChange={(e) => handleChange('motivoMudanca', e.target.value)}
            placeholder="Descreva suas principais motivações para essa mudança..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none h-20"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Qual seu estilo de trabalho preferido?
          </label>
          <textarea
            value={formData.estiloTrabalho}
            onChange={(e) => handleChange('estiloTrabalho', e.target.value)}
            placeholder="Ex: Remoto, colaborativo, autônomo, estruturado..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none h-20"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Quais valores são mais importantes para você no trabalho?
          </label>
          <textarea
            value={formData.valoresImportantes}
            onChange={(e) => handleChange('valoresImportantes', e.target.value)}
            placeholder="Ex: Crescimento, equilíbrio vida-trabalho, impacto social..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none h-20"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Quais são seus maiores desafios hoje?
          </label>
          <textarea
            value={formData.maioresDesafios}
            onChange={(e) => handleChange('maioresDesafios', e.target.value)}
            placeholder="Descreva os obstáculos que você enfrenta atualmente..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none h-20"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Onde você se vê profissionalmente em 5 anos?
          </label>
          <textarea
            value={formData.ondeMeVejo5Anos}
            onChange={(e) => handleChange('ondeMeVejo5Anos', e.target.value)}
            placeholder="Descreva sua visão de futuro profissional..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none h-20"
          />
        </div>
      </div>

      <div className="mt-6 flex justify-end">
        <button
          onClick={() => onComplete(formData)}
          disabled={!isFormValid}
          className={`
            inline-flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200
            ${isFormValid
              ? 'bg-blue-600 hover:bg-blue-700 text-white'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }
          `}
        >
          Continuar para Questionário de Sabotadores
        </button>
      </div>
      
      {!isFormValid && (
        <p className="mt-2 text-xs text-gray-500 text-right">
          Preencha todos os campos com pelo menos 10 caracteres
        </p>
      )}
    </div>
  )
}

// Main Component
const Agent0 = () => {
  const [selectedFile, setSelectedFile] = useState(null)
  const [textContent, setTextContent] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  const [currentStep, setCurrentStep] = useState(0)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const [motivationData, setMotivationData] = useState(null)
  const [sabotadoresData, setSabotadoresData] = useState(null)
  const [currentQuestionnaire, setCurrentQuestionnaire] = useState('motivation') // 'motivation', 'sabotadores', 'cv'

  const handleFileSelect = (file) => {
    setSelectedFile(file)
    setTextContent('')
    setError(null)
  }

  const handleMotivationComplete = (data) => {
    setMotivationData(data)
    setCurrentQuestionnaire('sabotadores')
  }

  const handleSabotadoresComplete = (data) => {
    setSabotadoresData(data)
    setCurrentQuestionnaire('cv')
  }

  const handleAnalyze = async () => {
    if (!selectedFile && !textContent.trim()) {
      setError('Por favor, faça upload de um arquivo ou cole o texto do currículo.')
      return
    }

    if (textContent.trim() && textContent.trim().length < 500) {
      setError('O texto deve ter pelo menos 500 caracteres para uma análise adequada.')
      return
    }

    if (!motivationData || !sabotadoresData) {
      setError('Por favor, complete todos os questionários primeiro.')
      return
    }

    setIsProcessing(true)
    setError(null)
    setCurrentStep(1)

    try {
      // Preparar dados para envio
      const formData = new FormData()
      
      if (selectedFile) {
        formData.append('file', selectedFile)
        // Adicionar dados de motivação ao FormData
        formData.append('motivationData', JSON.stringify(motivationData))
        formData.append('sabotadoresData', JSON.stringify(sabotadoresData))
        setCurrentStep(2) // Processando arquivo
      } else {
        // Para texto, usar JSON
        const requestData = {
          text: textContent.trim(),
          motivationData: motivationData,
          sabotadoresData: sabotadoresData
        }
        
        setCurrentStep(2) // Processando texto
        
        // Chamar API real do backend
        const response = await fetch(config.endpoints.agent0.analyzeCV, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestData)
        })
        
        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.error || 'Erro na análise')
        }
        
        setCurrentStep(3) // Analisando estrutura
        
        const results = await response.json()
        
        setCurrentStep(4) // Finalizando
        
        setResults(results)
        setCurrentStep(5)
        return
      }
      
      // Para arquivo, usar FormData
      setCurrentStep(2)
      
      const response = await fetch(config.endpoints.agent0.analyzeCV, {
        method: 'POST',
        body: formData
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Erro na análise')
      }
      
      setCurrentStep(3) // Analisando estrutura
      
      const results = await response.json()
      
      setCurrentStep(4) // Finalizando
      
      setResults(results)
      setCurrentStep(5)
      
    } catch (err) {
      console.error('Erro na análise:', err)
      setError(err.message || 'Erro ao processar o currículo. Verifique se o backend está rodando.')
    } finally {
      setIsProcessing(false)
    }
  }

  const canAnalyze = (selectedFile || textContent.trim().length >= 500) && !isProcessing

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Diagnóstico Completo do Perfil Profissional
          </h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Análise detalhada do seu currículo seguindo a metodologia dos 13 passos da Carolina Martins, 
            identificação de sabotadores e mapeamento de gaps profissionais.
          </p>
        </div>

        {/* Progress */}
        {isProcessing && (
          <div className="mb-6">
            <ProgressIndicator currentStep={currentStep} steps={5} />
            <div className="text-center text-sm text-gray-600">
              {currentStep === 1 && 'Extraindo texto do documento...'}
              {currentStep === 2 && 'Analisando estrutura metodológica...'}
              {currentStep === 3 && 'Verificando validações de honestidade...'}
              {currentStep === 4 && 'Extraindo palavras-chave...'}
              {currentStep === 5 && 'Finalizando análise...'}
            </div>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center">
              <ExclamationTriangleIcon className="w-5 h-5 text-red-600 mr-2" />
              <span className="text-red-800">{error}</span>
            </div>
          </div>
        )}

        {!results ? (
          /* Input Section */
          <div className="space-y-6">
            {/* Motivation Questionnaire */}
            {currentQuestionnaire === 'motivation' && (
              <MotivationQuestionnaire onComplete={handleMotivationComplete} />
            )}
            
            {/* Sabotadores Questionnaire */}
            {currentQuestionnaire === 'sabotadores' && (
              <SabotadoresQuestionnaire onComplete={handleSabotadoresComplete} />
            )}
            
            {/* CV Upload Section - Only show after questionnaires */}
            {currentQuestionnaire === 'cv' && (
              <>
                {/* Summary of completed questionnaires */}
                <div className="space-y-3 mb-6">
                  <div className="bg-green-50 rounded-xl border border-green-200 p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="text-sm font-medium text-green-900 flex items-center">
                          <CheckCircleIcon className="w-4 h-4 mr-1" />
                          Questionário de Motivação Completo
                        </h4>
                        <p className="text-sm text-green-700 mt-1">Cargo objetivo: {motivationData.cargoObjetivo}</p>
                      </div>
                      <button
                        onClick={() => setCurrentQuestionnaire('motivation')}
                        className="text-sm text-green-600 hover:text-green-700 font-medium"
                      >
                        Editar
                      </button>
                    </div>
                  </div>
                  
                  <div className="bg-orange-50 rounded-xl border border-orange-200 p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="text-sm font-medium text-orange-900 flex items-center">
                          <CheckCircleIcon className="w-4 h-4 mr-1" />
                          Questionário de Sabotadores Completo
                        </h4>
                        <p className="text-sm text-orange-700 mt-1">
                          {sabotadoresData.sabotadoresIdentificados.length} sabotadores identificados
                        </p>
                      </div>
                      <button
                        onClick={() => setCurrentQuestionnaire('sabotadores')}
                        className="text-sm text-orange-600 hover:text-orange-700 font-medium"
                      >
                        Editar
                      </button>
                    </div>
                  </div>
                </div>
                
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                  <FileUpload
                    onFileSelect={handleFileSelect}
                    selectedFile={selectedFile}
                    isProcessing={isProcessing}
                  />
                </div>

                <div className="text-center">
                  <span className="text-gray-500">ou</span>
                </div>

                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                  <TextInput
                    value={textContent}
                    onChange={setTextContent}
                    disabled={isProcessing || !!selectedFile}
                  />
                </div>
              </>
            )}

            {currentQuestionnaire === 'cv' && (
              <div className="text-center">
                <button
                  onClick={handleAnalyze}
                  disabled={!canAnalyze}
                  className={`
                    inline-flex items-center px-6 py-3 rounded-lg text-sm font-medium transition-all duration-200
                    ${canAnalyze
                      ? 'bg-blue-600 hover:bg-blue-700 text-white shadow-sm hover:shadow-md transform hover:-translate-y-0.5'
                      : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    }
                  `}
                >
                  {isProcessing ? (
                    <>
                      <ArrowPathIcon className="w-4 h-4 mr-2 animate-spin" />
                      Analisando Currículo...
                    </>
                  ) : (
                    <>
                      <SparklesIcon className="w-4 h-4 mr-2" />
                      Analisar Currículo
                    </>
                  )}
                </button>
              </div>
            )}
          </div>
        ) : (
          /* Results Section */
          <div>
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-semibold text-gray-900">
                Resultados da Análise
              </h3>
              <button
                onClick={() => {
                  setResults(null)
                  setSelectedFile(null)
                  setTextContent('')
                  setCurrentStep(0)
                  setCurrentQuestionnaire('motivation')
                  setMotivationData(null)
                  setSabotadoresData(null)
                }}
                className="text-sm text-blue-600 hover:text-blue-700 font-medium"
              >
                Nova Análise
              </button>
            </div>
            <ResultsDisplay results={results} />
          </div>
        )}

        {/* Info Section */}
        <div className="mt-12 bg-blue-50 rounded-xl p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-3">
            O que será analisado?
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-blue-800">
            <div>
              <h4 className="font-medium mb-2">Estrutura Metodológica:</h4>
              <ul className="space-y-1">
                <li>• Presença dos 13 passos</li>
                <li>• Formatação profissional</li>
                <li>• Organização do conteúdo</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium mb-2">Validações de Honestidade:</h4>
              <ul className="space-y-1">
                <li>• Consistência de datas</li>
                <li>• Resultados quantificados</li>
                <li>• Detalhamento adequado</li>
              </ul>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default Agent0