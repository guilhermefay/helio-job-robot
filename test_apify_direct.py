#!/usr/bin/env python3
"""
Teste direto do APIFY LinkedIn Scraper
"""
import os
import sys
from dotenv import load_dotenv
load_dotenv()

# Adicionar o path do projeto
sys.path.insert(0, '.')

from core.services.linkedin_apify_scraper import LinkedInApifyScraper

def main():
    print("🧪 TESTE DIRETO DO APIFY SCRAPER")
    print("=" * 50)
    
    # Criar instância
    scraper = LinkedInApifyScraper()
    
    # Teste de credenciais
    print("\n1. 🔑 Verificando credenciais...")
    if scraper.verificar_credenciais():
        print("   ✅ Credenciais OK!")
    else:
        print("   ❌ Problema com credenciais!")
        return
    
    # Teste de coleta
    print("\n2. 🎯 Iniciando coleta de vagas...")
    print("   Cargo: 'python developer'")
    print("   Local: 'São Paulo'")
    print("   Limite: 5 vagas (teste rápido)")
    
    try:
        vagas = scraper.coletar_vagas_linkedin(
            cargo="python developer",
            localizacao="São Paulo",
            limite=5
        )
        
        print(f"\n3. 📊 RESULTADO:")
        print(f"   Total de vagas: {len(vagas)}")
        
        if vagas:
            print(f"\n   📝 Primeira vaga:")
            primeira = vagas[0]
            for key, value in primeira.items():
                print(f"      {key}: {value}")
        else:
            print("   ❌ Nenhuma vaga encontrada!")
            
    except Exception as e:
        print(f"   🚨 ERRO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 