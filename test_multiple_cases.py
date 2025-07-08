#!/usr/bin/env python3
"""
Script para testar múltiplos casos de currículo
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

# Caso 1: Currículo problemático (esperado: ~25%)
CURRICULO_RUIM = """
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

FORMAÇÃO
Faculdade de Tecnologia (2015 - 2019)
- Acho que me formei em alguma coisa de TI

HOBBIES
- Jogar videogame
- Assistir Netflix
"""

# Caso 2: Currículo médio (esperado: ~50-60%)
CURRICULO_MEDIO = """
João Paulo Santos
Telefone: (11) 98765-4321
Email: joao.santos@email.com
LinkedIn: linkedin.com/in/joaopaulosantos

OBJETIVO
Desenvolvedor Full Stack buscando oportunidades em empresas de tecnologia

EXPERIÊNCIA PROFISSIONAL

Desenvolvedor Pleno - Tech Solutions (2021 - 2023)
- Desenvolvimento de aplicações web usando React e Node.js
- Participação em projetos ágeis com equipe de 5 pessoas
- Criação de APIs RESTful
- Manutenção de bases de dados PostgreSQL

Desenvolvedor Júnior - StartupXYZ (2019 - 2021)
- Desenvolvimento front-end com HTML, CSS e JavaScript
- Suporte ao time sênior em projetos diversos
- Documentação de código

FORMAÇÃO
Bacharelado em Ciência da Computação - Universidade Federal (2015-2019)

IDIOMAS
- Português: Nativo
- Inglês: Intermediário

COMPETÊNCIAS TÉCNICAS
- Linguagens: JavaScript, Python, Java
- Frameworks: React, Node.js, Express
- Bancos de dados: PostgreSQL, MongoDB
- Ferramentas: Git, Docker, AWS
"""

# Caso 3: Currículo bom seguindo metodologia (esperado: ~75-85%)
CURRICULO_BOM = """
Maria Clara Ferreira
Telefone: (11) 94567-8901
Email: maria.ferreira@gmail.com
LinkedIn: linkedin.com/in/mariaclaraferreira

OBJETIVO PROFISSIONAL
Product Manager Senior especializada em produtos digitais B2B no setor financeiro

RESUMO EXECUTIVO
Product Manager com 8 anos de experiência em produtos digitais, sendo 5 anos no setor financeiro. 
Especialista em metodologias ágeis e discovery de produto, com histórico comprovado de lançamento 
de produtos que geraram mais de R$ 50M em receita. Liderança de squads multidisciplinares de até 
15 pessoas e forte atuação em estratégia de produto baseada em dados.

EXPERIÊNCIA PROFISSIONAL

Product Manager Senior - Fintech ABC (2020 - Presente)
• Liderança do desenvolvimento de nova plataforma de pagamentos que aumentou a base de clientes em 150% (de 200k para 500k usuários)
• Redução de 40% no churn através de implementação de features baseadas em pesquisa com usuários
• Aumento de 35% no NPS (de 42 para 57) através de melhorias na jornada do cliente
• Gestão de roadmap de produto com budget de R$ 5M/ano
• Implementação de processo de discovery contínuo que reduziu retrabalho em 60%

Product Manager Pleno - Banco Digital XYZ (2018 - 2020)
• Lançamento de feature de investimentos que capturou R$ 100M em AuM nos primeiros 6 meses
• Aumento de 25% na conversão do funil de onboarding através de otimizações baseadas em dados
• Redução de 30% no tempo de time-to-market através de implementação de metodologia ágil
• Liderança de squad de 8 pessoas (devs, designers, QA)

Product Analyst - Startup 123 (2015 - 2018)
• Implementação de cultura data-driven que aumentou velocidade de tomada de decisão em 40%
• Criação de dashboards que economizaram 20h/semana do time de produto
• Apoio no lançamento de 3 produtos que geraram R$ 10M em receita acumulada

FORMAÇÃO
MBA em Gestão de Produtos Digitais - FGV (2019-2021)
Bacharelado em Administração - USP (2011-2015)

CERTIFICAÇÕES
• Certified Scrum Product Owner (CSPO)
• Product Management Certificate - Product School
• Data Analytics - Google

IDIOMAS
• Português: Nativo
• Inglês: Fluente (TOEFL 110/120)
• Espanhol: Intermediário

COMPETÊNCIAS TÉCNICAS
• Ferramentas: Jira, Mixpanel, Amplitude, Figma, SQL
• Metodologias: Scrum, Kanban, Design Thinking, Lean Startup
• Analytics: Google Analytics, Tableau, Python básico para análise de dados
"""

async def testar_casos():
    """Testa múltiplos casos de currículo"""
    print("🚀 Testando múltiplos casos de currículo...")
    print("=" * 80)
    
    # Criar analisador
    analyzer = AICurriculumAnalyzer()
    
    casos = [
        ("Currículo Problemático", CURRICULO_RUIM, "25-35%"),
        ("Currículo Médio", CURRICULO_MEDIO, "50-65%"),
        ("Currículo Bom (Metodologia Carolina)", CURRICULO_BOM, "75-90%")
    ]
    
    for nome, curriculo, esperado in casos:
        print(f"\n📄 Testando: {nome}")
        print(f"   Score esperado: {esperado}")
        print("-" * 40)
        
        # Executar análise
        resultado = await analyzer.analisar_curriculo_completo(
            curriculo,
            objetivo_vaga="Cargo na área de tecnologia",
            palavras_chave_usuario=["tecnologia", "inovação", "liderança"]
        )
        
        score = resultado.get('score_geral', 'N/A')
        print(f"   ✅ Score obtido: {score}%")
        
        # Mostrar principais problemas/destaques
        red_flags = resultado.get('red_flags', [])
        if red_flags:
            print("   🚨 Problemas:")
            for flag in red_flags[:2]:  # Mostrar só os 2 primeiros
                print(f"      - {flag}")
        
        pontos_fortes = resultado.get('pontos_fortes', [])
        if pontos_fortes:
            print("   💪 Pontos fortes:")
            for ponto in pontos_fortes[:2]:  # Mostrar só os 2 primeiros
                print(f"      - {ponto}")
    
    print("\n" + "=" * 80)
    print("✅ Testes concluídos!")

if __name__ == "__main__":
    asyncio.run(testar_casos())