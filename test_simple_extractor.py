#!/usr/bin/env python3
"""
Teste do extrator simplificado
"""
from core.services.simple_keyword_extractor import SimpleKeywordExtractor

# Vaga de teste
vagas = [{
    "titulo": "Desenvolvedor React",
    "empresa": "Tech Co",
    "descricao": "Buscamos dev com React, JavaScript, TypeScript, Git, API REST, Jest"
}]

extractor = SimpleKeywordExtractor()
resultado = extractor.extract_keywords(vagas, "desenvolvedor react")

print("\n✅ Resultado:")
print(f"Modelo usado: {resultado['modelo_usado']}")
print("\nTop 10 palavras-chave:")
for i, kw in enumerate(resultado['top_10_palavras_chave'], 1):
    print(f"{i}. {kw['termo']}")