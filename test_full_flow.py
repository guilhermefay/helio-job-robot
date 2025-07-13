#!/usr/bin/env python3
"""
Teste completo do fluxo de análise de palavras-chave
"""
import asyncio
import json
from core.services.ai_keyword_extractor import AIKeywordExtractor

# Simular vagas coletadas do Indeed
vagas_reais = [
    {
        "titulo": "Desenvolvedor Frontend React Pleno",
        "empresa": "Tech Solutions LTDA",
        "descricao": """
        Estamos em busca de um Desenvolvedor Frontend React Pleno para integrar nossa equipe de tecnologia.
        
        Requisitos:
        - Experiência sólida com React.js e seu ecossistema (Redux, Context API, Hooks)
        - Domínio de JavaScript ES6+ e TypeScript
        - Conhecimento avançado em HTML5, CSS3, SASS/SCSS
        - Experiência com testes unitários (Jest, React Testing Library)
        - Familiaridade com Git e metodologias ágeis (Scrum/Kanban)
        - Conhecimento em consumo de APIs REST
        - Inglês técnico para leitura
        
        Diferenciais:
        - Next.js
        - Node.js
        - AWS ou outras clouds
        - GraphQL
        - CI/CD
        
        Oferecemos:
        - Salário competitivo
        - Vale refeição e alimentação
        - Plano de saúde e odontológico
        - Home office flexível
        """
    },
    {
        "titulo": "Frontend Developer - Remote",
        "empresa": "Digital Agency Brasil",
        "descricao": """
        Join our team as a Frontend Developer!
        
        We're looking for:
        - Strong React.js skills (3+ years)
        - JavaScript/TypeScript expertise
        - CSS preprocessors (SASS, LESS)
        - Responsive design and mobile-first approach
        - Version control with Git/GitHub
        - API integration experience
        - Good communication skills
        
        Nice to have:
        - Vue.js or Angular experience
        - Backend knowledge (Node.js)
        - Docker
        - Agile methodologies
        - UI/UX design sense
        
        Benefits:
        - 100% remote work
        - Flexible hours
        - International projects
        """
    },
    {
        "titulo": "Desenvolvedor Front-end Sênior",
        "empresa": "Startup Fintech",
        "descricao": """
        Vaga para Desenvolvedor Front-end Sênior em startup fintech em crescimento.
        
        O que esperamos:
        - Expertise em React.js e JavaScript moderno
        - TypeScript é obrigatório
        - Styled Components ou Emotion
        - Testes automatizados (Jest, Cypress)
        - Arquitetura de aplicações SPA
        - Performance optimization
        - Acessibilidade web (WCAG)
        - Git flow
        
        Conhecimentos desejáveis:
        - Micro-frontends
        - Web Components
        - PWA
        - React Native
        - Backend em Node.js
        - MongoDB ou PostgreSQL
        - Kubernetes
        
        Regime: CLT ou PJ
        Local: São Paulo (híbrido)
        """
    },
    {
        "titulo": "React Developer",
        "empresa": "E-commerce Platform",
        "descricao": """
        Seeking React Developer for our e-commerce platform team.
        
        Requirements:
        - React.js (Hooks, Context)
        - State management (Redux/MobX)
        - JavaScript ES6+
        - HTML5/CSS3
        - RESTful APIs
        - Git version control
        - Unit testing
        
        Plus:
        - E-commerce experience
        - Payment gateway integration
        - SEO knowledge
        - Performance optimization
        - A/B testing
        
        We offer competitive salary and growth opportunities.
        """
    },
    {
        "titulo": "Programador Frontend Jr/Pleno",
        "empresa": "Software House",
        "descricao": """
        Oportunidade para Programador Frontend nível júnior a pleno.
        
        Requisitos básicos:
        - React.js (mínimo 1 ano)
        - JavaScript
        - HTML e CSS
        - Git básico
        - Vontade de aprender
        
        Desejável:
        - TypeScript
        - Sass
        - Webpack
        - NPM/Yarn
        - Linux
        
        Oferecemos treinamento e mentoria!
        """
    }
]

async def testar_analise_completa():
    """Testa o fluxo completo de análise"""
    print("🚀 TESTE COMPLETO DO AGENTE 1 - ANÁLISE DE PALAVRAS-CHAVE")
    print("=" * 60)
    
    # Configurações da busca
    cargo_objetivo = "desenvolvedor frontend react"
    area_interesse = "tecnologia"
    
    print(f"\n📋 Configuração:")
    print(f"   Cargo: {cargo_objetivo}")
    print(f"   Área: {area_interesse}")
    print(f"   Total de vagas: {len(vagas_reais)}")
    
    # Criar extrator
    extractor = AIKeywordExtractor()
    
    print("\n🤖 Iniciando análise com IA...")
    print("   (Isso pode levar 10-30 segundos)")
    
    try:
        # Executar análise
        resultado = await extractor.extrair_palavras_chave_ia(
            vagas=vagas_reais,
            cargo_objetivo=cargo_objetivo,
            area_interesse=area_interesse
        )
        
        print("\n✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        
        # Mostrar TOP 10
        print("\n🏆 TOP 10 PALAVRAS-CHAVE MAIS IMPORTANTES:")
        print("-" * 40)
        
        top_10 = resultado.get('top_10_palavras_chave', [])
        for i, palavra in enumerate(top_10[:10], 1):
            termo = palavra.get('termo', 'N/A')
            freq = palavra.get('frequencia', 0)
            cat = palavra.get('categoria', 'N/A')
            print(f"{i:2d}. {termo:<20} | {freq} menções | {cat}")
        
        # Mostrar categorias
        print("\n📊 PALAVRAS POR CATEGORIA:")
        print("-" * 40)
        
        categorias = resultado.get('categorias', {})
        for categoria, termos in categorias.items():
            if termos:
                print(f"\n🏷️  {categoria.upper()}:")
                # Mostrar apenas os 5 primeiros de cada categoria
                for termo in termos[:5]:
                    print(f"   • {termo}")
                if len(termos) > 5:
                    print(f"   ... e mais {len(termos) - 5} termos")
        
        # Estatísticas
        print("\n📈 ESTATÍSTICAS DA ANÁLISE:")
        print("-" * 40)
        print(f"   Total de palavras únicas: {resultado.get('total_palavras_unicas', 0)}")
        print(f"   Modelo usado: {resultado.get('modelo_usado', 'N/A')}")
        print(f"   Tempo de processamento: ~{resultado.get('tempo_processamento', 'N/A')}s")
        
        # Salvar resultado completo
        output_file = 'resultado_analise_completa.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Resultado completo salvo em: {output_file}")
        
        # Insights
        insights = resultado.get('insights_adicionais', {})
        if insights:
            print("\n💡 INSIGHTS ADICIONAIS:")
            print("-" * 40)
            
            tendencias = insights.get('tendencias_emergentes', [])
            if tendencias:
                print("\n🚀 Tendências emergentes:")
                for t in tendencias[:3]:
                    print(f"   • {t}")
            
            recomendacoes = insights.get('recomendacoes', [])
            if recomendacoes:
                print("\n📌 Recomendações para o candidato:")
                for r in recomendacoes[:3]:
                    print(f"   • {r}")
        
        print("\n✨ Análise finalizada com sucesso!")
        
    except Exception as e:
        print(f"\n❌ ERRO NA ANÁLISE: {type(e).__name__}")
        print(f"   Mensagem: {e}")
        import traceback
        print("\nTraceback completo:")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(testar_analise_completa())