#!/usr/bin/env python3
"""
API HELIO - Streaming de Coleta de Vagas com LOGS DETALHADOS
Código direto no api_server.py para Railway
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

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(__file__))

# Imports do sistema HELIO
try:
    from core.services.job_scraper import JobScraper
    from core.services.linkedin_apify_scraper import LinkedInApifyScraper
    logger.info("✅ Imports do sistema HELIO carregados com sucesso")
    SISTEMA_DISPONIVEL = True
except ImportError as e:
    logger.error(f"❌ Erro ao importar módulos HELIO: {e}")
    JobScraper = None
    LinkedInApifyScraper = None
    SISTEMA_DISPONIVEL = False

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
    """Health check com informações detalhadas do sistema"""
    
    # Verificar componentes do sistema
    sistema_status = {
        'status': 'ok',
        'service': 'helio-streaming-api-direct',
        'timestamp': datetime.now().isoformat(),
        'componentes': {
            'job_scraper': JobScraper is not None,
            'linkedin_scraper': LinkedInApifyScraper is not None,
            'apify_token': bool(os.getenv('APIFY_API_TOKEN')),
            'sistema_disponivel': SISTEMA_DISPONIVEL
        },
        'versao': '2.1-direct',
        'modo': 'production' if not app.debug else 'development'
    }
    
    # Log do status
    logger.info(f"🏥 Health check - Sistema: {sistema_status}")
    
    return jsonify(sistema_status)

@app.route('/api/agent1/collect-jobs-stream', methods=['POST', 'OPTIONS'])
@cross_origin()
def collect_jobs_stream():
    """
    🚀 ENDPOINT DE STREAMING PARA COLETA DE VAGAS
    Integração completa com sistema HELIO
    """
    
    if request.method == 'OPTIONS':
        return '', 200
    
    def generate_stream():
        """Gerador de stream com logs detalhados em tempo real"""
        
        try:
            # ================================
            # 📋 VALIDAÇÃO DE ENTRADA
            # ================================
            
            logger.info("🚀 INICIANDO STREAMING DE COLETA DE VAGAS")
            
            # Capturar dados do request no contexto correto
            data = request.get_json() if request else None
            
            if not data:
                error_msg = "❌ Dados não fornecidos na requisição"
                logger.error(error_msg)
                yield f"data: {json.dumps({'error': error_msg, 'timestamp': datetime.now().isoformat()})}\n\n"
                return
            
            # Extrair parâmetros
            cargo = data.get('cargo_objetivo', 'Desenvolvedor')
            area = data.get('area_interesse', 'Tecnologia')
            localizacao = data.get('localizacao', 'Brasil')
            quantidade = data.get('total_vagas_desejadas', 800)
            
            logger.info(f"📋 Parâmetros recebidos:")
            logger.info(f"   • Cargo: {cargo}")
            logger.info(f"   • Área: {area}")
            logger.info(f"   • Localização: {localizacao}")
            logger.info(f"   • Quantidade: {quantidade}")
            
            # Enviar confirmação inicial
            yield f"data: {json.dumps({'status': 'iniciando', 'message': f'🚀 Iniciando coleta de vagas para {cargo}...', 'parametros': {'cargo': cargo, 'area': area, 'localizacao': localizacao, 'quantidade': quantidade}, 'timestamp': datetime.now().isoformat()})}\n\n"
            
            # ================================
            # 🔧 VERIFICAR CONFIGURAÇÃO
            # ================================
            
            yield f"data: {json.dumps({'status': 'verificando_config', 'message': '🔧 Verificando configuração do sistema...', 'timestamp': datetime.now().isoformat()})}\n\n"
            
            # Verificar token Apify
            apify_token = os.getenv('APIFY_API_TOKEN')
            if not apify_token:
                error_msg = "❌ APIFY_API_TOKEN não configurado"
                logger.error(error_msg)
                yield f"data: {json.dumps({'error': error_msg, 'detalhes': 'Configure a variável de ambiente APIFY_API_TOKEN', 'timestamp': datetime.now().isoformat()})}\n\n"
                return
            
            logger.info(f"✅ APIFY_API_TOKEN configurado: {apify_token[:10]}...")
            
            yield f"data: {json.dumps({'status': 'config_ok', 'message': '✅ Configuração verificada com sucesso', 'detalhes': f'Token: {apify_token[:10]}...', 'timestamp': datetime.now().isoformat()})}\n\n"
            
            # ================================
            # 🔄 VERIFICAR SISTEMA
            # ================================
            
            yield f"data: {json.dumps({'status': 'verificando_sistema', 'message': '🔄 Verificando disponibilidade do sistema...', 'timestamp': datetime.now().isoformat()})}\n\n"
            
            if not SISTEMA_DISPONIVEL:
                logger.warning("⚠️ Sistema HELIO não disponível - usando modo demonstração")
                
                yield f"data: {json.dumps({'status': 'modo_demo', 'message': '🎭 Sistema em modo demonstração (módulos não carregados)', 'timestamp': datetime.now().isoformat()})}\n\n"
                
                # Simular coleta progressiva
                vagas_demo = []
                for i in range(1, min(quantidade + 1, 21)):  # Máximo 20 para demo
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
                    
                    # Enviar vaga individual
                    yield f"data: {json.dumps({'type': 'nova_vaga', 'vaga': vaga, 'total_atual': i, 'meta': quantidade, 'progresso': (i / min(quantidade, 20)) * 100, 'timestamp': datetime.now().isoformat()})}\n\n"
                    
                    # Update de progresso a cada 3 vagas
                    if i % 3 == 0:
                        yield f"data: {json.dumps({'status': 'executando', 'total_vagas': i, 'message': f'⏳ Coletando... {i} vagas encontradas (DEMO)', 'timestamp': datetime.now().isoformat()})}\n\n"
                    
                    time.sleep(1.0)  # Simular tempo real
                
                # Finalizar demo
                yield f"data: {json.dumps({'status': 'concluido', 'total_vagas': len(vagas_demo), 'message': f'✅ Demo concluída! {len(vagas_demo)} vagas simuladas', 'timestamp': datetime.now().isoformat()})}\n\n"
                
                yield f"data: {json.dumps({'status': 'finalizado', 'total_vagas': len(vagas_demo), 'vagas': vagas_demo, 'timestamp': datetime.now().isoformat()})}\n\n"
                
                return
            
            # ================================
            # 🔄 INICIALIZAR SCRAPERS
            # ================================
            
            yield f"data: {json.dumps({'status': 'inicializando_scrapers', 'message': '🔄 Inicializando scrapers...', 'timestamp': datetime.now().isoformat()})}\n\n"
            
            logger.info("🔄 Inicializando JobScraper...")
            job_scraper = JobScraper()
            
            logger.info("🔄 Inicializando LinkedInApifyScraper...")
            linkedin_scraper = LinkedInApifyScraper()
            
            # Verificar credenciais
            if not linkedin_scraper.verificar_credenciais():
                error_msg = "❌ Credenciais do LinkedIn Apify inválidas"
                logger.error(error_msg)
                yield f"data: {json.dumps({'error': error_msg, 'timestamp': datetime.now().isoformat()})}\n\n"
                return
            
            logger.info("✅ Scrapers inicializados com sucesso")
            yield f"data: {json.dumps({'status': 'scrapers_ok', 'message': '✅ Scrapers inicializados com sucesso', 'timestamp': datetime.now().isoformat()})}\n\n"
            
            # ================================
            # 🚀 INICIAR COLETA STREAMING
            # ================================
            
            yield f"data: {json.dumps({'status': 'iniciando_coleta', 'message': '🚀 Iniciando coleta via Apify...', 'timestamp': datetime.now().isoformat()})}\n\n"
            
            try:
                # Usar método de streaming do JobScraper
                run_id, dataset_id = job_scraper.iniciar_coleta_streaming(
                    area_interesse=area,
                    cargo_objetivo=cargo,
                    localizacao=localizacao,
                    total_vagas_desejadas=quantidade
                )
                
                logger.info(f"✅ Coleta iniciada - Run ID: {run_id}, Dataset ID: {dataset_id}")
                
                yield f"data: {json.dumps({'status': 'coleta_iniciada', 'message': '✅ Coleta iniciada no Apify', 'run_id': run_id, 'dataset_id': dataset_id, 'timestamp': datetime.now().isoformat()})}\n\n"
                
                # ================================
                # 🔄 POLLING COM ATUALIZAÇÕES
                # ================================
                
                vagas_coletadas = []
                offset_atual = 0
                tempo_inicio = time.time()
                timeout_segundos = 420  # 7 minutos
                
                while True:
                    tempo_decorrido = time.time() - tempo_inicio
                    
                    # Verificar timeout
                    if tempo_decorrido > timeout_segundos:
                        logger.warning(f"⏰ Timeout após {timeout_segundos} segundos")
                        yield f"data: {json.dumps({'status': 'timeout', 'message': f'⏰ Timeout após {timeout_segundos//60} minutos - finalizando com dados parciais', 'tempo_decorrido': int(tempo_decorrido), 'timestamp': datetime.now().isoformat()})}\n\n"
                        break
                    
                    # Verificar status da execução
                    status_run = job_scraper.verificar_status_run(run_id)
                    logger.info(f"📊 Status da execução: {status_run}")
                    
                    yield f"data: {json.dumps({'status': 'monitorando', 'run_status': status_run, 'message': f'🔍 Monitorando execução... Status: {status_run}', 'tempo_decorrido': int(tempo_decorrido), 'timestamp': datetime.now().isoformat()})}\n\n"
                    
                    # Contar resultados atuais
                    total_resultados = job_scraper.contar_resultados_dataset(dataset_id)
                    logger.info(f"📊 Total de resultados no dataset: {total_resultados}")
                    
                    # Se há novos resultados, buscar e enviar
                    if total_resultados > offset_atual:
                        novos_resultados = total_resultados - offset_atual
                        logger.info(f"📥 Buscando {novos_resultados} novos resultados...")
                        
                        # Buscar novos resultados
                        resultados_parciais = job_scraper.obter_resultados_parciais(
                            dataset_id, offset_atual, novos_resultados
                        )
                        
                        if resultados_parciais:
                            vagas_coletadas.extend(resultados_parciais)
                            offset_atual = total_resultados
                            
                            logger.info(f"✅ {len(resultados_parciais)} novas vagas adicionadas")
                            
                            # Enviar atualização com novas vagas
                            yield f"data: {json.dumps({'type': 'novas_vagas', 'novas_vagas': resultados_parciais, 'total_atual': len(vagas_coletadas), 'meta': quantidade, 'progresso': min((len(vagas_coletadas) / quantidade) * 100, 100), 'message': f'📥 {len(resultados_parciais)} novas vagas coletadas (Total: {len(vagas_coletadas)})', 'timestamp': datetime.now().isoformat()})}\n\n"
                    
                    # Verificar se execução foi concluída
                    if status_run in ['SUCCEEDED', 'FAILED', 'ABORTED', 'TIMED-OUT']:
                        logger.info(f"🏁 Execução finalizada com status: {status_run}")
                        break
                    
                    # Aguardar antes da próxima verificação
                    time.sleep(10)
                
                # ================================
                # 🏁 FINALIZAÇÃO
                # ================================
                
                # Buscar resultados finais se necessário
                total_final = job_scraper.contar_resultados_dataset(dataset_id)
                if total_final > len(vagas_coletadas):
                    logger.info(f"📥 Buscando resultados finais...")
                    resultados_finais = job_scraper.obter_todos_resultados(dataset_id)
                    vagas_coletadas = resultados_finais
                
                logger.info(f"🏁 Coleta finalizada - {len(vagas_coletadas)} vagas coletadas")
                
                yield f"data: {json.dumps({'status': 'concluido', 'total_vagas': len(vagas_coletadas), 'meta': quantidade, 'percentual_atingido': (len(vagas_coletadas) / quantidade) * 100, 'tempo_total': int(time.time() - tempo_inicio), 'message': f'✅ Coleta concluída! {len(vagas_coletadas)} vagas encontradas', 'timestamp': datetime.now().isoformat()})}\n\n"
                
                # Enviar dados finais
                yield f"data: {json.dumps({'status': 'finalizado', 'total_vagas': len(vagas_coletadas), 'vagas': vagas_coletadas, 'timestamp': datetime.now().isoformat()})}\n\n"
                
            except Exception as e:
                error_msg = f"❌ Erro durante coleta: {str(e)}"
                logger.error(error_msg, exc_info=True)
                yield f"data: {json.dumps({'error': error_msg, 'detalhes': str(e), 'timestamp': datetime.now().isoformat()})}\n\n"
            
        except Exception as e:
            error_msg = f"❌ Erro crítico no streaming: {str(e)}"
            logger.error(error_msg, exc_info=True)
            yield f"data: {json.dumps({'error': error_msg, 'timestamp': datetime.now().isoformat()})}\n\n"
    
    return Response(
        generate_stream(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
    )

@app.route('/api/agent1/collect-keywords', methods=['POST', 'OPTIONS'])
@cross_origin()
def collect_keywords():
    """
    🎯 ENDPOINT PARA COLETA DE VAGAS E EXTRAÇÃO DE PALAVRAS-CHAVE
    Compatível com o frontend Agent1.jsx
    """
    
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        logger.info("🎯 Iniciando coleta de vagas e análise de palavras-chave")
        
        # Capturar dados da requisição
        data = request.get_json()
        if not data:
            logger.error("❌ Dados não fornecidos na requisição")
            return jsonify({'error': 'Dados não fornecidos na requisição'}), 400
        
        # Extrair parâmetros
        cargo = data.get('cargo_objetivo', 'Desenvolvedor')
        area = data.get('area_interesse', 'Tecnologia')
        localizacao = data.get('localizacao', 'Brasil')
        quantidade = data.get('total_vagas_desejadas', 100)
        
        logger.info(f"📋 Parâmetros recebidos: cargo={cargo}, area={area}, localizacao={localizacao}, quantidade={quantidade}")
        
        # Verificar se sistema está disponível
        if not SISTEMA_DISPONIVEL:
            logger.warning("⚠️ Sistema não disponível - retornando dados simulados")
            
            # Retornar dados simulados compatíveis com o frontend
            vagas_demo = []
            for i in range(1, min(quantidade + 1, 51)):  # Máximo 50 para demo
                vaga = {
                    'id': i,
                    'titulo': f'{cargo} - Posição {i}',
                    'empresa': f'Empresa Tech {i}',
                    'localizacao': localizacao,
                    'descricao': f'Vaga para {cargo} com experiência em tecnologias modernas. React, Node.js, Python, AWS.',
                    'link': f'https://linkedin.com/jobs/view/{1000000 + i}',
                    'nivel': 'Pleno' if i % 3 == 0 else 'Júnior',
                    'tipo': 'Híbrido' if i % 2 == 0 else 'Remoto'
                }
                vagas_demo.append(vaga)
            
            # Simular palavras-chave extraídas
            palavras_chave_demo = {
                'hard_skills': ['React', 'Node.js', 'Python', 'JavaScript', 'AWS', 'Docker', 'MongoDB', 'TypeScript', 'Git'],
                'soft_skills': ['Comunicação', 'Trabalho em equipe', 'Resolução de problemas', 'Criatividade', 'Adaptabilidade'],
                'ferramentas': ['GitHub', 'VS Code', 'Jira', 'Slack', 'Figma', 'Postman'],
                'frameworks': ['React', 'Express', 'Django', 'FastAPI', 'Next.js']
            }
            
            resultado_demo = {
                'id': f'demo_{int(time.time())}',
                'demo_mode': True,
                'parametros': {
                    'cargo_objetivo': cargo,
                    'area_interesse': area,
                    'localizacao': localizacao,
                    'total_vagas_desejadas': quantidade
                },
                'estatisticas': {
                    'totalVagas': len(vagas_demo),
                    'vagasAnalisadas': len(vagas_demo),
                    'successRate': 100,
                    'tempoColeta': '45 segundos (DEMO)'
                },
                'vagas': vagas_demo,
                'palavras_chave': palavras_chave_demo,
                'transparencia': {
                    'metodo_coleta': 'Demonstração com dados simulados',
                    'fontes_utilizadas': ['LinkedIn (Simulado)', 'Indeed (Simulado)'],
                    'filtros_aplicados': f'Cargo: {cargo}, Localização: {localizacao}',
                    'observacoes': 'Dados gerados para demonstração do sistema'
                },
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Demo concluída: {len(vagas_demo)} vagas simuladas")
            return jsonify(resultado_demo)
        
        # Se sistema disponível, usar scrapers reais
        logger.info("🔄 Sistema disponível - executando coleta real")
        
        # Verificar token Apify
        apify_token = os.getenv('APIFY_API_TOKEN')
        if not apify_token:
            logger.error("❌ APIFY_API_TOKEN não configurado")
            return jsonify({'error': 'APIFY_API_TOKEN não configurado'}), 500
        
        # Inicializar scrapers
        job_scraper = JobScraper()
        linkedin_scraper = LinkedInApifyScraper()
        
        # Verificar credenciais
        if not linkedin_scraper.verificar_credenciais():
            logger.error("❌ Credenciais do LinkedIn Apify inválidas")
            return jsonify({'error': 'Credenciais do LinkedIn Apify inválidas'}), 500
        
        logger.info("✅ Scrapers inicializados - iniciando coleta...")
        
        # Executar coleta (versão simplificada sem streaming)
        try:
            # Usar coleta simples por enquanto
            vagas_coletadas = job_scraper.coletar_vagas_simples(
                area_interesse=area,
                cargo_objetivo=cargo,
                localizacao=localizacao,
                total_vagas_desejadas=min(quantidade, 100)  # Limitar para evitar timeout
            )
            
            if not vagas_coletadas:
                logger.warning("⚠️ Nenhuma vaga coletada - usando fallback demo")
                # Fallback para demo - retornar resposta simulada
                vagas_demo = []
                for i in range(1, 21):  # 20 vagas demo
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
                
                resultado_fallback = {
                    'id': f'fallback_{int(time.time())}',
                    'demo_mode': True,
                    'parametros': {
                        'cargo_objetivo': cargo,
                        'area_interesse': area,
                        'localizacao': localizacao,
                        'total_vagas_desejadas': quantidade
                    },
                    'estatisticas': {
                        'totalVagas': len(vagas_demo),
                        'vagasAnalisadas': len(vagas_demo),
                        'successRate': 100,
                        'tempoColeta': 'Fallback demo'
                    },
                    'vagas': vagas_demo,
                    'transparencia': {
                        'metodo_coleta': 'Fallback - coleta real falhou',
                        'fontes_utilizadas': ['Demo'],
                        'filtros_aplicados': f'Cargo: {cargo}, Localização: {localizacao}',
                        'observacoes': 'Dados demo após falha na coleta real'
                    },
                    'timestamp': datetime.now().isoformat()
                }
                
                return jsonify(resultado_fallback)
            
            logger.info(f"✅ {len(vagas_coletadas)} vagas coletadas com sucesso")
            
            # Preparar resultado real
            resultado_real = {
                'id': f'real_{int(time.time())}',
                'demo_mode': False,
                'parametros': {
                    'cargo_objetivo': cargo,
                    'area_interesse': area,
                    'localizacao': localizacao,
                    'total_vagas_desejadas': quantidade
                },
                'estatisticas': {
                    'totalVagas': len(vagas_coletadas),
                    'vagasAnalisadas': len(vagas_coletadas),
                    'successRate': 100,
                    'tempoColeta': 'Tempo real'
                },
                'vagas': vagas_coletadas,
                'transparencia': {
                    'metodo_coleta': 'Apify LinkedIn Scraper',
                    'fontes_utilizadas': ['LinkedIn via Apify'],
                    'filtros_aplicados': f'Cargo: {cargo}, Localização: {localizacao}',
                    'observacoes': 'Dados coletados em tempo real'
                },
                'timestamp': datetime.now().isoformat()
            }
            
            return jsonify(resultado_real)
            
        except Exception as scraper_error:
            logger.error(f"❌ Erro na coleta real: {scraper_error}")
            # Fallback para demo em caso de erro
            vagas_demo = []
            for i in range(1, 21):  # 20 vagas demo
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
            
            resultado_erro = {
                'id': f'erro_{int(time.time())}',
                'demo_mode': True,
                'parametros': {
                    'cargo_objetivo': cargo,
                    'area_interesse': area,
                    'localizacao': localizacao,
                    'total_vagas_desejadas': quantidade
                },
                'estatisticas': {
                    'totalVagas': len(vagas_demo),
                    'vagasAnalisadas': len(vagas_demo),
                    'successRate': 100,
                    'tempoColeta': 'Demo após erro'
                },
                'vagas': vagas_demo,
                'transparencia': {
                    'metodo_coleta': 'Demo após erro de scraping',
                    'fontes_utilizadas': ['Demo'],
                    'filtros_aplicados': f'Cargo: {cargo}, Localização: {localizacao}',
                    'observacoes': f'Erro na coleta real: {str(scraper_error)}'
                },
                'timestamp': datetime.now().isoformat()
            }
            
            return jsonify(resultado_erro)
    
    except Exception as e:
        error_msg = f"❌ Erro crítico: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return jsonify({'error': error_msg}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🚀 Iniciando HELIO Streaming API DIRECT na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=False) 