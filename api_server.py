#!/usr/bin/env python3
"""
API HELIO - Integração REAL com APIFY LinkedIn Scraper
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

# Adicionar path para os módulos do projeto
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Importar serviço Google Jobs via APIFY
from core.services.google_jobs_scraper import GoogleJobsScraper

app = Flask(__name__)

# Configuração CORS para Vercel
CORS(app, 
     origins=[
         'https://agenteslinkedin.vercel.app',
         'https://helio-job-robot.vercel.app', 
         'https://helio-job-robot-*.vercel.app',
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
    
    logger.info(f"🌐 CORS Debug - Origin: {origin}")
    
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
    """Health check com status do APIFY"""
    
    apify_token = os.environ.get('APIFY_API_TOKEN')
    apify_status = "configurado" if apify_token else "não configurado"
    
    sistema_status = {
        'status': 'ok',
        'service': 'helio-apify-api',
        'timestamp': datetime.now().isoformat(),
        'versao': '3.0-apify-real',
        'apify_status': apify_status,
        'port': os.environ.get('PORT', '5000')
    }
    
    logger.info(f"🏥 Health check OK - APIFY: {apify_status}")
    return jsonify(sistema_status)

@app.route('/api/agent1/collect-keywords', methods=['POST', 'OPTIONS'])
@cross_origin()
def collect_keywords():
    """
    🎯 ENDPOINT REAL PARA COLETA COM APIFY LINKEDIN SCRAPER
    """
    
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        logger.info("🎯 Iniciando coleta REAL com APIFY LinkedIn Scraper")
        
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
        
        logger.info(f"📋 Parâmetros: cargo={cargo}, área={area}, local={localizacao}, qtd={quantidade}")
        
        # Verificar token APIFY
        apify_token = os.environ.get('APIFY_API_TOKEN')
        if not apify_token:
            logger.error("❌ APIFY_API_TOKEN não configurado!")
            return jsonify({
                'error': 'APIFY_API_TOKEN não configurado',
                'message': 'Configure a variável de ambiente APIFY_API_TOKEN no Railway'
            }), 500
        
        # Instanciar scraper Google Jobs
        scraper = GoogleJobsScraper()
        
        # Executar coleta
        logger.info("🚀 Iniciando scraping com Google Jobs...")
        vagas = scraper.coletar_vagas_google(
            cargo=cargo,
            localizacao=localizacao,
            limite=quantidade
        )
        
        # Criar resultado no formato esperado
        resultado_scraping = {
            'vagas': vagas,
            'total_coletadas': len(vagas)
        }
        
        if not resultado_scraping or not resultado_scraping.get('vagas'):
            logger.error("❌ Nenhuma vaga coletada pelo APIFY")
            return jsonify({
                'error': 'Nenhuma vaga encontrada',
                'message': 'O APIFY não retornou vagas para os parâmetros informados'
            }), 404
        
        # Processar resultado
        vagas_processadas = resultado_scraping['vagas']
        total_vagas = len(vagas_processadas)
        
        # Montar resposta final
        resultado = {
            'apify_mode': True,
            'id': f'apify_{int(time.time())}',
            'timestamp': datetime.now().isoformat(),
            'parametros': {
                'area_interesse': area,
                'cargo_objetivo': cargo,
                'localizacao': localizacao,
                'total_vagas_desejadas': quantidade
            },
            'estatisticas': {
                'totalVagas': total_vagas,
                'vagasAnalisadas': total_vagas,
                'successRate': 100 if total_vagas > 0 else 0,
                'tempoColeta': resultado_scraping.get('tempo_execucao', 'N/A')
            },
            'transparencia': {
                'fontes_utilizadas': ['LinkedIn via APIFY'],
                'metodo_coleta': 'APIFY LinkedIn Jobs Scraper',
                'filtros_aplicados': f'Cargo: {cargo}, Localização: {localizacao}',
                'observacoes': 'Dados reais coletados do LinkedIn via APIFY API',
                'actor_id': resultado_scraping.get('actor_id', 'N/A'),
                'run_id': resultado_scraping.get('run_id', 'N/A')
            },
            'vagas': vagas_processadas
        }
        
        logger.info(f"✅ Coleta APIFY finalizada: {total_vagas} vagas")
        return jsonify(resultado)
        
    except Exception as e:
        logger.error(f"❌ Erro na coleta APIFY: {e}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'error': 'Erro na coleta APIFY',
            'message': str(e),
            'apify_mode': True
        }), 500

@app.route('/', methods=['GET'])
def root():
    """Endpoint raiz"""
    apify_token = os.environ.get('APIFY_API_TOKEN')
    apify_status = "✅ CONFIGURADO" if apify_token else "❌ NÃO CONFIGURADO"
    
    return jsonify({
        'service': 'HELIO Job Robot API',
        'status': 'online',
        'mode': 'APIFY REAL',
        'apify_status': apify_status,
        'endpoints': [
            '/api/health',
            '/api/agent1/collect-keywords'
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🚀 Iniciando HELIO APIFY API na porta {port}")
    logger.info(f"🔑 APIFY Token: {'✅ CONFIGURADO' if os.environ.get('APIFY_API_TOKEN') else '❌ NÃO CONFIGURADO'}")
    app.run(host='0.0.0.0', port=port, debug=False) 