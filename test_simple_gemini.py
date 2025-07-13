#!/usr/bin/env python3
"""
Teste simples do Gemini para verificar o problema
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configurar Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Prompt simples de teste
prompt = """Analise este texto e extraia 3 palavras-chave:

"Procuramos desenvolvedor frontend com experiência em React e JavaScript. 
Conhecimento em Git é essencial."

Retorne APENAS um JSON no formato:
{
  "palavras": ["palavra1", "palavra2", "palavra3"]
}
"""

try:
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.3,
            "max_output_tokens": 1000,
            "candidate_count": 1,
            "top_k": 40,
            "top_p": 0.95
        }
    )
    
    print("Resposta completa:")
    print(response)
    print("\nCandidatos:", len(response.candidates))
    
    if response.candidates:
        print("\nFinish reason:", response.candidates[0].finish_reason)
        if response.candidates[0].content.parts:
            print("Texto:", response.candidates[0].content.parts[0].text)
        else:
            print("Sem parts no content")
    
except Exception as e:
    print(f"Erro: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()