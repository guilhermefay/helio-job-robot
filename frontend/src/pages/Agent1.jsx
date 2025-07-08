import React, { useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import config from '../config'
import {
  MagnifyingGlassIcon,
  MapPinIcon,
  BriefcaseIcon,
  BuildingOfficeIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  ChartBarIcon,
  TagIcon,
  SparklesIcon,
  ArrowPathIcon,
  ClockIcon,
  GlobeAltIcon
} from '@heroicons/react/24/outline'
import ProgressStream from '../components/ProgressStream'

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
              <div className="flex items-center justify-center w-8 h-8 bg-green-600 rounded-lg">
                <MagnifyingGlassIcon className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">
                  Agente 1 - Palavras-chave
                </h1>
                <p className="text-sm text-gray-600">
                  Mapeamento de palavras-chave do mercado
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

// Search Configuration Component
const SearchConfiguration = ({ config, onChange, disabled }) => {
  const handleChange = (field, value) => {
    onChange({
      ...config,
      [field]: value
    })
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Configuração da Busca
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Área de Interesse */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <BriefcaseIcon className="w-4 h-4 inline mr-1" />
            Área de Interesse
          </label>
          <input
            type="text"
            value={config.area}
            onChange={(e) => handleChange('area', e.target.value)}
            disabled={disabled}
            placeholder="Ex: Marketing Digital, Desenvolvimento, RH..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent disabled:bg-gray-50"
          />
        </div>

        {/* Cargo Objetivo */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <SparklesIcon className="w-4 h-4 inline mr-1" />
            Cargo Objetivo
          </label>
          <input
            type="text"
            value={config.cargo}
            onChange={(e) => handleChange('cargo', e.target.value)}
            disabled={disabled}
            placeholder="Ex: Analista, Coordenador, Gerente..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent disabled:bg-gray-50"
          />
        </div>

        {/* Localização */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <MapPinIcon className="w-4 h-4 inline mr-1" />
            Localização
          </label>
          <input
            type="text"
            value={config.localizacao}
            onChange={(e) => handleChange('localizacao', e.target.value)}
            disabled={disabled}
            placeholder="Ex: São Paulo, Rio de Janeiro, Remoto..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent disabled:bg-gray-50"
          />
        </div>

        {/* Número de Vagas */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <ChartBarIcon className="w-4 h-4 inline mr-1" />
            Quantidade de Vagas
          </label>
          <select
            value={config.quantidade}
            onChange={(e) => handleChange('quantidade', parseInt(e.target.value))}
            disabled={disabled}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent disabled:bg-gray-50"
          >
            <option value={20}>20 vagas (teste rápido)</option>
            <option value={50}>50 vagas</option>
            <option value={100}>100 vagas</option>
            <option value={150}>150 vagas</option>
            <option value={200}>200 vagas</option>
            <option value={300}>300 vagas</option>
            <option value={500}>500 vagas (5-7 min)</option>
            <option value={1000}>1000 vagas (8-10 min)</option>
          </select>
        </div>
      </div>

      {/* Segmentos */}
      <div className="mt-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          <BuildingOfficeIcon className="w-4 h-4 inline mr-1" />
          Segmentos de Interesse (opcional)
        </label>
        <textarea
          value={config.segmentos}
          onChange={(e) => handleChange('segmentos', e.target.value)}
          disabled={disabled}
          placeholder="Ex: Startups, Multinacionais, Consultoria, E-commerce..."
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none disabled:bg-gray-50"
          rows={3}
        />
      </div>
    </div>
  )
}

// Progress Component
const ProgressIndicator = ({ currentStep, steps, stepLabels }) => {
  return (
    <div className="w-full">
      <div className="flex justify-between text-sm text-gray-600 mb-2">
        <span>Etapa {currentStep} de {steps}</span>
        <span>{stepLabels[currentStep - 1]}</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div 
          className="bg-green-600 h-2 rounded-full transition-all duration-500 ease-out"
          style={{ width: `${(currentStep / steps) * 100}%` }}
        />
      </div>
    </div>
  )
}

// Collection Results Component
const CollectionResults = ({ collectionData, onAnalyze, isAnalyzing, config }) => {
  const [showVagas, setShowVagas] = useState(false)
  
  if (!collectionData) return null
  
  return (
    <div className="space-y-6">
      {/* Aviso de Modo Demo */}
      {collectionData.demo_mode && (
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
          <div className="flex items-start">
            <ExclamationTriangleIcon className="w-5 h-5 text-amber-600 mr-2 mt-0.5" />
            <div>
              <h4 className="text-sm font-medium text-amber-800">Modo Demonstração Ativo</h4>
              <p className="text-sm text-amber-700 mt-1">
                Estas são vagas de exemplo para demonstrar o funcionamento do sistema. 
                Para coletar vagas reais, configure a variável APIFY_API_TOKEN no arquivo .env
              </p>
            </div>
          </div>
        </div>
      )}
      
      {/* Estatísticas da Coleta */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <CheckCircleIcon className="w-5 h-5 mr-2 text-green-600" />
          Vagas Coletadas com Sucesso!
        </h3>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-gray-50 rounded-lg p-4 text-center">
            <p className="text-3xl font-bold text-gray-900">{collectionData.estatisticas.totalVagas}</p>
            <p className="text-sm text-gray-600">Vagas Coletadas</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4 text-center">
            <p className="text-3xl font-bold text-gray-900">{collectionData.estatisticas.fontes}</p>
            <p className="text-sm text-gray-600">Fontes Utilizadas</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4 text-center">
            <p className="text-3xl font-bold text-green-600">100%</p>
            <p className="text-sm text-gray-600">Taxa de Sucesso</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4 text-center">
            <p className="text-3xl font-bold text-gray-900">{collectionData.vagas.length}</p>
            <p className="text-sm text-gray-600">Com Descrição</p>
          </div>
        </div>
        
        {/* Fontes */}
        <div className="mb-6">
          <h4 className="text-sm font-medium text-gray-700 mb-2">Fontes Utilizadas:</h4>
          <div className="flex flex-wrap gap-2">
            {collectionData.fontes.map((fonte, index) => (
              <span key={index} className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                {fonte.nome} ({fonte.vagas} vagas)
              </span>
            ))}
          </div>
        </div>
        
        {/* Botão para mostrar vagas */}
        <button
          onClick={() => setShowVagas(!showVagas)}
          className="text-sm text-blue-600 hover:text-blue-700 font-medium flex items-center"
        >
          <GlobeAltIcon className="w-4 h-4 mr-1" />
          {showVagas ? 'Ocultar' : 'Ver'} Vagas Coletadas
        </button>
        
        {/* Lista de Vagas */}
        {showVagas && (
          <div className="mt-4 space-y-3 max-h-96 overflow-y-auto">
            {collectionData.vagas.map((vaga, index) => (
              <div key={index} className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                <div className="flex justify-between items-start mb-2">
                  <h5 className="font-medium text-gray-900">{vaga.titulo}</h5>
                  <span className="text-xs text-gray-500 bg-gray-200 px-2 py-1 rounded">
                    {vaga.fonte}
                  </span>
                </div>
                <p className="text-sm text-gray-600 mb-1">{vaga.empresa} • {vaga.localizacao}</p>
                {vaga.descricao && vaga.descricao !== 'Descrição não disponível' && (
                  <p className="text-xs text-gray-500 line-clamp-3">{vaga.descricao}</p>
                )}
                {vaga.url && (
                  <a href={vaga.url} target="_blank" rel="noopener noreferrer" 
                     className="text-xs text-blue-600 hover:text-blue-700 mt-2 inline-block">
                    Ver vaga completa →
                  </a>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
      
      {/* Botão para Análise */}
      <div className="text-center">
        <button
          onClick={onAnalyze}
          disabled={isAnalyzing}
          className={`
            inline-flex items-center px-8 py-3 rounded-lg text-sm font-medium transition-all duration-200
            ${!isAnalyzing
              ? 'bg-green-600 hover:bg-green-700 text-white shadow-sm hover:shadow-md transform hover:-translate-y-0.5'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }
          `}
        >
          {isAnalyzing ? (
            <>
              <ArrowPathIcon className="w-4 h-4 mr-2 animate-spin" />
              Analisando com IA...
            </>
          ) : (
            <>
              <SparklesIcon className="w-4 h-4 mr-2" />
              Analisar e Extrair Palavras-chave
            </>
          )}
        </button>
        
        {!isAnalyzing && (
          <p className="text-sm text-gray-600 mt-2">
            Clique para enviar as vagas para análise com Gemini e extrair as palavras-chave
          </p>
        )}
        
        {/* Loading da Análise */}
        {isAnalyzing && (
          <div className="mt-4 bg-purple-50 border border-purple-200 rounded-lg p-4">
            <div className="flex items-start">
              <SparklesIcon className="w-5 h-5 text-purple-600 mr-2 mt-0.5 animate-pulse" />
              <div className="flex-1">
                <h4 className="text-sm font-medium text-purple-800">Analisando com Gemini...</h4>
                <p className="text-xs text-purple-700 mt-1">
                  O Gemini está processando {collectionData.estatisticas.totalVagas} vagas para extrair as palavras-chave mais relevantes.
                </p>
                <div className="mt-2">
                  <div className="flex items-center text-xs text-purple-600">
                    <div className="animate-pulse mr-2">●</div>
                    <span>Processando descrições das vagas</span>
                  </div>
                  <div className="flex items-center text-xs text-purple-600 mt-1">
                    <div className="animate-pulse mr-2">●</div>
                    <span>Identificando termos técnicos e comportamentais</span>
                  </div>
                  <div className="flex items-center text-xs text-purple-600 mt-1">
                    <div className="animate-pulse mr-2">●</div>
                    <span>Aplicando metodologia Carolina Martins</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

// Transparency Section Component  
const TransparencySection = ({ transparencia }) => {
  const [activeTab, setActiveTab] = useState('logs')
  
  if (!transparencia) return null

  return (
    <div className="bg-gray-50 rounded-xl border border-gray-300 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
        <InformationCircleIcon className="w-5 h-5 mr-2 text-blue-600" />
        🔍 Transparência Total - Veja tudo que o agente fez
      </h3>
      
      {/* Tabs */}
      <div className="flex space-x-4 mb-4 border-b border-gray-200">
        {[
          { id: 'logs', label: 'Logs do Processo', count: transparencia?.logs_detalhados?.length },
          { id: 'vagas', label: 'Vagas Coletadas', count: transparencia?.vagas_coletadas?.length },
          { id: 'palavras', label: 'Palavras Extraídas', count: transparencia?.palavras_brutas?.length }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`pb-2 px-1 text-sm font-medium border-b-2 transition-colors ${
              activeTab === tab.id
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            {tab.label} ({tab.count || 0})
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="max-h-96 overflow-y-auto">
        {activeTab === 'logs' && (
          <div className="space-y-2">
            <h4 className="font-medium text-gray-900 mb-3">Processo passo a passo:</h4>
            {transparencia?.logs_detalhados?.map((log, index) => (
              <div key={index} className="text-sm bg-white p-3 rounded border-l-4 border-blue-500">
                <code className="text-gray-700">{log}</code>
              </div>
            ))}
          </div>
        )}
        
        {activeTab === 'vagas' && (
          <div className="space-y-3">
            <h4 className="font-medium text-gray-900 mb-3">Todas as vagas coletadas:</h4>
            {transparencia?.vagas_coletadas?.map((vaga, index) => (
              <div key={index} className={`p-4 rounded border ${
                vaga.is_demo ? 'bg-yellow-50 border-yellow-300' : 'bg-white'
              }`}>
                <div className="flex justify-between items-start mb-2">
                  <h5 className="font-medium text-gray-900">
                    {vaga.url ? (
                      <a 
                        href={vaga.url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="hover:text-blue-600 hover:underline"
                      >
                        {vaga.titulo}
                        <svg className="inline-block w-3 h-3 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                        </svg>
                      </a>
                    ) : (
                      vaga.titulo
                    )}
                    {vaga.is_demo && (
                      <span className="ml-2 text-xs bg-yellow-200 text-yellow-800 px-2 py-1 rounded">
                        🎭 DEMO
                      </span>
                    )}
                  </h5>
                  <span className={`text-xs px-2 py-1 rounded ${
                    vaga.fonte === 'demo_sistema' 
                      ? 'bg-yellow-100 text-yellow-800' 
                      : 'bg-blue-100 text-blue-800'
                  }`}>
                    {vaga.fonte}
                  </span>
                </div>
                <p className="text-sm text-gray-600 mb-1">{vaga.empresa}</p>
                <p className="text-xs text-gray-500 mb-2">{vaga.localizacao}</p>
                <p className="text-sm text-gray-700 mb-2">
                  {vaga.descricao?.substring(0, 300)}
                  {vaga.descricao?.length > 300 && '...'}
                </p>
                {vaga.url && (
                  <a 
                    href={vaga.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-xs text-blue-600 hover:text-blue-800 hover:underline"
                  >
                    Ver vaga completa →
                  </a>
                )}
              </div>
            ))}
          </div>
        )}
        
        {activeTab === 'palavras' && (
          <div className="space-y-2">
            <h4 className="font-medium text-gray-900 mb-3">Todas as palavras extraídas:</h4>
            <div className="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2">
              {transparencia?.palavras_brutas?.map((palavra, index) => (
                <span 
                  key={index} 
                  className="text-xs bg-white px-2 py-1 rounded border text-gray-700 text-center"
                >
                  {palavra}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

// Results Display Component
const ResultsDisplay = ({ results }) => {
  if (!results) return null

  // Log para debug
  console.log('Resultados recebidos:', results)

  const { 
    estatisticas = {}, 
    palavrasChave = {}, 
    validacaoIA = {}, 
    fontes = [], 
    transparencia = {}, 
    top_10_carolina_martins = [], 
    modelo_usado = '', 
    insights = {} 
  } = results
  
  // Garantir que arrays não sejam undefined
  const safeTop10 = top_10_carolina_martins || palavrasChave?.top10 || []
  const safeFontes = fontes || []

  return (
    <div className="space-y-6">
      {/* Demo Warning */}
      {transparencia?.vagas_coletadas?.some(vaga => vaga.is_demo) && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex items-center">
            <InformationCircleIcon className="w-5 h-5 text-yellow-600 mr-2" />
            <div>
              <h3 className="text-sm font-medium text-yellow-800">🎭 Modo Demonstração Ativo</h3>
              <p className="text-xs text-yellow-700 mt-1">
                Os dados exibidos são exemplos para demonstrar a funcionalidade. 
                Para coleta real, configure APIs de job boards (LinkedIn, Indeed, Google Jobs).
              </p>
            </div>
          </div>
        </div>
      )}

      {/* LinkedIn/Apify Info */}
      {!transparencia?.vagas_coletadas?.some(vaga => vaga.fonte?.toLowerCase().includes('linkedin')) && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-start">
            <InformationCircleIcon className="w-5 h-5 text-blue-600 mr-2 mt-0.5" />
            <div className="flex-1">
              <h3 className="text-sm font-medium text-blue-800">💡 Dica: Ative a coleta do LinkedIn com Apify</h3>
              <p className="text-xs text-blue-700 mt-1 mb-2">
                Para coletar vagas reais do LinkedIn, configure o Apify (mais barato e confiável que Selenium):
              </p>
              <ol className="text-xs text-blue-700 space-y-1 ml-4">
                <li>1. Crie uma conta gratuita em <a href="https://apify.com" target="_blank" rel="noopener noreferrer" className="underline">apify.com</a></li>
                <li>2. Copie seu API Token do dashboard</li>
                <li>3. Adicione ao arquivo .env: <code className="bg-blue-100 px-1 py-0.5 rounded">APIFY_API_TOKEN=seu_token</code></li>
                <li>4. Reinicie o servidor backend</li>
              </ol>
              <p className="text-xs text-blue-600 mt-2">
                ✨ Actor recomendado: <a href="https://apify.com/curious_coder/linkedin-jobs-scraper" target="_blank" rel="noopener noreferrer" className="underline font-medium">curious_coder/linkedin-jobs-scraper</a> (mais barato)
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Estatísticas */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <ChartBarIcon className="w-5 h-5 mr-2 text-green-600" />
          Estatísticas da Coleta
        </h3>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">{estatisticas.totalVagas || 0}</div>
            <div className="text-sm text-gray-600">Vagas Coletadas</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">{estatisticas.palavrasEncontradas || 0}</div>
            <div className="text-sm text-gray-600">Palavras Únicas</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-600">{estatisticas.categoriasIdentificadas || 0}</div>
            <div className="text-sm text-gray-600">Categorias</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-600">{estatisticas.fontes || 0}</div>
            <div className="text-sm text-gray-600">Fontes</div>
          </div>
        </div>
        
        {/* Metodologia Carolina Martins Check */}
        {estatisticas.metodologia_carolina_martins && (
          <div className="mt-4 p-3 bg-purple-50 rounded-lg">
            <div className="flex items-center justify-between text-sm">
              <span className="text-purple-700 font-medium">Metodologia Carolina Martins:</span>
              <div className="flex items-center space-x-3">
                <span className={`flex items-center ${estatisticas.metodologia_carolina_martins.fase1_alvo_atingido ? 'text-green-600' : 'text-yellow-600'}`}>
                  {estatisticas.metodologia_carolina_martins.fase1_alvo_atingido ? (
                    <CheckCircleIcon className="w-4 h-4 mr-1" />
                  ) : (
                    <ExclamationTriangleIcon className="w-4 h-4 mr-1" />
                  )}
                  Fase 1: {estatisticas.metodologia_carolina_martins.fase1_total_palavras} palavras
                </span>
                <span className="text-purple-600">
                  Fase 2: TOP {estatisticas.metodologia_carolina_martins.fase2_top10}
                </span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Palavras-chave por Categoria */}
      {palavrasChave && (
        <>
          {/* Verifica se é o formato novo (com mpc_completo) ou antigo */}
          {palavrasChave.mpc_completo ? (
            // Novo formato da IA
            <div className="space-y-6">
              {/* Palavras essenciais */}
              {palavrasChave.mpc_completo.essenciais?.length > 0 && (
                <div className="bg-green-50 rounded-xl border border-green-200 p-6">
                  <h4 className="text-lg font-semibold text-green-900 mb-4">
                    🎯 Palavras Essenciais (presentes em &gt;60% das vagas)
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                    {palavrasChave.mpc_completo.essenciais.map((palavra, index) => (
                      <div key={index} className="bg-white rounded-lg p-3 border border-green-300">
                        <div className="font-medium text-gray-900">{palavra.termo}</div>
                        <div className="flex items-center justify-between mt-1">
                          <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">
                            {palavra.categoria}
                          </span>
                          <span className="text-xs text-green-600 font-medium">
                            {palavra.frequencia_percentual?.toFixed(0) || palavra.frequencia_absoluta}%
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Palavras importantes */}
              {palavrasChave.mpc_completo.importantes?.length > 0 && (
                <div className="bg-blue-50 rounded-xl border border-blue-200 p-6">
                  <h4 className="text-lg font-semibold text-blue-900 mb-4">
                    💡 Palavras Importantes (30-60% das vagas)
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                    {palavrasChave.mpc_completo.importantes.map((palavra, index) => (
                      <div key={index} className="bg-white rounded-lg p-3 border border-blue-300">
                        <div className="font-medium text-gray-900">{palavra.termo}</div>
                        <div className="flex items-center justify-between mt-1">
                          <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                            {palavra.categoria}
                          </span>
                          <span className="text-xs text-blue-600 font-medium">
                            {palavra.frequencia_percentual?.toFixed(0) || palavra.frequencia_absoluta}%
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Palavras complementares */}
              {palavrasChave.mpc_completo.complementares?.length > 0 && (
                <div className="bg-gray-50 rounded-xl border border-gray-200 p-6">
                  <h4 className="text-lg font-semibold text-gray-900 mb-4">
                    📌 Palavras Complementares (&lt;30% das vagas)
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                    {palavrasChave.mpc_completo.complementares.slice(0, 9).map((palavra, index) => (
                      <div key={index} className="bg-white rounded-lg p-3 border border-gray-300">
                        <div className="font-medium text-gray-900">{palavra.termo}</div>
                        <div className="flex items-center justify-between mt-1">
                          <span className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
                            {palavra.categoria}
                          </span>
                          <span className="text-xs text-gray-600 font-medium">
                            {palavra.frequencia_percentual?.toFixed(0) || palavra.frequencia_absoluta}%
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                  {palavrasChave.mpc_completo.complementares.length > 9 && (
                    <div className="text-xs text-gray-500 mt-3">
                      +{palavrasChave.mpc_completo.complementares.length - 9} palavras adicionais
                    </div>
                  )}
                </div>
              )}
            </div>
          ) : (
            // Formato antigo (compatibilidade)
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {Object.entries(palavrasChave).map(([categoria, palavras]) => (
                Array.isArray(palavras) && (
                  <div key={categoria} className="bg-white rounded-xl border border-gray-200 p-6">
                    <h4 className="text-lg font-semibold text-gray-900 mb-4 capitalize">
                      {categoria === 'tecnicas' ? 'Técnicas' : 
                       categoria === 'comportamentais' ? 'Comportamentais' : 
                       categoria === 'digitais' ? 'Digitais' : categoria}
                    </h4>
                    
                    <div className="space-y-2">
                      {palavras.slice(0, 10).map((palavra, index) => (
                        <div key={index} className="flex items-center justify-between">
                          <span className="text-sm text-gray-700">{palavra.termo}</span>
                          <div className="flex items-center space-x-2">
                            <span className="text-xs bg-gray-100 px-2 py-1 rounded">
                              {palavra.frequencia}x
                            </span>
                            <div className="w-12 bg-gray-200 rounded-full h-1">
                              <div 
                                className="bg-green-500 h-1 rounded-full"
                                style={{ width: `${palavras.length > 0 ? (palavra.frequencia / Math.max(...palavras.map(p => p.frequencia || 1))) * 100 : 50}%` }}
                              />
                            </div>
                          </div>
                        </div>
                      ))}
                      
                      {palavras.length > 10 && (
                        <div className="text-xs text-gray-500 mt-2">
                          +{palavras.length - 10} palavras adicionais
                        </div>
                      )}
                    </div>
                  </div>
                )
              ))}
            </div>
          )}
        </>
      )}

      {/* TOP 10 Carolina Martins */}
      {safeTop10 && safeTop10.length > 0 && (
        <div className="bg-purple-50 rounded-xl border border-purple-200 p-6">
          <h3 className="text-lg font-semibold text-purple-900 mb-4 flex items-center">
            <SparklesIcon className="w-5 h-5 mr-2 text-purple-600" />
            TOP 10 Palavras-Chave - Fase 2 Carolina Martins
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {safeTop10 && Array.isArray(safeTop10) && safeTop10.map((palavra, index) => (
              <div key={index} className="flex items-center justify-between bg-white rounded-lg p-3">
                <div className="flex items-center">
                  <span className="text-lg font-bold text-purple-600 mr-3">#{index + 1}</span>
                  <div>
                    <span className="font-medium text-gray-900">{palavra.termo}</span>
                    <span className="ml-2 text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded">
                      {palavra.categoria}
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-medium text-purple-600">
                    {palavra.importancia ? (palavra.importancia * 100).toFixed(0) : Math.round(palavra.frequencia_percentual || 90)}%
                  </div>
                  <div className="text-xs text-gray-500">importância</div>
                </div>
              </div>
            ))}
          </div>
          
          <div className="mt-4 p-3 bg-purple-100 rounded-lg">
            <p className="text-xs text-purple-800">
              <strong>💡 Como usar:</strong> Estas são as 10 palavras mais estratégicas para otimizar seu currículo. 
              Use 3-4 no título do LinkedIn e distribua as demais no resumo e experiências.
            </p>
          </div>
        </div>
      )}

      {/* Insights da IA (novo formato) */}
      {insights && (
        <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-xl border border-purple-200 p-6">
          <h3 className="text-lg font-semibold text-purple-900 mb-4 flex items-center">
            <SparklesIcon className="w-5 h-5 mr-2 text-purple-600" />
            Insights da IA - {modelo_usado || 'Gemini 2.5 Pro'}
          </h3>
          
          <div className="space-y-4">
            {insights && insights.tendencias_emergentes && insights.tendencias_emergentes.length > 0 && (
              <div>
                <h4 className="font-medium text-purple-800 mb-2">🚀 Tendências Emergentes:</h4>
                <div className="flex flex-wrap gap-2">
                  {insights.tendencias_emergentes.map((tendencia, index) => (
                    <span key={index} className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm">
                      {tendencia}
                    </span>
                  ))}
                </div>
              </div>
            )}
            
            {insights && insights.gaps_identificados && insights.gaps_identificados.length > 0 && (
              <div>
                <h4 className="font-medium text-blue-800 mb-2">🎯 Oportunidades de Diferenciação:</h4>
                <ul className="space-y-1">
                  {insights.gaps_identificados.map((gap, index) => (
                    <li key={index} className="text-sm text-blue-700 flex items-start">
                      <CheckCircleIcon className="w-4 h-4 mr-2 mt-0.5 flex-shrink-0 text-blue-600" />
                      {gap}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            {insights && insights.recomendacoes && insights.recomendacoes.length > 0 && (
              <div>
                <h4 className="font-medium text-green-800 mb-2">💡 Recomendações Personalizadas:</h4>
                <ul className="space-y-1">
                  {insights.recomendacoes.map((rec, index) => (
                    <li key={index} className="text-sm text-green-700 flex items-start">
                      <CheckCircleIcon className="w-4 h-4 mr-2 mt-0.5 flex-shrink-0 text-green-600" />
                      {rec}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Validação de IA (formato antigo) */}
      {validacaoIA && (
        <div className="bg-blue-50 rounded-xl border border-blue-200 p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-4 flex items-center">
            <SparklesIcon className="w-5 h-5 mr-2 text-blue-600" />
            Validação e Sugestões da IA
          </h3>
        
        <div className="space-y-4">
          {validacaoIA.recomendacoes && validacaoIA.recomendacoes.length > 0 && (
            <div>
              <h4 className="font-medium text-blue-900 mb-2">Recomendações:</h4>
              <ul className="space-y-1">
                {validacaoIA.recomendacoes.map((recomendacao, index) => (
                  <li key={index} className="text-sm text-blue-800 flex items-start">
                    <CheckCircleIcon className="w-4 h-4 mr-2 mt-0.5 flex-shrink-0 text-green-600" />
                    {recomendacao}
                  </li>
                ))}
              </ul>
            </div>
          )}
          
          {validacaoIA.alertas && validacaoIA.alertas.length > 0 && (
            <div>
              <h4 className="font-medium text-blue-900 mb-2">Alertas:</h4>
              <ul className="space-y-1">
                {validacaoIA.alertas.map((alerta, index) => (
                  <li key={index} className="text-sm text-blue-800 flex items-start">
                    <ExclamationTriangleIcon className="w-4 h-4 mr-2 mt-0.5 flex-shrink-0 text-yellow-600" />
                    {alerta}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
      )}

      {/* Fontes */}
      {safeFontes && safeFontes.length > 0 && (
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <GlobeAltIcon className="w-5 h-5 mr-2 text-gray-600" />
            Fontes Utilizadas
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {safeFontes.map((fonte, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <div className="font-medium text-gray-900">{fonte.nome}</div>
                  <div className="text-sm text-gray-600">{fonte.vagas} vagas</div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-medium text-green-600">{fonte.taxa}%</div>
                  <div className="text-xs text-gray-500">sucesso</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Transparência Total */}
      <TransparencySection transparencia={transparencia} />

      {/* Próximos Passos */}
      <div className="bg-green-50 rounded-xl border border-green-200 p-6">
        <h3 className="text-lg font-semibold text-green-900 mb-3">
          Próximos Passos Recomendados
        </h3>
        <div className="space-y-2">
          <p className="text-sm text-green-800">• Execute o Agente 2 para otimizar seu currículo com as palavras-chave encontradas</p>
          <p className="text-sm text-green-800">• Incorpore as palavras-chave técnicas em suas experiências profissionais</p>
          <p className="text-sm text-green-800">• Desenvolva as competências comportamentais identificadas como prioritárias</p>
          <p className="text-sm text-green-800">• Prepare-se para otimização do LinkedIn com essas palavras-chave</p>
        </div>
      </div>
    </div>
  )
}

// Main Component
const Agent1 = () => {
  const [searchConfig, setSearchConfig] = useState({
    area: '',
    cargo: '',
    localizacao: '',
    quantidade: 100,
    segmentos: ''
  })
  const [isProcessing, setIsProcessing] = useState(false)
  const [currentStep, setCurrentStep] = useState(0)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const [useStreaming, setUseStreaming] = useState(true)
  const [isStreamActive, setIsStreamActive] = useState(false)
  const [streamRequestData, setStreamRequestData] = useState(null)
  const [collectionData, setCollectionData] = useState(null) // Dados da coleta
  const [isAnalyzing, setIsAnalyzing] = useState(false) // Estado da análise

  const stepLabels = [
    'Configurando busca',
    'Coletando vagas do LinkedIn Jobs',
    'Coletando vagas do Google Jobs',
    'Coletando fontes complementares',
    'Extraindo palavras-chave',
    'Categorizando termos',
    'Validando com IA',
    'Finalizando análise'
  ]

  const handleStreamComplete = async (resultId) => {
    try {
      // Buscar resultado completo
      const response = await fetch(`${config.endpoints.results}/${resultId}`)
      const data = await response.json()
      setResults(data)
      setIsStreamActive(false)
      setIsProcessing(false)
    } catch (err) {
      setError('Erro ao carregar resultados')
      setIsStreamActive(false)
      setIsProcessing(false)
    }
  }

  const handleStreamError = (errorMessage) => {
    setError(errorMessage)
    setIsStreamActive(false)
    setIsProcessing(false)
  }

  const handleStartCollection = async () => {
    if (!searchConfig.area.trim() || !searchConfig.cargo.trim() || !searchConfig.localizacao.trim()) {
      setError('Por favor, preencha todos os campos obrigatórios.')
      return
    }

    setIsProcessing(true)
    setError(null)
    setResults(null)
    setCollectionData(null)

    // Sempre usar o novo fluxo de 2 etapas
    setCurrentStep(1)
    try {
      const requestData = {
        area_interesse: searchConfig.area.trim(),
        cargo_objetivo: searchConfig.cargo.trim(),
        localizacao: searchConfig.localizacao.trim(),
        total_vagas_desejadas: searchConfig.quantidade,
        segmentos_alvo: searchConfig.segmentos.trim() ? config.segmentos.trim().split(',').map(s => s.trim()) : [],
        tipo_vaga: 'hibrido' // Adicionar tipo de vaga
      }

      setCurrentStep(2)

      // ETAPA 1: Coletar vagas
      // Primeiro tentar o endpoint real
      let response = await fetch(config.endpoints.agent1.collectJobs, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
      })
      
      // Se demorar muito ou falhar, sugerir modo demo
      if (!response.ok || response.status === 500) {
        const shouldUseDemo = window.confirm(
          'A coleta de vagas reais está demorando ou falhou.\n\n' +
          'Deseja usar o modo demonstração com vagas de exemplo?\n\n' +
          'Isso permitirá testar o sistema completo.'
        )
        
        if (shouldUseDemo) {
          console.log('Mudando para modo DEMO...')
          response = await fetch(config.endpoints.agent1.collectJobsDemo, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
          })
        }
      }

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Erro na coleta de vagas')
      }

      setCurrentStep(4)
      const collectionResult = await response.json()
      
      // Salvar dados da coleta
      setCollectionData(collectionResult)
      setIsProcessing(false)
      
      // Mostrar aviso se for modo demo
      if (collectionResult.demo_mode) {
        console.log('🎭 MODO DEMO ATIVADO - Usando vagas de exemplo')
      }
      
      // Mostrar vagas coletadas e botão para análise
      console.log(`✅ ${collectionResult.estatisticas.totalVagas} vagas coletadas!`)
      
    } catch (err) {
      console.error('Erro na coleta:', err)
      setError(err.message || 'Erro ao coletar vagas. Verifique se o backend está rodando.')
      setIsProcessing(false)
    }
  }

  const handleAnalyzeKeywords = async () => {
    if (!collectionData || !collectionData.id) {
      setError('Nenhuma coleta disponível para análise')
      return
    }

    setIsAnalyzing(true)
    setError(null)
    setCurrentStep(5)

    try {
      const requestData = {
        collection_id: collectionData.id,
        area_interesse: searchConfig.area.trim(),
        cargo_objetivo: searchConfig.cargo.trim()
      }

      setCurrentStep(6)

      // ETAPA 2: Analisar palavras-chave com Gemini
      const response = await fetch(config.endpoints.agent1.analyzeKeywords, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Erro na análise de palavras-chave')
      }

      setCurrentStep(7)
      const analysisResult = await response.json()
      
      setCurrentStep(8)
      await new Promise(resolve => setTimeout(resolve, 500))
      
      // Mesclar dados da coleta com análise
      const finalResult = {
        ...collectionData,
        ...analysisResult,
        transparencia: {
          vagas_coletadas: collectionData.vagas,
          ...analysisResult.transparencia
        }
      }
      
      setResults(finalResult)
      setIsAnalyzing(false)
      
    } catch (err) {
      console.error('Erro na análise:', err)
      setError(err.message || 'Erro ao analisar palavras-chave.')
      setIsAnalyzing(false)
    }
  }

  const handleStartCollectionOld = async () => {
    if (!searchConfig.area.trim() || !searchConfig.cargo.trim() || !searchConfig.localizacao.trim()) {
      setError('Por favor, preencha todos os campos obrigatórios.')
      return
    }

    setIsProcessing(true)
    setError(null)
    setResults(null)

    if (useStreaming) {
      // Usar novo endpoint com streaming
      try {
        const requestData = {
          area_interesse: searchConfig.area.trim(),
          cargo_objetivo: searchConfig.cargo.trim(),
          localizacao: searchConfig.localizacao.trim(),
          total_vagas_desejadas: searchConfig.quantidade,
          segmentos_alvo: searchConfig.segmentos.trim() ? config.segmentos.trim().split(',').map(s => s.trim()) : []
        }

        // Salvar dados da requisição e ativar o stream
        setStreamRequestData(requestData)
        setIsStreamActive(true)
      } catch (err) {
        setError(err.message)
        setIsProcessing(false)
      }
    } else {
      // Usar endpoint tradicional (mantido para compatibilidade)
      setCurrentStep(1)
      try {
        const requestData = {
          area_interesse: searchConfig.area.trim(),
          cargo_objetivo: searchConfig.cargo.trim(),
          localizacao: searchConfig.localizacao.trim(),
          total_vagas_desejadas: searchConfig.quantidade,
          segmentos_alvo: searchConfig.segmentos.trim() ? config.segmentos.trim().split(',').map(s => s.trim()) : []
        }

        setCurrentStep(2)

        const response = await fetch('http://localhost:5001/api/agent1/collect-keywords', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestData)
        })

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.error || 'Erro na coleta de palavras-chave')
        }

        setCurrentStep(4)
        const results = await response.json()
        setCurrentStep(6)

        await new Promise(resolve => setTimeout(resolve, 500))
        setCurrentStep(7)
        
        await new Promise(resolve => setTimeout(resolve, 500))
        setCurrentStep(8)

        setResults(results)

      } catch (err) {
        console.error('Erro na coleta:', err)
        setError(err.message || 'Erro ao coletar vagas. Verifique se o backend está rodando.')
      } finally {
        setIsProcessing(false)
      }
    }
  }

  const canStartCollection = (
    config.area.trim() && 
    config.cargo.trim() && 
    config.localizacao.trim() && 
    !isProcessing
  )

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      {/* Progress Stream Modal */}
      <ProgressStream 
        isActive={isStreamActive}
        onComplete={handleStreamComplete}
        onError={handleStreamError}
        requestData={streamRequestData}
      />
      
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Mapa de Palavras-Chave (MPC)
          </h2>
          <p className="text-gray-600 max-w-3xl mx-auto">
            Coletamos vagas reais do mercado para identificar as palavras-chave mais relevantes 
            para sua área de atuação, categorizando-as em técnicas, comportamentais e digitais.
          </p>
        </div>

        {/* Progress */}
        {isProcessing && (
          <div className="mb-6">
            <ProgressIndicator 
              currentStep={currentStep} 
              steps={8} 
              stepLabels={stepLabels}
            />
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

        {!results && !collectionData ? (
          /* Configuration Section */
          <div className="space-y-6">
                          <SearchConfiguration
                config={searchConfig}
                onChange={setSearchConfig}
              disabled={isProcessing}
            />

            <div className="text-center">
              <button
                onClick={handleStartCollection}
                disabled={!canStartCollection}
                className={`
                  inline-flex items-center px-8 py-3 rounded-lg text-sm font-medium transition-all duration-200
                  ${canStartCollection
                    ? 'bg-green-600 hover:bg-green-700 text-white shadow-sm hover:shadow-md transform hover:-translate-y-0.5'
                    : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  }
                `}
              >
                {isProcessing ? (
                  <>
                    <ArrowPathIcon className="w-4 h-4 mr-2 animate-spin" />
                    Coletando Vagas...
                  </>
                ) : (
                  <>
                    <MagnifyingGlassIcon className="w-4 h-4 mr-2" />
                    Iniciar Coleta de Vagas
                  </>
                )}
              </button>
              
              {/* Loading Warning */}
              {isProcessing && (
                <div className="mt-4 bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div className="flex items-start">
                    <ClockIcon className="w-5 h-5 text-blue-600 mr-2 mt-0.5" />
                    <div className="flex-1">
                      <h4 className="text-sm font-medium text-blue-800">Coletando vagas reais...</h4>
                      <p className="text-xs text-blue-700 mt-1">
                        Tempo estimado:
                        {searchConfig.quantidade <= 50 && ' 1-2 minutos'}
                        {searchConfig.quantidade > 50 && searchConfig.quantidade <= 100 && ' 2-3 minutos'}
                        {searchConfig.quantidade > 100 && searchConfig.quantidade <= 200 && ' 3-5 minutos'}
                        {searchConfig.quantidade > 200 && ' 5-10 minutos (grande volume)'}
                      </p>
                      <div className="mt-2">
                        <div className="flex items-center text-xs text-blue-600">
                          <div className="animate-pulse mr-2">●</div>
                          <span>Buscando {searchConfig.quantidade} vagas do LinkedIn via Apify</span>
                        </div>
                        <div className="flex items-center text-xs text-blue-600 mt-1">
                          <div className="animate-pulse mr-2">●</div>
                          <span>Processando descrições completas das vagas</span>
                        </div>
                        <div className="flex items-center text-xs text-blue-600 mt-1">
                          <div className="animate-pulse mr-2">●</div>
                          <span>Organizando dados para análise</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        ) : collectionData && !results ? (
          /* Collection Results - Show jobs before analysis */
          <CollectionResults 
            collectionData={collectionData}
            onAnalyze={handleAnalyzeKeywords}
            isAnalyzing={isAnalyzing}
            config={searchConfig}
          />
        ) : results ? (
          /* Results Section */
          <div>
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-semibold text-gray-900">
                Resultados da Análise
              </h3>
              <button
                onClick={() => {
                  setResults(null)
                  setCollectionData(null)
                  setCurrentStep(0)
                }}
                className="text-sm text-green-600 hover:text-green-700 font-medium"
              >
                Nova Análise
              </button>
            </div>
            <ResultsDisplay results={results} />
          </div>
        ) : null}

        {/* Info Section */}
        <div className="mt-12 space-y-6">
          {/* Metodologia Carolina Martins */}
          <div className="bg-purple-50 rounded-xl p-6 border border-purple-200">
            <h3 className="text-lg font-semibold text-purple-900 mb-3 flex items-center">
              <SparklesIcon className="w-5 h-5 mr-2" />
              Metodologia Carolina Martins - Quantidades Recomendadas
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <div className="bg-white rounded-lg p-4">
                <h4 className="font-semibold text-purple-800 mb-2">📊 Fase 1: Pesquisa Ampla</h4>
                <p className="text-purple-700 text-2xl font-bold mb-1">20-40</p>
                <p className="text-purple-600 text-xs">palavras-chave iniciais</p>
                <p className="text-gray-600 text-xs mt-2">Análise de no mínimo 20 vagas ou perfis do LinkedIn</p>
              </div>
              <div className="bg-white rounded-lg p-4">
                <h4 className="font-semibold text-purple-800 mb-2">🎯 Fase 2: Priorização</h4>
                <p className="text-purple-700 text-2xl font-bold mb-1">TOP 10</p>
                <p className="text-purple-600 text-xs">palavras mais estratégicas</p>
                <p className="text-gray-600 text-xs mt-2">Base para otimizar título e resumo</p>
              </div>
              <div className="bg-white rounded-lg p-4">
                <h4 className="font-semibold text-purple-800 mb-2">💼 LinkedIn</h4>
                <p className="text-purple-700 text-2xl font-bold mb-1">3-4 / 50</p>
                <p className="text-purple-600 text-xs">no título / competências</p>
                <p className="text-gray-600 text-xs mt-2">Título: 3-4 fortes<br/>Competências: exatas 50</p>
              </div>
            </div>
            <div className="mt-4 p-3 bg-purple-100 rounded-lg">
              <p className="text-xs text-purple-800">
                <strong>💡 Dica:</strong> Uma "palavra-chave" pode ser um termo composto. 
                Ex: "gerenciamento de frotas" é UMA palavra-chave, não duas.
              </p>
            </div>
          </div>

          {/* Como funciona */}
          <div className="bg-green-50 rounded-xl p-6">
            <h3 className="text-lg font-semibold text-green-900 mb-3">
              Como funciona o MPC?
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-green-800">
              <div>
                <h4 className="font-medium mb-2">Coleta de Dados:</h4>
                <ul className="space-y-1">
                  <li>• Busca automatizada em múltiplas fontes</li>
                  <li>• Análise de descrições de vagas reais</li>
                  <li>• Extração de termos relevantes</li>
                </ul>
              </div>
              <div>
                <h4 className="font-medium mb-2">Categorização:</h4>
                <ul className="space-y-1">
                  <li>• Técnicas: ferramentas e tecnologias</li>
                  <li>• Comportamentais: soft skills</li>
                  <li>• Digitais: marketing e vendas online</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default Agent1