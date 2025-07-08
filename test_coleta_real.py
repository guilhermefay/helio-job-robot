"""
Teste da coleta real de vagas
Demonstra o funcionamento do sistema com APIs reais
"""

import asyncio
import os
from dotenv import load_dotenv
from core.services.job_scraper import JobScraper

# Carrega variáveis de ambiente
load_dotenv()

async def testar_coleta_real():
    """Testa a coleta de vagas com APIs reais"""
    
    print("=" * 80)
    print("🚀 TESTE DE COLETA REAL DE VAGAS - SISTEMA HELIO")
    print("=" * 80)
    
    # Inicializa o scraper
    scraper = JobScraper()
    
    # Parâmetros de teste
    cargo = "analista de marketing"
    area = "marketing"
    localizacao = "São Paulo, SP"
    total_vagas = 20  # Começar com poucas para teste
    
    print(f"\n📋 PARÂMETROS DO TESTE:")
    print(f"   Cargo: {cargo}")
    print(f"   Área: {area}")
    print(f"   Localização: {localizacao}")
    print(f"   Total desejado: {total_vagas} vagas")
    
    # Verifica APIs configuradas
    print("\n🔐 VERIFICANDO APIS:")
    adzuna_configured = bool(os.getenv('ADZUNA_APP_ID') and os.getenv('ADZUNA_APP_KEY'))
    print(f"   Adzuna API: {'✅ Configurada' if adzuna_configured else '❌ Não configurada'}")
    
    if not adzuna_configured:
        print("\n⚠️  ATENÇÃO: Para dados 100% reais, configure as APIs no arquivo .env")
        print("   1. Copie .env.example para .env")
        print("   2. Registre-se em https://developer.adzuna.com/ (gratuito)")
        print("   3. Adicione suas chaves no .env")
    
    # Executa coleta
    print("\n🔍 INICIANDO COLETA...")
    vagas = scraper.coletar_vagas_multiplas_fontes(
        area_interesse=area,
        cargo_objetivo=cargo,
        localizacao=localizacao,
        total_vagas_desejadas=total_vagas
    )
    
    # Exibe resultados
    print("\n" + "=" * 80)
    print("📊 RESULTADOS DA COLETA")
    print("=" * 80)
    print(f"Total coletado: {len(vagas)} vagas")
    
    # Análise por fonte
    fontes = {}
    for vaga in vagas:
        fonte = vaga.get('fonte', 'desconhecida')
        fontes[fonte] = fontes.get(fonte, 0) + 1
    
    print("\n📈 BREAKDOWN POR FONTE:")
    for fonte, count in fontes.items():
        api_real = any(vaga.get('api_real') or vaga.get('scraping_real') for vaga in vagas if vaga.get('fonte') == fonte)
        status = "🟢 REAL" if api_real else "🟡 AGREGADO"
        print(f"   {fonte}: {count} vagas {status}")
    
    # Mostra exemplos de vagas
    print("\n📄 EXEMPLOS DE VAGAS COLETADAS:")
    print("-" * 80)
    
    # Mostra até 3 vagas de exemplo
    for i, vaga in enumerate(vagas[:3], 1):
        print(f"\nVAGA {i}:")
        print(f"  Título: {vaga.get('titulo', 'N/A')}")
        print(f"  Empresa: {vaga.get('empresa', 'N/A')}")
        print(f"  Local: {vaga.get('localizacao', 'N/A')}")
        print(f"  Fonte: {vaga.get('fonte', 'N/A')}")
        
        # Indica se é real ou não
        if vaga.get('api_real'):
            print(f"  Status: ✅ VAGA REAL (API)")
        elif vaga.get('scraping_real'):
            print(f"  Status: ✅ VAGA REAL (Web Scraping)")
        elif vaga.get('baseado_em_dados_reais'):
            print(f"  Status: 🟡 AGREGADO (baseado em dados reais)")
        else:
            print(f"  Status: 🟠 FALLBACK")
        
        # Mostra parte da descrição
        descricao = vaga.get('descricao', '')[:200]
        if descricao:
            print(f"  Descrição: {descricao}...")
        
        if vaga.get('url'):
            print(f"  URL: {vaga.get('url')}")
    
    # Extrai palavras-chave
    print("\n" + "-" * 80)
    print("🔤 PALAVRAS-CHAVE EXTRAÍDAS:")
    print("-" * 80)
    
    palavras_contador = scraper.extrair_palavras_chave_descricoes(vagas)
    
    # Top 10 palavras
    palavras_ordenadas = sorted(palavras_contador.items(), key=lambda x: x[1], reverse=True)[:10]
    
    for palavra, freq in palavras_ordenadas:
        percentual = (freq / len(vagas)) * 100
        print(f"  {palavra}: {freq}x ({percentual:.1f}% das vagas)")
    
    print("\n" + "=" * 80)
    print("✅ TESTE CONCLUÍDO!")
    print("=" * 80)
    
    # Instruções finais
    print("\n💡 PRÓXIMOS PASSOS:")
    print("1. Configure as APIs no .env para dados 100% reais")
    print("2. Execute o agente 1 completo: python test_agente1_real.py")
    print("3. O sistema irá coletar e analisar vagas reais automaticamente")
    
    return vagas

if __name__ == "__main__":
    # Executa o teste
    asyncio.run(testar_coleta_real())