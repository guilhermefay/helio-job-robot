import React, { useState } from 'react';
import { MOCK_COLLECTION_DATA, MOCK_SEARCH_CONFIG } from '../utils/mockData';

const DebugPanel = ({ 
  onLoadMockData, 
  onTestAnalysis, 
  searchConfig, 
  collectionData, 
  isAnalyzing 
}) => {
  const [showDebug, setShowDebug] = useState(false);
  const [testLog, setTestLog] = useState([]);

  const addLog = (message, type = 'info') => {
    const timestamp = new Date().toLocaleTimeString();
    setTestLog(prev => [...prev, { message, type, timestamp }]);
  };

  const testSearchConfigSafety = () => {
    addLog('🧪 Testando segurança do searchConfig...', 'info');
    
    try {
      // Teste 1: searchConfig undefined
      const undefinedConfig = undefined;
      const result1 = undefinedConfig?.cargo?.trim() || 'SEGURO';
      addLog(`✅ Teste 1 (undefined): ${result1}`, 'success');
      
      // Teste 2: searchConfig sem cargo
      const partialConfig = { localizacao: 'SP' };
      const result2 = partialConfig?.cargo?.trim() || 'SEGURO';
      addLog(`✅ Teste 2 (sem cargo): ${result2}`, 'success');
      
      // Teste 3: cargo null
      const nullCargoConfig = { cargo: null };
      const result3 = nullCargoConfig?.cargo?.trim() || 'SEGURO';
      addLog(`✅ Teste 3 (cargo null): ${result3}`, 'success');
      
      // Teste 4: cargo string vazia
      const emptyCargoConfig = { cargo: '' };
      const result4 = emptyCargoConfig?.cargo?.trim() || 'SEGURO';
      addLog(`✅ Teste 4 (cargo vazio): ${result4}`, 'success');
      
      // Teste 5: cargo normal
      const normalConfig = { cargo: '  Desenvolvedor  ' };
      const result5 = normalConfig?.cargo?.trim() || 'SEGURO';
      addLog(`✅ Teste 5 (normal): "${result5}"`, 'success');
      
      addLog('🎉 Todos os testes de segurança passaram!', 'success');
      
    } catch (error) {
      addLog(`❌ Erro nos testes: ${error.message}`, 'error');
    }
  };

  const testAnalysisWithMockData = async () => {
    addLog('🚀 Iniciando teste de análise com dados mock...', 'info');
    
    // Carregar dados mock
    onLoadMockData(MOCK_COLLECTION_DATA, MOCK_SEARCH_CONFIG);
    addLog('📦 Dados mock carregados', 'success');
    
    // Aguardar um pouco para o estado atualizar
    setTimeout(() => {
      addLog('🔍 Iniciando análise...', 'info');
      onTestAnalysis();
    }, 1000);
  };

  const clearLog = () => {
    setTestLog([]);
  };

  if (!showDebug) {
    return (
      <div className="fixed bottom-4 right-4 z-50">
        <button
          onClick={() => setShowDebug(true)}
          className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg shadow-lg text-sm font-medium"
        >
          🔧 Debug
        </button>
      </div>
    );
  }

  return (
    <div className="fixed bottom-4 right-4 z-50 bg-white border border-gray-300 rounded-lg shadow-xl w-96 max-h-96 overflow-hidden">
      <div className="bg-gray-100 px-4 py-2 border-b flex justify-between items-center">
        <h3 className="font-medium text-gray-900">🔧 Painel de Debug</h3>
        <button
          onClick={() => setShowDebug(false)}
          className="text-gray-500 hover:text-gray-700"
        >
          ✕
        </button>
      </div>
      
      <div className="p-4 space-y-3">
        {/* Botões de teste */}
        <div className="grid grid-cols-1 gap-2">
          <button
            onClick={testSearchConfigSafety}
            className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded text-sm"
          >
            🧪 Testar Segurança
          </button>
          
          <button
            onClick={testAnalysisWithMockData}
            disabled={isAnalyzing}
            className="bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white px-3 py-2 rounded text-sm"
          >
            {isAnalyzing ? '⏳ Analisando...' : '🚀 Teste Rápido Análise'}
          </button>
          
          <button
            onClick={() => onLoadMockData(MOCK_COLLECTION_DATA, MOCK_SEARCH_CONFIG)}
            className="bg-purple-600 hover:bg-purple-700 text-white px-3 py-2 rounded text-sm"
          >
            📦 Carregar Mock
          </button>
        </div>
        
        {/* Estado atual */}
        <div className="text-xs bg-gray-50 p-2 rounded">
          <div><strong>SearchConfig:</strong> {searchConfig ? '✅' : '❌'}</div>
          <div><strong>Cargo:</strong> "{searchConfig?.cargo || 'undefined'}"</div>
          <div><strong>CollectionData:</strong> {collectionData ? '✅' : '❌'}</div>
          <div><strong>Vagas:</strong> {collectionData?.vagas?.length || 0}</div>
        </div>
        
        {/* Log */}
        <div className="border-t pt-2">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium">Log:</span>
            <button
              onClick={clearLog}
              className="text-xs text-gray-500 hover:text-gray-700"
            >
              Limpar
            </button>
          </div>
          
          <div className="bg-black text-green-400 p-2 rounded text-xs max-h-32 overflow-y-auto font-mono">
            {testLog.length === 0 ? (
              <div className="text-gray-500">Nenhum teste executado</div>
            ) : (
              testLog.map((log, index) => (
                <div key={index} className={`
                  ${log.type === 'error' ? 'text-red-400' : ''}
                  ${log.type === 'success' ? 'text-green-400' : ''}
                  ${log.type === 'info' ? 'text-blue-400' : ''}
                `}>
                  [{log.timestamp}] {log.message}
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DebugPanel;