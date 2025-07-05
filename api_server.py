#!/usr/bin/env python3
"""
API REST para integração frontend-backend do sistema HELIO
Expõe endpoints para os agentes funcionais
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import json
import logging
from pathlib import Path
import uuid
from datetime import datetime
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

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar aplicação Flask
app = Flask(__name__)
CORS(app)  # Permitir requisições do frontend

# Configurar diretório de uploads
UPLOAD_FOLDER = Path('uploads')
UPLOAD_FOLDER.mkdir(exist_ok=True)

# Inicializar serviços
document_processor = DocumentProcessor()
job_scraper = JobScraper()
ai_validator = AIValidator()
ai_analyzer = AICurriculumAnalyzer()

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
        
        # Validar dados de entrada
        required_fields = ['area', 'cargo', 'localizacao', 'quantidade']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Campo obrigatório: {field}'}), 400
        
        # Gerar ID único para a coleta
        collection_id = str(uuid.uuid4())
        
        # Preparar parâmetros
        params = {
            'area_interesse': data['area'],
            'cargo_objetivo': data['cargo'],
            'localizacao': data['localizacao'],
            'total_vagas_desejadas': int(data['quantidade']),
            'segmentos': data.get('segmentos', ''),
            'user_id': 1  # ID padrão para demo
        }
        
        logger.info(f"Iniciando coleta de palavras-chave - ID: {collection_id}")
        logger.info(f"Parâmetros: {params}")
        
        # Coletar vagas reais
        print(f"🎯 Coletando vagas REAIS para '{params['cargo_objetivo']}' em '{params['area_interesse']}'...")
        vagas_coletadas = job_scraper.coletar_vagas_multiplas_fontes(
            area_interesse=params['area_interesse'],
            cargo_objetivo=params['cargo_objetivo'],
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
        
        # Extrair palavras-chave das vagas coletadas com método aprimorado
        print("🔤 Extraindo palavras-chave das descrições das vagas...")
        todas_descricoes = ' '.join([vaga.get('descricao', '') for vaga in vagas_coletadas])
        palavras_extraidas = document_processor.extrair_palavras_chave_curriculo(todas_descricoes)
        
        print(f"✅ {len(palavras_extraidas)} palavras-chave extraídas")
        
        # Categorizar palavras-chave usando metodologia aprimorada 
        def categorizar_palavra_detalhada(palavra):
            palavra_lower = palavra.lower()
            
            # Digitais/Tecnológicas (expandido)
            if any(tech in palavra_lower for tech in [
                'excel', 'power bi', 'sql', 'python', 'java', 'javascript', 'react', 'angular',
                'tableau', 'google analytics', 'sap', 'oracle', 'crm', 'erp', 'autocad',
                'photoshop', 'word', 'powerpoint', 'teams', 'slack', 'jira', 'confluence',
                'git', 'agile', 'scrum', 'kanban', 'salesforce', 'hubspot', 'mailchimp'
            ]):
                return 'digitais'
            
            # Comportamentais (expandido)
            elif any(comp in palavra_lower for comp in [
                'liderança', 'comunicação', 'trabalho em equipe', 'gestão de equipe',
                'proatividade', 'organização', 'planejamento', 'negociação', 'relacionamento',
                'criatividade', 'inovação', 'adaptabilidade', 'flexibilidade', 'responsabilidade',
                'comprometimento', 'iniciativa', 'empatia', 'colaboração', 'motivação'
            ]):
                return 'comportamentais'
            
            # Técnicas (padrão)
            else:
                return 'tecnicas'
        
        # Categoriza palavras sem limite artificial
        palavras_por_categoria = {'tecnicas': [], 'comportamentais': [], 'digitais': []}
        
        for i, palavra in enumerate(palavras_extraidas):
            categoria = categorizar_palavra_detalhada(palavra)
            # Simula frequência baseada na posição (mais frequentes primeiro)
            frequencia = max(20 - (i // 5), 1)  # Decresce gradualmente
            palavras_por_categoria[categoria].append({
                'termo': palavra,
                'frequencia': frequencia
            })
        
        # Limita a 15 palavras por categoria para não sobrecarregar
        for categoria in palavras_por_categoria:
            palavras_por_categoria[categoria] = palavras_por_categoria[categoria][:15]
        
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
        
        # Processar resultado
        resultado_final = {
            'id': collection_id,
            'timestamp': datetime.now().isoformat(),
            'estatisticas': {
                'totalVagas': len(vagas_coletadas),
                'palavrasEncontradas': len(palavras_extraidas),
                'categoriasIdentificadas': len([cat for cat in palavras_por_categoria if palavras_por_categoria[cat]]),
                'fontes': len(fontes_utilizadas)
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
            'debug_info': {
                'fontes_originais': fontes_utilizadas,
                'total_categorias_preenchidas': len([cat for cat in palavras_por_categoria if palavras_por_categoria[cat]]),
                'coleta_real_ativa': True
            }
        }
        
        # Armazenar resultado
        results_store[collection_id] = resultado_final
        
        logger.info(f"Coleta concluída - ID: {collection_id}, Vagas: {resultado_final['estatisticas']['totalVagas']}")
        
        return jsonify(resultado_final)
        
    except Exception as e:
        logger.error(f"Erro na coleta de palavras-chave: {str(e)}")
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/api/results/<result_id>', methods=['GET'])
def get_result(result_id):
    """Obter resultado por ID"""
    if result_id not in results_store:
        return jsonify({'error': 'Resultado não encontrado'}), 404
    
    return jsonify(results_store[result_id])

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
    print("🚀 Iniciando servidor API HELIO...")
    print("🔗 Frontend: http://localhost:3000")
    print("🔗 Backend API: http://localhost:5001")
    print("📚 Documentação: http://localhost:5001/api/health")
    
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )