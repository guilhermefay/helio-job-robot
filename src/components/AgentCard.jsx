import React from 'react'
import { 
  UserCircleIcon, 
  MagnifyingGlassIcon, 
  DocumentTextIcon, 
  GlobeAltIcon, 
  PencilSquareIcon,
  CheckCircleIcon,
  ClockIcon,
  ArrowRightIcon
} from '@heroicons/react/24/outline'

// Mapeamento dos ícones
const iconMap = {
  UserCircleIcon,
  MagnifyingGlassIcon,
  DocumentTextIcon,
  GlobeAltIcon,
  PencilSquareIcon,
  CheckCircleIcon,
  ClockIcon
}

const colorVariants = {
  blue: {
    bg: 'bg-blue-50',
    border: 'border-blue-200',
    text: 'text-blue-700',
    button: 'bg-blue-600 hover:bg-blue-700 text-white',
    buttonDisabled: 'bg-gray-300 text-gray-500 cursor-not-allowed',
    icon: 'text-blue-600'
  },
  green: {
    bg: 'bg-green-50',
    border: 'border-green-200',
    text: 'text-green-700',
    button: 'bg-green-600 hover:bg-green-700 text-white',
    buttonDisabled: 'bg-gray-300 text-gray-500 cursor-not-allowed',
    icon: 'text-green-600'
  },
  purple: {
    bg: 'bg-purple-50',
    border: 'border-purple-200',
    text: 'text-purple-700',
    button: 'bg-purple-600 hover:bg-purple-700 text-white',
    buttonDisabled: 'bg-gray-300 text-gray-500 cursor-not-allowed',
    icon: 'text-purple-600'
  },
  orange: {
    bg: 'bg-orange-50',
    border: 'border-orange-200',
    text: 'text-orange-700',
    button: 'bg-orange-600 hover:bg-orange-700 text-white',
    buttonDisabled: 'bg-gray-300 text-gray-500 cursor-not-allowed',
    icon: 'text-orange-600'
  }
}

const AgentCard = ({ agent, onSelect, className = "" }) => {
  const IconComponent = iconMap[agent.icon] || UserCircleIcon
  const colors = colorVariants[agent.color] || colorVariants.blue
  const isActive = agent.status === 'ativo'
  const isComingSoon = agent.status === 'em_breve'

  const handleClick = () => {
    if (isActive && onSelect) {
      onSelect(agent)
    }
  }

  return (
    <div 
      className={`
        relative bg-white rounded-xl border-2 shadow-md transition-all duration-300 ease-in-out
        ${isActive ? 'hover:shadow-lg hover:-translate-y-1 cursor-pointer' : 'cursor-default'}
        ${isActive ? colors.border : 'border-gray-200'}
        ${className}
      `}
      onClick={handleClick}
    >
      {/* Status Badge */}
      <div className="absolute top-4 right-4">
        <div className={`
          inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium
          ${isActive ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'}
        `}>
          {isActive && <CheckCircleIcon className="w-3 h-3 mr-1" />}
          {isComingSoon && <ClockIcon className="w-3 h-3 mr-1" />}
          {isActive ? 'Ativo' : 'Em Breve'}
        </div>
      </div>

      {/* Card Content */}
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start space-x-4 mb-4">
          <div className={`
            flex-shrink-0 w-12 h-12 rounded-lg flex items-center justify-center
            ${isActive ? colors.bg : 'bg-gray-50'}
          `}>
            <IconComponent className={`
              w-6 h-6 
              ${isActive ? colors.icon : 'text-gray-400'}
            `} />
          </div>
          
          <div className="flex-1 min-w-0">
            <h3 className="text-lg font-semibold text-gray-900 mb-1">
              {agent.name}
            </h3>
            <p className="text-sm text-gray-600 line-clamp-2">
              {agent.shortDesc}
            </p>
          </div>
        </div>

        {/* Description */}
        <p className="text-sm text-gray-700 mb-4 line-clamp-3">
          {agent.description}
        </p>

        {/* Features Preview */}
        <div className="mb-4">
          <h4 className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">
            Principais recursos:
          </h4>
          <div className="space-y-1">
            {agent.features?.slice(0, 3).map((feature, index) => (
              <div key={index} className="flex items-center text-xs text-gray-600">
                <div className="w-1 h-1 bg-gray-400 rounded-full mr-2 flex-shrink-0" />
                <span className="line-clamp-1">{feature}</span>
              </div>
            ))}
            {agent.features?.length > 3 && (
              <div className="text-xs text-gray-500">
                +{agent.features.length - 3} recursos adicionais
              </div>
            )}
          </div>
        </div>

        {/* Metadata */}
        <div className="flex items-center justify-between text-xs text-gray-500 mb-4">
          <span>⏱️ {agent.estimatedTime || 'N/A'}</span>
          <span>📋 {agent.methodology ? agent.methodology.split(' ')[0] + '...' : 'Metodologia'}</span>
        </div>

        {/* Action Button */}
        <div className="pt-2">
          {isActive ? (
            <button
              className={`
                w-full flex items-center justify-center px-4 py-2.5 rounded-lg
                text-sm font-medium transition-colors duration-200
                focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500
                ${colors.button}
              `}
              onClick={handleClick}
            >
              <span>Executar Agente</span>
              <ArrowRightIcon className="w-4 h-4 ml-2" />
            </button>
          ) : (
            <div className="space-y-2">
              <button
                disabled
                className={`
                  w-full flex items-center justify-center px-4 py-2.5 rounded-lg
                  text-sm font-medium transition-colors duration-200
                  ${colors.buttonDisabled}
                `}
              >
                <ClockIcon className="w-4 h-4 mr-2" />
                <span>Em Desenvolvimento</span>
              </button>
              {agent.comingSoonMessage && (
                <p className="text-xs text-gray-500 text-center px-2">
                  {agent.comingSoonMessage}
                </p>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Hover Effect for Active Cards */}
      {isActive && (
        <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-blue-500/5 to-transparent opacity-0 hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
      )}
    </div>
  )
}

export default AgentCard