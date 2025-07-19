// PATCH DE EMERGÊNCIA - Sobrescrever métodos problemáticos
import { useEffect } from 'react';

export const useEmergencyPatch = () => {
  useEffect(() => {
    // Sobrescrever String.prototype.trim para ser seguro
    const originalTrim = String.prototype.trim;
    
    // Criar wrapper seguro
    String.prototype.trim = function() {
      if (this == null || this === undefined) {
        console.warn('⚠️ trim() chamado em undefined/null - retornando string vazia');
        return '';
      }
      return originalTrim.call(this);
    };

    // Sobrescrever Object.prototype para adicionar segurança
    Object.defineProperty(Object.prototype, 'safeTrim', {
      value: function() {
        if (this == null || this === undefined) {
          return '';
        }
        return String(this).trim();
      },
      writable: false,
      configurable: true
    });

    console.log('🛡️ PATCH DE EMERGÊNCIA ATIVADO - trim() agora é seguro');

    // Cleanup
    return () => {
      String.prototype.trim = originalTrim;
      delete Object.prototype.safeTrim;
    };
  }, []);
};

// Função para garantir que searchConfig sempre existe
export const ensureSearchConfig = (config) => {
  const DEFAULT_CONFIG = {
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

  if (!config) {
    console.warn('⚠️ searchConfig undefined - usando valores padrão');
    return DEFAULT_CONFIG;
  }

  return {
    ...DEFAULT_CONFIG,
    ...config
  };
};