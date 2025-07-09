#!/usr/bin/env python3
"""
API HELIO - Streaming de Coleta de Vagas com LOGS DETALHADOS
Integração completa com sistema de agentes
"""
import os
import sys
import json
import time
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any
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
    from core.services.agente_1_palavras_chave import MPCCarolinaMartins
    from core.services.linkedin_apify_scraper import LinkedInApifyScraper
    logger.info("✅ Imports do sistema HELIO carregados com sucesso")
except ImportError as e:
    logger.error(f"❌ Erro ao importar módulos HELIO: {e}")
    # Fallback para demonstração
    JobScraper = None
    MPCCarolinaMartins = None
    LinkedInApifyScraper = None

app = Flask(__name__)
CORS(app, origins=['https://agenteslinkedin.vercel.app', 'http://localhost:3000'])

@app.route('/api/health', methods=['GET'])
@cross_origin()
def health():
    """Health check com informações detalhadas do sistema"""
    
    # Verificar componentes do sistema
    sistema_status = {
        'status': 'ok',
        'service': 'helio-streaming-api',
        'timestamp': datetime.now().isoformat(),
        'componentes': {
            'job_scraper': JobScraper is not None,
            'mpc_agent': MPCCarolinaMartins is not None,
            'linkedin_scraper': LinkedInApifyScraper is not None,
            'apify_token': bool(os.getenv('APIFY_API_TOKEN')),
        },
        'versao': '2.0-streaming',
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
            
            data = request.get_json()
            
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
            yield f"data: {json.dumps({
                'status': 'iniciando',
                'message': f'🚀 Iniciando coleta de vagas para {cargo}...',
                'parametros': {
                    'cargo': cargo,
                    'area': area,
                    'localizacao': localizacao,
                    'quantidade': quantidade
                },
                'timestamp': datetime.now().isoformat()
            })}\n\n"
            
            # ================================
            # 🔧 VERIFICAR CONFIGURAÇÃO
            # ================================
            
            yield f"data: {json.dumps({
                'status': 'verificando_config',
                'message': '🔧 Verificando configuração do sistema...',
                'timestamp': datetime.now().isoformat()
            })}\n\n"
            
            # Verificar token Apify
            apify_token = os.getenv('APIFY_API_TOKEN')
            if not apify_token:
                error_msg = "❌ APIFY_API_TOKEN não configurado"
                logger.error(error_msg)
                yield f"data: {json.dumps({
                    'error': error_msg,
                    'detalhes': 'Configure a variável de ambiente APIFY_API_TOKEN',
                    'timestamp': datetime.now().isoformat()
                })}\n\n"
                return
            
            logger.info(f"✅ APIFY_API_TOKEN configurado: {apify_token[:10]}...")
            
            yield f"data: {json.dumps({
                'status': 'config_ok',
                'message': '✅ Configuração verificada com sucesso',
                'timestamp': datetime.now().isoformat()
            })}\n\n"
            
            # ================================
            # 🔄 INICIALIZAR SCRAPERS
            # ================================
            
            yield f"data: {json.dumps({
                'status': 'inicializando_scrapers',
                'message': '🔄 Inicializando scrapers...',
                'timestamp': datetime.now().isoformat()
            })}\n\n"
            
            if JobScraper and LinkedInApifyScraper:
                logger.info("🔄 Inicializando JobScraper...")
                job_scraper = JobScraper()
                
                logger.info("🔄 Inicializando LinkedInApifyScraper...")
                linkedin_scraper = LinkedInApifyScraper()
                
                # Verificar credenciais
                if not linkedin_scraper.verificar_credenciais():
                    error_msg = "❌ Credenciais do LinkedIn Apify inválidas"
                    logger.error(error_msg)
                    yield f"data: {json.dumps({
                        'error': error_msg,
                        'timestamp': datetime.now().isoformat()
                    })}\n\n"
                    return
                
                logger.info("✅ Scrapers inicializados com sucesso")
                yield f"data: {json.dumps({
                    'status': 'scrapers_ok',
                    'message': '✅ Scrapers inicializados com sucesso',
                    'timestamp': datetime.now().isoformat()
                })}\n\n"
                
                # ================================
                # 🚀 INICIAR COLETA STREAMING
                # ================================
                
                yield f"data: {json.dumps({
                    'status': 'iniciando_coleta',
                    'message': '🚀 Iniciando coleta via Apify...',
                    'timestamp': datetime.now().isoformat()
                })}\n\n"
                
                try:
                    # Usar método de streaming do JobScraper
                    run_id, dataset_id = job_scraper.iniciar_coleta_streaming(
                        area_interesse=area,
                        cargo_objetivo=cargo,
                        localizacao=localizacao,
                        total_vagas_desejadas=quantidade
                    )
                    
                    logger.info(f"✅ Coleta iniciada - Run ID: {run_id}, Dataset ID: {dataset_id}")
                    
                    yield f"data: {json.dumps({
                        'status': 'coleta_iniciada',
                        'message': '✅ Coleta iniciada no Apify',
                        'run_id': run_id,
                        'dataset_id': dataset_id,
                        'timestamp': datetime.now().isoformat()
                    })}\n\n"
                    
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
                            yield f"data: {json.dumps({
                                'status': 'timeout',
                                'message': f'⏰ Timeout após {timeout_segundos//60} minutos - finalizando com dados parciais',
                                'tempo_decorrido': int(tempo_decorrido),
                                'timestamp': datetime.now().isoformat()
                            })}\n\n"
                            break
                        
                        # Verificar status da execução
                        status_run = job_scraper.verificar_status_run(run_id)
                        logger.info(f"📊 Status da execução: {status_run}")
                        
                        yield f"data: {json.dumps({
                            'status': 'monitorando',
                            'run_status': status_run,
                            'message': f'🔍 Monitorando execução... Status: {status_run}',
                            'tempo_decorrido': int(tempo_decorrido),
                            'timestamp': datetime.now().isoformat()
                        })}\n\n"
                        
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
                                yield f"data: {json.dumps({
                                    'type': 'novas_vagas',
                                    'novas_vagas': resultados_parciais,
                                    'total_atual': len(vagas_coletadas),
                                    'meta': quantidade,
                                    'progresso': min((len(vagas_coletadas) / quantidade) * 100, 100),
                                    'message': f'📥 {len(resultados_parciais)} novas vagas coletadas (Total: {len(vagas_coletadas)})',
                                    'timestamp': datetime.now().isoformat()
                                })}\n\n"
                        
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
                    
                    yield f"data: {json.dumps({
                        'status': 'concluido',
                        'total_vagas': len(vagas_coletadas),
                        'meta': quantidade,
                        'percentual_atingido': (len(vagas_coletadas) / quantidade) * 100,
                        'tempo_total': int(time.time() - tempo_inicio),
                        'message': f'✅ Coleta concluída! {len(vagas_coletadas)} vagas encontradas',
                        'timestamp': datetime.now().isoformat()
                    })}\n\n"
                    
                    # Enviar dados finais
                    yield f"data: {json.dumps({
                        'status': 'finalizado',
                        'total_vagas': len(vagas_coletadas),
                        'vagas': vagas_coletadas,
                        'timestamp': datetime.now().isoformat()
                    })}\n\n"
                    
                except Exception as e:
                    error_msg = f"❌ Erro durante coleta: {str(e)}"
                    logger.error(error_msg, exc_info=True)
                    yield f"data: {json.dumps({
                        'error': error_msg,
                        'detalhes': str(e),
                        'timestamp': datetime.now().isoformat()
                    })}\n\n"
            
            else:
                # ================================
                # 🎭 MODO DEMONSTRAÇÃO
                # ================================
                
                logger.warning("⚠️ Componentes do sistema não disponíveis - usando modo demonstração")
                
                yield f"data: {json.dumps({
                    'status': 'modo_demo',
                    'message': '🎭 Sistema em modo demonstração',
                    'timestamp': datetime.now().isoformat()
                })}\n\n"
                
                # Simular coleta progressiva
                vagas_demo = []
                for i in range(1, min(quantidade + 1, 51)):  # Máximo 50 para demo
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
                    yield f"data: {json.dumps({
                        'type': 'nova_vaga',
                        'vaga': vaga,
                        'total_atual': i,
                        'meta': quantidade,
                        'progresso': (i / quantidade) * 100,
                        'timestamp': datetime.now().isoformat()
                    })}\n\n"
                    
                    # Update de progresso a cada 5 vagas
                    if i % 5 == 0:
                        yield f"data: {json.dumps({
                            'status': 'executando',
                            'total_vagas': i,
                            'message': f'⏳ Coletando... {i} vagas encontradas (DEMO)',
                            'timestamp': datetime.now().isoformat()
                        })}\n\n"
                    
                    time.sleep(0.5)  # Simular tempo real
                
                # Finalizar demo
                yield f"data: {json.dumps({
                    'status': 'concluido',
                    'total_vagas': len(vagas_demo),
                    'message': f'✅ Demo concluída! {len(vagas_demo)} vagas simuladas',
                    'timestamp': datetime.now().isoformat()
                })}\n\n"
                
                yield f"data: {json.dumps({
                    'status': 'finalizado',
                    'total_vagas': len(vagas_demo),
                    'vagas': vagas_demo,
                    'timestamp': datetime.now().isoformat()
                })}\n\n"
            
        except Exception as e:
            error_msg = f"❌ Erro crítico no streaming: {str(e)}"
            logger.error(error_msg, exc_info=True)
            yield f"data: {json.dumps({
                'error': error_msg,
                'timestamp': datetime.now().isoformat()
            })}\n\n"
    
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🚀 Iniciando HELIO Streaming API na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=False) 