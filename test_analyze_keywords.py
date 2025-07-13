#!/usr/bin/env python3
"""
Script para testar a funcionalidade de análise de palavras-chave
"""
import asyncio
import json
from core.services.ai_keyword_extractor import AIKeywordExtractor

# Dados de teste - simulando vagas coletadas
vagas_teste = [
    {
        "titulo": "Desenvolvedor Frontend React",
        "empresa": "Tech Solutions",
        "descricao": """
        Procuramos desenvolvedor frontend com experiência em React.
        
        Requisitos:
        - Experiência sólida com React e JavaScript ES6+
        - Conhecimento em HTML5, CSS3 e responsividade
        - Experiência com Git e metodologias ágeis
        - TypeScript é um diferencial
        
        Oferecemos:
        - Salário competitivo
        - Home office flexível
        - Benefícios completos
        """
    },
    {
        "titulo": "Desenvolvedor Front-end Sênior",
        "empresa": "Digital Agency",
        "descricao": """
        Vaga para desenvolvedor front-end sênior.
        
        Requisitos obrigatórios:
        - React.js avançado
        - JavaScript/TypeScript
        - CSS/SASS
        - Testes unitários (Jest)
        - Inglês técnico
        
        Diferenciais:
        - Next.js
        - Node.js
        - AWS
        """
    },
    {
        "titulo": "Frontend Developer",
        "empresa": "Startup Inovadora",
        "descricao": """
        Buscamos frontend developer para nosso time.
        
        O que esperamos:
        - Domínio de React e seu ecossistema
        - JavaScript moderno
        - Styled Components ou CSS-in-JS
        - Versionamento com Git
        - Comunicação efetiva
        
        Plus:
        - Vue.js ou Angular
        - GraphQL
        - Docker
        """
    }
]

async def testar_analise():
    """Testa a análise de palavras-chave"""
    print("🧪 Iniciando teste de análise de palavras-chave...")
    print(f"📊 Total de vagas de teste: {len(vagas_teste)}")
    
    # Criar extrator
    extractor = AIKeywordExtractor()
    
    # Parâmetros de busca
    cargo_objetivo = "desenvolvedor front end"
    area_interesse = "tecnologia"
    
    print(f"\n🎯 Cargo objetivo: {cargo_objetivo}")
    print(f"🏢 Área de interesse: {area_interesse}")
    
    try:
        # Executar análise
        print("\n🤖 Iniciando análise com IA...")
        resultado = await extractor.extrair_palavras_chave_ia(
            vagas=vagas_teste,
            cargo_objetivo=cargo_objetivo,
            area_interesse=area_interesse
        )
        
        # Mostrar resultados
        print("\n✅ ANÁLISE CONCLUÍDA!")
        print("\n📋 TOP 10 PALAVRAS-CHAVE (Carolina Martins):")
        for i, palavra in enumerate(resultado.get('top_10_carolina_martins', []), 1):
            print(f"   {i}. {palavra['termo']} ({palavra['frequencia']} menções)")
            if palavra.get('justificativa'):
                print(f"      → {palavra['justificativa']}")
        
        print("\n📊 CATEGORIZAÇÃO:")
        categorias = resultado.get('categorias', {})
        for categoria, termos in categorias.items():
            if termos:
                print(f"\n🏷️  {categoria.upper()}:")
                for termo in termos[:5]:  # Mostrar apenas top 5 de cada categoria
                    print(f"   • {termo}")
        
        print(f"\n📈 ESTATÍSTICAS:")
        print(f"   - Total de palavras únicas: {resultado.get('total_palavras_unicas', 0)}")
        print(f"   - Modelo usado: {resultado.get('modelo_usado', 'Não informado')}")
        
        # Salvar resultado completo
        with open('test_analyze_result.json', 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
        print("\n💾 Resultado completo salvo em: test_analyze_result.json")
        
    except Exception as e:
        print(f"\n❌ ERRO NA ANÁLISE: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(testar_analise())