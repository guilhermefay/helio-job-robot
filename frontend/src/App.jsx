import React, { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom'
import { 
  HomeIcon, 
  ChevronLeftIcon,
  SparklesIcon,
  UserGroupIcon
} from '@heroicons/react/24/outline'

// Components
import AgentCard from './components/AgentCard'

// Pages
import Agent0 from './pages/Agent0'
import Agent1 from './pages/Agent1'

// Data
import { agents, getActiveAgents, getComingSoonAgents } from './data/agents'

// Header Component
const Header = ({ showBackButton = false, title = null }) => {
  const navigate = useNavigate()

  return (
    <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Left Side */}
          <div className="flex items-center space-x-4">
            {showBackButton && (
              <button
                onClick={() => navigate('/')}
                className="flex items-center text-gray-600 hover:text-gray-900 transition-colors"
              >
                <ChevronLeftIcon className="w-5 h-5 mr-1" />
                <span className="text-sm font-medium">Voltar</span>
              </button>
            )}
            
            <div className="flex items-center space-x-3">
              <div className="flex items-center justify-center w-8 h-8 bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg">
                <SparklesIcon className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">
                  {title || 'HELIO - Jornada IA'}
                </h1>
                {!title && (
                  <p className="text-sm text-gray-600">
                    Sua jornada rumo ao próximo emprego começa aqui
                  </p>
                )}
              </div>
            </div>
          </div>

          {/* Right Side */}
          <div className="flex items-center space-x-4">
            <div className="hidden sm:flex items-center space-x-2 text-sm text-gray-600">
              <UserGroupIcon className="w-4 h-4" />
              <span>Metodologia Carolina Martins</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

// Dashboard Component
const Dashboard = () => {
  const navigate = useNavigate()
  const activeAgents = getActiveAgents()
  const comingSoonAgents = getComingSoonAgents()

  const handleAgentSelect = (agent) => {
    navigate(agent.route)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            5 Agentes Autônomos para sua Carreira
          </h2>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Sistema completo baseado na metodologia "Carreira Meteórica" da Carolina Martins. 
            Cada agente executa uma etapa específica para acelerar sua recolocação profissional.
          </p>
        </div>

        {/* Active Agents Section */}
        <section className="mb-12">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-2xl font-semibold text-gray-900">
              Agentes Disponíveis
            </h3>
            <div className="flex items-center space-x-2 text-sm text-green-600">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span>Prontos para uso</span>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {activeAgents.map((agent) => (
              <AgentCard
                key={agent.id}
                agent={agent}
                onSelect={handleAgentSelect}
                className="h-full"
              />
            ))}
          </div>
        </section>

        {/* Coming Soon Section */}
        <section>
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-2xl font-semibold text-gray-900">
              Próximos Agentes
            </h3>
            <div className="flex items-center space-x-2 text-sm text-gray-500">
              <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
              <span>Em desenvolvimento</span>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {comingSoonAgents.map((agent) => (
              <AgentCard
                key={agent.id}
                agent={agent}
                className="h-full"
              />
            ))}
          </div>
        </section>

        {/* Info Section */}
        <section className="mt-16 bg-blue-50 rounded-2xl p-8">
          <div className="text-center">
            <h3 className="text-xl font-semibold text-blue-900 mb-3">
              Metodologia Validada
            </h3>
            <p className="text-blue-700 mb-4 max-w-2xl mx-auto">
              Sistema baseado na metodologia "Carreira Meteórica" da Carolina Martins, 
              validada por mais de 13.000 alunos e reconhecida como referência em recolocação profissional.
            </p>
            <div className="flex flex-wrap justify-center gap-4 text-sm text-blue-600">
              <span className="bg-white px-3 py-1 rounded-full">✓ 13 Passos do Currículo</span>
              <span className="bg-white px-3 py-1 rounded-full">✓ 10 Passos do LinkedIn</span>
              <span className="bg-white px-3 py-1 rounded-full">✓ MPC (Mapa de Palavras-chave)</span>
              <span className="bg-white px-3 py-1 rounded-full">✓ Identificação de Sabotadores</span>
            </div>
          </div>
        </section>
      </main>
    </div>
  )
}

// Main App Component
const App = () => {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/agent0" element={<Agent0 />} />
          <Route path="/agent1" element={<Agent1 />} />
          
          {/* Placeholder routes for coming soon agents */}
          <Route path="/agent2" element={
            <div className="min-h-screen bg-gray-50">
              <Header showBackButton title="Agente 2 - Currículo" />
              <div className="max-w-4xl mx-auto px-4 py-16 text-center">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Em Desenvolvimento</h2>
                <p className="text-gray-600">Este agente está sendo implementado.</p>
              </div>
            </div>
          } />
          
          <Route path="/agent3" element={
            <div className="min-h-screen bg-gray-50">
              <Header showBackButton title="Agente 3 - LinkedIn" />
              <div className="max-w-4xl mx-auto px-4 py-16 text-center">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Em Desenvolvimento</h2>
                <p className="text-gray-600">Este agente está sendo implementado.</p>
              </div>
            </div>
          } />
          
          <Route path="/agent4" element={
            <div className="min-h-screen bg-gray-50">
              <Header showBackButton title="Agente 4 - Conteúdo" />
              <div className="max-w-4xl mx-auto px-4 py-16 text-center">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Em Desenvolvimento</h2>
                <p className="text-gray-600">Este agente está sendo implementado.</p>
              </div>
            </div>
          } />
        </Routes>
      </div>
    </Router>
  )
}

export default App