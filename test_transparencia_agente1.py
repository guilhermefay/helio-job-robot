#!/usr/bin/env python3
"""
🔍 SCRIPT DE TESTE - TRANSPARÊNCIA TOTAL DO AGENTE 1
Este script demonstra como acessar os dados completos de transparência do Agente 1
"""

import requests
import json
import time
from datetime import datetime

def test_transparencia_completa():
    """Testa a transparência completa do Agent 1"""
    
    BASE_URL = "http://localhost:5001/api"
    
    print("=" * 80)
    print("🔍 TESTE DE TRANSPARÊNCIA TOTAL - AGENTE 1")
    print("=" * 80)
    
    # PASSO 1: Executar coleta de palavras-chave
    print("🎯 PASSO 1: Executando coleta de palavras-chave...")
    
    payload = {
        "area_interesse": "tecnologia",
        "cargo_objetivo": "desenvolvedor python",
        "localizacao": "São Paulo, SP",
        "total_vagas_desejadas": 20
    }
    
    try:
        response = requests.post(f"{BASE_URL}/agent1/collect-keywords", json=payload)
        if response.status_code == 200:
            result = response.json()
            result_id = result['id']
            print(f"✅ Coleta executada com sucesso! ID: {result_id}")
            
            # Mostrar resumo básico
            print(f"📊 Resumo: {result['estatisticas']['totalVagas']} vagas, {result['estatisticas']['palavrasEncontradas']} palavras")
            print(f"📂 Fontes: {[f['nome'] for f in result['fontes']]}")
        else:
            print(f"❌ Erro na coleta: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return
    
    # PASSO 2: Acessar dados de transparência
    print(f"\n🔍 PASSO 2: Acessando dados de transparência para ID: {result_id}")
    
    try:
        transparency_response = requests.get(f"{BASE_URL}/agent1/transparency/{result_id}")
        if transparency_response.status_code == 200:
            transparency_data = transparency_response.json()
            
            print("✅ Dados de transparência obtidos!")
            print(f"📅 Timestamp: {transparency_data['timestamp']}")
            print(f"📊 Resumo da coleta:")
            print(f"   • Total de vagas: {transparency_data['resumo_coleta']['total_vagas']}")
            print(f"   • Total de palavras: {transparency_data['resumo_coleta']['total_palavras']}")
            print(f"   • Fontes utilizadas: {list(transparency_data['resumo_coleta']['fontes_utilizadas'].keys())}")
            print(f"   • Método de extração: {transparency_data['resumo_coleta']['metodo_extracao']}")
            
            # Mostrar logs detalhados
            print("\n📋 LOGS DETALHADOS DO PROCESSO:")
            for i, log in enumerate(transparency_data['logs_processo'], 1):
                print(f"   {i}. {log}")
            
            # Mostrar primeiras 5 vagas coletadas
            print("\n📄 PRIMEIRAS 5 VAGAS COLETADAS:")
            for i, vaga in enumerate(transparency_data['vagas_individuais'][:5], 1):
                print(f"   {i}. {vaga['titulo']} - {vaga['empresa']} ({vaga['fonte']})")
                print(f"      Descrição: {vaga['descricao'][:100]}...")
                print()
            
            # Mostrar primeiras 20 palavras brutas
            print("🔤 PRIMEIRAS 20 PALAVRAS EXTRAÍDAS:")
            for i, palavra in enumerate(transparency_data['palavras_brutas'][:20], 1):
                print(f"   {i}. {palavra}")
            
            # Salvar dados completos em arquivo
            filename = f"transparencia_agente1_{result_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(transparency_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 Dados completos salvos em: {filename}")
            
        else:
            print(f"❌ Erro ao obter transparência: {transparency_response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao acessar transparência: {e}")
    
    # PASSO 3: Listar todas as análises
    print("\n📋 PASSO 3: Listando todas as análises disponíveis...")
    
    try:
        list_response = requests.get(f"{BASE_URL}/agent1/results")
        if list_response.status_code == 200:
            analyses = list_response.json()
            print(f"✅ {analyses['total_analyses']} análises encontradas:")
            
            for analysis in analyses['analyses']:
                print(f"   • ID: {analysis['id']}")
                print(f"     Data: {analysis['timestamp']}")
                print(f"     Vagas: {analysis['total_vagas']}, Palavras: {analysis['total_palavras']}")
                print(f"     Fontes: {', '.join(analysis['fontes'])}")
                print(f"     Transparência: {'✅' if analysis['transparencia_disponivel'] else '❌'}")
                print()
        else:
            print(f"❌ Erro ao listar análises: {list_response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao listar análises: {e}")
    
    print("=" * 80)
    print("🎉 TESTE DE TRANSPARÊNCIA CONCLUÍDO!")
    print("=" * 80)
    print("\n🔍 COMO USAR A TRANSPARÊNCIA:")
    print("1. Execute uma coleta: POST /api/agent1/collect-keywords")
    print("2. Obtenha o ID do resultado")
    print("3. Acesse transparência: GET /api/agent1/transparency/{result_id}")
    print("4. Liste todas as análises: GET /api/agent1/results")
    print("\n💡 Os dados incluem:")
    print("   • Todas as vagas coletadas individualmente")
    print("   • Todas as palavras-chave extraídas")
    print("   • Logs detalhados do processo")
    print("   • Informações sobre fontes e métodos usados")

if __name__ == "__main__":
    test_transparencia_completa()