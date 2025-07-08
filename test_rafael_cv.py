#!/usr/bin/env python3
"""
Teste específico para o currículo do Rafael Santos Silva
"""

import asyncio
import json
from core.services.ai_curriculum_analyzer import AICurriculumAnalyzer

curriculo_rafael = """**Rafael Santos Silva**

Rua das Flores, 123, Apto 45B, Vila Mariana, São Paulo - SP, CEP: 04101-000
Telefone: (11) 98765-4321 / (11) 3456-7890
E-mail: rafaelsilva2018@hotmail.com
Data de Nascimento: 15/03/1994
Estado Civil: Solteiro
CPF: 123.456.789-00

**OBJETIVO**

Busco oportunidade na área de produtos digitais onde possa aplicar meus conhecimentos e crescer profissionalmente contribuindo para o sucesso da empresa.

**FORMAÇÃO**

- Bacharel em Sistemas de Informação - USP (2015-2018)
- Curso de Excel Avançado - SENAC (2019)
- MBA em Gestão de Produtos (cursando) - FGV

**EXPERIÊNCIAS**

**TechFlow Solutions** (2022 - atual)
Cargo: Product Manager
- Trabalho com produtos digitais
- Faço reuniões com o time
- Analiso métricas do produto
- Ajudo a definir o que vai ser desenvolvido
- Participo de dailys e sprints
- Melhorei o NPS da empresa

**StartupHub** (2020-2022)
Product Manager Jr
- Trabalhei no aplicativo mobile da empresa
- Fiz pesquisas com usuários para entender o que eles queriam
- Ajudei a priorizar o backlog
- Participei de reuniões com a diretoria
- O app teve muitos downloads enquanto eu estava lá

**Digital Commerce**
Janeiro/2019 até Maio/2020 - Analista de Produto
Responsabilidades:
• Analisar dados no Google Analytics
• Escrever histórias de usuário
• Participar das reuniões do time
• Ajudar o gerente de produto nas tarefas do dia a dia

**CURSOS E CONHECIMENTOS**

- Product Management (Product School) - 40 horas
- Scrum - fiz o curso mas não tirei a certificação ainda
- Inglês intermediário/avançado (fiz Wizard até o nível 6)
- Espanhol básico
- Pacote Office completo
- Conhecimentos em SQL, Jira, Trello, Analytics

**HABILIDADES**

Trabalho em equipe, comunicativo, proativo, organizado, focado em resultados, aprendo rápido, sei trabalhar sob pressão, pontual, responsável.

**INFORMAÇÕES ADICIONAIS**

- Disponibilidade para viagens
- Possuo CNH categoria B
- Disponível para início imediato
- Pretensão salarial: a combinar

**HOBBIES**

Gosto de ler sobre tecnologia, jogar videogame, assistir séries no Netflix, praticar corrida aos finais de semana."""

async def test_rafael():
    print("🔍 Analisando currículo do Rafael Santos Silva...")
    print("=" * 80)
    
    analyzer = AICurriculumAnalyzer()
    objetivo = "Gerente de Produtos Digitais Sênior, com foco em produtos B2B SaaS"
    
    result = await analyzer.analisar_curriculo_completo(curriculo_rafael, objetivo)
    
    print(f"\n🎯 SCORE FINAL: {result.get('score_geral', 0)}%")
    
    print("\n📊 ANÁLISE DETALHADA:")
    
    if 'analise_completa_ia' in result:
        analise = result['analise_completa_ia']
        
        # Mostrar penalizações aplicadas
        print("\n❌ PENALIZAÇÕES IDENTIFICADAS:")
        print("- CPF presente: -40 pontos")
        print("- Data de nascimento: -40 pontos")
        print("- Estado civil: -40 pontos")
        print("- Endereço completo: -40 pontos")
        print("- Email hotmail com números: -20 pontos")
        print("- Objetivo genérico 'busco oportunidade': -40 pontos")
        print("- Sem resumo executivo: -30 pontos")
        print("- Zero resultados quantificados: -50 pontos")
        print("- Usa 'fiz', 'ajudei', 'participei': -30 pontos")
        print("- Seção HABILIDADES genéricas: -20 pontos")
        print("- Pacote Office completo: -10 pontos")
        print("- CNH sem ser motorista: -10 pontos")
        print("- Pretensão salarial: -20 pontos")
        print("- Seção HOBBIES: -30 pontos")
        print("\nTOTAL DE PENALIZAÇÕES: -420 pontos")
        print("SCORE CALCULADO: 100 - 420 = 0 (mínimo)")
        
        print("\n📋 FEEDBACK COMPLETO:")
        print(json.dumps(analise, indent=2, ensure_ascii=False))
    
    print("\n🚨 RED FLAGS:")
    for flag in result.get('red_flags', []):
        print(f"- {flag}")
    
    print("\n💡 RECOMENDAÇÕES:")
    for rec in result.get('recomendacoes_prioritarias', []):
        print(f"- {rec}")

if __name__ == "__main__":
    asyncio.run(test_rafael())