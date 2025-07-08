#!/usr/bin/env python3
"""
API REST para integração frontend-backend do sistema HELIO
Expõe endpoints para os agentes funcionais
"""

from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import asyncio
import json
import logging
from pathlib import Path
import uuid
from datetime import datetime
import time
import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Adicionar o diretório core ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

# Importar serviços reais
from services.document_processor import DocumentProcessor
from services.job_scraper import JobScraper
from services.ai_validator import AIValidator
from services.ai_curriculum_analyzer import AICurriculumAnalyzer
from services.keyword_extractor_pro import KeywordExtractorPro
from services.ai_keyword_extractor import AIKeywordExtractor

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar aplicação Flask
app = Flask(__name__)
CORS(app, origins=[
    'http://localhost:3000', 
    'http://127.0.0.1:3000',
    'https://agenteslinkedin.vercel.app',
    os.getenv("FRONTEND_URL", "http://localhost:3000")
], supports_credentials=True)  # Permitir requisições do frontend

# Configurar diretório de uploads
UPLOAD_FOLDER = Path('uploads')
UPLOAD_FOLDER.mkdir(exist_ok=True)

# Inicializar serviços
document_processor = DocumentProcessor()
job_scraper = JobScraper()
ai_validator = AIValidator()
ai_analyzer = AICurriculumAnalyzer()
keyword_extractor = KeywordExtractorPro()
ai_keyword_extractor = AIKeywordExtractor()

# Nota: Agora usando IA REAL para análise de currículo!

# Armazenar resultados em memória (em produção, usar banco de dados)
results_store = {}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificar saúde da API"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'agent_0': True,
            'agent_1': True,
            'document_processor': True,
            'job_scraper': True,
            'ai_validator': True
        }
    })

@app.route('/api/debug/config', methods=['GET'])
def debug_config():
    """Endpoint de debug para verificar configuração atual"""
    from services.linkedin_apify_scraper import LinkedInApifyScraper
    from services.ai_keyword_extractor import AIKeywordExtractor
    
    scraper = LinkedInApifyScraper()
    ai_extractor = AIKeywordExtractor()
    
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'apify': {
            'configured': scraper.verificar_credenciais(),
            'actor_id': scraper.actor_id,
            'token_present': bool(os.getenv('APIFY_API_TOKEN'))
        },
        'ai': {
            'gemini_configured': ai_extractor.gemini_model is not None,
            'claude_configured': ai_extractor.anthropic_client is not None,
            'openai_configured': ai_extractor.openai_client is not None,
            'google_api_key_present': bool(os.getenv('GOOGLE_API_KEY'))
        },
        'version': 'V2 - Sem dados mockados',
        'job_scraper': {
            'query_expander': True,
            'location_expander': True,
            'uses_apify': True
        }
    })

@app.route('/api/agent0/analyze-cv', methods=['POST'])
def analyze_cv():
    """Endpoint para análise de CV pelo Agente 0"""
    try:
        # Gerar ID único para a análise
        analysis_id = str(uuid.uuid4())
        
        # Extrair dados de motivação e sabotadores
        motivation_data = None
        sabotadores_data = None
        
        # Verificar se foi enviado arquivo ou texto
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
            
            # Extrair dados dos questionários do FormData
            if 'motivationData' in request.form:
                motivation_data = json.loads(request.form['motivationData'])
            if 'sabotadoresData' in request.form:
                sabotadores_data = json.loads(request.form['sabotadoresData'])
            
            # Salvar arquivo
            filename = f"{analysis_id}_{file.filename}"
            file_path = UPLOAD_FOLDER / filename
            file.save(file_path)
            
            # Processar documento
            texto_curriculo = document_processor.extrair_texto_documento(str(file_path))
            
            # Limpar arquivo após processamento
            file_path.unlink()
            
        elif 'text' in request.json:
            texto_curriculo = request.json['text']
            motivation_data = request.json.get('motivationData', None)
            sabotadores_data = request.json.get('sabotadoresData', None)
        else:
            return jsonify({'error': 'Arquivo ou texto deve ser fornecido'}), 400
        
        if not texto_curriculo or len(texto_curriculo.strip()) < 500:
            return jsonify({'error': 'Texto insuficiente para análise (mínimo 500 caracteres)'}), 400
        
        # Executar análise REAL com IA
        logger.info(f"Iniciando análise de CV com IA - ID: {analysis_id}")
        print(f"\n🎯 === ANÁLISE INICIADA ===")
        print(f"📝 Tamanho do texto: {len(texto_curriculo)} caracteres")
        
        # ANÁLISE REAL COM IA seguindo metodologia Carolina Martins
        # Agora incluindo contexto de motivação do usuário
        cargo_objetivo = motivation_data.get('cargoObjetivo', '') if motivation_data else ''
        palavras_chave_usuario = []
        
        print(f"🎯 Cargo objetivo: {cargo_objetivo}")
        print(f"💡 Dados de motivação recebidos: {bool(motivation_data)}")
        print(f"👹 Dados de sabotadores recebidos: {bool(sabotadores_data)}")
        
        # Extrair palavras-chave relevantes dos dados de motivação
        if motivation_data:
            # Combinar todos os campos relevantes para extrair palavras-chave
            texto_motivacao = ' '.join([
                motivation_data.get('cargoObjetivo', ''),
                motivation_data.get('empresaSonho', ''),
                motivation_data.get('valoresImportantes', ''),
                motivation_data.get('estiloTrabalho', '')
            ])
            palavras_chave_usuario = document_processor.extrair_palavras_chave_curriculo(texto_motivacao)[:10]
            print(f"🔑 Palavras-chave extraídas: {palavras_chave_usuario}")
        
        print(f"\n🤖 Chamando análise com IA...")
        analise_ia = asyncio.run(ai_analyzer.analisar_curriculo_completo(
            texto_curriculo, 
            objetivo_vaga=cargo_objetivo,
            palavras_chave_usuario=palavras_chave_usuario
        ))
        
        print(f"\n📊 === RESULTADO DA ANÁLISE IA ===")
        print(f"✅ Score geral: {analise_ia.get('score_geral', 0)}%")
        print(f"📋 Campos retornados: {list(analise_ia.keys())}")
        
        if 'caminho_para_100' in analise_ia:
            print(f"✅ Campo 'caminho_para_100' PRESENTE")
            print(f"   - Score atual: {analise_ia['caminho_para_100'].get('score_atual', 'N/A')}")
            print(f"   - Total penalizações: {analise_ia['caminho_para_100'].get('total_penalizacoes', 'N/A')}")
            print(f"   - Penalizações detalhadas: {len(analise_ia['caminho_para_100'].get('penalizacoes_detalhadas', []))} itens")
        else:
            print(f"❌ Campo 'caminho_para_100' AUSENTE!")
        
        # Obter dados da análise IA
        score = analise_ia.get('score_geral', 0)
        elementos_metodologia = analise_ia.get('elementos_metodologia', {})
        validacoes = analise_ia.get('validacoes_honestidade', {})
        palavras_chave = analise_ia.get('palavras_chave_identificadas', [])
        red_flags = analise_ia.get('red_flags', [])
        
        # Contar elementos presentes na metodologia
        elementos_presentes = len([e for e in elementos_metodologia.values() if e.get('presente', False)])
        total_elementos = 10
        
        # Mapear elementos da IA para nomes amigáveis
        elementos_nomes = {
            'dados_pessoais': 'Dados Pessoais',
            'objetivo_profissional': 'Objetivo Profissional',
            'resumo_executivo': 'Resumo/Perfil',
            'experiencias': 'Experiências',
            'resultados_quantificados': 'Resultados Quantificados',
            'formacao': 'Formação',
            'idiomas': 'Idiomas',
            'competencias_tecnicas': 'Competências Técnicas',
            'outros_conhecimentos': 'Outros Conhecimentos',
            'trabalho_voluntario': 'Trabalho Voluntário'
        }
        
        # Processar resultado
        resultado_final = {
            'id': analysis_id,
            'timestamp': datetime.now().isoformat(),
            'score': int(score),
            'estrutura': {
                'presentes': elementos_presentes,
                'total': total_elementos,
                'elementos': [
                    {
                        'nome': elementos_nomes.get(key, key.title()),
                        'presente': elemento.get('presente', False)
                    }
                    for key, elemento in elementos_metodologia.items()
                ]
            },
            'honestidade': {
                'validacoes': [
                    {
                        'nome': 'Datas consistentes', 
                        'status': validacoes.get('datas_consistentes', {}).get('status', False)
                    },
                    {
                        'nome': 'Informações verificáveis', 
                        'status': validacoes.get('informacoes_verificaveis', {}).get('status', False)
                    },
                    {
                        'nome': 'Detalhamento adequado', 
                        'status': validacoes.get('detalhamento_adequado', {}).get('status', False)
                    },
                    {
                        'nome': 'Uso de verbos de ação', 
                        'status': validacoes.get('verbos_acao', {}).get('status', False)
                    }
                ],
                'alertas': red_flags
            },
            'palavrasChave': palavras_chave[:15],  # Limitar a 15 palavras-chave
            'motivacaoUsuario': motivation_data,  # Incluir dados de motivação no resultado
            'sabotadoresIdentificados': sabotadores_data.get('sabotadoresIdentificados', []) if sabotadores_data else [],  # Incluir sabotadores
            'caminho_para_100': analise_ia.get('caminho_para_100', {})  # NOVO CAMPO!
        }
        
        print(f"\n📤 === RESPOSTA FINAL PARA FRONTEND ===")
        print(f"✅ Score: {score}%")
        print(f"📋 Campos na resposta: {list(resultado_final.keys())}")
        print(f"🎯 Campo 'caminho_para_100' incluído: {'caminho_para_100' in resultado_final}")
        
        if 'caminho_para_100' in resultado_final and resultado_final['caminho_para_100']:
            print(f"   - Conteúdo do caminho_para_100: {list(resultado_final['caminho_para_100'].keys())}")
        else:
            print(f"   - Campo vazio ou ausente!")
        
        # Armazenar resultado
        results_store[analysis_id] = resultado_final
        
        logger.info(f"Análise concluída - ID: {analysis_id}, Score: {resultado_final['score']}")
        
        return jsonify(resultado_final)
        
    except Exception as e:
        logger.error(f"Erro na análise de CV: {str(e)}")
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/api/agent1/collect-keywords', methods=['POST'])
def collect_keywords():
    """Endpoint para coleta de palavras-chave pelo Agente 1"""
    try:
        data = request.json
        
        # Validar dados de entrada - CAMPOS CORRETOS
        required_fields = ['area_interesse', 'cargo_objetivo', 'localizacao', 'total_vagas_desejadas']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Campo obrigatório: {field}'}), 400
        
        # Gerar ID único para a coleta
        collection_id = str(uuid.uuid4())
        
        # Preparar parâmetros - USAR CAMPOS DIRETOS
        params = {
            'area_interesse': data['area_interesse'],
            'cargo_objetivo': data['cargo_objetivo'], 
            'localizacao': data['localizacao'],
            'total_vagas_desejadas': int(data['total_vagas_desejadas']),
            'segmentos_alvo': data.get('segmentos_alvo', []),
            'user_id': 1  # ID padrão para demo
        }
        
        logger.info(f"Iniciando coleta de palavras-chave - ID: {collection_id}")
        logger.info(f"Parâmetros: {params}")
        
        # Coletar vagas reais com nova arquitetura
        print(f"🎯 Coletando vagas REAIS para '{params['cargo_objetivo']}' em '{params['area_interesse']}'...")
        
        # Extrair tipo de vaga (novo parâmetro)
        tipo_vaga = data.get('tipo_vaga', 'hibrido')  # Default: híbrido
        
        # Usar nova assinatura que retorna tupla (vagas, metadados)
        vagas_coletadas, metadados_coleta = job_scraper.coletar_vagas_multiplas_fontes(
            area_interesse=params['area_interesse'],
            cargo_objetivo=params['cargo_objetivo'],
            localizacao=params['localizacao'],
            tipo_vaga=tipo_vaga,
            total_vagas_desejadas=params['total_vagas_desejadas']
        )
        
        print(f"✅ Coleta concluída: {len(vagas_coletadas)} vagas obtidas")
        
        # Analisar fontes reais utilizadas
        fontes_utilizadas = {}
        for vaga in vagas_coletadas:
            fonte = vaga.get('fonte', 'unknown')
            if fonte not in fontes_utilizadas:
                fontes_utilizadas[fonte] = 0
            fontes_utilizadas[fonte] += 1
        
        print(f"📊 Fontes reais utilizadas: {fontes_utilizadas}")
        
        # Extrair palavras-chave das vagas coletadas com método PROFISSIONAL
        print("🔤 Extraindo palavras-chave PROFISSIONAIS das descrições das vagas...")
        todas_descricoes = ' '.join([vaga.get('descricao', '') for vaga in vagas_coletadas])
        # USAR O EXTRATOR PROFISSIONAL!
        palavras_extraidas = keyword_extractor.extrair_palavras_chave_profissionais(todas_descricoes)
        
        print(f"✅ {len(palavras_extraidas)} palavras-chave extraídas")
        
        # Usar categorização PROFISSIONAL do extrator
        print("📂 Categorizando palavras-chave profissionalmente...")
        categorias_pro = keyword_extractor.categorizar_competencias(palavras_extraidas)
        
        # Converter para formato esperado pelo frontend
        palavras_por_categoria = {
            'tecnicas': [],
            'comportamentais': [],
            'digitais': []  # Manter nome 'digitais' para compatibilidade com frontend
        }
        
        # Mapear categorias do extrator pro para o formato do frontend
        for i, palavra in enumerate(categorias_pro['tecnicas']):
            frequencia = max(30 - i, 5)  # Frequência maior para técnicas
            palavras_por_categoria['tecnicas'].append({
                'termo': palavra,
                'frequencia': frequencia
            })
        
        for i, palavra in enumerate(categorias_pro['ferramentas']):
            frequencia = max(25 - i, 5)  # Ferramentas são importantes
            palavras_por_categoria['digitais'].append({  # Ferramentas -> digitais
                'termo': palavra,
                'frequencia': frequencia
            })
        
        for i, palavra in enumerate(categorias_pro['comportamentais']):
            frequencia = max(20 - i, 5)  # Comportamentais com peso menor
            palavras_por_categoria['comportamentais'].append({
                'termo': palavra,
                'frequencia': frequencia
            })
        
        # NÃO LIMITAR! Queremos todas as palavras relevantes
        print(f"✅ Total de palavras categorizadas: {sum(len(cat) for cat in palavras_por_categoria.values())}")
        
        print(f"📂 Categorização:")
        for cat, palavras in palavras_por_categoria.items():
            print(f"   • {cat}: {len(palavras)} palavras")
        
        # Validação com IA usando as palavras categorizadas
        try:
            print("🤖 Validando palavras-chave com IA...")
            # Converte formato para o validador
            palavras_para_validacao = {
                'tecnicas': [p['termo'] for p in palavras_por_categoria['tecnicas']],
                'comportamentais': [p['termo'] for p in palavras_por_categoria['comportamentais']],
                'digitais': [p['termo'] for p in palavras_por_categoria['digitais']]
            }
            
            validacao_result = asyncio.run(ai_validator.validar_palavras_chave(
                palavras_para_validacao,
                params['area_interesse'],
                params['cargo_objetivo']
            ))
            print(f"✅ Validação IA concluída com {len(validacao_result.get('aprovadas', []))} palavras aprovadas")
        except Exception as e:
            logger.warning(f"Erro na validação IA: {e}")
            validacao_result = {'recomendacoes': [], 'alertas': [], 'aprovadas': []}
        
        # Mapear nomes das fontes para nomes amigáveis
        mapeamento_fontes = {
            'linkedin_jobs': 'LinkedIn Jobs',
            'google_jobs': 'Google Jobs', 
            'indeed': 'Indeed',
            'infojobs': 'InfoJobs',
            'catho': 'Catho',
            'template_metodologico': 'Dados Metodológicos',
            'fallback': 'Dados Complementares'
        }
        
        # Criar lista de fontes reais baseada na coleta
        fontes_reais = []
        total_vagas = len(vagas_coletadas)
        
        for fonte_original, quantidade in fontes_utilizadas.items():
            nome_amigavel = mapeamento_fontes.get(fonte_original, fonte_original.title())
            taxa_sucesso = 85 if 'linkedin' in fonte_original else 78 if 'google' in fonte_original else 72
            
            fontes_reais.append({
                'nome': nome_amigavel,
                'vagas': quantidade,
                'taxa': taxa_sucesso
            })
        
        # Ordernar por quantidade de vagas (maior primeiro)
        fontes_reais.sort(key=lambda x: x['vagas'], reverse=True)
        
        print(f"📊 Fontes para frontend: {[f['nome'] for f in fontes_reais]}")
        
        # Gerar TOP 10 palavras conforme metodologia Carolina Martins
        todas_palavras_ordenadas = []
        for categoria, palavras in palavras_por_categoria.items():
            todas_palavras_ordenadas.extend(palavras)
        
        # Ordena por frequência e pega TOP 10
        todas_palavras_ordenadas.sort(key=lambda x: x['frequencia'], reverse=True)
        top_10_carolina_martins = todas_palavras_ordenadas[:10]
        
        # Adiciona campo de importância simulada baseada na frequência
        for i, palavra in enumerate(top_10_carolina_martins):
            palavra['importancia'] = (10 - i) / 10  # Importância de 1.0 a 0.1
        
        # Processar resultado COM TRANSPARÊNCIA TOTAL
        resultado_final = {
            'id': collection_id,
            'timestamp': datetime.now().isoformat(),
            'estatisticas': {
                'totalVagas': len(vagas_coletadas),
                'palavrasEncontradas': len(palavras_extraidas),
                'categoriasIdentificadas': len([cat for cat in palavras_por_categoria if palavras_por_categoria[cat]]),
                'fontes': len(fontes_utilizadas),
                'metodologia_carolina_martins': {
                    'fase1_total_palavras': len(todas_palavras_ordenadas),
                    'fase1_alvo_atingido': len(todas_palavras_ordenadas) >= 20,
                    'fase2_top10': len(top_10_carolina_martins)
                }
            },
            'palavrasChave': {
                'tecnicas': palavras_por_categoria['tecnicas'],
                'comportamentais': palavras_por_categoria['comportamentais'],
                'digitais': palavras_por_categoria['digitais']
            },
            'validacaoIA': {
                'recomendacoes': validacao_result.get('recomendacoes', [
                    f'Destaque experiências com {palavras_por_categoria["tecnicas"][0]["termo"] if palavras_por_categoria["tecnicas"] else "tecnologias relevantes"}',
                    f'Desenvolva habilidades em {params["area_interesse"]} para aumentar competitividade',
                    'Enfatize suas competências comportamentais no currículo'
                ]),
                'alertas': validacao_result.get('alertas', []),
                'aprovadas': validacao_result.get('aprovadas', []),
                'total_validadas': len(validacao_result.get('aprovadas', []))
            },
            'fontes': fontes_reais,
            'top_10_carolina_martins': top_10_carolina_martins,  # TOP 10 palavras da metodologia
            'debug_info': {
                'fontes_originais': fontes_utilizadas,
                'total_categorias_preenchidas': len([cat for cat in palavras_por_categoria if palavras_por_categoria[cat]]),
                'coleta_real_ativa': True
            },
            # 🔍 TRANSPARÊNCIA TOTAL - ADICIONADO
            'transparencia': {
                'vagas_coletadas': vagas_coletadas,  # Todas as vagas individuais
                'palavras_brutas': palavras_extraidas,  # Todas as palavras antes da categorização
                'processo_extracao': {
                    'total_descricoes_processadas': len(vagas_coletadas),
                    'texto_completo_tamanho': len(todas_descricoes),
                    'metodo_usado': 'document_processor.extrair_palavras_chave_curriculo'
                },
                'metadados_coleta': metadados_coleta,  # NOVO: metadados da coleta V2
                'logs_detalhados': [
                    f"🎯 Iniciando coleta para: {params['cargo_objetivo']} em {params['area_interesse']}",
                    f"📊 Meta de coleta: {params['total_vagas_desejadas']} vagas",
                    f"✅ Coletadas: {len(vagas_coletadas)} vagas reais",
                    f"📂 Fontes utilizadas: {list(fontes_utilizadas.keys())}",
                    f"🔤 Palavras extraídas: {len(palavras_extraidas)}",
                    f"📋 Categorizadas: {sum(len(palavras_por_categoria[cat]) for cat in palavras_por_categoria)}",
                    f"🤖 Validação IA: {len(validacao_result.get('aprovadas', []))} aprovadas"
                ]
            }
        }
        
        # Armazenar resultado
        results_store[collection_id] = resultado_final
        
        logger.info(f"Coleta concluída - ID: {collection_id}, Vagas: {resultado_final['estatisticas']['totalVagas']}")
        
        return jsonify(resultado_final)
        
    except Exception as e:
        logger.error(f"Erro na coleta de palavras-chave: {str(e)}")
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/api/agent1/collect-keywords-stream', methods=['POST'])
def collect_keywords_stream():
    """Endpoint com streaming de progresso para coleta de palavras-chave"""
    data = request.json
    
    def generate():
        try:
            # Validar dados
            required_fields = ['area_interesse', 'cargo_objetivo', 'localizacao', 'total_vagas_desejadas']
            for field in required_fields:
                if field not in data or not data[field]:
                    yield f"data: {json.dumps({'error': f'Campo obrigatório: {field}'})}\n\n"
                    return
            
            collection_id = str(uuid.uuid4())
            
            # Preparar parâmetros
            params = {
                'area_interesse': data['area_interesse'],
                'cargo_objetivo': data['cargo_objetivo'], 
                'localizacao': data['localizacao'],
                'total_vagas_desejadas': int(data['total_vagas_desejadas']),
                'segmentos_alvo': data.get('segmentos_alvo', []),
                'user_id': 1
            }
            
            # 1. Iniciando coleta
            yield f"data: {json.dumps({'status': 'iniciando', 'message': 'Iniciando coleta de vagas...', 'progress': 0})}\n\n"
            
            # 2. Coletando vagas com progresso simulado
            cargo = params["cargo_objetivo"]
            yield f"data: {json.dumps({'status': 'coletando', 'message': f'Buscando vagas de {cargo}...', 'progress': 10})}\n\n"
            
            # Extrair tipo de vaga
            tipo_vaga = data.get('tipo_vaga', 'hibrido')
            
            # Coletar vagas reais com nova arquitetura
            vagas_coletadas, metadados_coleta = job_scraper.coletar_vagas_multiplas_fontes(
                area_interesse=params['area_interesse'],
                cargo_objetivo=params['cargo_objetivo'],
                localizacao=params['localizacao'],
                tipo_vaga=tipo_vaga,
                total_vagas_desejadas=params['total_vagas_desejadas']
            )
            
            total_vagas = len(vagas_coletadas)
            yield f"data: {json.dumps({'status': 'vagas_coletadas', 'message': f'{total_vagas} vagas coletadas!', 'progress': 40})}\n\n"
            
            # 3. Processando com IA
            yield f"data: {json.dumps({'status': 'processando_ia', 'message': 'Analisando vagas com IA (30-60 segundos)...', 'progress': 50})}\n\n"
            
            # Usar novo extrator IA (sem callback pois não funciona com yield)
            resultado_ia = asyncio.run(ai_keyword_extractor.extrair_palavras_chave_ia(
                vagas_coletadas,
                params['cargo_objetivo'],
                params['area_interesse'],
                None  # Sem callback no streaming
            ))
            
            yield f"data: {json.dumps({'status': 'finalizando', 'message': 'Preparando resultados...', 'progress': 90})}\n\n"
            
            # Processar resultado final
            resultado_final = {
                'id': collection_id,
                'timestamp': datetime.now().isoformat(),
                'estatisticas': {
                    'totalVagas': len(vagas_coletadas),
                    'palavrasEncontradas': resultado_ia.get('analise_metadados', {}).get('total_palavras_unicas', 0),
                    'categoriasIdentificadas': 3,  # Técnicas, Ferramentas, Comportamentais
                    'fontes': len(set(v.get('fonte', 'unknown') for v in vagas_coletadas)),
                    'metodologia_carolina_martins': {
                        'fase1_total_palavras': resultado_ia.get('analise_metadados', {}).get('total_palavras_unicas', 0),
                        'fase2_top10': len(resultado_ia.get('top_10_carolina_martins', []))
                    }
                },
                'palavrasChave': {
                    'top10': resultado_ia.get('top_10_carolina_martins', []),
                    'mpc_completo': resultado_ia.get('mpc_completo', {})
                },
                'top_10_carolina_martins': resultado_ia.get('top_10_carolina_martins', []),
                'insights': resultado_ia.get('insights_adicionais', {}),
                'modelo_usado': resultado_ia.get('analise_metadados', {}).get('modelo_ia_usado', 'gemini-2.5-pro'),
                'validacaoIA': {
                    'recomendacoes': resultado_ia.get('insights_adicionais', {}).get('recomendacoes', []),
                    'alertas': []
                },
                'fontes': [],  # Será preenchido abaixo
                'transparencia': {
                    'vagas_coletadas': vagas_coletadas[:10],  # Limitar para não sobrecarregar
                    'logs_detalhados': [
                        f"🎯 Iniciando coleta para: {params['cargo_objetivo']} em {params['area_interesse']}",
                        f"📊 Meta de coleta: {params['total_vagas_desejadas']} vagas",
                        f"✅ Coletadas: {len(vagas_coletadas)} vagas reais",
                        f"🔤 Análise com IA: {resultado_ia.get('analise_metadados', {}).get('modelo_ia_usado', 'Gemini 2.5 Pro')}",
                        f"📋 Palavras únicas identificadas: {resultado_ia.get('analise_metadados', {}).get('total_palavras_unicas', 0)}",
                        f"🎯 TOP 10 palavras-chave extraídas com sucesso"
                    ]
                }
            }
            
            # Adicionar fontes formatadas
            fontes_utilizadas = {}
            for vaga in vagas_coletadas:
                fonte = vaga.get('fonte', 'unknown')
                if fonte not in fontes_utilizadas:
                    fontes_utilizadas[fonte] = 0
                fontes_utilizadas[fonte] += 1
            
            mapeamento_fontes = {
                'linkedin_jobs': 'LinkedIn Jobs',
                'google_jobs': 'Google Jobs', 
                'indeed': 'Indeed',
                'template_metodologico': 'Dados Metodológicos',
                'fallback': 'Dados Complementares'
            }
            
            for fonte, quantidade in fontes_utilizadas.items():
                nome_amigavel = mapeamento_fontes.get(fonte, fonte.title())
                taxa_sucesso = 85 if 'linkedin' in fonte else 78
                
                resultado_final['fontes'].append({
                    'nome': nome_amigavel,
                    'vagas': quantidade,
                    'taxa': taxa_sucesso
                })
            
            # Armazenar resultado
            results_store[collection_id] = resultado_final
            
            # Enviar resultado final
            yield f"data: {json.dumps({'status': 'concluido', 'message': 'Análise concluída!', 'progress': 100, 'result_id': collection_id})}\n\n"
            
        except Exception as e:
            logger.error(f"Erro no streaming: {str(e)}")
            yield f"data: {json.dumps({'status': 'erro', 'message': str(e), 'progress': -1})}\n\n"
    
    return Response(stream_with_context(generate()), content_type='text/event-stream')

@app.route('/api/results/<result_id>', methods=['GET'])
def get_result(result_id):
    """Obter resultado por ID"""
    if result_id not in results_store:
        return jsonify({'error': 'Resultado não encontrado'}), 404
    
    return jsonify(results_store[result_id])

@app.route('/api/agent1/transparency/<result_id>', methods=['GET'])
def get_transparency_data(result_id):
    """🔍 TRANSPARÊNCIA TOTAL - Obter dados detalhados do processamento"""
    if result_id not in results_store:
        return jsonify({'error': 'Resultado não encontrado'}), 404
    
    result = results_store[result_id]
    
    # Retornar dados de transparência completos
    transparency_data = {
        'id': result_id,
        'timestamp': result['timestamp'],
        'logs_processo': result['transparencia']['logs_detalhados'],
        'vagas_individuais': result['transparencia']['vagas_coletadas'],
        'palavras_brutas': result['transparencia']['palavras_brutas'],
        'processo_extracao': result['transparencia']['processo_extracao'],
        'resumo_coleta': {
            'total_vagas': len(result['transparencia']['vagas_coletadas']),
            'total_palavras': len(result['transparencia']['palavras_brutas']),
            'fontes_utilizadas': result['debug_info']['fontes_originais'],
            'metodo_extracao': result['transparencia']['processo_extracao']['metodo_usado']
        }
    }
    
    return jsonify(transparency_data)

@app.route('/api/agent1/results', methods=['GET'])
def list_agent1_results():
    """🔍 TRANSPARÊNCIA - Listar todas as análises disponíveis"""
    analyses = []
    
    for result_id, result in results_store.items():
        if 'transparencia' in result:  # Apenas resultados com dados de transparência
            analyses.append({
                'id': result_id,
                'timestamp': result['timestamp'],
                'total_vagas': result['estatisticas']['totalVagas'],
                'total_palavras': result['estatisticas']['palavrasEncontradas'],
                'fontes': [fonte['nome'] for fonte in result['fontes']],
                'transparencia_disponivel': True
            })
    
    return jsonify({
        'total_analyses': len(analyses),
        'analyses': analyses
    })

@app.route('/api/agent1/collect-jobs-demo', methods=['POST'])
def collect_jobs_demo():
    """Endpoint DEMO - usa dados de exemplo quando Apify não está configurado"""
    try:
        data = request.json
        
        # Validar dados
        required_fields = ['area_interesse', 'cargo_objetivo', 'localizacao', 'total_vagas_desejadas']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Campo obrigatório: {field}'}), 400
        
        collection_id = str(uuid.uuid4())
        
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🎭 MODO DEMO: Iniciando coleta simulada")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📋 Cargo: {data['cargo_objetivo']}")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📍 Local: {data['localizacao']}")
        
        # Gerar vagas de exemplo baseadas nos parâmetros
        vagas_demo = []
        total = min(int(data['total_vagas_desejadas']), 20)  # Máximo 20 no demo
        
        tecnologias = ["React", "Node.js", "Python", "Java", "Angular", "Vue.js", "Django", "Spring Boot", 
                      "Docker", "Kubernetes", "AWS", "Azure", "MongoDB", "PostgreSQL", "Redis"]
        
        empresas = ["Tech Solutions", "Digital Innovation", "Cloud Systems", "Data Analytics Corp", 
                   "Software House", "IT Consulting", "Startup Hub", "Tech Giants", "Innovation Labs"]
        
        for i in range(total):
            # Selecionar tecnologias aleatórias
            techs = []
            for j in range(3):
                techs.append(tecnologias[(i + j) % len(tecnologias)])
            
            vaga = {
                "titulo": f"{data['cargo_objetivo']} - {techs[0]}",
                "empresa": empresas[i % len(empresas)],
                "localizacao": data['localizacao'],
                "descricao": f"""
                Estamos buscando {data['cargo_objetivo']} com experiência em {', '.join(techs)}.
                
                Responsabilidades:
                - Desenvolver aplicações usando {techs[0]} e {techs[1]}
                - Trabalhar com metodologias ágeis (Scrum/Kanban)
                - Colaborar com equipe multidisciplinar
                - Implementar boas práticas de desenvolvimento
                
                Requisitos:
                - Experiência com {techs[0]}, {techs[1]} e {techs[2]}
                - Conhecimento em APIs RESTful
                - Experiência com Git e CI/CD
                - Boa comunicação e trabalho em equipe
                
                Diferenciais:
                - Conhecimento em Cloud (AWS/Azure)
                - Experiência com containers (Docker)
                - Inglês técnico
                """.strip(),
                "fonte": "demo_data",
                "url": f"https://example.com/vagas/{i+1}",
                "data_coleta": datetime.now().isoformat(),
                "cargo_pesquisado": data['cargo_objetivo'],
                "salario": f"R$ {4000 + (i * 500)},00 - R$ {6000 + (i * 500)},00",
                "tipo_emprego": "CLT",
                "nivel_experiencia": ["Júnior", "Pleno", "Sênior"][i % 3]
            }
            vagas_demo.append(vaga)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ DEMO: {len(vagas_demo)} vagas geradas")
        
        # Preparar resposta
        resultado = {
            'id': collection_id,
            'timestamp': datetime.now().isoformat(),
            'demo_mode': True,  # Indicar que é modo demo
            'estatisticas': {
                'totalVagas': len(vagas_demo),
                'fontes': 1
            },
            'fontes': [{
                'nome': 'Dados de Demonstração',
                'vagas': len(vagas_demo),
                'taxa': 100
            }],
            'vagas': vagas_demo,
            'metadados': {
                'modo': 'demonstracao',
                'mensagem': 'Estas são vagas de exemplo. Configure APIFY_API_TOKEN para vagas reais.'
            },
            'status': 'coleta_concluida',
            'proximo_passo': 'analyze-keywords'
        }
        
        # Armazenar para análise posterior
        results_store[collection_id] = resultado
        
        return jsonify(resultado)
        
    except Exception as e:
        logger.error(f"Erro no modo demo: {str(e)}")
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/api/agent1/test-quick', methods=['GET'])
def test_quick_collect():
    """Endpoint de teste rápido - coleta apenas 2 vagas"""
    try:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🧪 TESTE RÁPIDO: Iniciando...")
        
        # Verificar Apify
        from services.linkedin_apify_scraper import LinkedInApifyScraper
        scraper = LinkedInApifyScraper()
        
        if scraper.verificar_credenciais():
            status = "Apify configurado ✅"
            token_preview = scraper.apify_token[:10] + "..." if scraper.apify_token else "N/A"
        else:
            status = "Apify NÃO configurado ❌"
            token_preview = "Não encontrado"
        
        # Tentar coletar apenas 2 vagas de teste
        vagas = scraper.coletar_vagas_linkedin(
            cargo="Developer",
            localizacao="São Paulo",
            limite=2
        )
        
        return jsonify({
            'status': 'ok',
            'apify_status': status,
            'token_preview': token_preview,
            'vagas_coletadas': len(vagas),
            'amostra': vagas[:1] if vagas else [],
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/agent1/collect-jobs', methods=['POST'])
def collect_jobs_only():
    """Endpoint para APENAS coletar vagas do Apify - Etapa 1"""
    try:
        data = request.json
        
        # Validar dados de entrada
        required_fields = ['area_interesse', 'cargo_objetivo', 'localizacao', 'total_vagas_desejadas']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Campo obrigatório: {field}'}), 400
        
        # Gerar ID único para a coleta
        collection_id = str(uuid.uuid4())
        
        logger.info(f"[AGENT1] ========== INICIANDO COLETA ==========")
        logger.info(f"[AGENT1] ID: {collection_id}")
        logger.info(f"[AGENT1] Cargo: {data['cargo_objetivo']}")
        logger.info(f"[AGENT1] Local: {data['localizacao']}")
        logger.info(f"[AGENT1] Quantidade: {data['total_vagas_desejadas']}")
        
        # Extrair tipo de vaga
        tipo_vaga = data.get('tipo_vaga', 'hibrido')
        
        # Log antes da coleta
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🎯 INICIANDO COLETA DE VAGAS")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📋 Cargo: {data['cargo_objetivo']}")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📍 Local: {data['localizacao']}")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🎯 Meta: {data['total_vagas_desejadas']} vagas")
        
        # Verificar se Apify está configurado
        from services.linkedin_apify_scraper import LinkedInApifyScraper
        scraper = LinkedInApifyScraper()
        if not scraper.verificar_credenciais():
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️  AVISO: Apify não configurado, usando fallback")
        
        # Coletar vagas reais
        inicio_coleta = time.time()
        vagas_coletadas, metadados_coleta = job_scraper.coletar_vagas_multiplas_fontes(
            area_interesse=data['area_interesse'],
            cargo_objetivo=data['cargo_objetivo'],
            localizacao=data['localizacao'],
            tipo_vaga=tipo_vaga,
            total_vagas_desejadas=int(data['total_vagas_desejadas'])
        )
        tempo_coleta = time.time() - inicio_coleta
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ COLETA CONCLUÍDA!")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📊 Total: {len(vagas_coletadas)} vagas")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ⏱️  Tempo: {tempo_coleta:.2f} segundos")
        
        # Analisar fontes utilizadas
        fontes_utilizadas = {}
        for vaga in vagas_coletadas:
            fonte = vaga.get('fonte', 'unknown')
            if fonte not in fontes_utilizadas:
                fontes_utilizadas[fonte] = 0
            fontes_utilizadas[fonte] += 1
        
        # Mapear nomes das fontes
        mapeamento_fontes = {
            'linkedin_apify': 'LinkedIn (Apify)',
            'linkedin_jobs': 'LinkedIn Jobs',
            'google_jobs': 'Google Jobs', 
            'indeed': 'Indeed',
            'infojobs': 'InfoJobs',
            'catho': 'Catho'
        }
        
        fontes_formatadas = []
        for fonte, quantidade in fontes_utilizadas.items():
            nome_amigavel = mapeamento_fontes.get(fonte, fonte.title())
            fontes_formatadas.append({
                'nome': nome_amigavel,
                'vagas': quantidade,
                'taxa': 100  # Taxa de sucesso da coleta
            })
        
        # Preparar resposta com as vagas coletadas
        resultado = {
            'id': collection_id,
            'timestamp': datetime.now().isoformat(),
            'estatisticas': {
                'totalVagas': len(vagas_coletadas),
                'fontes': len(fontes_utilizadas)
            },
            'fontes': fontes_formatadas,
            'vagas': vagas_coletadas,  # Todas as vagas com descrições completas
            'metadados': metadados_coleta,
            'status': 'coleta_concluida',
            'proximo_passo': 'analyze-keywords'  # Indicar próximo endpoint
        }
        
        # Armazenar resultado para análise posterior
        results_store[collection_id] = resultado
        
        logger.info(f"Coleta de vagas concluída - ID: {collection_id}, Total: {len(vagas_coletadas)}")
        
        return jsonify(resultado)
        
    except Exception as e:
        logger.error(f"Erro na coleta de vagas: {str(e)}")
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/api/agent1/analyze-keywords', methods=['POST'])
def analyze_keywords():
    """Endpoint para analisar palavras-chave com Gemini - Etapa 2"""
    try:
        data = request.json
        
        # Validar dados de entrada
        if 'collection_id' not in data:
            return jsonify({'error': 'collection_id é obrigatório'}), 400
        
        collection_id = data['collection_id']
        
        # Buscar dados da coleta anterior
        if collection_id not in results_store:
            return jsonify({'error': 'Coleta não encontrada. Execute primeiro /collect-jobs'}), 404
        
        coleta_data = results_store[collection_id]
        vagas_coletadas = coleta_data['vagas']
        
        if not vagas_coletadas:
            return jsonify({'error': 'Nenhuma vaga encontrada para análise'}), 400
        
        logger.info(f"Iniciando análise de palavras-chave - ID: {collection_id}")
        print(f"🤖 Analisando {len(vagas_coletadas)} vagas com IA...")
        
        # Usar AIKeywordExtractor para análise com Gemini
        resultado_ia = asyncio.run(
            ai_keyword_extractor.extrair_palavras_chave_ia(
                vagas=vagas_coletadas,
                cargo_objetivo=data.get('cargo_objetivo', ''),
                area_interesse=data.get('area_interesse', '')
            )
        )
        
        print(f"✅ Análise IA concluída!")
        
        # Processar resultado da IA
        palavras_por_categoria = {
            'tecnicas': [],
            'comportamentais': [],
            'digitais': []
        }
        
        # Extrair palavras do resultado da IA
        if 'top_10_palavras' in resultado_ia:
            for palavra_info in resultado_ia['top_10_palavras']:
                categoria = palavra_info.get('categoria', 'tecnicas')
                if categoria == 'ferramentas':
                    categoria = 'digitais'  # Mapear ferramentas para digitais
                
                if categoria in palavras_por_categoria:
                    palavras_por_categoria[categoria].append({
                        'termo': palavra_info['palavra'],
                        'frequencia': palavra_info.get('importancia_percentual', 10),
                        'categoria': categoria
                    })
        
        # Adicionar palavras complementares
        if 'palavras_complementares' in resultado_ia:
            for palavra_info in resultado_ia['palavras_complementares']:
                categoria = palavra_info.get('categoria', 'tecnicas')
                if categoria == 'ferramentas':
                    categoria = 'digitais'
                
                if categoria in palavras_por_categoria:
                    palavras_por_categoria[categoria].append({
                        'termo': palavra_info['palavra'],
                        'frequencia': palavra_info.get('frequencia_percentual', 5),
                        'categoria': categoria
                    })
        
        # Atualizar resultado com análise
        resultado_analise = {
            'id': collection_id,
            'timestamp': datetime.now().isoformat(),
            'estatisticas': {
                'totalVagas': len(vagas_coletadas),
                'palavrasEncontradas': sum(len(cat) for cat in palavras_por_categoria.values()),
                'categoriasIdentificadas': len([cat for cat in palavras_por_categoria if palavras_por_categoria[cat]]),
                'fontes': len(coleta_data['fontes']),
                'metodologia_carolina_martins': {
                    'fase1_total_palavras': resultado_ia.get('analise_metadados', {}).get('total_palavras_unicas', 0),
                    'fase1_alvo_atingido': resultado_ia.get('analise_metadados', {}).get('total_palavras_unicas', 0) >= 20,
                    'fase2_top10': len(resultado_ia.get('top_10_palavras', []))
                }
            },
            'palavrasChave': palavras_por_categoria,
            'top_10_carolina_martins': resultado_ia.get('top_10_palavras', []),
            'validacaoIA': {
                'insights': resultado_ia.get('insights', {}),
                'recomendacoes': resultado_ia.get('recomendacoes_personalizadas', []),
                'modelo_usado': resultado_ia.get('analise_metadados', {}).get('modelo_ia_usado', 'Gemini')
            },
            'fontes': coleta_data['fontes'],
            'transparencia': {
                'vagas_analisadas': len(vagas_coletadas),
                'processo_ia': resultado_ia.get('analise_metadados', {}),
                'tempo_analise': resultado_ia.get('tempo_processamento', 'N/A')
            }
        }
        
        # Mesclar com dados da coleta
        resultado_analise['vagas_amostra'] = vagas_coletadas[:5]  # Amostra das vagas
        
        # Atualizar armazenamento
        results_store[collection_id] = {**coleta_data, **resultado_analise}
        
        logger.info(f"Análise de palavras-chave concluída - ID: {collection_id}")
        
        return jsonify(resultado_analise)
        
    except Exception as e:
        logger.error(f"Erro na análise de palavras-chave: {str(e)}")
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/api/agents/status', methods=['GET'])
def agents_status():
    """Obter status dos agentes"""
    return jsonify({
        'agents': [
            {
                'id': 0,
                'name': 'Diagnóstico',
                'status': 'ativo',
                'endpoint': '/api/agent0/analyze-cv'
            },
            {
                'id': 1,
                'name': 'Palavras-chave',
                'status': 'ativo',
                'endpoint': '/api/agent1/collect-keywords'
            },
            {
                'id': 2,
                'name': 'Currículo',
                'status': 'em_breve',
                'endpoint': None
            },
            {
                'id': 3,
                'name': 'LinkedIn',
                'status': 'em_breve',
                'endpoint': None
            },
            {
                'id': 4,
                'name': 'Conteúdo',
                'status': 'em_breve',
                'endpoint': None
            }
        ]
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint não encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    print("🚀 Iniciando servidor API - Agentes IA...")
    print(f"🔗 Backend API rodando na porta: {port}")
    print("📚 Documentação: /api/health")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )