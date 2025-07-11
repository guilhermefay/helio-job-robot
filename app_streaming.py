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
    from core.services.indeed_scraper import IndeedScraper
    logger.info("✅ Scrapers importados com sucesso")
except ImportError as e:
    logger.warning(f"⚠️ Erro ao importar scrapers: {e}")
    JobScraper = None
    IndeedScraper = None

app = Flask(__name__)

# CORS para Vercel - configuração completa
CORS(app, 
     resources={
         r"/api/*": {
             "origins": [
                 'https://agenteslinkedin.vercel.app',
                 'https://linekdinagent.vercel.app',  # Nova origem
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
            'https://linekdinagent.vercel.app',  # Nova origem
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
        'port': os.environ.get('PORT', 'not set'),
        'railway_env': os.environ.get('RAILWAY_ENVIRONMENT', 'not set'),
        'endpoints': [
            '/api/health',
            '/api/agent1/collect-keywords',
            '/api/agent1/collect-jobs-stream',
            '/api/agent1/analyze-keywords-stream'
        ]
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check for Railway"""
    return 'OK', 200

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
        quantidade = min(data.get('total_vagas_desejadas', 20), 100)  # Limitar a 100 para economizar
        
        # Extrair parâmetros avançados
        raio_km = int(data.get('raio', 25))
        nivel = data.get('nivel', 'todos')
        tipo_contrato = data.get('tipoContrato', 'todos')
        dias_publicacao = data.get('diasPublicacao', 'todos')
        ordenar = data.get('ordenar', 'date')
        modalidade = data.get('modalidade', 'todos')
        
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
        if JobScraper and IndeedScraper:
            # Instanciar scraper Indeed
            scraper = IndeedScraper()
            
            # Executar coleta
            logger.info("🚀 Iniciando scraping com Indeed...")
            logger.info(f"Token APIFY presente: {'Sim' if scraper.apify_token else 'Não'}")
            # Preparar parâmetros para o scraper
            kwargs = {
                'raio_km': raio_km
            }
            
            # Adicionar modalidade
            if modalidade == 'remote':
                kwargs['remoto'] = True
            
            # Adicionar nível se especificado
            if nivel != 'todos':
                kwargs['nivel'] = nivel
                
            # Adicionar tipo de contrato se especificado
            if tipo_contrato != 'todos':
                kwargs['tipo_vaga'] = tipo_contrato
                
            # Adicionar filtro de data se especificado
            if dias_publicacao != 'todos':
                kwargs['dias_publicacao'] = dias_publicacao
                
            # Adicionar ordenação
            kwargs['ordenar'] = ordenar
            
            resultado_scraping = scraper.coletar_vagas_indeed(
                cargo=cargo,
                localizacao=localizacao,
                limite=quantidade,
                **kwargs
            )
            
            if not resultado_scraping:
                logger.error("❌ Nenhuma vaga coletada pelo Indeed")
                return jsonify({
                    'error': 'Nenhuma vaga encontrada',
                    'message': 'O Indeed não retornou vagas para os parâmetros informados'
                }), 404
            
            # Processar resultado
            vagas_processadas = resultado_scraping
            total_vagas = len(vagas_processadas)
            
            # Montar resposta final
            resultado = {
                'apify_mode': True,
                'id': f'indeed_{int(time.time())}',
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
                    'tempoColeta': 'N/A'
                },
                'transparencia': {
                    'fontes_utilizadas': ['Indeed via APIFY'],
                    'metodo_coleta': 'APIFY Indeed Scraper',
                    'filtros_aplicados': f'Cargo: {cargo}, Localização: {localizacao}',
                    'observacoes': 'Dados reais coletados do Indeed via APIFY API',
                    'actor_id': 'borderline/indeed-scraper',
                    'run_id': 'N/A'
                },
                'vagas': vagas_processadas
            }
            
            logger.info(f"✅ Coleta Indeed finalizada: {total_vagas} vagas")
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

@app.route('/api/agent1/cancel-collection', methods=['POST', 'OPTIONS'])
def cancel_collection():
    """Endpoint para cancelar coleta em andamento"""
    
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        run_id = data.get('run_id')
        
        if not run_id:
            return jsonify({'error': 'run_id não fornecido'}), 400
        
        # Verificar se os scrapers estão disponíveis
        if IndeedScraper:
            indeed_scraper = IndeedScraper()
            
            # Cancelar o run
            success = indeed_scraper.cancelar_run(run_id)
            
            if success:
                return jsonify({
                    'status': 'success',
                    'message': 'Coleta cancelada com sucesso',
                    'run_id': run_id
                })
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Erro ao cancelar coleta'
                }), 500
        else:
            return jsonify({
                'status': 'error',
                'message': 'Serviço não disponível'
            }), 503
            
    except Exception as e:
        logger.error(f"❌ Erro ao cancelar coleta: {e}")
        return jsonify({
            'error': 'Erro ao cancelar coleta',
            'message': str(e)
        }), 500

@app.route('/api/agent1/collect-jobs-stream', methods=['POST', 'OPTIONS'])
def collect_jobs_stream():
    """Endpoint de streaming de coleta de vagas (Indeed)"""
    
    if request.method == 'OPTIONS':
        return '', 200
    
    # Obter dados ANTES do generator
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    cargo = data.get('cargo_objetivo', 'Desenvolvedor')
    area = data.get('area_interesse', 'Tecnologia')
    localizacao = data.get('localizacao', 'São Paulo')
    quantidade = min(data.get('total_vagas_desejadas', 20), 100)  # Limitar a 100 para economizar
    
    # Extrair parâmetros avançados para streaming
    raio_km = int(data.get('raio', 25))
    nivel = data.get('nivel', 'todos')
    tipo_contrato = data.get('tipoContrato', 'todos')
    dias_publicacao = data.get('diasPublicacao', 'todos')
    ordenar = data.get('ordenar', 'date')
    modalidade = data.get('modalidade', 'todos')
    
    def generate_stream():
        try:
            # Enviar confirmação inicial
            yield f"data: {json.dumps({'status': 'iniciando', 'message': f'Iniciando coleta no Indeed para {cargo}...', 'timestamp': datetime.now().isoformat()})}\n\n"
            
            # Verificar token APIFY
            apify_token = os.getenv('APIFY_API_TOKEN')
            if not apify_token:
                yield f"data: {json.dumps({'error': 'APIFY_API_TOKEN não configurado', 'timestamp': datetime.now().isoformat()})}\n\n"
                return
            
            yield f"data: {json.dumps({'status': 'config_ok', 'message': 'Configuração verificada', 'timestamp': datetime.now().isoformat()})}\n\n"
            
            # Verificar se o scraper está disponível
            if IndeedScraper:
                logger.info("✅ Indeed Scraper disponível")
                indeed_scraper = IndeedScraper()
                
                # Verificar credenciais
                if not indeed_scraper.apify_token:
                    yield f"data: {json.dumps({'error': 'Token APIFY não configurado', 'timestamp': datetime.now().isoformat()})}\n\n"
                    return
                
                yield f"data: {json.dumps({'status': 'scrapers_ok', 'message': 'Indeed scraper inicializado', 'timestamp': datetime.now().isoformat()})}\n\n"
                
                # Iniciar coleta
                try:
                    # Preparar kwargs para streaming
                    stream_kwargs = {
                        'raio_km': raio_km
                    }
                    
                    # Adicionar modalidade
                    if modalidade == 'remote':
                        stream_kwargs['remoto'] = True
                    
                    # Adicionar nível se especificado
                    if nivel != 'todos':
                        stream_kwargs['nivel'] = nivel
                        
                    # Adicionar tipo de contrato se especificado
                    if tipo_contrato != 'todos':
                        stream_kwargs['tipo_vaga'] = tipo_contrato
                        
                    # Adicionar filtro de data se especificado
                    if dias_publicacao != 'todos':
                        stream_kwargs['dias_publicacao'] = dias_publicacao
                        
                    # Adicionar ordenação
                    stream_kwargs['ordenar'] = ordenar
                    
                    run_id, dataset_id = indeed_scraper.iniciar_execucao_indeed(
                        cargo=cargo,
                        localizacao=localizacao,
                        limite=quantidade,
                        **stream_kwargs
                    )
                    
                    if not run_id:
                        yield f"data: {json.dumps({'error': 'Erro ao iniciar coleta no Indeed', 'timestamp': datetime.now().isoformat()})}\n\n"
                        return
                    
                    yield f"data: {json.dumps({'status': 'coleta_iniciada', 'run_id': run_id, 'dataset_id': dataset_id, 'timestamp': datetime.now().isoformat()})}\n\n"
                    
                    # Polling com timeout
                    vagas_coletadas = []
                    tempo_inicio = time.time()
                    timeout_segundos = 300  # 5 minutos
                    
                    while True:
                        tempo_decorrido = time.time() - tempo_inicio
                        
                        if tempo_decorrido > timeout_segundos:
                            yield f"data: {json.dumps({'status': 'timeout', 'message': 'Timeout - finalizando', 'timestamp': datetime.now().isoformat()})}\n\n"
                            break
                        
                        # Verificar status
                        status_run = indeed_scraper.verificar_status_run(run_id)
                        yield f"data: {json.dumps({'status': 'monitorando', 'run_status': status_run, 'timestamp': datetime.now().isoformat()})}\n\n"
                        
                        # Obter resultados parciais
                        novos_resultados = indeed_scraper.obter_resultados_parciais(
                            dataset_id, 
                            offset=len(vagas_coletadas),
                            limit=quantidade
                        )
                        
                        if novos_resultados:
                            vagas_coletadas.extend(novos_resultados)
                            yield f"data: {json.dumps({'type': 'novas_vagas', 'novas_vagas': novos_resultados, 'total_atual': len(vagas_coletadas), 'timestamp': datetime.now().isoformat()})}\n\n"
                        
                        if status_run in ['SUCCEEDED', 'FAILED', 'ABORTED', 'TIMED-OUT']:
                            if status_run == 'SUCCEEDED':
                                logger.info(f"✅ Run finalizada com sucesso!")
                                # Pegar resultados finais se houver mais
                                resultados_finais = indeed_scraper.obter_resultados_parciais(
                                    dataset_id,
                                    offset=len(vagas_coletadas),
                                    limit=quantidade - len(vagas_coletadas)
                                )
                                if resultados_finais:
                                    vagas_coletadas.extend(resultados_finais)
                                    yield f"data: {json.dumps({'type': 'novas_vagas', 'novas_vagas': resultados_finais, 'total_atual': len(vagas_coletadas), 'timestamp': datetime.now().isoformat()})}\n\n"
                            break
                        
                        time.sleep(5)  # Check a cada 5 segundos
                    
                    # Finalizar
                    logger.info(f"🏁 Finalizando streaming com {len(vagas_coletadas)} vagas")
                    yield f"data: {json.dumps({'status': 'concluido', 'total_vagas': len(vagas_coletadas), 'timestamp': datetime.now().isoformat()})}\n\n"
                    
                    # Evento final
                    yield f"data: {json.dumps({'status': 'finalizado', 'vagas': vagas_coletadas, 'timestamp': datetime.now().isoformat()})}\n\n"
                    
                except Exception as e:
                    logger.error(f"Erro durante coleta Indeed: {e}")
                    yield f"data: {json.dumps({'error': f'Erro durante coleta: {str(e)}', 'timestamp': datetime.now().isoformat()})}\n\n"
            
            else:
                # Modo demonstração
                yield f"data: {json.dumps({'status': 'modo_demo', 'message': 'Indeed Scraper não disponível', 'timestamp': datetime.now().isoformat()})}\n\n"
            
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

@app.route('/api/agent1/analyze-keywords-stream', methods=['POST', 'OPTIONS'])
def analyze_keywords_stream():
    """Endpoint de streaming para análise de palavras-chave com IA"""
    
    if request.method == 'OPTIONS':
        return '', 200
    
    # Obter dados ANTES do generator
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    vagas = data.get('vagas', [])
    cargo_objetivo = data.get('cargo_objetivo', '')
    area_interesse = data.get('area_interesse', '')
    
    def generate_analysis_stream():
        try:
            # Enviar confirmação inicial
            yield f"data: {json.dumps({'status': 'iniciando', 'message': 'Preparando análise com IA...', 'timestamp': datetime.now().isoformat()})}\n\n"
            
            # Verificar se temos o AIKeywordExtractor
            try:
                from core.services.ai_keyword_extractor import AIKeywordExtractor
                extractor = AIKeywordExtractor()
                yield f"data: {json.dumps({'status': 'extractor_ok', 'message': 'Extrator de palavras-chave carregado', 'timestamp': datetime.now().isoformat()})}\n\n"
            except ImportError as e:
                yield f"data: {json.dumps({'error': 'Extrator não disponível', 'timestamp': datetime.now().isoformat()})}\n\n"
                return
            
            # Etapa 1: Preparação dos dados
            yield f"data: {json.dumps({'status': 'preparando', 'message': f'Preparando {len(vagas)} vagas para análise...', 'progress': 10, 'timestamp': datetime.now().isoformat()})}\n\n"
            time.sleep(0.5)
            
            # Etapa 2: Verificação de modelos IA
            yield f"data: {json.dumps({'status': 'verificando_ia', 'message': 'Verificando modelos de IA disponíveis...', 'progress': 20, 'timestamp': datetime.now().isoformat()})}\n\n"
            
            modelos_disponiveis = []
            if extractor.gemini_model:
                modelos_disponiveis.append('Gemini 2.5 Flash')
            if extractor.anthropic_client:
                modelos_disponiveis.append('Claude')
            if extractor.openai_client:
                modelos_disponiveis.append('GPT-4')
            
            modelos_text = ", ".join(modelos_disponiveis)
            yield f"data: {json.dumps({'status': 'modelos_encontrados', 'message': f'Modelos disponíveis: {modelos_text}', 'progress': 30, 'timestamp': datetime.now().isoformat()})}\n\n"
            
            # Etapa 3: Análise com IA
            yield f"data: {json.dumps({'status': 'analisando', 'message': 'Enviando vagas para análise com IA...', 'progress': 40, 'timestamp': datetime.now().isoformat()})}\n\n"
            
            # Simular progresso de análise
            mensagens_progresso = [
                ('processando_descricoes', 'Processando descrições das vagas...', 50),
                ('identificando_padroes', 'Identificando padrões e termos recorrentes...', 60),
                ('categorizando', 'Categorizando palavras-chave...', 70),
                ('aplicando_metodologia', 'Aplicando metodologia Carolina Martins...', 80),
                ('finalizando', 'Finalizando análise e preparando resultados...', 90)
            ]
            
            for status, mensagem, progresso in mensagens_progresso:
                yield f"data: {json.dumps({'status': status, 'message': mensagem, 'progress': progresso, 'timestamp': datetime.now().isoformat()})}\n\n"
                time.sleep(2)  # Simular processamento
            
            # Executar análise real
            try:
                # Como o método é assíncrono, precisamos executá-lo em um loop
                import asyncio
                
                # Callback para enviar atualizações
                async def callback_progresso(msg):
                    yield f"data: {json.dumps({'status': 'processando', 'message': msg, 'timestamp': datetime.now().isoformat()})}\n\n"
                
                # Executar análise de forma segura
                try:
                    # Tentar usar loop existente se disponível
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        # Se o loop já está rodando, usar uma task
                        import concurrent.futures
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            future = executor.submit(
                                asyncio.run,
                                extractor.extrair_palavras_chave_ia(
                                    vagas=vagas,
                                    cargo_objetivo=cargo_objetivo,
                                    area_interesse=area_interesse
                                )
                            )
                            resultado = future.result()
                    else:
                        resultado = loop.run_until_complete(
                            extractor.extrair_palavras_chave_ia(
                                vagas=vagas,
                                cargo_objetivo=cargo_objetivo,
                                area_interesse=area_interesse
                            )
                        )
                except RuntimeError:
                    # Se não há loop, criar um novo
                    resultado = asyncio.run(
                        extractor.extrair_palavras_chave_ia(
                            vagas=vagas,
                            cargo_objetivo=cargo_objetivo,
                            area_interesse=area_interesse
                        )
                    )
                
                # Enviar resultado final
                yield f"data: {json.dumps({'status': 'concluido', 'resultado': resultado, 'progress': 100, 'timestamp': datetime.now().isoformat()})}\n\n"
                
            except Exception as e:
                logger.error(f"Erro na análise IA: {e}")
                yield f"data: {json.dumps({'error': f'Erro na análise: {str(e)}', 'timestamp': datetime.now().isoformat()})}\n\n"
            
        except Exception as e:
            logger.error(f"Erro crítico no streaming: {e}")
            yield f"data: {json.dumps({'error': f'Erro crítico: {str(e)}', 'timestamp': datetime.now().isoformat()})}\n\n"
    
    return Response(
        generate_analysis_stream(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
    )


# Print environment info at module level
logger.info("=" * 50)
logger.info("🚀 HELIO JOB ROBOT - INICIALIZANDO")
logger.info(f"📍 Ambiente: {'Railway' if os.environ.get('RAILWAY_ENVIRONMENT') else 'Local'}")
logger.info(f"🔑 PORT: {os.environ.get('PORT', 'Não definido')}")
logger.info(f"🔑 APIFY_API_TOKEN: {'Configurado' if os.environ.get('APIFY_API_TOKEN') else 'Não configurado'}")
logger.info("=" * 50)

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