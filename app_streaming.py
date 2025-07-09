#!/usr/bin/env python3
"""
HELIO API STREAMING - Versão Simplificada e Corrigida
"""
import os
import sys
import json
import time
import logging
from datetime import datetime
from flask import Flask, request, Response, jsonify
from flask_cors import CORS, cross_origin

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Adicionar path para os módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Tentar importar os scrapers
try:
    from core.services.job_scraper import JobScraper
    from core.services.linkedin_apify_scraper import LinkedInApifyScraper
    logger.info("✅ Scrapers importados com sucesso")
except ImportError as e:
    logger.warning(f"⚠️ Erro ao importar scrapers: {e}")
    JobScraper = None
    LinkedInApifyScraper = None

app = Flask(__name__)

# CORS para Vercel
CORS(app, 
     origins=[
         'https://agenteslinkedin.vercel.app',
         'http://localhost:3000',
         'http://localhost:3001'
     ], 
     allow_headers=['Content-Type', 'Authorization'], 
     methods=['GET', 'POST', 'OPTIONS'])

@app.route('/api/health', methods=['GET'])
@cross_origin()
def health():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'service': 'helio-streaming-api',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/agent1/collect-jobs-stream', methods=['POST', 'OPTIONS'])
@cross_origin()
def collect_jobs_stream():
    """Endpoint de streaming de coleta de vagas"""
    
    if request.method == 'OPTIONS':
        return '', 200
    
    def generate_stream():
        try:
            # Obter dados da requisição
            data = request.get_json()
            if not data:
                yield f"data: {json.dumps({'error': 'Dados não fornecidos'})}\n\n"
                return
            
            cargo = data.get('cargo_objetivo', 'Desenvolvedor')
            area = data.get('area_interesse', 'Tecnologia')
            localizacao = data.get('localizacao', 'São Paulo')
            quantidade = data.get('total_vagas_desejadas', 20)
            
            # Enviar confirmação inicial
            yield f"data: {json.dumps({'status': 'iniciando', 'message': f'Iniciando coleta para {cargo}...', 'timestamp': datetime.now().isoformat()})}\n\n"
            
            # Verificar token APIFY
            apify_token = os.getenv('APIFY_API_TOKEN')
            if not apify_token:
                yield f"data: {json.dumps({'error': 'APIFY_API_TOKEN não configurado', 'timestamp': datetime.now().isoformat()})}\n\n"
                return
            
            yield f"data: {json.dumps({'status': 'config_ok', 'message': 'Configuração verificada', 'timestamp': datetime.now().isoformat()})}\n\n"
            
            # Verificar se os scrapers estão disponíveis
            if JobScraper and LinkedInApifyScraper:
                logger.info("Usando APIFY real")
                job_scraper = JobScraper()
                linkedin_scraper = LinkedInApifyScraper()
                
                # Verificar credenciais
                if not linkedin_scraper.verificar_credenciais():
                    yield f"data: {json.dumps({'error': 'Credenciais APIFY inválidas', 'timestamp': datetime.now().isoformat()})}\n\n"
                    return
                
                yield f"data: {json.dumps({'status': 'scrapers_ok', 'message': 'Scrapers inicializados', 'timestamp': datetime.now().isoformat()})}\n\n"
                
                # Iniciar coleta
                try:
                    run_id, dataset_id = job_scraper.iniciar_coleta_streaming(
                        area_interesse=area,
                        cargo_objetivo=cargo,
                        localizacao=localizacao,
                        total_vagas_desejadas=quantidade
                    )
                    
                    yield f"data: {json.dumps({'status': 'coleta_iniciada', 'run_id': run_id, 'dataset_id': dataset_id, 'timestamp': datetime.now().isoformat()})}\n\n"
                    
                    # Polling com timeout
                    vagas_coletadas = []
                    tempo_inicio = time.time()
                    timeout_segundos = 420  # 7 minutos
                    
                    while True:
                        tempo_decorrido = time.time() - tempo_inicio
                        
                        if tempo_decorrido > timeout_segundos:
                            yield f"data: {json.dumps({'status': 'timeout', 'message': 'Timeout - finalizando', 'timestamp': datetime.now().isoformat()})}\n\n"
                            break
                        
                        # Verificar status
                        status_run = job_scraper.verificar_status_run(run_id)
                        yield f"data: {json.dumps({'status': 'monitorando', 'run_status': status_run, 'timestamp': datetime.now().isoformat()})}\n\n"
                        
                        # Contar resultados
                        total_resultados = job_scraper.contar_resultados_dataset(dataset_id)
                        
                        if total_resultados > len(vagas_coletadas):
                            novos_resultados = job_scraper.obter_resultados_parciais(dataset_id, len(vagas_coletadas), total_resultados - len(vagas_coletadas))
                            
                            if novos_resultados:
                                vagas_coletadas.extend(novos_resultados)
                                yield f"data: {json.dumps({'type': 'novas_vagas', 'novas_vagas': novos_resultados, 'total_atual': len(vagas_coletadas), 'timestamp': datetime.now().isoformat()})}\n\n"
                        
                        if status_run in ['SUCCEEDED', 'FAILED', 'ABORTED', 'TIMED-OUT']:
                            break
                        
                        time.sleep(10)
                    
                    # Finalizar
                    yield f"data: {json.dumps({'status': 'concluido', 'total_vagas': len(vagas_coletadas), 'timestamp': datetime.now().isoformat()})}\n\n"
                    yield f"data: {json.dumps({'status': 'finalizado', 'vagas': vagas_coletadas, 'timestamp': datetime.now().isoformat()})}\n\n"
                    
                except Exception as e:
                    yield f"data: {json.dumps({'error': f'Erro durante coleta: {str(e)}', 'timestamp': datetime.now().isoformat()})}\n\n"
            
            else:
                # Modo demonstração
                logger.warning("Usando modo demonstração")
                yield f"data: {json.dumps({'status': 'modo_demo', 'message': 'Sistema em modo demonstração', 'timestamp': datetime.now().isoformat()})}\n\n"
                
                vagas_demo = []
                for i in range(1, min(quantidade + 1, 11)):
                    vaga = {
                        'id': i,
                        'titulo': f'{cargo} - Posição {i}',
                        'empresa': f'Empresa Tech {i}',
                        'localizacao': localizacao,
                        'descricao': f'Vaga para {cargo} com experiência em tecnologias modernas.',
                        'link': f'https://linkedin.com/jobs/view/{1000000 + i}'
                    }
                    vagas_demo.append(vaga)
                    
                    yield f"data: {json.dumps({'type': 'nova_vaga', 'vaga': vaga, 'total_atual': i, 'timestamp': datetime.now().isoformat()})}\n\n"
                    time.sleep(0.5)
                
                yield f"data: {json.dumps({'status': 'concluido', 'total_vagas': len(vagas_demo), 'timestamp': datetime.now().isoformat()})}\n\n"
                yield f"data: {json.dumps({'status': 'finalizado', 'vagas': vagas_demo, 'timestamp': datetime.now().isoformat()})}\n\n"
            
        except Exception as e:
            logger.error(f"Erro crítico: {e}")
            yield f"data: {json.dumps({'error': f'Erro crítico: {str(e)}', 'timestamp': datetime.now().isoformat()})}\n\n"
    
    return Response(
        generate_stream(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Iniciando HELIO Streaming API na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=False) 