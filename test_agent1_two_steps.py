#!/usr/bin/env python3
"""
Teste do Agente 1 com fluxo em 2 etapas:
1. Coletar vagas
2. Analisar palavras-chave
"""

import requests
import json
import time

BASE_URL = "http://localhost:5001"

def test_collect_jobs():
    """Etapa 1: Testar coleta de vagas"""
    print("🎯 ETAPA 1: Coletando vagas do Apify...")
    
    payload = {
        "area_interesse": "Tecnologia",
        "cargo_objetivo": "Desenvolvedor Full Stack",
        "localizacao": "São Paulo, SP",
        "total_vagas_desejadas": 10,
        "tipo_vaga": "hibrido"
    }
    
    response = requests.post(f"{BASE_URL}/api/agent1/collect-jobs", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Coleta concluída!")
        print(f"   - ID da coleta: {data['id']}")
        print(f"   - Total de vagas: {data['estatisticas']['totalVagas']}")
        print(f"   - Fontes: {data['estatisticas']['fontes']}")
        
        # Mostrar algumas vagas
        print("\n📋 Primeiras 3 vagas coletadas:")
        for i, vaga in enumerate(data['vagas'][:3]):
            print(f"\n   Vaga {i+1}:")
            print(f"   - Título: {vaga['titulo']}")
            print(f"   - Empresa: {vaga['empresa']}")
            print(f"   - Localização: {vaga['localizacao']}")
            print(f"   - Fonte: {vaga['fonte']}")
            print(f"   - Tem descrição: {'Sim' if vaga.get('descricao') and vaga['descricao'] != 'Descrição não disponível' else 'Não'}")
        
        return data['id']
    else:
        print(f"❌ Erro na coleta: {response.status_code}")
        print(response.json())
        return None

def test_analyze_keywords(collection_id):
    """Etapa 2: Testar análise de palavras-chave"""
    print(f"\n🤖 ETAPA 2: Analisando palavras-chave com Gemini...")
    
    payload = {
        "collection_id": collection_id,
        "area_interesse": "Tecnologia",
        "cargo_objetivo": "Desenvolvedor Full Stack"
    }
    
    response = requests.post(f"{BASE_URL}/api/agent1/analyze-keywords", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Análise concluída!")
        print(f"   - Palavras encontradas: {data['estatisticas']['palavrasEncontradas']}")
        print(f"   - Categorias: {data['estatisticas']['categoriasIdentificadas']}")
        print(f"   - Modelo usado: {data['validacaoIA']['modelo_usado']}")
        
        # Mostrar TOP 10
        if 'top_10_carolina_martins' in data:
            print("\n🏆 TOP 10 Palavras-chave (Metodologia Carolina Martins):")
            for i, palavra in enumerate(data['top_10_carolina_martins'][:10]):
                print(f"   {i+1}. {palavra.get('palavra', palavra)} ({palavra.get('categoria', 'N/A')})")
        
        # Mostrar insights
        if 'validacaoIA' in data and 'insights' in data['validacaoIA']:
            print("\n💡 Insights da IA:")
            insights = data['validacaoIA']['insights']
            if isinstance(insights, dict):
                for key, value in insights.items():
                    print(f"   - {key}: {value}")
        
        return data
    else:
        print(f"❌ Erro na análise: {response.status_code}")
        print(response.json())
        return None

if __name__ == "__main__":
    print("🚀 Teste do Agente 1 - Fluxo em 2 Etapas\n")
    
    # Etapa 1: Coletar vagas
    collection_id = test_collect_jobs()
    
    if collection_id:
        # Aguardar um pouco
        print("\n⏳ Aguardando 2 segundos antes da análise...")
        time.sleep(2)
        
        # Etapa 2: Analisar palavras-chave
        analysis_result = test_analyze_keywords(collection_id)
        
        if analysis_result:
            print("\n✅ TESTE COMPLETO COM SUCESSO!")
            print(f"   - Vagas coletadas: {analysis_result['estatisticas']['totalVagas']}")
            print(f"   - Palavras extraídas: {analysis_result['estatisticas']['palavrasEncontradas']}")
            print(f"   - Fase 1 atingida: {analysis_result['estatisticas']['metodologia_carolina_martins']['fase1_alvo_atingido']}")
    else:
        print("\n❌ Teste falhou na coleta de vagas")