"""
Extrator simplificado de palavras-chave
"""
import os
import json
import google.generativeai as genai
from typing import List, Dict, Any
from collections import Counter
import re

class SimpleKeywordExtractor:
    def __init__(self):
        # Configurar Gemini
        if os.getenv('GOOGLE_API_KEY'):
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            print("✅ Gemini configurado com sucesso")
        else:
            self.model = None
            print("❌ GOOGLE_API_KEY não configurada")
    
    def extract_keywords(self, vagas: List[Dict[str, Any]], cargo: str) -> Dict[str, Any]:
        """Extrai palavras-chave das vagas"""
        
        if not self.model:
            return self._fallback_extraction(vagas)
        
        # Preparar texto resumido (limitar tamanho)
        texto_vagas = self._prepare_text(vagas[:3])  # Usar só 3 primeiras vagas
        
        prompt = f"""Analise estas vagas para {cargo} e liste as 10 principais palavras-chave técnicas.

{texto_vagas}

Retorne SOMENTE um JSON assim:
{{"palavras": ["React", "JavaScript", "TypeScript", "Git", "CSS", "HTML", "API", "Agile", "Testing", "Node.js"]}}"""

        try:
            # Configurações de segurança permissivas
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
            
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.1,
                    "max_output_tokens": 500,
                    "candidate_count": 1
                },
                safety_settings=safety_settings
            )
            
            # Extrair JSON da resposta
            text = response.text
            # Remover markdown se houver
            text = text.replace('```json', '').replace('```', '').strip()
            
            result = json.loads(text)
            palavras = result.get('palavras', [])
            
            return {
                "success": True,
                "top_10_palavras_chave": [
                    {"termo": p, "frequencia": 1, "categoria": "tecnica"} 
                    for p in palavras
                ],
                "modelo_usado": "gemini-2.0-flash-exp"
            }
            
        except Exception as e:
            print(f"❌ Erro Gemini: {e}")
            return self._fallback_extraction(vagas)
    
    def _prepare_text(self, vagas: List[Dict[str, Any]]) -> str:
        """Prepara texto resumido das vagas"""
        texts = []
        for i, vaga in enumerate(vagas, 1):
            desc = vaga.get('descricao', '')
            # Pegar só os primeiros 300 caracteres
            desc_resumo = desc[:300] + "..." if len(desc) > 300 else desc
            texts.append(f"VAGA {i}: {desc_resumo}")
        return "\n\n".join(texts)
    
    def _fallback_extraction(self, vagas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extração simples sem IA"""
        print("⚠️ Usando extração fallback (sem IA)")
        
        # Palavras-chave comuns para frontend
        keywords_tech = [
            "React", "JavaScript", "TypeScript", "CSS", "HTML", "Git",
            "API", "REST", "Node.js", "Jest", "Redux", "Hooks",
            "Responsive", "Agile", "SASS", "Webpack", "NPM"
        ]
        
        # Contar ocorrências nas descrições
        all_text = " ".join([v.get('descricao', '') for v in vagas]).lower()
        
        found_keywords = []
        for kw in keywords_tech:
            if kw.lower() in all_text:
                count = all_text.count(kw.lower())
                found_keywords.append({
                    "termo": kw,
                    "frequencia": count,
                    "categoria": "tecnica"
                })
        
        # Ordenar por frequência
        found_keywords.sort(key=lambda x: x['frequencia'], reverse=True)
        
        return {
            "success": True,
            "top_10_palavras_chave": found_keywords[:10],
            "modelo_usado": "fallback_regex"
        }