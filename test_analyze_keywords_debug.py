#!/usr/bin/env python3
"""
Script de teste com debug detalhado para o endpoint de análise de palavras-chave
"""

import requests
import json
import sys

# Configuração
BASE_URL = "http://localhost:5001"
ENDPOINT = f"{BASE_URL}/api/agent1/analyze-keywords-stream"

# Dados de teste mínimos
test_data = {
    "vagas": [
        {
            "titulo": "Desenvolvedor Python",
            "empresa": "Tech Co",
            "descricao": "Procuramos desenvolvedor Python com experiência.",
            "localizacao": "São Paulo",
            "link": "https://example.com/vaga"
        }
    ],
    "cargo_objetivo": "Desenvolvedor Python",
    "area_interesse": "TI"
}

def test_with_debug():
    print("🔍 Teste com DEBUG do endpoint de análise")
    print(f"URL: {ENDPOINT}")
    print(f"Dados enviados: {json.dumps(test_data, indent=2)}")
    print("-" * 50)
    
    try:
        response = requests.post(
            ENDPOINT,
            json=test_data,
            headers={'Content-Type': 'application/json'},
            stream=True
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print("-" * 50)
        
        if response.status_code != 200:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(f"Resposta: {response.text}")
            return
        
        print("📊 Stream de eventos:\n")
        
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                print(f"RAW: {line_str}")
                
                if line_str.startswith('data: '):
                    try:
                        data = json.loads(line_str[6:])
                        print(f"PARSED: {json.dumps(data, indent=2, ensure_ascii=False)}")
                    except json.JSONDecodeError as e:
                        print(f"JSON ERROR: {e}")
                
                print("-" * 30)
        
    except Exception as e:
        print(f"❌ Erro: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_with_debug()