#!/usr/bin/env python3
"""
Teste do processamento em lotes - verifica se o sistema divide corretamente as vagas
"""

import requests
import json
import time

BASE_URL = "http://localhost:5001"
ENDPOINT = f"{BASE_URL}/api/agent1/analyze-keywords-stream"

def criar_vagas_teste(quantidade):
    """Cria várias vagas de teste para verificar processamento em lotes"""
    vagas = []
    for i in range(quantidade):
        vagas.append({
            "titulo": f"Vaga {i+1} - Desenvolvedor {['Python', 'Java', 'JavaScript', 'React', 'Node'][i % 5]}",
            "empresa": f"Empresa {i+1}",
            "descricao": f"""
            Descrição da vaga {i+1}.
            Procuramos profissional com experiência em {['Python', 'Java', 'JavaScript', 'React', 'Node'][i % 5]}.
            Conhecimentos em {['Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP'][i % 5]} são diferenciais.
            """,
            "localizacao": f"São Paulo - {'Remoto' if i % 2 == 0 else 'Presencial'}",
            "link": f"https://example.com/vaga{i+1}"
        })
    return vagas

def test_batch(quantidade_vagas):
    print(f"\n🧪 TESTE COM {quantidade_vagas} VAGAS")
    print("=" * 60)
    
    test_data = {
        "vagas": criar_vagas_teste(quantidade_vagas),
        "cargo_objetivo": "Desenvolvedor",
        "area_interesse": "Tecnologia"
    }
    
    start_time = time.time()
    mensagens_batch = []
    
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
        
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    try:
                        data = json.loads(line_str[6:])
                        
                        # Capturar mensagens sobre processamento em lotes
                        if data.get('message'):
                            msg = data['message']
                            if 'lote' in msg.lower() or 'batch' in msg.lower():
                                mensagens_batch.append(msg)
                            print(f"→ {data.get('status', '')}: {msg}")
                        
                        if data.get('error'):
                            print(f"\n❌ ERRO: {data['error']}")
                            return
                            
                    except json.JSONDecodeError:
                        pass
        
        elapsed_time = time.time() - start_time
        
        print(f"\n📊 ESTATÍSTICAS:")
        print(f"  • Tempo total: {elapsed_time:.2f} segundos")
        print(f"  • Tempo médio por vaga: {elapsed_time/quantidade_vagas:.2f} segundos")
        
        if quantidade_vagas > 20:
            print(f"\n🔄 PROCESSAMENTO EM LOTES:")
            print(f"  • Esperado: SIM (>{20} vagas)")
            print(f"  • Lotes esperados: {quantidade_vagas // 10 + (1 if quantidade_vagas % 10 else 0)}")
            if mensagens_batch:
                print(f"  • Mensagens sobre lotes capturadas: {len(mensagens_batch)}")
                for msg in mensagens_batch[:3]:
                    print(f"    - {msg}")
        else:
            print(f"\n📝 PROCESSAMENTO ÚNICO:")
            print(f"  • Esperado: SIM (<= 20 vagas)")
        
    except Exception as e:
        print(f"❌ Erro: {type(e).__name__}: {e}")

if __name__ == "__main__":
    print("🚀 TESTE DE PROCESSAMENTO EM LOTES")
    print("=" * 60)
    print("Este teste verifica se o sistema divide corretamente as vagas em lotes")
    print("quando há mais de 20 vagas para análise.")
    
    # Testar com diferentes quantidades
    test_batch(5)    # Sem lotes (< 20)
    test_batch(25)   # Com lotes (> 20, espera 3 lotes)
    test_batch(50)   # Com lotes (> 20, espera 5 lotes)