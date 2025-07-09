// Theme configuration - HELIO System
// Baseado nas cores do LinkedIn com adaptações para acessibilidade

export const theme = {
  colors: {
    // Cores principais do LinkedIn
    primary: {
      50: '#E8F4FD',
      100: '#D1E9FB',
      200: '#A3D3F7',
      300: '#75BDF3',
      400: '#47A7EF',
      500: '#0077B5', // Azul principal LinkedIn
      600: '#005885',
      700: '#004268',
      800: '#002C4A',
      900: '#00162D'
    },
    
    // Tons de cinza
    gray: {
      50: '#F3F6F9',  // Fundo principal
      100: '#E5E9ED',
      200: '#D4DCE5',
      300: '#9AA5B1',
      400: '#6B7684',
      500: '#4B5563',
      600: '#374151',
      700: '#1F2937',
      800: '#111827',
      900: '#1D1D1F'   // Texto principal
    },
    
    // Cores de status
    success: {
      50: '#ECFDF5',
      500: '#10B981',
      600: '#059669'
    },
    
    warning: {
      50: '#FFFBEB',
      500: '#F59E0B',
      600: '#D97706'
    },
    
    error: {
      50: '#FEF2F2',
      500: '#EF4444',
      600: '#DC2626'
    },
    
    // Cores especiais
    accent: {
      blue: '#0077B5',
      lightBlue: '#E8F4FD',
      darkBlue: '#004268'
    }
  },
  
  spacing: {
    xs: '0.5rem',
    sm: '1rem',
    md: '1.5rem',
    lg: '2rem',
    xl: '3rem',
    xxl: '4rem'
  },
  
  borderRadius: {
    sm: '0.375rem',
    md: '0.5rem',
    lg: '0.75rem',
    xl: '1rem'
  },
  
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)'
  },
  
  typography: {
    fontFamily: {
      sans: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'],
      mono: ['SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'Liberation Mono', 'Courier New', 'monospace']
    },
    
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      lg: '1.125rem',
      xl: '1.25rem',
      '2xl': '1.5rem',
      '3xl': '1.875rem',
      '4xl': '2.25rem'
    },
    
    fontWeight: {
      normal: '400',
      medium: '500',
      semibold: '600',
      bold: '700'
    }
  },
  
  animation: {
    duration: {
      fast: '150ms',
      normal: '300ms',
      slow: '500ms'
    },
    
    easing: {
      default: 'cubic-bezier(0.4, 0, 0.2, 1)',
      in: 'cubic-bezier(0.4, 0, 1, 1)',
      out: 'cubic-bezier(0, 0, 0.2, 1)',
      inOut: 'cubic-bezier(0.4, 0, 0.2, 1)'
    }
  }
}

// Utility functions
export const getStatusColor = (status) => {
  switch (status) {
    case 'ativo':
      return theme.colors.success[500]
    case 'em_breve':
      return theme.colors.gray[400]
    case 'processando':
      return theme.colors.primary[500]
    case 'erro':
      return theme.colors.error[500]
    default:
      return theme.colors.gray[400]
  }
}

export const getStatusBgColor = (status) => {
  switch (status) {
    case 'ativo':
      return theme.colors.success[50]
    case 'em_breve':
      return theme.colors.gray[50]
    case 'processando':
      return theme.colors.primary[50]
    case 'erro':
      return theme.colors.error[50]
    default:
      return theme.colors.gray[50]
  }
}