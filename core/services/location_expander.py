"""
Location Expander - Sistema HELIO
Expansão geográfica inteligente usando IA
"""

import os
import json
import logging
from typing import List, Dict, Any
from dataclasses import dataclass
import google.generativeai as genai
from anthropic import Anthropic
import openai
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()


@dataclass
class LocalidadeExpandida:
    """Representa uma localidade expandida com metadados"""
    nome: str
    distancia_km: float
    relevancia: float
    tipo: str  # 'cidade_principal', 'regiao_metropolitana', 'cidade_proxima', 'remoto'
    justificativa: str


class LocationExpander:
    """
    Expande localização de forma inteligente usando IA
    Considera mobilidade urbana, mercado de trabalho e preferências
    """
    
    def __init__(self):
        # Configurar clientes de IA
        self.gemini_client = None
        self.anthropic_client = None
        self.openai_client = None
        
        # Tentar configurar Gemini (preferencial por ter conhecimento geográfico brasileiro)
        if os.getenv('GOOGLE_API_KEY'):
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            self.gemini_client = genai.GenerativeModel('gemini-1.5-pro')
            logger.info("✅ Gemini configurado para expansão geográfica")
        
        # Fallback para Claude
        elif os.getenv('ANTHROPIC_API_KEY'):
            self.anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
            logger.info("✅ Claude configurado para expansão geográfica")
        
        # Fallback para OpenAI
        elif os.getenv('OPENAI_API_KEY'):
            openai.api_key = os.getenv('OPENAI_API_KEY')
            self.openai_client = openai
            logger.info("✅ OpenAI configurado para expansão geográfica")
        
        # Cache de expansões para economizar chamadas
        self.cache = {}
    
    def expandir_localizacao(
        self,
        local_base: str,
        tipo_vaga: str,
        limite: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Expande localização considerando tipo de vaga e mobilidade
        
        Args:
            local_base: Cidade/estado base do usuário
            tipo_vaga: presencial, hibrido ou remoto
            limite: Quantidade máxima de locais
            
        Returns:
            Lista de localizações ordenadas por relevância
        """
        
        # Verificar cache
        cache_key = f"{local_base}_{tipo_vaga}_{limite}"
        if cache_key in self.cache:
            logger.info(f"📍 Usando cache para {local_base}")
            return self.cache[cache_key]
        
        # Para vagas remotas, retornar conjunto padrão
        if tipo_vaga == "remoto":
            return self._locais_remotos_padrao()
        
        # Usar IA para expansão inteligente
        locais_expandidos = []
        
        try:
            if self.gemini_client:
                locais_expandidos = self._expandir_com_gemini(local_base, tipo_vaga, limite)
            elif self.anthropic_client:
                locais_expandidos = self._expandir_com_claude(local_base, tipo_vaga, limite)
            elif self.openai_client:
                locais_expandidos = self._expandir_com_openai(local_base, tipo_vaga, limite)
            else:
                logger.warning("⚠️ Nenhuma IA configurada, usando expansão básica")
                locais_expandidos = self._expansao_basica(local_base, tipo_vaga)
        
        except Exception as e:
            logger.error(f"❌ Erro na expansão com IA: {e}")
            locais_expandidos = self._expansao_basica(local_base, tipo_vaga)
        
        # Cachear resultado
        self.cache[cache_key] = locais_expandidos
        
        return locais_expandidos[:limite]
    
    def _expandir_com_gemini(self, local_base: str, tipo_vaga: str, limite: int) -> List[Dict[str, Any]]:
        """
        Usa Gemini para expansão geográfica inteligente
        """
        prompt = self._criar_prompt_expansao(local_base, tipo_vaga, limite)
        
        try:
            response = self.gemini_client.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.3,
                    "max_output_tokens": 2000,
                }
            )
            
            # Extrair JSON da resposta
            texto = response.text
            inicio = texto.find('[')
            fim = texto.rfind(']') + 1
            
            if inicio >= 0 and fim > inicio:
                locais = json.loads(texto[inicio:fim])
                return locais
            
        except Exception as e:
            logger.error(f"Erro Gemini: {e}")
        
        return []
    
    def _expandir_com_claude(self, local_base: str, tipo_vaga: str, limite: int) -> List[Dict[str, Any]]:
        """
        Usa Claude para expansão geográfica
        """
        prompt = self._criar_prompt_expansao(local_base, tipo_vaga, limite)
        
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                temperature=0.3,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            texto = response.content[0].text
            inicio = texto.find('[')
            fim = texto.rfind(']') + 1
            
            if inicio >= 0 and fim > inicio:
                locais = json.loads(texto[inicio:fim])
                return locais
                
        except Exception as e:
            logger.error(f"Erro Claude: {e}")
        
        return []
    
    def _expandir_com_openai(self, local_base: str, tipo_vaga: str, limite: int) -> List[Dict[str, Any]]:
        """
        Usa OpenAI para expansão geográfica
        """
        prompt = self._criar_prompt_expansao(local_base, tipo_vaga, limite)
        
        try:
            response = self.openai_client.ChatCompletion.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "Você é um especialista em geografia brasileira e mercado de trabalho."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            texto = response.choices[0].message.content
            inicio = texto.find('[')
            fim = texto.rfind(']') + 1
            
            if inicio >= 0 and fim > inicio:
                locais = json.loads(texto[inicio:fim])
                return locais
                
        except Exception as e:
            logger.error(f"Erro OpenAI: {e}")
        
        return []
    
    def _criar_prompt_expansao(self, local_base: str, tipo_vaga: str, limite: int) -> str:
        """
        Cria prompt otimizado para expansão geográfica
        """
        
        distancia_max = "50km" if tipo_vaga == "presencial" else "100km"
        
        prompt = f"""Você é um especialista em geografia brasileira e mercado de trabalho.

Tarefa: Expandir a busca de vagas a partir de "{local_base}" para trabalho {tipo_vaga}.

Considere:
1. Distância e tempo de deslocamento (máximo {distancia_max} para {tipo_vaga})
2. Conexões de transporte público e rodovias
3. Polos de emprego e centros empresariais
4. Qualidade do mercado de trabalho local

Para trabalho {tipo_vaga}, priorize:
- Presencial: cidades muito próximas, mesma região metropolitana
- Híbrido: cidades em um raio maior, considerando deslocamento 2-3x por semana
- Remoto: principais centros de tecnologia do Brasil

Retorne APENAS um JSON array com {limite} locais no formato:
[
  {{
    "nome": "Cidade, Estado",
    "distancia_km": 0,
    "relevancia": 1.0,
    "tipo": "cidade_principal",
    "justificativa": "Cidade base do candidato"
  }},
  {{
    "nome": "Cidade Próxima, Estado", 
    "distancia_km": 25,
    "relevancia": 0.9,
    "tipo": "regiao_metropolitana",
    "justificativa": "Mesma região metropolitana, fácil acesso"
  }}
]

IMPORTANTE: 
- Use nomes reais de cidades brasileiras
- Formato: "Cidade, UF" (ex: "São Paulo, SP")
- Ordene por relevância decrescente
- Retorne APENAS o JSON, sem texto adicional"""
        
        return prompt
    
    def _expansao_basica(self, local_base: str, tipo_vaga: str) -> List[Dict[str, Any]]:
        """
        Expansão básica sem IA - usa dados pré-definidos
        """
        # Regiões metropolitanas principais do Brasil
        regioes_metro = {
            "são paulo": ["São Paulo, SP", "Guarulhos, SP", "São Bernardo do Campo, SP", "Santo André, SP", "Osasco, SP"],
            "rio de janeiro": ["Rio de Janeiro, RJ", "Niterói, RJ", "São Gonçalo, RJ", "Duque de Caxias, RJ", "Nova Iguaçu, RJ"],
            "belo horizonte": ["Belo Horizonte, MG", "Contagem, MG", "Betim, MG", "Nova Lima, MG", "Ribeirão das Neves, MG"],
            "porto alegre": ["Porto Alegre, RS", "Canoas, RS", "Gravataí, RS", "Viamão, RS", "Novo Hamburgo, RS"],
            "curitiba": ["Curitiba, PR", "São José dos Pinhais, PR", "Colombo, PR", "Araucária, PR", "Pinhais, PR"],
            "campinas": ["Campinas, SP", "Jundiaí, SP", "Americana, SP", "Sumaré, SP", "Hortolândia, SP"],
            "brasília": ["Brasília, DF", "Taguatinga, DF", "Ceilândia, DF", "Águas Claras, DF", "Samambaia, DF"]
        }
        
        # Identificar região
        local_lower = local_base.lower()
        cidades = [local_base]  # Sempre incluir cidade base
        
        # Buscar região metropolitana
        for regiao, lista_cidades in regioes_metro.items():
            if regiao in local_lower:
                cidades.extend(lista_cidades[:4])  # Adicionar até 4 cidades próximas
                break
        
        # Se não encontrou, adicionar capitais principais
        if len(cidades) == 1:
            if tipo_vaga == "hibrido":
                cidades.extend([
                    "São Paulo, SP",
                    "Rio de Janeiro, RJ", 
                    "Belo Horizonte, MG"
                ])
            else:  # presencial
                # Apenas cidade base para presencial sem região metro
                pass
        
        # Formatar resultado
        resultado = []
        for i, cidade in enumerate(cidades[:10]):
            resultado.append({
                "nome": cidade,
                "distancia_km": 0 if i == 0 else (i * 20),  # Estimativa
                "relevancia": 1.0 - (i * 0.1),
                "tipo": "cidade_principal" if i == 0 else "expansao_basica",
                "justificativa": "Expansão básica sem IA"
            })
        
        return resultado
    
    def _locais_remotos_padrao(self) -> List[Dict[str, Any]]:
        """
        Retorna locais padrão para vagas remotas
        """
        return [
            {
                "nome": "Remote",
                "distancia_km": 0,
                "relevancia": 1.0,
                "tipo": "remoto",
                "justificativa": "Busca global para vagas remotas"
            },
            {
                "nome": "Brasil",
                "distancia_km": 0,
                "relevancia": 0.95,
                "tipo": "remoto",
                "justificativa": "Vagas remotas nacionais"
            },
            {
                "nome": "São Paulo, SP",
                "distancia_km": 0,
                "relevancia": 0.9,
                "tipo": "remoto",
                "justificativa": "Principal hub de tecnologia"
            },
            {
                "nome": "Rio de Janeiro, RJ",
                "distancia_km": 0,
                "relevancia": 0.85,
                "tipo": "remoto",
                "justificativa": "Segundo maior hub tecnológico"
            },
            {
                "nome": "Belo Horizonte, MG",
                "distancia_km": 0,
                "relevancia": 0.8,
                "tipo": "remoto",
                "justificativa": "Hub emergente de startups"
            }
        ]