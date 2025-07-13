#!/usr/bin/env python3
"""
Debug completo da análise de palavras-chave
"""
import asyncio
import json
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from core.services.ai_keyword_extractor import AIKeywordExtractor

# Dados de teste simples
vagas_teste = [
    {
        "titulo": "Desenvolvedor Frontend",
        "empresa": "Tech Company",
        "descricao": "Procuramos desenvolvedor com React e JavaScript"
    }
]

async def testar():
    print("🧪 Teste de Debug AI")
    
    extractor = AIKeywordExtractor()
    
    # Testar Gemini diretamente
    if extractor.gemini_model:
        print("\n📱 Testando Gemini diretamente...")
        try:
            prompt_simples = """Liste 5 palavras-chave da vaga: "Desenvolvedor com React e JavaScript". 
            
Retorne APENAS JSON:
{"palavras": ["palavra1", "palavra2", "palavra3", "palavra4", "palavra5"]}"""
            
            resultado = extractor._chamar_gemini(prompt_simples)
            print("✅ Gemini funcionou!")
            print(json.dumps(resultado, indent=2))
        except Exception as e:
            print(f"❌ Erro Gemini: {e}")
            
            # Testar resposta crua
            try:
                import google.generativeai as genai
                
                safety_settings = [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ]
                
                response = extractor.gemini_model.generate_content(
                    prompt_simples,
                    generation_config={
                        "temperature": 0.1,
                        "max_output_tokens": 500,
                        "candidate_count": 1
                    },
                    safety_settings=safety_settings
                )
                
                print(f"\n🔍 Debug resposta Gemini:")
                print(f"Candidates: {len(response.candidates)}")
                if response.candidates:
                    print(f"Finish reason: {response.candidates[0].finish_reason}")
                    print(f"Safety ratings: {response.candidates[0].safety_ratings}")
                    if response.candidates[0].content.parts:
                        print(f"Text: {response.candidates[0].content.parts[0].text}")
            except Exception as debug_e:
                print(f"Debug error: {debug_e}")

if __name__ == "__main__":
    asyncio.run(testar())