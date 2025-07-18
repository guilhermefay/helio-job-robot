#!/usr/bin/env python3
"""
Teste completo do endpoint de análise com verificação de resultado
"""

import requests
import json
import time

BASE_URL = "http://localhost:5001"
ENDPOINT = f"{BASE_URL}/api/agent1/analyze-keywords-stream"

test_data = {
    "vagas": [
        {
            "titulo": "Desenvolvedor Full Stack Python/React",
            "empresa": "Tech Solutions",
            "descricao": """
            Buscamos desenvolvedor full stack com experiência em:
            - Python (Django/FastAPI)
            - React.js e TypeScript
            - PostgreSQL e Redis
            - Docker e Kubernetes
            - CI/CD com GitLab
            - Metodologias ágeis (Scrum)
            """,
            "localizacao": "São Paulo - Remoto",
            "link": "https://example.com/vaga1"
        }
    ],
    "cargo_objetivo": "Desenvolvedor Full Stack",
    "area_interesse": "Desenvolvimento de Software"
}

def test_complete():
    print("🧪 TESTE COMPLETO DO AGENT1 - ANÁLISE DE PALAVRAS-CHAVE")
    print("=" * 60)
    
    try:
        response = requests.post(
            ENDPOINT,
            json=test_data,
            headers={'Content-Type': 'application/json'},
            stream=True
        )
        
        if response.status_code != 200:
            print(f"❌ Erro HTTP: {response.status_code}")
            return
        
        resultado_final = None
        
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    try:
                        data = json.loads(line_str[6:])
                        
                        # Mostrar progresso
                        if data.get('status'):
                            print(f"→ {data['status']}: {data.get('message', '')}")
                        
                        # Capturar resultado final
                        if data.get('resultado'):
                            resultado_final = data['resultado']
                            
                        # Verificar erros
                        if data.get('error'):
                            print(f"\n❌ ERRO: {data['error']}")
                            return
                            
                    except json.JSONDecodeError:
                        pass
        
        print("\n" + "=" * 60)
        
        if resultado_final:
            print("✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
            print("\n📊 RESULTADO DA ANÁLISE:")
            
            # Verificar estrutura esperada
            estruturas = [
                'analise_metadados',
                'top_10_palavras_chave',
                'mpc_completo'
            ]
            
            for estrutura in estruturas:
                if estrutura in resultado_final:
                    print(f"  ✓ {estrutura} presente")
                else:
                    print(f"  ✗ {estrutura} AUSENTE")
            
            # Mostrar top 10 palavras-chave
            if 'top_10_palavras_chave' in resultado_final:
                print("\n🔝 TOP 10 PALAVRAS-CHAVE:")
                for palavra in resultado_final['top_10_palavras_chave'][:5]:
                    print(f"  • {palavra}")
                if len(resultado_final['top_10_palavras_chave']) > 5:
                    print(f"  ... e mais {len(resultado_final['top_10_palavras_chave']) - 5} palavras")
            
            # Mostrar metadados
            if 'analise_metadados' in resultado_final:
                meta = resultado_final['analise_metadados']
                print(f"\n📈 METADADOS:")
                print(f"  • Modelo IA: {meta.get('modelo_ia_usado', 'N/A')}")
                print(f"  • Total palavras únicas: {meta.get('total_palavras_unicas', 'N/A')}")
                print(f"  • Total vagas: {meta.get('total_vagas', 'N/A')}")
        else:
            print("⚠️ Nenhum resultado retornado")
        
    except Exception as e:
        print(f"❌ Erro: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_complete()