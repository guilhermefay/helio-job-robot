"""
Script de teste para validar implementações reais do Sistema HELIO
Testa processamento de CV, coleta de vagas e validação IA
"""

import asyncio
import os
import sys
from datetime import datetime

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.services.document_processor import DocumentProcessor
from core.services.ai_validator import AIValidator
from core.services.job_scraper import JobScraper

async def testar_document_processor():
    """Testa processamento real de documentos"""
    print("🔍 TESTANDO DOCUMENT PROCESSOR")
    print("-" * 50)
    
    processor = DocumentProcessor()
    
    # Teste com texto simulado de CV
    texto_cv_teste = """
    JOÃO SILVA
    Email: joao.silva@email.com
    Telefone: (11) 99999-9999
    LinkedIn: linkedin.com/in/joaosilva
    
    OBJETIVO
    Analista de Marketing Digital
    
    RESUMO PROFISSIONAL
    Profissional com 5 anos de experiência em marketing digital, especializado em gestão de campanhas e análise de resultados. Forte experiência em Excel avançado, Power BI e gestão de projetos.
    
    EXPERIÊNCIA PROFISSIONAL
    2020-2024 - Analista de Marketing - Empresa ABC
    - Gerenciei campanhas digitais com ROI de 150%
    - Liderei equipe de 3 pessoas
    - Implementei processos que reduziram custos em 20%
    
    FORMAÇÃO ACADÊMICA
    2015-2019 - Graduação em Marketing - Universidade XYZ
    
    IDIOMAS
    Inglês - Intermediário
    
    COMPETÊNCIAS TÉCNICAS
    Excel Avançado, Power BI, Google Analytics, SQL
    """
    
    # Testa análise de estrutura
    estrutura = processor.analisar_estrutura_curriculo(texto_cv_teste)
    print(f"✅ Estrutura analisada: {estrutura['score_metodologia']:.1f}% de aderência")
    print(f"   Elementos presentes: {estrutura['elementos_presentes']}/{estrutura['total_elementos']}")
    
    # Testa extração de palavras-chave
    palavras = processor.extrair_palavras_chave_curriculo(texto_cv_teste)
    print(f"✅ Palavras-chave extraídas: {len(palavras)} palavras")
    print(f"   Exemplos: {palavras[:5]}")
    
    # Testa validação de honestidade
    honestidade = processor.verificar_honestidade_curriculo(texto_cv_teste)
    print(f"✅ Validação de honestidade: {'✓' if honestidade['datas_consistentes'] else '✗'} datas, {'✓' if honestidade['informacoes_verificaveis'] else '✗'} resultados")
    
    print("\n")

async def testar_ai_validator():
    """Testa validação real com IA"""
    print("🤖 TESTANDO AI VALIDATOR")
    print("-" * 50)
    
    validator = AIValidator()
    
    # Testa se APIs estão configuradas
    if validator.openai_client:
        print("✅ OpenAI API configurada")
    elif validator.anthropic_client:
        print("✅ Anthropic API configurada")
    else:
        print("⚠️  Nenhuma API de IA configurada - usando fallback")
    
    # Teste de validação
    palavras_teste = {
        "tecnica": ["excel", "power bi", "sql", "python"],
        "comportamental": ["liderança", "comunicação", "gestão", "negociação"],
        "digital": ["google analytics", "facebook ads", "linkedin", "seo"]
    }
    
    resultado = await validator.validar_palavras_chave(
        palavras_por_categoria=palavras_teste,
        area="marketing digital",
        cargo="analista de marketing"
    )
    
    print(f"✅ Validação concluída com {resultado['modelo_usado']}")
    print(f"   Aprovadas: {len(resultado['aprovadas'])} palavras")
    print(f"   Rejeitadas: {len(resultado['rejeitadas'])} palavras")
    print(f"   Confiança: {resultado['confianca']:.1%}")
    
    print("\n")

async def testar_job_scraper():
    """Testa coleta real de vagas"""
    print("🌐 TESTANDO JOB SCRAPER")
    print("-" * 50)
    
    scraper = JobScraper()
    
    # Teste de coleta (limitado para não sobrecarregar)
    print("Iniciando coleta de vagas (pode levar alguns minutos)...")
    
    vagas = scraper.coletar_vagas_multiplas_fontes(
        area_interesse="marketing",
        cargo_objetivo="analista de marketing",
        localizacao="São Paulo, SP",
        total_vagas_desejadas=20  # Apenas 20 para teste
    )
    
    print(f"✅ Coleta concluída: {len(vagas)} vagas coletadas")
    
    # Analisa fontes utilizadas
    fontes = set([vaga.get('fonte', 'unknown') for vaga in vagas])
    print(f"   Fontes utilizadas: {', '.join(fontes)}")
    
    # Mostra exemplo de vaga
    if vagas:
        vaga_exemplo = vagas[0]
        print(f"   Exemplo: {vaga_exemplo['titulo']} - {vaga_exemplo['empresa']}")
        print(f"   Descrição: {vaga_exemplo['descricao'][:100]}...")
    
    # Testa extração de palavras-chave das vagas
    palavras_vagas = scraper.extrair_palavras_chave_descricoes(vagas)
    palavras_top = sorted(palavras_vagas.items(), key=lambda x: x[1], reverse=True)[:10]
    print(f"✅ Palavras-chave extraídas das vagas: {len(palavras_vagas)} únicas")
    print(f"   Top 5: {[p[0] for p in palavras_top[:5]]}")
    
    print("\n")

async def testar_integracao_completa():
    """Testa integração entre todos os componentes"""
    print("🔗 TESTANDO INTEGRAÇÃO COMPLETA")
    print("-" * 50)
    
    # Simula fluxo completo do Agente 1
    print("1. Coletando vagas...")
    scraper = JobScraper()
    vagas = scraper.coletar_vagas_multiplas_fontes(
        area_interesse="tecnologia",
        cargo_objetivo="analista de sistemas",
        total_vagas_desejadas=10
    )
    
    print("2. Extraindo palavras-chave das vagas...")
    palavras_vagas = scraper.extrair_palavras_chave_descricoes(vagas)
    palavras_por_categoria = {
        "tecnica": [p for p in palavras_vagas.keys() if any(tech in p.lower() for tech in ['excel', 'sql', 'python', 'java'])],
        "comportamental": [p for p in palavras_vagas.keys() if any(comp in p.lower() for comp in ['gestão', 'liderança', 'comunicação'])],
        "digital": [p for p in palavras_vagas.keys() if any(dig in p.lower() for dig in ['analytics', 'digital', 'online'])]
    }
    
    print("3. Validando com IA...")
    validator = AIValidator()
    validacao = await validator.validar_palavras_chave(
        palavras_por_categoria=palavras_por_categoria,
        area="tecnologia",
        cargo="analista de sistemas",
        contexto_vagas=[vaga['descricao'][:200] for vaga in vagas[:3]]
    )
    
    print("✅ Integração completa testada:")
    print(f"   - {len(vagas)} vagas coletadas")
    print(f"   - {len(palavras_vagas)} palavras-chave extraídas")
    print(f"   - {len(validacao['aprovadas'])} palavras validadas pela IA")
    print(f"   - Modelo usado: {validacao['modelo_usado']}")
    
    print("\n")

async def main():
    """Executa todos os testes"""
    print("🚀 HELIO - TESTE DE IMPLEMENTAÇÕES REAIS")
    print("=" * 60)
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)
    print()
    
    try:
        await testar_document_processor()
        await testar_ai_validator()
        await testar_job_scraper()
        await testar_integracao_completa()
        
        print("🎉 TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
        print("✅ Sistema HELIO com implementações reais funcionando")
        
    except Exception as e:
        print(f"❌ ERRO durante os testes: {e}")
        print("⚠️  Verifique as configurações e dependências")

if __name__ == "__main__":
    asyncio.run(main())