import React, { useState } from 'react'
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
  SparklesIcon,
  ArrowPathIcon,
  GlobeAltIcon,
  AdjustmentsHorizontalIcon,
  ChevronDownIcon,
  ChevronUpIcon,
  CalendarDaysIcon,
  UserGroupIcon,
  CurrencyDollarIcon,
  ClockIcon
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
  const [showAdvanced, setShowAdvanced] = useState(false)
  
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
            placeholder="Ex: Desenvolvedor Python, Analista de Marketing, Gerente de Vendas..."
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
            <option value={100}>100 vagas (limite máximo)</option>
          </select>
          {config.quantidade > 100 && (
            <p className="text-xs text-yellow-600 mt-1">
              ⚠️ Limite ajustado para 100 vagas para economizar custos
            </p>
          )}
        </div>

        {/* Tipo de Vaga */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <BriefcaseIcon className="w-4 h-4 inline mr-1" />
            Tipo de Vaga
          </label>
          <select
            value={config.tipoVaga || 'todos'}
            onChange={(e) => handleChange('tipoVaga', e.target.value)}
            disabled={disabled}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent disabled:bg-gray-50"
          >
            <option value="todos">Todos os tipos</option>
            <option value="presencial">Presencial</option>
            <option value="remoto">Remoto</option>
            <option value="hibrido">Híbrido</option>
          </select>
        </div>
      </div>
      
      {/* Aviso sobre limite */}
      <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-sm text-blue-700">
          <InformationCircleIcon className="w-4 h-4 inline mr-1" />
          <strong>Nota:</strong> Para economizar custos, limitamos a busca a 100 vagas por pesquisa (custo aprox. US$ 0,50).
        </p>
      </div>

      {/* Botão para Filtros Avançados */}
      <div className="mt-6">
        <button
          type="button"
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="flex items-center text-sm font-medium text-gray-700 hover:text-gray-900"
        >
          <AdjustmentsHorizontalIcon className="w-4 h-4 mr-2" />
          Filtros Avançados
          {showAdvanced ? (
            <ChevronUpIcon className="w-4 h-4 ml-1" />
          ) : (
            <ChevronDownIcon className="w-4 h-4 ml-1" />
          )}
        </button>
      </div>
      
      {/* Filtros Avançados */}
      {showAdvanced && (
        <div className="mt-4 p-4 bg-gray-50 rounded-lg space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Raio de Busca */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <MapPinIcon className="w-4 h-4 inline mr-1" />
                Raio de Busca
              </label>
              <select
                value={config.raio || '25'}
                onChange={(e) => handleChange('raio', e.target.value)}
                disabled={disabled}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent disabled:bg-gray-50"
              >
                <option value="5">5 km</option>
                <option value="10">10 km</option>
                <option value="15">15 km</option>
                <option value="25">25 km (padrão)</option>
                <option value="50">50 km</option>
                <option value="100">100 km</option>
              </select>
            </div>
            
            {/* Nível de Experiência */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <UserGroupIcon className="w-4 h-4 inline mr-1" />
                Nível de Experiência
              </label>
              <select
                value={config.nivel || 'todos'}
                onChange={(e) => handleChange('nivel', e.target.value)}
                disabled={disabled}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent disabled:bg-gray-50"
              >
                <option value="todos">Todos os níveis</option>
                <option value="entry_level">Júnior / Entry Level</option>
                <option value="mid_level">Pleno / Mid Level</option>
                <option value="senior_level">Sênior / Senior Level</option>
              </select>
            </div>
            
            {/* Tipo de Contrato */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <BriefcaseIcon className="w-4 h-4 inline mr-1" />
                Tipo de Contrato
              </label>
              <select
                value={config.tipoContrato || 'todos'}
                onChange={(e) => handleChange('tipoContrato', e.target.value)}
                disabled={disabled}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent disabled:bg-gray-50"
              >
                <option value="todos">Todos os tipos</option>
                <option value="fulltime">Tempo integral (CLT)</option>
                <option value="parttime">Meio período</option>
                <option value="contract">Contrato / PJ</option>
                <option value="internship">Estágio</option>
                <option value="temporary">Temporário</option>
              </select>
            </div>
            
            {/* Data de Publicação */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <CalendarDaysIcon className="w-4 h-4 inline mr-1" />
                Publicadas nos últimos
              </label>
              <select
                value={config.diasPublicacao || 'todos'}
                onChange={(e) => handleChange('diasPublicacao', e.target.value)}
                disabled={disabled}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent disabled:bg-gray-50"
              >
                <option value="todos">Qualquer data</option>
                <option value="1">24 horas</option>
                <option value="3">3 dias</option>
                <option value="7">7 dias</option>
                <option value="14">14 dias</option>
                <option value="30">30 dias</option>
              </select>
            </div>
            
            {/* Ordenar por */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <ArrowPathIcon className="w-4 h-4 inline mr-1" />
                Ordenar por
              </label>
              <select
                value={config.ordenar || 'date'}
                onChange={(e) => handleChange('ordenar', e.target.value)}
                disabled={disabled}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent disabled:bg-gray-50"
              >
                <option value="date">Mais recentes</option>
                <option value="relevance">Mais relevantes</option>
              </select>
            </div>
            
            {/* Apenas Remoto */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <GlobeAltIcon className="w-4 h-4 inline mr-1" />
                Modalidade
              </label>
              <select
                value={config.modalidade || 'todos'}
                onChange={(e) => handleChange('modalidade', e.target.value)}
                disabled={disabled}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent disabled:bg-gray-50"
              >
                <option value="todos">Todas as modalidades</option>
                <option value="remote">Apenas remoto</option>
                <option value="presencial">Apenas presencial</option>
              </select>
            </div>
          </div>
          
          {/* Segmentos */}
          <div className="mt-4">
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
      )}
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
const CollectionResults = ({ 
  collectionData, 
  onAnalyze, 
  isAnalyzing, 
  config, 
  analysisStatus, 
  analysisMessage, 
  analysisProgress, 
  onCancelAnalysis 
}) => {
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
          {collectionData.estatisticas.totalVagas > 0 ? (
            <>
              <CheckCircleIcon className="w-5 h-5 mr-2 text-green-600" />
              Vagas Coletadas com Sucesso!
            </>
          ) : (
            <>
              <ExclamationTriangleIcon className="w-5 h-5 mr-2 text-yellow-600" />
              Nenhuma Vaga Encontrada
            </>
          )}
        </h3>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-gray-50 rounded-lg p-4 text-center">
            <p className="text-3xl font-bold text-gray-900">{collectionData.estatisticas.totalVagas}</p>
            <p className="text-sm text-gray-600">Vagas Coletadas</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4 text-center">
            <p className="text-3xl font-bold text-gray-900">{collectionData.estatisticas.fontes || 1}</p>
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
        
        {/* Mensagem quando não há vagas */}
        {collectionData.estatisticas.totalVagas === 0 && (
          <div className="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
            <h4 className="text-sm font-medium text-yellow-800 mb-2">Por que não foram encontradas vagas?</h4>
            <ul className="text-sm text-yellow-700 space-y-1">
              <li>• Houve um problema temporário com a coleta do Apify</li>
              <li>• O Actor pode ter finalizado muito rápido sem coletar os dados</li>
              <li>• Possível problema de configuração ou limite de requisições</li>
            </ul>
            <p className="text-sm text-yellow-700 mt-3">
              <strong>Solução:</strong> Tente novamente em alguns segundos. Se o problema persistir, verifique o dashboard do Apify.
            </p>
          </div>
        )}
        
        {/* Fontes */}
        {collectionData.fontes && collectionData.fontes.length > 0 && (
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
        )}
        
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
          disabled={isAnalyzing || collectionData.estatisticas.totalVagas === 0}
          className={`
            inline-flex items-center px-8 py-3 rounded-lg text-sm font-medium transition-all duration-200
            ${!isAnalyzing && collectionData.estatisticas.totalVagas > 0
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
        
        {/* Loading da Análise com Streaming */}
        {isAnalyzing && (
          <div className="mt-4 bg-purple-50 border border-purple-200 rounded-lg p-4">
            <div className="flex items-start justify-between">
              <div className="flex items-start flex-1">
                <SparklesIcon className="w-5 h-5 text-purple-600 mr-2 mt-0.5 animate-pulse" />
                <div className="flex-1">
                  <h4 className="text-sm font-medium text-purple-800">
                    {analysisStatus === 'concluido' ? 'Análise Concluída!' : 'Analisando com IA...'}
                  </h4>
                  <p className="text-xs text-purple-700 mt-1">
                    {analysisMessage || `Processando ${collectionData.estatisticas.totalVagas} vagas para extrair palavras-chave.`}
                  </p>
                  
                  {/* Barra de Progresso */}
                  {analysisProgress > 0 && (
                    <div className="mt-3">
                      <div className="flex justify-between text-xs text-purple-600 mb-1">
                        <span>Progresso</span>
                        <span>{analysisProgress}%</span>
                      </div>
                      <div className="w-full bg-purple-200 rounded-full h-2">
                        <div 
                          className="bg-purple-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${analysisProgress}%` }}
                        />
                      </div>
                    </div>
                  )}

                  <div className="mt-2 space-y-1">
                    <div className={`flex items-center text-xs ${analysisStatus === 'preparando' || analysisStatus === 'iniciando' ? 'text-purple-600 font-medium' : 'text-purple-500'}`}>
                      <div className={`mr-2 ${analysisStatus === 'preparando' || analysisStatus === 'iniciando' ? 'animate-pulse' : ''}`}>●</div>
                      <span>Preparando dados para análise</span>
                    </div>
                    <div className={`flex items-center text-xs ${analysisStatus === 'verificando_ia' ? 'text-purple-600 font-medium' : 'text-purple-500'}`}>
                      <div className={`mr-2 ${analysisStatus === 'verificando_ia' ? 'animate-pulse' : ''}`}>●</div>
                      <span>Verificando modelos de IA disponíveis</span>
                    </div>
                    <div className={`flex items-center text-xs ${analysisStatus === 'analisando' || analysisStatus === 'processando_descricoes' ? 'text-purple-600 font-medium' : 'text-purple-500'}`}>
                      <div className={`mr-2 ${analysisStatus === 'analisando' || analysisStatus === 'processando_descricoes' ? 'animate-pulse' : ''}`}>●</div>
                      <span>Processando descrições das vagas</span>
                    </div>
                    <div className={`flex items-center text-xs ${analysisStatus === 'identificando_padroes' ? 'text-purple-600 font-medium' : 'text-purple-500'}`}>
                      <div className={`mr-2 ${analysisStatus === 'identificando_padroes' ? 'animate-pulse' : ''}`}>●</div>
                      <span>Identificando padrões e termos</span>
                    </div>
                    <div className={`flex items-center text-xs ${analysisStatus === 'aplicando_metodologia' ? 'text-purple-600 font-medium' : 'text-purple-500'}`}>
                      <div className={`mr-2 ${analysisStatus === 'aplicando_metodologia' ? 'animate-pulse' : ''}`}>●</div>
                      <span>Aplicando metodologia Carolina Martins</span>
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Botão de Cancelar */}
              {analysisStatus !== 'concluido' && (
                <button
                  onClick={onCancelAnalysis}
                  className="ml-4 px-3 py-1 text-xs bg-red-100 text-red-700 rounded-md hover:bg-red-200 transition-colors"
                >
                  Cancelar
                </button>
              )}
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
                Para coleta real, configure a API do Indeed via Apify.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Indeed/Apify Info */}
      {!transparencia?.vagas_coletadas?.some(vaga => vaga.fonte?.toLowerCase().includes('indeed')) && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-start">
            <InformationCircleIcon className="w-5 h-5 text-blue-600 mr-2 mt-0.5" />
            <div className="flex-1">
              <h3 className="text-sm font-medium text-blue-800">💡 Dica: Ative a coleta do Indeed com Apify</h3>
              <p className="text-xs text-blue-700 mt-1 mb-2">
                Para coletar vagas reais do Indeed, configure o Apify:
              </p>
              <ol className="text-xs text-blue-700 space-y-1 ml-4">
                <li>1. Crie uma conta gratuita em <a href="https://apify.com" target="_blank" rel="noopener noreferrer" className="underline">apify.com</a></li>
                <li>2. Copie seu API Token do dashboard</li>
                <li>3. Adicione ao arquivo .env: <code className="bg-blue-100 px-1 py-0.5 rounded">APIFY_API_TOKEN=seu_token</code></li>
                <li>4. Reinicie o servidor backend</li>
              </ol>
              <p className="text-xs text-blue-600 mt-2">
                ✨ Actor usado: <a href="https://apify.com/borderline/indeed-scraper" target="_blank" rel="noopener noreferrer" className="underline font-medium">borderline/indeed-scraper</a> (US$ 0,50 por 100 vagas)
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
              Use 3-4 no título do currículo e distribua as demais no resumo e experiências.
            </p>
          </div>
        </div>
      )}

      {/* Insights da IA (novo formato) */}
      {insights && (
        <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-xl border border-purple-200 p-6">
          <h3 className="text-lg font-semibold text-purple-900 mb-4 flex items-center">
            <SparklesIcon className="w-5 h-5 mr-2 text-purple-600" />
            Insights da IA - {modelo_usado || 'Gemini 1.5 Pro'}
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
          <p className="text-sm text-green-800">• Prepare-se para otimização do currículo e LinkedIn com essas palavras-chave</p>
        </div>
      </div>
    </div>
  )
}

const StreamingJobCollection = ({ isVisible, onClose, onJobsCollected, searchConfig }) => {
  const [status, setStatus] = useState('iniciando')
  const [message, setMessage] = useState('Preparando coleta...')
  const [progress, setProgress] = useState(0)
  const [vagasColetadas, setVagasColetadas] = useState([])
  const [error, setError] = useState(null)
  const [abortController, setAbortController] = useState(null)
  const [runId, setRunId] = useState(null)
  const [isCancelling, setIsCancelling] = useState(false)
  const [isInitialLoad, setIsInitialLoad] = useState(true)
  
  const handleCancel = async () => {
    console.log('🔴 BOTÃO CANCELAR CLICADO!')
    console.log('📊 runId atual:', runId)
    console.log('📊 abortController:', abortController)
    
    if (!runId) {
      console.log('⚠️ Sem run_id, apenas abortando fetch')
      // Se não temos run_id, apenas abortar o fetch
      if (abortController) {
        abortController.abort()
      }
      onClose()
      return
    }
    
    console.log('🚀 Tentando cancelar run_id:', runId)
    setIsCancelling(true)
    
    try {
      // Cancelar no Apify
      const response = await fetch(`${config.baseURL}/api/agent1/cancel-collection`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ run_id: runId })
      })
      
      console.log('📡 Response status:', response.status)
      const responseData = await response.text()
      console.log('📄 Response data:', responseData)
      
      if (response.ok) {
        console.log('✅ Coleta cancelada com sucesso')
      } else {
        console.error('❌ Erro na resposta:', response.status, responseData)
      }
    } catch (err) {
      console.error('💥 Erro ao cancelar coleta:', err)
    }
    
    // Abortar o streaming também
    if (abortController) {
      abortController.abort()
    }
    
    setIsCancelling(false)
    onClose()
  }
  
  React.useEffect(() => {
    if (!isVisible || !searchConfig) return
    
    // Usar fetch com streaming
    const startStreaming = async () => {
      const controller = new AbortController()
      setAbortController(controller)
      
      try {
        const requestData = {
          area_interesse: searchConfig.cargo.trim(), // Usar cargo como área também
          cargo_objetivo: searchConfig.cargo.trim(),
          localizacao: searchConfig.localizacao.trim(),
          total_vagas_desejadas: searchConfig.quantidade,
          segmentos_alvo: searchConfig.segmentos?.trim() ? searchConfig.segmentos.trim().split(',').map(s => s.trim()) : [],
          tipo_vaga: searchConfig.tipoVaga || 'todos',
          // Parâmetros avançados
          raio: searchConfig.raio || '25',
          nivel: searchConfig.nivel || 'todos',
          tipoContrato: searchConfig.tipoContrato || 'todos',
          diasPublicacao: searchConfig.diasPublicacao || 'todos',
          ordenar: searchConfig.ordenar || 'date',
          modalidade: searchConfig.modalidade || 'todos'
        }
        
        console.log('🚀 Iniciando streaming com dados:', requestData)
        
        const response = await fetch(`${config.baseURL}/api/agent1/collect-jobs-stream`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestData),
          signal: controller.signal
        })
        
        if (!response.ok) {
          throw new Error('Erro ao iniciar streaming')
        }
        
        const reader = response.body.getReader()
        const decoder = new TextDecoder()
        let buffer = ''
        
        while (true) {
          const { done, value } = await reader.read()
          if (done) break
          
          buffer += decoder.decode(value, { stream: true })
          
          // Processar eventos SSE completos
          const events = buffer.split('\n\n')
          buffer = events.pop() || '' // Manter o último evento incompleto no buffer
          
          for (const event of events) {
            const lines = event.split('\n')
            for (const line of lines) {
              if (line.startsWith('data: ')) {
                try {
                  const jsonStr = line.slice(6)
                  if (jsonStr.trim()) {
                    const data = JSON.parse(jsonStr)
                    console.log('📨 Streaming data:', data)
                    
                    if (data.status) {
                      setStatus(data.status)
                      if (data.message) setMessage(data.message)
                      // Capturar run_id quando a coleta iniciar
                      if (data.status === 'coleta_iniciada' && data.run_id) {
                        setRunId(data.run_id)
                      }
                    }
                    
                    if (data.type === 'novas_vagas') {
                      setVagasColetadas(prev => [...prev, ...data.novas_vagas])
                      setProgress(data.total_atual)
                      setIsInitialLoad(false)
                    }
                    
                    if (data.status === 'finalizado' && data.vagas) {
                      onJobsCollected(data.vagas)
                      return
                    }
                    
                    if (data.error) {
                      setError(data.error)
                      return
                    }
                  }
                } catch (err) {
                  console.error('Erro ao processar stream:', err)
                }
              }
            }
          }
        }
      } catch (err) {
        if (err.name !== 'AbortError') {
          console.error('Erro ao iniciar streaming:', err)
          setError(err.message)
        }
      }
    }
    
    startStreaming()
    
    return () => {
      if (abortController) {
        abortController.abort()
      }
    }
  }, [isVisible, searchConfig, onJobsCollected])
  
  if (!isVisible) return null
  
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg p-6 max-w-4xl w-full max-h-[90vh] flex flex-col">
        {!error ? (
          <>
            <div className="text-center mb-4">
              <h3 className="text-xl font-semibold mb-2">Coletando Vagas em Tempo Real</h3>
              <p className="text-gray-600">{message}</p>
              <div className="flex items-center justify-center mt-3 space-x-4">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                <span className="text-sm font-medium text-gray-700">
                  Status: <span className="text-blue-600">{status}</span>
                </span>
                <span className="text-sm font-medium text-gray-700">
                  Vagas coletadas: <span className="text-green-600">{progress}</span>
                </span>
              </div>
            </div>
            
            {/* Lista de vagas coletadas */}
            {isInitialLoad && vagasColetadas.length === 0 ? (
              <div className="flex-1 flex items-center justify-center border rounded-lg p-8 mb-4 bg-gray-50">
                <div className="text-center">
                  <div className="animate-pulse mb-4">
                    <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full">
                      <svg className="animate-spin h-8 w-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                    </div>
                  </div>
                  <h4 className="text-sm font-semibold text-gray-700 mb-2">
                    Conectando ao Indeed...
                  </h4>
                  <p className="text-xs text-gray-600">
                    Aguarde enquanto iniciamos a busca por vagas
                  </p>
                </div>
              </div>
            ) : vagasColetadas.length > 0 ? (
              <div className="flex-1 overflow-y-auto border rounded-lg p-4 mb-4 bg-gray-50">
                <h4 className="text-sm font-semibold text-gray-700 mb-3">
                  🔍 Vagas encontradas ({vagasColetadas.length}):
                </h4>
                <div className="space-y-2">
                  {vagasColetadas.slice(-10).map((vaga, index) => (
                    <div key={index} className="bg-white p-3 rounded-lg shadow-sm border border-gray-200 animate-fadeIn">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <h5 className="font-medium text-gray-900 text-sm">{vaga.titulo || vaga.title}</h5>
                          <p className="text-xs text-gray-600 mt-1">
                            <span className="font-medium">{vaga.empresa || vaga.company}</span>
                            {(vaga.localizacao || vaga.location) && ` • ${vaga.localizacao || vaga.location}`}
                          </p>
                        </div>
                        <span className="text-xs text-blue-600 font-medium">
                          #{vagasColetadas.length - 10 + index + 1}
                        </span>
                      </div>
                    </div>
                  ))}
                  {vagasColetadas.length > 10 && (
                    <p className="text-center text-xs text-gray-500 mt-2">
                      Mostrando as últimas 10 de {vagasColetadas.length} vagas...
                    </p>
                  )}
                </div>
              </div>
            ) : null}
          </>
        ) : (
          <div className="text-center">
            <ExclamationTriangleIcon className="w-12 h-12 text-red-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2 text-red-600">Erro na Coleta</h3>
            <p className="text-gray-600 mb-4">{error}</p>
          </div>
        )}
        
        <div className="text-center space-x-4">
          {!error && status !== 'concluido' && status !== 'finalizado' && (
            <button 
              onClick={handleCancel}
              disabled={isCancelling}
              className="px-6 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isCancelling ? 'Cancelando...' : 'Interromper Busca'}
            </button>
          )}
          <button 
            onClick={() => onClose(error || '')}
            className="px-6 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
          >
            {error || status === 'concluido' || status === 'finalizado' ? 'Fechar' : 'Ocultar'}
          </button>
        </div>
      </div>
    </div>
  )
}

// Main Component
const Agent1 = () => {
  const [searchConfig, setSearchConfig] = useState({
    cargo: '',
    localizacao: '',
    quantidade: 100,
    segmentos: '',
    tipoVaga: 'todos',
    // Novos campos avançados
    raio: '25',
    nivel: 'todos',
    tipoContrato: 'todos',
    diasPublicacao: 'todos',
    ordenar: 'date',
    modalidade: 'todos'
  })
  const [isProcessing, setIsProcessing] = useState(false)
  const [currentStep, setCurrentStep] = useState(0)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const [isStreamActive, setIsStreamActive] = useState(false)
  const [collectionData, setCollectionData] = useState(null) // Dados da coleta
  const [isAnalyzing, setIsAnalyzing] = useState(false) // Estado da análise
  
  // Estados para streaming da análise
  const [analysisStatus, setAnalysisStatus] = useState('')
  const [analysisMessage, setAnalysisMessage] = useState('')
  const [analysisProgress, setAnalysisProgress] = useState(0)
  const [analysisAbortController, setAnalysisAbortController] = useState(null)

  const stepLabels = [
    'Configurando busca',
    'Coletando vagas do Indeed',
    'Coletando vagas do Indeed',
    'Coletando fontes complementares',
    'Extraindo palavras-chave',
    'Categorizando termos',
    'Validando com IA',
    'Finalizando análise'
  ]

  const handleStreamComplete = (vagas) => {
    console.log('✅ Stream completado com', vagas.length, 'vagas')
    setIsStreamActive(false)
    
    // Montar o resultado da coleta
    const collectionResult = {
      demo_mode: false,
      id: `stream_${Date.now()}`,
      timestamp: new Date().toISOString(),
      parametros: {
        area_interesse: searchConfig.cargo.trim(), // Usar cargo como área também
        cargo_objetivo: searchConfig.cargo.trim(),
        localizacao: searchConfig.localizacao.trim(),
        total_vagas_desejadas: searchConfig.quantidade
      },
      estatisticas: {
        totalVagas: vagas.length,
        vagasAnalisadas: vagas.length,
        successRate: 100,
        tempoColeta: 'Via streaming',
        fontes: 1
      },
      fontes: [
        {
          nome: 'Indeed',
          vagas: vagas.length,
          taxa: 100
        }
      ],
      transparencia: {
        fontes_utilizadas: ['Indeed'],
        metodo_coleta: 'Streaming em tempo real',
        filtros_aplicados: `Cargo: ${searchConfig.cargo.trim()}, Localização: ${searchConfig.localizacao.trim()}`,
        observacoes: 'Coleta realizada via streaming'
      },
      vagas: vagas
    }
    
    setCollectionData(collectionResult)
    setIsProcessing(false)
  }

  const handleStreamError = (errorMessage) => {
    // Garantir que sempre seja uma string
    const message = typeof errorMessage === 'string' ? errorMessage : ''
    if (message) {
      setError(message)
    }
    setIsStreamActive(false)
    setIsProcessing(false)
  }

  const handleStartCollection = async () => {
    console.log('🚀 INICIANDO COLETA DE VAGAS - LOGS DETALHADOS - v1.0.1')
    console.log('📋 Validando campos obrigatórios...')
    
    if (!searchConfig.cargo.trim() || !searchConfig.localizacao.trim()) {
      console.error('❌ ERRO: Campos obrigatórios não preenchidos')
      console.log('Cargo:', searchConfig.cargo.trim()) 
      console.log('Localização:', searchConfig.localizacao.trim())
      setError('Por favor, preencha todos os campos obrigatórios.')
      return
    }

    console.log('✅ Campos validados com sucesso')
    console.log('🔄 Configurando estado inicial...')

    setIsProcessing(true)
    setError(null)
    setResults(null)
    setCollectionData(null)

    // Sempre usar o novo fluxo de 2 etapas
    setCurrentStep(1)
    try {
      const requestData = {
        area_interesse: searchConfig.cargo.trim(), // Usar cargo como área também
        cargo_objetivo: searchConfig.cargo.trim(),
        localizacao: searchConfig.localizacao.trim(),
        total_vagas_desejadas: searchConfig.quantidade,
        segmentos_alvo: searchConfig.segmentos.trim() ? searchConfig.segmentos.trim().split(',').map(s => s.trim()) : [],
        tipo_vaga: searchConfig.tipoVaga // Usar tipo de vaga selecionado
      }

      console.log('📦 Dados da requisição preparados:')
      console.log(JSON.stringify(requestData, null, 2))
      
      console.log('🌐 Configuração de endpoints:')
      console.log('Base URL:', config.baseURL)
      console.log('Endpoint coleta:', config.endpoints.agent1.collectKeywordsStream)

      setCurrentStep(2)

      console.log('🔥 FAZENDO REQUISIÇÃO PARA:', `${config.baseURL}${config.endpoints.agent1.collectKeywordsStream}`)
      console.log('📡 Método: POST')
      console.log('📋 Headers: Content-Type: application/json')
      console.log('⏰ Timestamp:', new Date().toISOString())
      
      // Tentar usar streaming primeiro
      console.log('🌊 Tentando usar streaming em:', `${config.baseURL}/api/agent1/collect-jobs-stream`)
      console.log('Streaming disponível?', true)
      
      // Verificar se streaming está disponível
      if (true) {
        console.log('🌊 Iniciando coleta com streaming...')
        setIsStreamActive(true)
        // O streaming será gerenciado pelo StreamingJobCollection
        return
      }

      // ETAPA 1: Coletar vagas
      // Primeiro tentar o endpoint real
      let response = await fetch(`${config.baseURL}${config.endpoints.agent1.collectKeywordsStream}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
      })
      
      console.log('📨 RESPOSTA RECEBIDA:')
      console.log('Status:', response.status)
      console.log('StatusText:', response.statusText)
      console.log('OK:', response.ok)
      console.log('Headers:', Object.fromEntries(response.headers.entries()))
      
      // Se demorar muito ou falhar, sugerir modo demo
      if (!response.ok || response.status === 500) {
        console.log('⚠️ PROBLEMA NA RESPOSTA:')
        console.log('Response OK:', response.ok)
        console.log('Status:', response.status)
        
        try {
          const errorText = await response.text()
          console.log('Conteúdo da resposta de erro:', errorText)
        } catch (e) {
          console.log('Não foi possível ler o conteúdo da resposta de erro')
        }
        
        const shouldUseDemo = window.confirm(
          'A coleta de vagas reais está demorando ou falhou.\n\n' +
          'Deseja usar o modo demonstração com vagas de exemplo?\n\n' +
          'Isso permitirá testar o sistema completo.'
        )
        
        if (shouldUseDemo) {
          console.log('🎭 Mudando para modo DEMO...')
          console.log('Endpoint DEMO:', config.endpoints.agent1.collectJobsDemo)
          response = await fetch(`${config.baseURL}${config.endpoints.agent1.collectKeywords}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
          })
          
          console.log('📨 RESPOSTA DEMO:')
          console.log('Status:', response.status)
          console.log('OK:', response.ok)
        }
      }

      if (!response.ok) {
        console.error('❌ ERRO FINAL NA RESPOSTA:')
        console.log('Status:', response.status)
        console.log('StatusText:', response.statusText)
        
        let errorMessage = 'Erro na coleta de vagas'
        try {
        const errorData = await response.json()
          console.log('Dados de erro:', errorData)
          errorMessage = errorData.error || errorMessage
        } catch (e) {
          console.log('Não foi possível fazer parse do JSON de erro')
          const errorText = await response.text()
          console.log('Texto da resposta de erro:', errorText)
        }
        
        throw new Error(errorMessage)
      }

      console.log('🎉 SUCESSO! Fazendo parse da resposta...')
      setCurrentStep(4)
      const collectionResult = await response.json()
      
      console.log('📊 RESULTADO DA COLETA:')
      console.log(JSON.stringify(collectionResult, null, 2))
      
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
      console.error('💥 ERRO CAPTURADO NO CATCH:')
      console.error('Tipo do erro:', err.constructor.name)
      console.error('Mensagem:', err.message)
      console.error('Stack:', err.stack)
      console.error('Erro completo:', err)
      
      setError(err.message || 'Erro ao coletar vagas. Verifique se o backend está rodando.')
      setIsProcessing(false)
    }
  }

  const handleAnalyzeKeywords = async () => {
    if (!collectionData || !collectionData.vagas) {
      setError('Nenhuma vaga disponível para análise')
      return
    }

    setIsAnalyzing(true)
    setError(null)
    setCurrentStep(5)
    setAnalysisStatus('iniciando')
    setAnalysisMessage('Preparando análise...')
    setAnalysisProgress(0)

    const controller = new AbortController()
    setAnalysisAbortController(controller)

    try {
      const response = await fetch(`${config.baseURL}/api/agent1/analyze-keywords-stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          vagas: collectionData.vagas,
          cargo_objetivo: searchConfig.cargo.trim(),
          area_interesse: searchConfig.area?.trim() || ''
        }),
        signal: controller.signal
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      try {
        while (true) {
          const { value, done } = await reader.read()
          if (done) break

          const chunk = decoder.decode(value, { stream: true })
          const lines = chunk.split('\n')

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.slice(6))
                
                if (data.status) {
                  setAnalysisStatus(data.status)
                  
                  // Atualizar step baseado no status
                  if (data.status === 'analisando') setCurrentStep(6)
                  if (data.status === 'concluido') setCurrentStep(8)
                }
                if (data.message) {
                  setAnalysisMessage(data.message)
                }
                if (data.progress !== undefined) {
                  setAnalysisProgress(data.progress)
                }
                if (data.resultado) {
                  // Mesclar dados da coleta com análise
                  const finalResult = {
                    ...collectionData,
                    ...data.resultado,
                    transparencia: {
                      vagas_coletadas: collectionData.vagas,
                      ...data.resultado.transparencia
                    }
                  }
                  setResults(finalResult)
                  setCurrentStep(8)
                }
                if (data.error) {
                  console.error('Erro na análise:', data.error)
                  setError(`Erro na análise: ${data.error}`)
                  break
                }
              } catch (parseError) {
                console.warn('Erro ao processar linha de streaming:', parseError)
              }
            }
          }
        }
      } finally {
        reader.releaseLock()
      }
    } catch (err) {
      if (err.name === 'AbortError') {
        console.log('Análise cancelada pelo usuário')
      } else {
        console.error('Erro na análise:', err)
        setError(err.message || 'Erro ao conectar com o servidor para análise')
      }
    } finally {
      setIsAnalyzing(false)
      setAnalysisAbortController(null)
    }
  }

  // Função para cancelar análise
  const handleCancelAnalysis = () => {
    if (analysisAbortController) {
      analysisAbortController.abort()
      setIsAnalyzing(false)
      setAnalysisStatus('')
      setAnalysisMessage('')
      setAnalysisProgress(0)
      setAnalysisAbortController(null)
    }
  }

  const canStartCollection = (
    searchConfig.cargo.trim() && 
    searchConfig.localizacao.trim() && 
    !isProcessing
  )

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      {/* Progress Stream Modal */}
      <StreamingJobCollection 
        isVisible={isStreamActive}
        onJobsCollected={handleStreamComplete}
        onClose={handleStreamError}
        searchConfig={searchConfig}
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
                onClick={() => {
                  console.log('🔥 BOTÃO CLICADO! Chamando handleStartCollection...')
                  handleStartCollection()
                }}
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
            </div>
          </div>
        ) : collectionData && !results ? (
          /* Collection Results - Show jobs before analysis */
          <CollectionResults 
            collectionData={collectionData}
            onAnalyze={handleAnalyzeKeywords}
            isAnalyzing={isAnalyzing}
            config={searchConfig}
            analysisStatus={analysisStatus}
            analysisMessage={analysisMessage}
            analysisProgress={analysisProgress}
            onCancelAnalysis={handleCancelAnalysis}
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
                <p className="text-gray-600 text-xs mt-2">Análise de no mínimo 20 vagas reais do mercado</p>
              </div>
              <div className="bg-white rounded-lg p-4">
                <h4 className="font-semibold text-purple-800 mb-2">🎯 Fase 2: Priorização</h4>
                <p className="text-purple-700 text-2xl font-bold mb-1">TOP 10</p>
                <p className="text-purple-600 text-xs">palavras mais estratégicas</p>
                <p className="text-gray-600 text-xs mt-2">Base para otimizar título e resumo</p>
              </div>
              <div className="bg-white rounded-lg p-4">
                <h4 className="font-semibold text-purple-800 mb-2">💼 Currículo/LinkedIn</h4>
                <p className="text-purple-700 text-2xl font-bold mb-1">3-4 / 50</p>
                <p className="text-purple-600 text-xs">no título / competências</p>
                <p className="text-gray-600 text-xs mt-2">Título: 3-4 principais<br/>Competências: distribuídas</p>
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