#!/usr/bin/env python3
"""
Teste minimalista do Gemini
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Texto super simples
texto = """
Vaga 1: Desenvolvedor React com JavaScript
Vaga 2: Frontend com React e TypeScript
Vaga 3: Dev React, Git e CSS
"""

prompt = f"""Liste 5 palavras-chave técnicas das vagas:

{texto}

JSON:
{{"palavras": ["palavra1", "palavra2", "palavra3", "palavra4", "palavra5"]}}"""

try:
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.1,
            "max_output_tokens": 200
        },
        safety_settings=[
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    )
    
    print("✅ Funcionou!")
    print("Resposta:", response.text)
    
except Exception as e:
    print(f"❌ Erro: {e}")
    if hasattr(e, 'response') and e.response:
        print("Candidates:", e.response.candidates)
        if e.response.candidates:
            print("Finish reason:", e.response.candidates[0].finish_reason)