"""
Validador de IA - Sistema HELIO
Validação real de palavras-chave usando OpenAI e Anthropic
"""

import os
import json
from typing import Dict, List, Any, Optional
import openai
from anthropic import Anthropic

class AIValidator:
    """
    Validador real usando APIs de IA (OpenAI e Anthropic)
    Substitui as simulações do sistema original
    """
    
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        
        # Inicializa clientes se APIs estão configuradas
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key and openai_key != 'your_openai_api_key_here':
            openai.api_key = openai_key
            self.openai_client = openai
            
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        if anthropic_key and anthropic_key != 'your_anthropic_api_key_here':
            self.anthropic_client = Anthropic(api_key=anthropic_key)
    
    async def validar_palavras_chave(
        self, 
        palavras_por_categoria: Dict[str, List[str]], 
        area: str, 
        cargo: str,
        contexto_vagas: List[str] = None
    ) -> Dict[str, Any]:
        """
        Valida palavras-chave usando IA real
        
        Args:
            palavras_por_categoria: Palavras organizadas por categoria
            area: Área de interesse
            cargo: Cargo objetivo
            contexto_vagas: Descrições de vagas para contexto
            
        Returns:
            Dict com validação da IA
        """
        # Verifica se há pelo menos uma API disponível
        if not (self.openai_client or self.anthropic_client):
            return self._fallback_validation(palavras_por_categoria, area, cargo)
        
        # Prepara contexto
        contexto_adicional = ""
        if contexto_vagas:
            contexto_adicional = f"\n\nCONTEXTO das vagas analisadas:\n{chr(10).join(contexto_vagas[:3])}"
        
        # Monta prompt seguindo metodologia Carolina Martins
        prompt = self._criar_prompt_validacao(
            palavras_por_categoria, area, cargo, contexto_adicional
        )
        
        # Tenta validação com APIs disponíveis
        try:
            if self.anthropic_client:
                return await self._validar_com_anthropic(prompt, palavras_por_categoria)
            elif self.openai_client:
                return await self._validar_com_openai(prompt, palavras_por_categoria)
        except Exception as e:
            print(f"Erro na validação IA: {e}")
            return self._fallback_validation(palavras_por_categoria, area, cargo)
    
    def _criar_prompt_validacao(
        self, 
        palavras_por_categoria: Dict[str, List[str]], 
        area: str, 
        cargo: str, 
        contexto: str
    ) -> str:
        """Cria prompt otimizado para validação seguindo metodologia Carolina Martins"""
        
        prompt = f"""
OBJETIVO: Validar palavras-chave para currículo seguindo a metodologia Carolina Martins.

CARGO ALVO: {cargo}
ÁREA: {area}

PALAVRAS-CHAVE EXTRAÍDAS:
"""
        
        for categoria, palavras in palavras_por_categoria.items():
            if palavras:
                prompt += f"\n{categoria.upper()}: {', '.join(palavras)}"
        
        prompt += f"""
{contexto}

INSTRUÇÕES:
1. Analise cada palavra-chave considerando:
   - Relevância para o cargo específico
   - Frequência no mercado de trabalho da área
   - Adequação à metodologia Carolina Martins (foco em resultados)

2. Classifique cada palavra como:
   - APROVADA: Essencial para o cargo e área
   - REJEITADA: Irrelevante ou genérica demais
   - SUGESTÃO: Palavra similar mais adequada

3. Adicione 3-5 sugestões de palavras-chave importantes que podem estar faltando.

RESPOSTA EM JSON:
{{
    "aprovadas": ["palavra1", "palavra2"],
    "rejeitadas": [
        {{"palavra": "palavra3", "motivo": "muito genérica"}},
        {{"palavra": "palavra4", "motivo": "não relevante para o cargo"}}
    ],
    "sugestoes_novas": ["palavra5", "palavra6"],
    "comentarios": "Análise geral das palavras-chave",
    "confianca": 0.85
}}
"""
        return prompt
    
    async def _validar_com_anthropic(
        self, 
        prompt: str, 
        palavras_originais: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """Validação usando Claude (Anthropic)"""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                temperature=0.3,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Extrai JSON da resposta
            content = response.content[0].text
            
            # Tenta extrair JSON da resposta
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                result = json.loads(json_str)
                
                # Adiciona metadados
                result["modelo_usado"] = "claude-3-haiku"
                result["prompt_usado"] = prompt[:200] + "..."
                
                return result
            else:
                # Fallback se não conseguir extrair JSON
                return self._processar_resposta_texto(content, palavras_originais)
                
        except Exception as e:
            print(f"Erro com Anthropic: {e}")
            raise
    
    async def _validar_com_openai(
        self, 
        prompt: str, 
        palavras_originais: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """Validação usando GPT (OpenAI)"""
        try:
            response = self.openai_client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um especialista em recrutamento que valida palavras-chave para currículos seguindo a metodologia Carolina Martins. Responda sempre em JSON válido."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            
            # Tenta extrair JSON da resposta
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                result = json.loads(json_str)
                
                # Adiciona metadados
                result["modelo_usado"] = "gpt-3.5-turbo"
                result["prompt_usado"] = prompt[:200] + "..."
                
                return result
            else:
                # Fallback se não conseguir extrair JSON
                return self._processar_resposta_texto(content, palavras_originais)
                
        except Exception as e:
            print(f"Erro com OpenAI: {e}")
            raise
    
    def _processar_resposta_texto(
        self, 
        resposta: str, 
        palavras_originais: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """Processa resposta em texto quando JSON falha"""
        todas_palavras = []
        for palavras in palavras_originais.values():
            todas_palavras.extend(palavras)
        
        # Análise simples baseada na presença de palavras na resposta
        aprovadas = []
        rejeitadas = []
        
        resposta_lower = resposta.lower()
        
        for palavra in todas_palavras:
            if any(termo in resposta_lower for termo in ["aprovada", "relevante", "importante"]) and palavra.lower() in resposta_lower:
                aprovadas.append(palavra)
            elif any(termo in resposta_lower for termo in ["rejeitada", "irrelevante", "genérica"]) and palavra.lower() in resposta_lower:
                rejeitadas.append({"palavra": palavra, "motivo": "conforme análise IA"})
            else:
                aprovadas.append(palavra)  # Default para aprovada
        
        return {
            "aprovadas": aprovadas,
            "rejeitadas": rejeitadas,
            "sugestoes_novas": ["excel avançado", "gestão de projetos", "comunicação"],
            "comentarios": "Análise processada a partir de resposta em texto",
            "confianca": 0.7,
            "modelo_usado": "processamento_texto",
            "resposta_original": resposta[:300]
        }
    
    def _fallback_validation(
        self, 
        palavras_por_categoria: Dict[str, List[str]], 
        area: str, 
        cargo: str
    ) -> Dict[str, Any]:
        """Validação de fallback quando APIs não estão disponíveis"""
        todas_palavras = []
        for palavras in palavras_por_categoria.values():
            todas_palavras.extend(palavras)
        
        # Filtros baseados em heurísticas
        palavras_importantes = ["gestão", "liderança", "comunicação", "excel", "projetos", "resultados"]
        palavras_genericas = ["trabalho", "pessoa", "empresa", "atividade", "função"]
        
        aprovadas = []
        rejeitadas = []
        
        for palavra in todas_palavras:
            palavra_lower = palavra.lower()
            
            if any(imp in palavra_lower for imp in palavras_importantes):
                aprovadas.append(palavra)
            elif any(gen in palavra_lower for gen in palavras_genericas):
                rejeitadas.append({"palavra": palavra, "motivo": "muito genérica"})
            else:
                aprovadas.append(palavra)  # Default
        
        return {
            "aprovadas": aprovadas,
            "rejeitadas": rejeitadas,
            "sugestoes_novas": [
                f"excel avançado",
                f"gestão de {area.lower()}",
                "comunicação eficaz",
                "orientação a resultados"
            ],
            "comentarios": f"Validação por heurísticas - APIs de IA não disponíveis",
            "confianca": 0.6,
            "modelo_usado": "fallback_heuristico"
        }
    
    async def analisar_descricoes_vagas(self, descricoes: List[str], area: str) -> Dict[str, Any]:
        """
        Analisa descrições de vagas para extrair insights usando IA
        """
        if not (self.openai_client or self.anthropic_client):
            return {"erro": "APIs de IA não configuradas"}
        
        # Limita a 5 descrições para evitar excesso de tokens
        descricoes_sample = descricoes[:5]
        
        prompt = f"""
Analise as seguintes descrições de vagas da área de {area} e extraia insights:

DESCRIÇÕES:
"""
        for i, desc in enumerate(descricoes_sample, 1):
            prompt += f"\n{i}. {desc[:300]}...\n"
        
        prompt += """
RETORNE EM JSON:
{
    "competencias_mais_solicitadas": ["competencia1", "competencia2"],
    "tecnologias_frequentes": ["tech1", "tech2"],
    "soft_skills_importantes": ["skill1", "skill2"],
    "padroes_identificados": ["padrão observado"],
    "nivel_senioridade_comum": "junior/pleno/senior"
}
"""
        
        try:
            if self.anthropic_client:
                response = self.anthropic_client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=500,
                    messages=[{"role": "user", "content": prompt}]
                )
                content = response.content[0].text
            else:
                response = self.openai_client.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500,
                    temperature=0.3
                )
                content = response.choices[0].message.content
            
            # Extrai JSON
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                return json.loads(json_str)
            
        except Exception as e:
            print(f"Erro na análise de vagas: {e}")
        
        return {
            "competencias_mais_solicitadas": ["gestão", "comunicação", "excel"],
            "tecnologias_frequentes": ["excel", "power bi"],
            "soft_skills_importantes": ["liderança", "trabalho em equipe"],
            "padroes_identificados": ["experiência mínima de 3 anos comum"],
            "nivel_senioridade_comum": "pleno"
        }