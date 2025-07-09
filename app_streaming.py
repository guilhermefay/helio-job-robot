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
from flask_cors import CORS

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

# CORS para Vercel - configuração completa
CORS(app, 
     resources={
         r"/api/*": {
             "origins": [
                 'https://agenteslinkedin.vercel.app',
                 'https://helio-job-robot.vercel.app', 
                 'https://helio-job-robot-*.vercel.app',
                 'http://localhost:3000',
                 'http://localhost:3001'
             ],
             "methods": ['GET', 'POST', 'OPTIONS', 'PUT', 'DELETE'],
             "allow_headers": ['Content-Type', 'Authorization'],
             "supports_credentials": True
         }
     })

@app.after_request
def after_request(response):
    """Ensure CORS headers are always sent"""
    origin = request.headers.get('Origin')
    if origin:
        logger.info(f"🌐 CORS Debug - Origin: {origin}, Method: {request.method}, Path: {request.path}")
        # Explicitly set CORS headers for known origins
        allowed_origins = [
            'https://agenteslinkedin.vercel.app',
            'https://helio-job-robot.vercel.app',
            'http://localhost:3000',
            'http://localhost:3001'
        ]
        if origin in allowed_origins:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'service': 'helio-job-robot',
        'status': 'running',
        'endpoints': [
            '/api/health',
            '/api/agent1/collect-keywords',
            '/api/agent1/collect-jobs-stream'
        ]
    })

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    apify_token = os.environ.get('APIFY_API_TOKEN')
    apify_status = "configurado" if apify_token else "não configurado"
    
    return jsonify({
        'status': 'ok',
        'service': 'helio-streaming-api',
        'timestamp': datetime.now().isoformat(),
        'versao': '4.0-simplificada',
        'apify_status': apify_status
    })

@app.route('/api/agent1/collect-keywords', methods=['POST', 'OPTIONS'])
def collect_keywords():
    """Endpoint principal para coleta de vagas - compatível com frontend"""
    
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
        
        # Verificar se os scrapers estão disponíveis
        if JobScraper and LinkedInApifyScraper:
            # Instanciar scraper APIFY
            scraper = LinkedInApifyScraper()
            
            # Executar coleta
            logger.info("🚀 Iniciando scraping com APIFY...")
            resultado_scraping = scraper.coletar_vagas(
                cargo=cargo,
                localizacao=localizacao,
                total_vagas=quantidade
            )
            
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
        
        else:
            # Fallback para modo demonstração
            logger.warning("⚠️ Scrapers não disponíveis - usando modo demonstração")
            
            # Simular coleta
            vagas_demo = []
            for i in range(1, min(quantidade + 1, 51)):
                vaga = {
                    'id': i,
                    'titulo': f'{cargo} - Posição {i}',
                    'empresa': f'Empresa Tech {i}',
                    'localizacao': localizacao,
                    'descricao': f'Vaga para {cargo} com experiência em tecnologias modernas.',
                    'link': f'https://linkedin.com/jobs/view/{1000000 + i}',
                    'nivel': 'Pleno' if i % 3 == 0 else 'Júnior',
                    'tipo': 'Híbrido' if i % 2 == 0 else 'Remoto'
                }
                vagas_demo.append(vaga)
            
            # Montar resposta demo
            resultado = {
                'demo_mode': True,
                'fallback_local': True,
                'id': f'local_{int(time.time())}',
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
                    'tempoColeta': '5 segundos (simulado)'
                },
                'transparencia': {
                    'fontes_utilizadas': ['Dados simulados'],
                    'metodo_coleta': 'Geração automática para demonstração',
                    'filtros_aplicados': f'Cargo: {cargo}, Localização: {localizacao}',
                    'observacoes': 'Dados simulados para demonstração do sistema'
                },
                'vagas': vagas_demo
            }
            
            logger.info(f"✅ Demo finalizada: {len(vagas_demo)} vagas simuladas")
            return jsonify(resultado)
        
    except Exception as e:
        logger.error(f"❌ Erro na coleta: {e}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'error': 'Erro na coleta',
            'message': str(e),
            'demo_mode': False
        }), 500

@app.route('/api/agent1/collect-jobs-stream', methods=['POST', 'OPTIONS'])
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
    logger.info(f"🚀 Iniciando HELIO Streaming API na porta {port}")
    logger.info(f"📍 Ambiente: {'Railway' if os.environ.get('RAILWAY_ENVIRONMENT') else 'Local'}")
    logger.info(f"🔑 APIFY_API_TOKEN: {'Configurado' if os.environ.get('APIFY_API_TOKEN') else 'Não configurado'}")
    
    try:
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar aplicação: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 