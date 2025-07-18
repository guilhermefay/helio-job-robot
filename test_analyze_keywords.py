#!/usr/bin/env python3
"""
Script para testar o endpoint de análise de palavras-chave do Agent1
"""

import requests
import json
import time

# Configuração
BASE_URL = "http://localhost:5001"
ENDPOINT = f"{BASE_URL}/api/agent1/analyze-keywords-stream"

# Dados de teste - vamos usar uma vaga de exemplo
test_data = {
    "vagas": [
        {
            "titulo": "Desenvolvedor Python Senior",
            "empresa": "Tech Company",
            "descricao": """
            Buscamos desenvolvedor Python com experiência em Django, Flask e FastAPI.
            Conhecimentos em Docker, Kubernetes e AWS são diferenciais.
            Experiência com bancos de dados PostgreSQL e MongoDB.
            Inglês fluente é obrigatório.
            """,
            "localizacao": "São Paulo, SP",
            "link": "https://example.com/vaga1"
        },
        {
            "titulo": "Engenheiro de Dados",
            "empresa": "Data Corp",
            "descricao": """
            Procuramos engenheiro de dados com experiência em Python, Spark e Airflow.
            Conhecimentos em AWS, especialmente S3, EMR e Glue.
            Experiência com SQL e modelagem de dados.
            Conhecimento em machine learning é um diferencial.
            """,
            "localizacao": "Rio de Janeiro, RJ",
            "link": "https://example.com/vaga2"
        }
    ],
    "cargo_objetivo": "Desenvolvedor Python",
    "area_interesse": "Engenharia de Software"
}

def test_analyze_keywords():
    print("🔍 Testando endpoint de análise de palavras-chave...")
    print(f"URL: {ENDPOINT}")
    print(f"Número de vagas: {len(test_data['vagas'])}")
    print("-" * 50)
    
    try:
        # Fazer a requisição
        response = requests.post(
            ENDPOINT,
            json=test_data,
            headers={'Content-Type': 'application/json'},
            stream=True
        )
        
        if response.status_code != 200:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(f"Resposta: {response.text}")
            return
        
        print("✅ Conexão estabelecida com sucesso!")
        print("\n📊 Recebendo análise em tempo real:\n")
        
        # Processar o stream
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    try:
                        data = json.loads(line_str[6:])
                        
                        if data.get('status'):
                            print(f"📌 Status: {data['status']}")
                            if data.get('message'):
                                print(f"   Mensagem: {data['message']}")
                            if data.get('progress'):
                                print(f"   Progresso: {data['progress']}%")
                        
                        if data.get('keywords'):
                            print("\n🎯 Palavras-chave encontradas:")
                            print(json.dumps(data['keywords'], indent=2, ensure_ascii=False))
                        
                        if data.get('error'):
                            print(f"\n❌ Erro: {data['error']}")
                            
                    except json.JSONDecodeError as e:
                        print(f"⚠️ Erro ao decodificar JSON: {e}")
                        print(f"   Linha: {line_str}")
        
        print("\n✅ Análise concluída!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor.")
        print("   Verifique se o backend está rodando em http://localhost:8000")
    except Exception as e:
        print(f"❌ Erro inesperado: {type(e).__name__}: {e}")

if __name__ == "__main__":
    print("🚀 Teste do Agent1 - Análise de Palavras-chave")
    print("=" * 50)
    test_analyze_keywords()