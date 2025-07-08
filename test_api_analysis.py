#!/usr/bin/env python3
"""
Script para testar a API de análise de currículo
"""
import requests
import json

# URL da API
API_URL = "http://localhost:5001/api/agent0/analyze-cv"

# Currículo problemático do teste
CURRICULO_TESTE = """
CURRICULUM VITAE

Nome: José da Silva
CPF: 123.456.789-00
Data de Nascimento: 15/03/1985
Estado Civil: Casado
Filhos: 2
Signo: Áries
Time de Futebol: Flamengo
Altura: 1,75m
Peso: 80kg
Email: josezinho123@hotmail.com
Telefone: (11) 99999-9999

OBJETIVO
Busco uma oportunidade de trabalho

EXPERIÊNCIA PROFISSIONAL

Analista de Sistemas - Empresa XYZ (2019 - 2023)
- Trabalhei quando dava vontade
- Fazia umas coisas de computador
- Às vezes chegava no horário
- Não lembro direito o que fazia

Estagiário - Empresa ABC (2017 - 2019)
- Fazia café para o pessoal
- Respondia email às vezes
- Tinha um computador legal

FORMAÇÃO
Faculdade de Tecnologia (2015 - 2019)
- Acho que me formei em alguma coisa de TI

IDIOMAS
- Português: Nativo
- Inglês: More or less

HOBBIES
- Jogar videogame
- Assistir Netflix
- Dormir até tarde nos finais de semana
- Comer pizza

INFORMAÇÕES ADICIONAIS
- Não gosto de acordar cedo
- Prefiro trabalhar de casa
- Tenho um gato chamado Miau
"""

# Dados de motivação simulados
MOTIVATION_DATA = {
    "cargoObjetivo": "Desenvolvedor Full Stack Senior",
    "empresaSonho": "Google",
    "valoresImportantes": "Inovação, trabalho em equipe",
    "estiloTrabalho": "Remoto com flexibilidade"
}

SABOTADORES_DATA = {
    "sabotadoresIdentificados": ["Procrastinação", "Falta de foco"]
}

def testar_api():
    """Testa a API de análise"""
    print("🚀 Testando API de análise de currículo...")
    print("=" * 80)
    
    # Preparar dados da requisição
    payload = {
        "text": CURRICULO_TESTE,
        "motivationData": MOTIVATION_DATA,
        "sabotadoresData": SABOTADORES_DATA
    }
    
    try:
        # Fazer requisição
        print("📡 Enviando requisição para API...")
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            resultado = response.json()
            
            print("\n✅ Resposta recebida com sucesso!")
            print("=" * 80)
            
            # Mostrar resultados
            print(f"\n📊 Score Geral: {resultado.get('score', 'N/A')}%")
            
            # Estrutura
            estrutura = resultado.get('estrutura', {})
            print(f"\n📋 Elementos Presentes: {estrutura.get('presentes', 0)}/{estrutura.get('total', 0)}")
            
            if 'elementos' in estrutura:
                print("\nDetalhamento:")
                for elem in estrutura['elementos']:
                    status = "✅" if elem.get('presente') else "❌"
                    print(f"   {status} {elem.get('nome')}")
            
            # Honestidade
            honestidade = resultado.get('honestidade', {})
            print("\n🔍 Validações de Honestidade:")
            for validacao in honestidade.get('validacoes', []):
                status = "✅" if validacao.get('status') else "❌"
                print(f"   {status} {validacao.get('nome')}")
            
            # Alertas
            alertas = honestidade.get('alertas', [])
            if alertas:
                print("\n🚨 Alertas:")
                for alerta in alertas:
                    print(f"   - {alerta}")
            
            # Palavras-chave
            palavras = resultado.get('palavrasChave', [])
            if palavras:
                print(f"\n🔑 Palavras-chave identificadas: {', '.join(palavras[:5])}...")
            
            # Salvar resposta completa para debug
            with open('api_response_debug.json', 'w', encoding='utf-8') as f:
                json.dump(resultado, f, ensure_ascii=False, indent=2)
            print("\n💾 Resposta completa salva em: api_response_debug.json")
            
        else:
            print(f"\n❌ Erro na requisição: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Erro: Não foi possível conectar à API")
        print("   Certifique-se de que o servidor está rodando em http://localhost:5001")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")

if __name__ == "__main__":
    testar_api()