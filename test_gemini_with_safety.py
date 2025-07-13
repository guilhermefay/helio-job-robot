#!/usr/bin/env python3
"""
Teste do Gemini com configurações de segurança
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configurar Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Configurações de segurança menos restritivas
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    }
]

model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Prompt com vagas reais
prompt = """Analise as seguintes descrições de vagas e extraia as 10 palavras-chave mais importantes para um desenvolvedor frontend.

VAGA 1:
Título: Desenvolvedor Frontend React
Empresa: Tech Solutions
Descrição: Procuramos desenvolvedor frontend com experiência em React. Requisitos: Experiência sólida com React e JavaScript ES6+, HTML5, CSS3, Git, metodologias ágeis. TypeScript é diferencial.

VAGA 2:
Título: Desenvolvedor Front-end Sênior
Empresa: Digital Agency
Descrição: Vaga para desenvolvedor front-end sênior. Requisitos: React.js avançado, JavaScript/TypeScript, CSS/SASS, Jest, Inglês técnico. Diferenciais: Next.js, Node.js, AWS.

VAGA 3:
Título: Frontend Developer
Empresa: Startup Inovadora  
Descrição: Buscamos frontend developer. Esperamos: React, JavaScript moderno, Styled Components, Git, comunicação. Plus: Vue.js, Angular, GraphQL, Docker.

RETORNE APENAS UM JSON VÁLIDO no formato abaixo:
{
  "top_10_palavras_chave": [
    {"termo": "React", "frequencia": 3, "categoria": "framework"},
    {"termo": "JavaScript", "frequencia": 3, "categoria": "linguagem"},
    ...
  ]
}"""

try:
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.1,
            "max_output_tokens": 1000,
            "candidate_count": 1
        },
        safety_settings=safety_settings
    )
    
    print("✅ Resposta recebida!")
    print("Finish reason:", response.candidates[0].finish_reason)
    print("\nTexto da resposta:")
    print(response.text)
    
except Exception as e:
    print(f"❌ Erro: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()