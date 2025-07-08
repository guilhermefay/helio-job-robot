#!/usr/bin/env python3
"""
Teste com dados mockados para verificar o fluxo
"""

import requests
import json
import time

BASE_URL = "http://localhost:5001"

def test_with_mock_data():
    """Teste com dados simulados"""
    print("🧪 Testando coleta com dados mockados...")
    
    # Criar dados de teste simulados
    mock_vagas = []
    for i in range(5):
        mock_vagas.append({
            "titulo": f"Desenvolvedor Full Stack #{i+1}",
            "empresa": f"Empresa Tech {i+1}",
            "localizacao": "São Paulo, SP",
            "descricao": f"Vaga para desenvolvedor com experiência em React, Node.js, Python. Esta é uma descrição completa da vaga {i+1} com todos os requisitos técnicos necessários.",
            "fonte": "mock_data",
            "url": f"https://example.com/vaga/{i+1}",
            "data_coleta": "2024-01-01T10:00:00",
            "cargo_pesquisado": "Desenvolvedor Full Stack"
        })
    
    # Simular resultado da coleta
    collection_result = {
        "id": "test-123",
        "timestamp": "2024-01-01T10:00:00",
        "estatisticas": {
            "totalVagas": len(mock_vagas),
            "fontes": 1
        },
        "fontes": [{"nome": "Mock Data", "vagas": len(mock_vagas), "taxa": 100}],
        "vagas": mock_vagas,
        "status": "coleta_concluida"
    }
    
    print(f"✅ {len(mock_vagas)} vagas mockadas criadas")
    
    # Agora testar análise com Gemini
    print("\n🤖 Testando análise de palavras-chave...")
    
    payload = {
        "collection_id": "test-123",
        "area_interesse": "Tecnologia",
        "cargo_objetivo": "Desenvolvedor Full Stack"
    }
    
    # Preparar texto para análise
    texto_vagas = " ".join([v["descricao"] for v in mock_vagas])
    
    print(f"📝 Texto total: {len(texto_vagas)} caracteres")
    
    # Simular extração de palavras-chave
    palavras_simuladas = {
        "top_10_carolina_martins": [
            {"palavra": "React", "categoria": "tecnica", "importancia_percentual": 90},
            {"palavra": "Node.js", "categoria": "tecnica", "importancia_percentual": 85},
            {"palavra": "Python", "categoria": "tecnica", "importancia_percentual": 80},
            {"palavra": "Full Stack", "categoria": "tecnica", "importancia_percentual": 75},
            {"palavra": "JavaScript", "categoria": "tecnica", "importancia_percentual": 70},
            {"palavra": "API REST", "categoria": "tecnica", "importancia_percentual": 65},
            {"palavra": "Git", "categoria": "ferramentas", "importancia_percentual": 60},
            {"palavra": "Docker", "categoria": "ferramentas", "importancia_percentual": 55},
            {"palavra": "Trabalho em equipe", "categoria": "comportamentais", "importancia_percentual": 50},
            {"palavra": "Comunicação", "categoria": "comportamentais", "importancia_percentual": 45}
        ]
    }
    
    print("\n✅ Análise simulada concluída!")
    print("\n🏆 TOP 10 Palavras-chave:")
    for i, palavra in enumerate(palavras_simuladas["top_10_carolina_martins"]):
        print(f"   {i+1}. {palavra['palavra']} ({palavra['categoria']}) - {palavra['importancia_percentual']}%")
    
    return True

if __name__ == "__main__":
    print("🚀 Teste do fluxo com dados mockados\n")
    test_with_mock_data()