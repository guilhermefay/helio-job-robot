#!/usr/bin/env python3
"""
Script para testar o analisador de currículo com IA
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Adicionar o diretório core ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from services.ai_curriculum_analyzer import AICurriculumAnalyzer

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

async def testar_analise():
    """Testa a análise do currículo"""
    print("🚀 Iniciando teste do analisador de currículo...")
    print("=" * 80)
    
    # Verificar variáveis de ambiente
    print("\n🔑 Verificando configuração de API Keys:")
    openai_key = os.getenv('OPENAI_API_KEY', '')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY', '')
    
    print(f"   OpenAI configurada: {'✅' if openai_key and 'sk-' in openai_key else '❌'}")
    print(f"   Anthropic configurada: {'✅' if anthropic_key and 'sk-' in anthropic_key else '❌'}")
    
    # Criar analisador
    analyzer = AICurriculumAnalyzer()
    
    print("\n🔍 Analisando currículo problemático...")
    print("=" * 80)
    
    # Executar análise
    resultado = await analyzer.analisar_curriculo_completo(
        CURRICULO_TESTE,
        objetivo_vaga="Desenvolvedor Full Stack Senior",
        palavras_chave_usuario=["Python", "React", "AWS", "Liderança"]
    )
    
    # Mostrar resultados
    print("\n📊 RESULTADO DA ANÁLISE:")
    print("=" * 80)
    print(f"Score Geral: {resultado.get('score_geral', 'N/A')}%")
    
    print("\n🚨 Red Flags encontrados:")
    for flag in resultado.get('red_flags', []):
        print(f"   - {flag}")
    
    print("\n📋 Elementos da Metodologia:")
    elementos = resultado.get('elementos_metodologia', {})
    for elem, info in elementos.items():
        presente = "✅" if info.get('presente', False) else "❌"
        print(f"   {elem}: {presente} (Qualidade: {info.get('qualidade', 0)}/10)")
    
    print("\n✅ Pontos Fortes:")
    for ponto in resultado.get('pontos_fortes', []):
        print(f"   - {ponto}")
    
    print("\n💡 Recomendações Prioritárias:")
    for rec in resultado.get('recomendacoes_prioritarias', []):
        print(f"   - {rec}")
    
    # Se houver análise completa da IA, mostrar mais detalhes
    if 'analise_completa_ia' in resultado:
        print("\n🤖 Análise Detalhada da IA:")
        analise_ia = resultado['analise_completa_ia']
        
        if 'analise_estrategica' in analise_ia:
            print("\n   📊 Análise Estratégica:")
            for item, dados in analise_ia['analise_estrategica'].items():
                print(f"      - {item}: {dados.get('qualidade', 0)}/10")
                print(f"        {dados.get('observacao', '')}")
        
        if 'analise_conteudo' in analise_ia:
            print("\n   📝 Análise de Conteúdo:")
            for item, dados in analise_ia['analise_conteudo'].items():
                print(f"      - {item}: {dados.get('qualidade', 0)}/10")
                print(f"        {dados.get('observacao', '')}")

if __name__ == "__main__":
    asyncio.run(testar_analise())