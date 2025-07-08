"""
Teste rápido do ScraperAPI com LinkedIn
Usa sua API key para coletar vagas REAIS
"""

import os
import sys

# Adiciona o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.services.linkedin_scraper_pro import LinkedInScraperPro

def testar_scraperapi():
    """Testa coleta de vagas do LinkedIn com ScraperAPI"""
    
    print("=" * 80)
    print("🚀 TESTE SCRAPERAPI - LINKEDIN JOBS REAL")
    print("=" * 80)
    
    # Sua API key
    os.environ['SCRAPERAPI_KEY'] = 'e7eb1cbb0b91a928ed304ec7ac74439f'
    
    # Parâmetros de teste
    cargo = "analista de marketing"
    localizacao = "São Paulo"
    limite = 10  # Começa com poucas para testar
    
    print(f"\n📋 Buscando vagas:")
    print(f"   Cargo: {cargo}")
    print(f"   Local: {localizacao}")
    print(f"   Limite: {limite} vagas")
    print(f"   API Key: e7eb1c...39f ✅")
    
    # Cria o scraper
    scraper = LinkedInScraperPro()
    
    # Coleta vagas
    print("\n🔍 Coletando vagas do LinkedIn...")
    vagas = scraper.coletar_vagas_linkedin(cargo, localizacao, limite)
    
    # Exibe resultados
    print("\n" + "=" * 80)
    print(f"📊 RESULTADOS: {len(vagas)} vagas coletadas")
    print("=" * 80)
    
    if vagas:
        for i, vaga in enumerate(vagas, 1):
            print(f"\n📄 VAGA {i}:")
            print(f"   Título: {vaga.get('titulo', 'N/A')}")
            print(f"   Empresa: {vaga.get('empresa', 'N/A')}")
            print(f"   Local: {vaga.get('localizacao', 'N/A')}")
            print(f"   Fonte: {vaga.get('fonte', 'N/A')}")
            print(f"   URL: {vaga.get('url', 'N/A')[:80]}...")
            
            # Mostra parte da descrição se disponível
            desc = vaga.get('descricao', '')
            if desc:
                print(f"   Descrição: {desc[:150]}...")
            
            # Informações extras se disponíveis
            if vaga.get('salario'):
                print(f"   Salário: {vaga.get('salario')}")
            if vaga.get('tipo_emprego'):
                print(f"   Tipo: {vaga.get('tipo_emprego')}")
            if vaga.get('data_publicacao'):
                print(f"   Publicado: {vaga.get('data_publicacao')}")
    else:
        print("\n⚠️  Nenhuma vaga foi coletada.")
        print("💡 Possíveis razões:")
        print("   - LinkedIn pode ter mudado a estrutura")
        print("   - Tente com outros termos de busca")
        print("   - Verifique se a API key está ativa")
    
    # Estatísticas
    print("\n" + "=" * 80)
    print("📈 ESTATÍSTICAS:")
    print("=" * 80)
    
    # Conta por fonte
    fontes = {}
    for vaga in vagas:
        fonte = vaga.get('fonte', 'desconhecida')
        fontes[fonte] = fontes.get(fonte, 0) + 1
    
    for fonte, count in fontes.items():
        print(f"   {fonte}: {count} vagas")
    
    # Custo estimado
    custo_estimado = len(vagas) * 0.001  # $0.001 por request
    print(f"\n💰 Custo estimado: ${custo_estimado:.3f}")
    print(f"   Requests restantes no trial: ~{5000 - len(vagas)}")
    
    print("\n✅ Teste concluído!")
    
    return vagas

if __name__ == "__main__":
    vagas = testar_scraperapi()
    
    # Salva resultado para análise
    if vagas:
        import json
        with open('scraperapi_resultado.json', 'w', encoding='utf-8') as f:
            json.dump(vagas, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Resultado salvo em: scraperapi_resultado.json")