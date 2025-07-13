#!/usr/bin/env python3
"""
Teste com 100 vagas usando processamento em lotes
"""
import asyncio
from core.services.ai_keyword_extractor import AIKeywordExtractor

# Gerar 100 vagas simuladas
vagas_teste = []
tecnologias = [
    "React", "Angular", "Vue.js", "JavaScript", "TypeScript", 
    "Node.js", "Python", "Java", "Docker", "Kubernetes",
    "AWS", "Git", "MongoDB", "PostgreSQL", "Redis"
]

for i in range(100):
    # Variar tecnologias por vaga
    tech_indices = [(i + j) % len(tecnologias) for j in range(5)]
    tech_vaga = [tecnologias[idx] for idx in tech_indices]
    
    vagas_teste.append({
        "titulo": f"Desenvolvedor Full Stack #{i+1}",
        "empresa": f"Tech Company {i+1}",
        "descricao": f"""
        Procuramos desenvolvedor com experiência em:
        - {tech_vaga[0]} e {tech_vaga[1]}
        - {tech_vaga[2]} para backend
        - {tech_vaga[3]} e {tech_vaga[4]}
        - Metodologias ágeis e CI/CD
        - Inglês fluente
        """
    })

async def testar():
    print("🚀 TESTE COM 100 VAGAS")
    print("=" * 50)
    
    extractor = AIKeywordExtractor()
    
    try:
        resultado = await extractor.extrair_palavras_chave_ia(
            vagas=vagas_teste,
            cargo_objetivo="desenvolvedor full stack",
            area_interesse="tecnologia"
        )
        
        print("\n✅ ANÁLISE CONCLUÍDA!")
        print(f"📊 Total de vagas analisadas: {resultado.get('analise_metadados', {}).get('total_vagas', 0)}")
        print(f"🔤 Total de palavras únicas: {resultado.get('total_palavras_unicas', 0)}")
        print(f"🤖 Modelo usado: {resultado.get('modelo_usado', 'N/A')}")
        
        print("\n🏆 TOP 10 PALAVRAS-CHAVE:")
        for i, palavra in enumerate(resultado.get('top_10_palavras_chave', [])[:10], 1):
            termo = palavra.get('termo', 'N/A')
            freq = palavra.get('frequencia', 0)
            perc = palavra.get('percentual', 0)
            cat = palavra.get('categoria', 'N/A')
            print(f"{i:2d}. {termo:<15} | {freq:>3} menções ({perc}%) | {cat}")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")

if __name__ == "__main__":
    asyncio.run(testar())