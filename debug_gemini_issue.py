#!/usr/bin/env python3
"""
Debug script para verificar problema com Gemini e descrições de vagas
"""

import os
import sys
import json
import asyncio
from datetime import datetime
from dotenv import load_dotenv

# Adicionar o diretório core ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

# Carregar variáveis de ambiente
load_dotenv()

# Importar serviços
from services.job_scraper import JobScraper
from services.linkedin_apify_scraper import LinkedInApifyScraper
from services.ai_keyword_extractor import AIKeywordExtractor

def verificar_configuracao():
    """Verifica a configuração do sistema"""
    print("🔍 VERIFICANDO CONFIGURAÇÃO DO SISTEMA")
    print("=" * 60)
    
    # Verificar Apify
    apify_token = os.getenv('APIFY_API_TOKEN')
    print(f"✓ APIFY_API_TOKEN configurado: {bool(apify_token)}")
    if apify_token:
        print(f"  Token (primeiros 10 chars): {apify_token[:10]}...")
    
    # Verificar Google API (Gemini)
    google_key = os.getenv('GOOGLE_API_KEY')
    print(f"✓ GOOGLE_API_KEY configurado: {bool(google_key)}")
    if google_key:
        print(f"  Key (primeiros 10 chars): {google_key[:10]}...")
    
    # Verificar outras APIs
    print(f"✓ ANTHROPIC_API_KEY configurado: {bool(os.getenv('ANTHROPIC_API_KEY'))}")
    print(f"✓ OPENAI_API_KEY configurado: {bool(os.getenv('OPENAI_API_KEY'))}")
    
    print("\n")
    return bool(apify_token), bool(google_key)

def testar_coleta_vagas():
    """Testa a coleta de vagas e verifica o conteúdo"""
    print("🚀 TESTANDO COLETA DE VAGAS")
    print("=" * 60)
    
    # Criar scraper
    scraper = LinkedInApifyScraper()
    
    # Verificar credenciais
    if not scraper.verificar_credenciais():
        print("❌ Apify não configurado! Usando fallback...")
    else:
        print("✅ Apify configurado corretamente")
    
    # Coletar algumas vagas
    print("\n📊 Coletando 5 vagas de teste...")
    vagas = scraper.coletar_vagas_linkedin(
        cargo="Python Developer",
        localizacao="São Paulo, Brazil",
        limite=5
    )
    
    print(f"\n✅ {len(vagas)} vagas coletadas")
    
    # Analisar conteúdo das vagas
    print("\n📋 ANÁLISE DAS VAGAS COLETADAS:")
    print("-" * 60)
    
    for i, vaga in enumerate(vagas, 1):
        print(f"\nVAGA {i}:")
        print(f"  Título: {vaga.get('titulo', 'N/A')}")
        print(f"  Empresa: {vaga.get('empresa', 'N/A')}")
        print(f"  Fonte: {vaga.get('fonte', 'N/A')}")
        print(f"  Apify real: {vaga.get('apify_real', False)}")
        
        descricao = vaga.get('descricao', '')
        print(f"  Descrição presente: {bool(descricao)}")
        if descricao:
            print(f"  Tamanho da descrição: {len(descricao)} caracteres")
            print(f"  Primeiros 100 chars: {descricao[:100]}...")
        else:
            print("  ⚠️  DESCRIÇÃO VAZIA!")
        
        # Verificar campos extras
        print(f"  Campos disponíveis: {list(vaga.keys())}")
    
    return vagas

async def testar_extracao_ia(vagas):
    """Testa a extração de palavras-chave via IA"""
    print("\n\n🤖 TESTANDO EXTRAÇÃO VIA IA")
    print("=" * 60)
    
    if not vagas:
        print("❌ Sem vagas para testar")
        return
    
    # Criar extrator
    extractor = AIKeywordExtractor()
    
    # Verificar modelos disponíveis
    print("🔍 Modelos de IA disponíveis:")
    print(f"  Gemini: {extractor.gemini_model is not None}")
    print(f"  Claude: {extractor.anthropic_client is not None}")
    print(f"  GPT-4: {extractor.openai_client is not None}")
    
    if not any([extractor.gemini_model, extractor.anthropic_client, extractor.openai_client]):
        print("\n❌ Nenhum modelo de IA configurado!")
        return
    
    # Testar extração
    print("\n📝 Iniciando extração de palavras-chave...")
    
    try:
        resultado = await extractor.extrair_palavras_chave_ia(
            vagas=vagas,
            cargo_objetivo="Python Developer",
            area_interesse="Tecnologia",
            callback_progresso=None
        )
        
        print("\n✅ EXTRAÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"Modelo usado: {resultado.get('analise_metadados', {}).get('modelo_ia_usado', 'N/A')}")
        print(f"Total palavras únicas: {resultado.get('analise_metadados', {}).get('total_palavras_unicas', 0)}")
        
        # Mostrar TOP 10
        top_10 = resultado.get('top_10_carolina_martins', [])
        if top_10:
            print(f"\n🏆 TOP 10 PALAVRAS-CHAVE:")
            for i, palavra in enumerate(top_10[:10], 1):
                print(f"  {i}. {palavra['termo']} ({palavra['frequencia_percentual']:.1f}%)")
        
    except Exception as e:
        print(f"\n❌ ERRO NA EXTRAÇÃO: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Função principal de debug"""
    print("\n" + "="*60)
    print("🔍 DEBUG: ANÁLISE DO PROBLEMA COM DESCRIÇÕES VAZIAS")
    print("="*60 + "\n")
    
    # 1. Verificar configuração
    apify_ok, gemini_ok = verificar_configuracao()
    
    if not apify_ok and not gemini_ok:
        print("❌ Sistema não configurado corretamente!")
        print("Configure pelo menos APIFY_API_TOKEN ou GOOGLE_API_KEY no arquivo .env")
        return
    
    # 2. Testar coleta de vagas
    vagas = testar_coleta_vagas()
    
    # 3. Verificar se as descrições estão vazias
    descricoes_vazias = sum(1 for v in vagas if not v.get('descricao'))
    if descricoes_vazias > 0:
        print(f"\n⚠️  PROBLEMA DETECTADO: {descricoes_vazias}/{len(vagas)} vagas com descrição vazia!")
        
        # Verificar se é problema do Apify ou do fallback
        usando_apify = any(v.get('apify_real', False) for v in vagas)
        if usando_apify:
            print("   → Problema no processamento do Apify")
            print("   → Verificar formato de resposta do Actor")
        else:
            print("   → Usando dados de fallback (sem Apify)")
            print("   → Configure APIFY_API_TOKEN para dados reais")
    
    # 4. Testar extração com IA (se houver descrições)
    if gemini_ok and any(v.get('descricao') for v in vagas):
        asyncio.run(testar_extracao_ia(vagas))
    elif not gemini_ok:
        print("\n⚠️  Gemini não configurado - não é possível testar extração IA")
    else:
        print("\n⚠️  Sem descrições válidas para testar extração IA")
    
    print("\n" + "="*60)
    print("🏁 DEBUG CONCLUÍDO")
    print("="*60)

if __name__ == "__main__":
    main()