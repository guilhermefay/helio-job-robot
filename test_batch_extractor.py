#!/usr/bin/env python3
"""
Teste do extrator em lotes
"""
import asyncio
from core.services.batch_keyword_extractor import BatchKeywordExtractor

# Simular 30 vagas
vagas_teste = []
for i in range(30):
    vagas_teste.append({
        "titulo": f"Desenvolvedor Frontend #{i+1}",
        "empresa": f"Empresa {i+1}",
        "descricao": f"""
        Vaga {i+1} para desenvolvedor com experiência em:
        - React.js e JavaScript ES6+
        - TypeScript {'(obrigatório)' if i % 3 == 0 else '(desejável)'}
        - Git e metodologias ágeis
        - {'Node.js' if i % 2 == 0 else 'CSS/SASS'}
        - {'Docker' if i % 5 == 0 else 'API REST'}
        - {'AWS' if i % 4 == 0 else 'Jest/Testing'}
        """
    })

async def testar():
    print("🧪 Teste de Extração em Lotes")
    print(f"📊 Total de vagas para teste: {len(vagas_teste)}")
    
    extractor = BatchKeywordExtractor()
    
    # Callback para mostrar progresso
    async def mostrar_progresso(msg):
        print(f"   → {msg}")
    
    # Processar em lotes de 5
    resultado = await extractor.extract_keywords_batch(
        vagas=vagas_teste,
        cargo="desenvolvedor frontend",
        batch_size=5,
        callback=mostrar_progresso
    )
    
    print("\n📊 RESULTADO FINAL:")
    print(f"✅ Sucesso: {resultado['success']}")
    print(f"📈 Total analisado: {resultado['total_vagas_analisadas']} vagas")
    print(f"📦 Lotes processados: {resultado['total_lotes_processados']}")
    print(f"🔤 Palavras únicas: {resultado['total_palavras_unicas']}")
    
    print("\n🏆 TOP 10 PALAVRAS-CHAVE:")
    for i, palavra in enumerate(resultado['top_10_palavras_chave'], 1):
        print(f"{i:2d}. {palavra['termo']:<15} | {palavra['frequencia']:>3} menções ({palavra['percentual']}%) | {palavra['categoria']}")
    
    print("\n📊 POR CATEGORIA:")
    for categoria, termos in resultado['categorias'].items():
        if termos:
            print(f"\n{categoria.upper()}:")
            for termo in termos[:3]:  # Top 3 de cada
                print(f"   • {termo['termo']} ({termo['frequencia']}x)")

if __name__ == "__main__":
    asyncio.run(testar())