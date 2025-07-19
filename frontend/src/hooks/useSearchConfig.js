import { useState, useCallback } from 'react';

// Configuração padrão garantida
const DEFAULT_SEARCH_CONFIG = {
  cargo: '',
  localizacao: '',
  quantidade: 100,
  segmentos: '',
  tipoVaga: 'todos',
  raio: '25',
  nivel: 'todos',
  tipoContrato: 'todos',
  diasPublicacao: 'todos',
  ordenar: 'date',
  modalidade: 'todos'
};

/**
 * Hook personalizado para gerenciar searchConfig de forma segura
 * Garante que nunca será undefined e todos os campos têm valores padrão
 */
export const useSearchConfig = () => {
  const [searchConfig, setSearchConfigState] = useState(DEFAULT_SEARCH_CONFIG);

  // Setter seguro que sempre mescla com valores padrão
  const setSearchConfig = useCallback((newConfig) => {
    if (typeof newConfig === 'function') {
      setSearchConfigState(prev => ({
        ...DEFAULT_SEARCH_CONFIG,
        ...prev,
        ...newConfig(prev)
      }));
    } else {
      setSearchConfigState(prev => ({
        ...DEFAULT_SEARCH_CONFIG,
        ...prev,
        ...newConfig
      }));
    }
  }, []);

  // Getters seguros para campos específicos
  const getSafeValue = useCallback((field) => {
    return searchConfig?.[field]?.toString().trim() || DEFAULT_SEARCH_CONFIG[field] || '';
  }, [searchConfig]);

  // Validações
  const isValid = useCallback(() => {
    const cargo = getSafeValue('cargo');
    const localizacao = getSafeValue('localizacao');
    return cargo.length > 0 && localizacao.length > 0;
  }, [getSafeValue]);

  // Dados preparados para API (sempre seguros)
  const getApiData = useCallback(() => {
    return {
      cargo_objetivo: getSafeValue('cargo'),
      area_interesse: getSafeValue('cargo'), // Usar cargo como área
      localizacao: getSafeValue('localizacao'),
      total_vagas_desejadas: searchConfig?.quantidade || 100,
      segmentos_alvo: getSafeValue('segmentos') ? 
        getSafeValue('segmentos').split(',').map(s => s.trim()).filter(s => s.length > 0) : [],
      tipo_vaga: searchConfig?.tipoVaga || 'todos',
      raio: searchConfig?.raio || '25',
      nivel: searchConfig?.nivel || 'todos',
      tipoContrato: searchConfig?.tipoContrato || 'todos',
      diasPublicacao: searchConfig?.diasPublicacao || 'todos',
      ordenar: searchConfig?.ordenar || 'date',
      modalidade: searchConfig?.modalidade || 'todos'
    };
  }, [searchConfig, getSafeValue]);

  return {
    searchConfig: { ...DEFAULT_SEARCH_CONFIG, ...searchConfig },
    setSearchConfig,
    getSafeValue,
    isValid,
    getApiData,
    DEFAULT_SEARCH_CONFIG
  };
};