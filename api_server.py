#!/usr/bin/env python3
"""
API HELIO - Streaming de Coleta de Vagas com LOGS DETALHADOS
Versão simplificada para Railway - sempre modo demo
"""
import os
import sys
import json
import time
import logging
from datetime import datetime
from flask import Flask, request, Response, jsonify
from flask_cors import CORS, cross_origin

# Configurar logging detalhado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuração CORS mais abrangente para Vercel e desenvolvimento
CORS(app, 
     origins=[
         'https://agenteslinkedin.vercel.app',
         'https://helio-job-robot.vercel.app', 
         'https://helio-job-robot-*.vercel.app',  # Domínios de preview do Vercel
         'http://localhost:3000',
         'http://localhost:3001'
     ], 
     allow_headers=['Content-Type', 'Authorization'], 
     methods=['GET', 'POST', 'OPTIONS', 'PUT', 'DELETE'],
     supports_credentials=True)

@app.after_request
def after_request(response):
    """Adiciona headers CORS em todas as respostas"""
    origin = request.headers.get('Origin')
    allowed_origins = [
        'https://agenteslinkedin.vercel.app',
        'https://helio-job-robot.vercel.app',
        'http://localhost:3000',
        'http://localhost:3001'
    ]
    
    # Log para debug do CORS
    logger.info(f"🌐 CORS Debug - Origin: {origin}")
    
    # Verificar origem exata ou padrão do Vercel
    if origin in allowed_origins or (origin and 'helio-job-robot' in origin and 'vercel.app' in origin):
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        logger.info(f"✅ CORS permitido para origem: {origin}")
    else:
        logger.warning(f"❌ CORS negado para origem: {origin}")
    
    return response

@app.route('/api/health', methods=['GET'])
@cross_origin()
def health():
    """Health check simplificado"""
    
    sistema_status = {
        'status': 'ok',
        'service': 'helio-demo-api',
        'timestamp': datetime.now().isoformat(),
        'versao': '3.0-demo-only',
        'modo': 'demo-always',
        'port': os.environ.get('PORT', '5000')
    }
    
    logger.info(f"🏥 Health check OK - {sistema_status}")
    return jsonify(sistema_status)

def gerar_vagas_demo(cargo, localizacao, quantidade):
    """Gera vagas de demonstração"""
    vagas_demo = []
    for i in range(1, min(quantidade + 1, 101)):  # Máximo 100 vagas demo
        vaga = {
            'id': i,
            'titulo': f'{cargo} - Posição {i}',
            'empresa': f'Empresa Tech {i}',
            'localizacao': localizacao,
            'descricao': f'Vaga para {cargo} com experiência em tecnologias modernas. Oportunidade em empresa inovadora.',
            'link': f'https://linkedin.com/jobs/view/{1000000 + i}',
            'nivel': 'Pleno' if i % 3 == 0 else 'Júnior',
            'tipo': 'Híbrido' if i % 2 == 0 else 'Remoto',
            'salario': f'R$ {4000 + (i * 100)},00' if i % 4 == 0 else '',
            'data_publicacao': '2 dias atrás'
        }
        vagas_demo.append(vaga)
    
    return vagas_demo

@app.route('/api/agent1/collect-keywords', methods=['POST', 'OPTIONS'])
@cross_origin()
def collect_keywords():
    """
    🎯 ENDPOINT DEMO PARA COLETA DE VAGAS E EXTRAÇÃO DE PALAVRAS-CHAVE
    Sempre funciona em modo demonstração
    """
    
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        logger.info("🎯 Iniciando coleta DEMO de vagas e análise de palavras-chave")
        
        # Capturar dados da requisição
        data = request.get_json()
        if not data:
            logger.error("❌ Dados não fornecidos na requisição")
            return jsonify({'error': 'Dados não fornecidos na requisição'}), 400
        
        # Extrair parâmetros
        cargo = data.get('cargo_objetivo', 'Desenvolvedor')
        area = data.get('area_interesse', 'Tecnologia')
        localizacao = data.get('localizacao', 'São Paulo')
        quantidade = data.get('total_vagas_desejadas', 20)
        
        logger.info(f"📋 Parâmetros recebidos: cargo={cargo}, área={area}, local={localizacao}, qtd={quantidade}")
        
        # Simular tempo de processamento
        time.sleep(2)
        
        # Gerar vagas demo
        vagas_demo = gerar_vagas_demo(cargo, localizacao, quantidade)
        
        # Montar resposta
        resultado = {
            'demo_mode': True,
            'id': f'demo_{int(time.time())}',
            'timestamp': datetime.now().isoformat(),
            'parametros': {
                'area_interesse': area,
                'cargo_objetivo': cargo,
                'localizacao': localizacao,
                'total_vagas_desejadas': quantidade
            },
            'estatisticas': {
                'totalVagas': len(vagas_demo),
                'vagasAnalisadas': len(vagas_demo),
                'successRate': 100,
                'tempoColeta': 'Demo instantâneo'
            },
            'transparencia': {
                'fontes_utilizadas': ['Demo'],
                'metodo_coleta': 'Dados de demonstração',
                'filtros_aplicados': f'Cargo: {cargo}, Localização: {localizacao}',
                'observacoes': 'Este é um modo de demonstração. Configure APIFY_API_TOKEN para coleta real.'
            },
            'vagas': vagas_demo
        }
        
        logger.info(f"✅ Resposta demo criada: {len(vagas_demo)} vagas")
        return jsonify(resultado)
        
    except Exception as e:
        logger.error(f"❌ Erro no endpoint demo: {e}")
        return jsonify({
            'error': 'Erro interno do servidor',
            'demo_mode': True,
            'message': str(e)
        }), 500

@app.route('/', methods=['GET'])
def root():
    """Endpoint raiz"""
    return jsonify({
        'service': 'HELIO Job Robot API',
        'status': 'online',
        'mode': 'demo',
        'endpoints': [
            '/api/health',
            '/api/agent1/collect-keywords'
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🚀 Iniciando HELIO Demo API na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=False) 