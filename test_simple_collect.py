#!/usr/bin/env python3
"""
Teste simples da coleta de vagas
"""

import os
import sys
from dotenv import load_dotenv

# Adicionar o diretório core ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

load_dotenv()

from services.linkedin_apify_scraper import LinkedInApifyScraper

def test_apify_direct():
    """Testa o Apify diretamente"""
    print("🔍 Testando Apify diretamente...")
    
    scraper = LinkedInApifyScraper()
    
    # Verificar credenciais
    if scraper.verificar_credenciais():
        print("✅ Apify configurado corretamente!")
        print(f"   Token presente: Sim")
        print(f"   Actor ID: {scraper.actor_id}")
    else:
        print("❌ Apify NÃO está configurado!")
        print("   Configure APIFY_API_TOKEN no arquivo .env")
        return
    
    # Tentar coletar apenas 3 vagas
    print("\n📋 Coletando 3 vagas de teste...")
    vagas = scraper.coletar_vagas_linkedin(
        cargo="Desenvolvedor",
        localizacao="São Paulo, Brazil",
        limite=3
    )
    
    print(f"\n✅ {len(vagas)} vagas coletadas")
    
    for i, vaga in enumerate(vagas):
        print(f"\nVaga {i+1}:")
        print(f"  - Título: {vaga.get('titulo', 'N/A')}")
        print(f"  - Empresa: {vaga.get('empresa', 'N/A')}")
        print(f"  - Fonte: {vaga.get('fonte', 'N/A')}")
        print(f"  - Tem descrição: {'Sim' if vaga.get('descricao') and vaga['descricao'] != 'Descrição não disponível' else 'Não'}")

if __name__ == "__main__":
    test_apify_direct()