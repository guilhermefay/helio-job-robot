#!/usr/bin/env python3
"""
Teste do prompt real do Gemini
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configurar Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Configurações de segurança
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
]

# Criar prompt similar ao usado no sistema
texto_vagas = """
--- VAGA 1 ---
Título: Desenvolvedor Frontend React
Empresa: Tech Solutions
Descrição:
Procuramos desenvolvedor com React, JavaScript, TypeScript, Git.
--- FIM VAGA 1 ---
"""

prompt = f"""Você é um especialista em análise de vagas de emprego. 
Sua tarefa é analisar 1 descrições de vagas para o cargo de "desenvolvedor frontend" 
na área de "tecnologia" e identificar as palavras-chave mais relevantes.

METODOLOGIA A SEGUIR:

1. EXTRAÇÃO: 
   - Identifique TODAS as competências técnicas, ferramentas, metodologias, soft skills e qualificações

2. TOP 10 PALAVRAS-CHAVE:
   - Liste as 10 palavras-chave mais estratégicas

TEXTO DAS VAGAS:
{texto_vagas}

RETORNE APENAS JSON VÁLIDO:

{{
  "top_10_palavras_chave": [
    {{"termo": "React", "frequencia": 1, "categoria": "framework"}},
    {{"termo": "JavaScript", "frequencia": 1, "categoria": "linguagem"}}
  ]
}}"""

print(f"Tamanho do prompt: {len(prompt)} caracteres")
print("\nTestando Gemini...")

try:
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.3,
            "max_output_tokens": 4000,
            "candidate_count": 1,
            "top_k": 40,
            "top_p": 0.95
        },
        safety_settings=safety_settings
    )
    
    print("\n✅ Resposta recebida!")
    print(f"Candidates: {len(response.candidates)}")
    if response.candidates:
        print(f"Finish reason: {response.candidates[0].finish_reason}")
        if response.candidates[0].content.parts:
            print("\nTexto da resposta:")
            print(response.candidates[0].content.parts[0].text)
        else:
            print("❌ Sem parts no content")
            print(f"Safety ratings: {response.candidates[0].safety_ratings}")
    
except Exception as e:
    print(f"\n❌ Erro: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()