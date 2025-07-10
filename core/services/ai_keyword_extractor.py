"""
Extrator de Palavras-Chave via IA - Sistema HELIO
Abordagem "Pura IA" seguindo metodologia Carolina Martins
Usa LLMs com grande janela de contexto para análise completa
"""

import os
import json
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import openai
from anthropic import Anthropic
import google.generativeai as genai
from collections import Counter
from dotenv import load_dotenv

# Garantir que as variáveis de ambiente sejam carregadas
load_dotenv()

class AIKeywordExtractor:
    """
    Extrator que envia todas as descrições de vagas para um LLM
    para análise completa e extração inteligente de palavras-chave
    """
    
    def __init__(self):
        # Configurar clientes de IA
        self.anthropic_client = None
        self.openai_client = None
        self.gemini_model = None
        
        # Claude (200k tokens de contexto)
        if os.getenv('ANTHROPIC_API_KEY'):
            try:
                self.anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
                print("✅ Claude client inicializado com sucesso")
            except Exception as e:
                print(f"❌ Erro ao inicializar Claude: {e}")
                self.anthropic_client = None
        
        # OpenAI GPT-4 Turbo (128k tokens)
        if os.getenv('OPENAI_API_KEY'):
            try:
                openai.api_key = os.getenv('OPENAI_API_KEY')
                self.openai_client = openai
                print("✅ OpenAI client inicializado com sucesso")
            except Exception as e:
                print(f"❌ Erro ao inicializar OpenAI: {e}")
                self.openai_client = None
        
        # Google Gemini 2.5 Flash (2M tokens input)
        if os.getenv('GOOGLE_API_KEY'):
            try:
                genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
                # Usando Gemini 2.5 Flash (2025)
                self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
                print("✅ Gemini client inicializado com sucesso")
            except Exception as e:
                print(f"❌ Erro ao inicializar Gemini: {e}")
                self.gemini_model = None
    
    async def extrair_palavras_chave_ia(
        self, 
        vagas: List[Dict[str, Any]], 
        cargo_objetivo: str,
        area_interesse: str,
        callback_progresso: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Extrai palavras-chave usando análise completa via IA
        
        Args:
            vagas: Lista de dicionários com descrições de vagas
            cargo_objetivo: Cargo alvo do usuário
            area_interesse: Área de interesse
            callback_progresso: Função para reportar progresso
            
        Returns:
            Dict com análise completa incluindo top 10 e categorização
        """
        
        if callback_progresso:
            await callback_progresso("Preparando descrições para análise IA...")
        
        # Preparar texto agregado
        texto_agregado = self._preparar_texto_vagas(vagas)
        total_vagas = len(vagas)
        
        print(f"\n🤖 === EXTRAÇÃO VIA IA ===")
        print(f"📊 Total de vagas: {total_vagas}")
        print(f"📝 Tamanho do texto: {len(texto_agregado)} caracteres")
        print(f"🎯 Cargo: {cargo_objetivo}")
        print(f"🏢 Área: {area_interesse}")
        
        # Criar prompt sofisticado
        prompt = self._criar_prompt_extracao(
            texto_agregado, 
            cargo_objetivo, 
            area_interesse, 
            total_vagas
        )
        
        if callback_progresso:
            await callback_progresso("Analisando vagas com IA (isso pode levar 30-60 segundos)...")
        
        # Escolher modelo baseado em disponibilidade e tamanho
        resultado = None
        modelo_usado = None
        
        try:
            print(f"\n🔍 Verificando modelos disponíveis:")
            print(f"   - Gemini configurado: {self.gemini_model is not None}")
            print(f"   - Claude configurado: {self.anthropic_client is not None}")
            print(f"   - GPT-4 configurado: {self.openai_client is not None}")
            print(f"   - Tamanho do texto: {len(texto_agregado)} caracteres")
            
            # Preferência: Gemini 2.5 Flash (2M tokens) > Claude (200k) > GPT-4 (128k)
            if self.gemini_model:
                try:
                    if callback_progresso:
                        await callback_progresso("Usando Google Gemini 2.5 Flash...")
                    print(f"✅ Chamando Gemini 2.5 Flash...")
                    resultado = self._chamar_gemini(prompt)
                    modelo_usado = "gemini-2.5-flash"
                except Exception as gemini_error:
                    print(f"⚠️ Gemini falhou: {gemini_error}")
                    print(f"🔄 Tentando com Claude como fallback...")
                    
                    # Fallback para Claude se Gemini falhar
                    if self.anthropic_client and len(texto_agregado) < 180000:
                        if callback_progresso:
                            await callback_progresso("Usando Claude 3 Sonnet (fallback)...")
                        resultado = self._chamar_claude(prompt)
                        modelo_usado = "claude-3-sonnet"
                    else:
                        raise gemini_error
                
            elif self.anthropic_client and len(texto_agregado) < 180000:
                if callback_progresso:
                    await callback_progresso("Usando Claude 3 Sonnet...")
                print(f"✅ Chamando Claude 3 Sonnet...")
                resultado = self._chamar_claude(prompt)
                modelo_usado = "claude-3-sonnet"
                
            elif self.openai_client and len(texto_agregado) < 100000:
                if callback_progresso:
                    await callback_progresso("Usando GPT-4 Turbo...")
                print(f"✅ Chamando GPT-4 Turbo...")
                resultado = self._chamar_gpt4(prompt)
                modelo_usado = "gpt-4-turbo"
                
            else:
                raise Exception("Texto muito grande ou nenhuma API configurada. Por favor, configure pelo menos uma API key (GOOGLE_API_KEY, ANTHROPIC_API_KEY ou OPENAI_API_KEY)")
                
        except Exception as e:
            print(f"❌ Erro na análise IA: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            if callback_progresso:
                await callback_progresso(f"Erro: {str(e)}")
            
            # NÃO usar fallback - é melhor falhar do que dar resultado ruim
            erro_msg = f"Não foi possível analisar as vagas com IA. {str(e)}"
            raise Exception(erro_msg)
        
        if callback_progresso:
            await callback_progresso("Processando resultados da IA...")
        
        # Processar e validar resultado
        resultado_final = self._processar_resultado_ia(resultado, modelo_usado)
        
        print(f"\n✅ Análise concluída com {modelo_usado}")
        print(f"🔝 Top 10 palavras: {len(resultado_final.get('top_10_carolina_martins', []))}")
        print(f"📊 Total palavras categorizadas: {resultado_final.get('total_palavras_unicas', 0)}")
        
        return resultado_final
    
    def _preparar_texto_vagas(self, vagas: List[Dict[str, Any]]) -> str:
        """Prepara texto agregado das vagas com separadores claros"""
        textos = []
        
        for i, vaga in enumerate(vagas, 1):
            titulo = vaga.get('titulo', 'Sem título')
            empresa = vaga.get('empresa', 'Empresa não informada')
            descricao = vaga.get('descricao', '')
            
            # Formato estruturado para melhor compreensão da IA
            texto_vaga = f"""
--- VAGA {i} ---
Título: {titulo}
Empresa: {empresa}
Descrição:
{descricao}
--- FIM VAGA {i} ---
"""
            textos.append(texto_vaga)
        
        return '\n'.join(textos)
    
    def _criar_prompt_extracao(
        self, 
        texto_vagas: str, 
        cargo_objetivo: str,
        area_interesse: str,
        total_vagas: int
    ) -> str:
        """Cria prompt sofisticado para extração via IA"""
        
        prompt = f"""Você é o Agente de Palavras-chave do método Carreira Meteórica da Carolina Martins. 
Sua tarefa é analisar {total_vagas} descrições de vagas para o cargo de "{cargo_objetivo}" 
na área de "{area_interesse}" e gerar um Mapa de Palavras-Chave (MPC) completo e estruturado.

METODOLOGIA CAROLINA MARTINS A SEGUIR:

1. EXTRAÇÃO: 
   - Identifique TODAS as competências técnicas, ferramentas, metodologias, soft skills e qualificações
   - Capture termos compostos (ex: "machine learning", "gestão de projetos") como unidades únicas
   - IGNORE termos genéricos como "dinâmico", "proativo", "inovador", "estratégico" quando isolados
   - FOQUE em competências ESPECÍFICAS e MENSURÁVEIS

2. CONTAGEM DE FREQUÊNCIA:
   - Calcule em quantas das {total_vagas} vagas cada termo aparece
   - Considere variações do mesmo termo (SQL/MySQL, React/React.js) como ocorrências do termo principal

3. CATEGORIZAÇÃO em três grupos:
   - TÉCNICAS: Conhecimentos específicos da área, linguagens de programação, frameworks, metodologias
   - FERRAMENTAS: Softwares, plataformas, ferramentas de produtividade (Excel, SAP, Photoshop)
   - COMPORTAMENTAIS: Soft skills REAIS e específicas (não adjetivos genéricos)

4. PRIORIZAÇÃO por frequência:
   - ESSENCIAL: presente em >60% das vagas
   - IMPORTANTE: presente em 30-60% das vagas
   - COMPLEMENTAR: presente em <30% das vagas

5. TOP 10 CAROLINA MARTINS:
   - Liste as 10 palavras-chave mais estratégicas combinando frequência e relevância para o cargo

REGRAS CRÍTICAS - LEIA COM ATENÇÃO:

❌ PALAVRAS PROIBIDAS (NUNCA incluir no resultado):
- Stop words: você, nosso, nossa, para, com, sem, sobre, após, mais, menos, muito
- Genéricos sem contexto: desenvolvimento, experiência, conhecimento, habilidade, oportunidade
- Adjetivos vazios: bom, ótimo, excelente, dinâmico, proativo, inovador, estratégico
- Palavras de contexto: empresa, cliente, equipe, vaga, candidato, profissional, mercado
- Verbos comuns: fazer, ter, ser, estar, poder, dever, buscar, atuar

✅ EXEMPLOS DE BOAS PALAVRAS-CHAVE:
- Técnicas: React.js, Python, Node.js, AWS, Docker, Kubernetes, SQL, MongoDB, API REST
- Ferramentas: Jira, Figma, Tableau, Power BI, Git, Postman, VS Code, Slack
- Comportamentais: gestão de conflitos, mentoria de equipes, apresentação executiva
- Termos compostos: machine learning, cloud computing, metodologia ágil, design thinking

⚠️ IMPORTANTE:
- Mínimo 30 palavras únicas relevantes
- Cada palavra do TOP 10 deve ser ÚTIL para otimizar um currículo
- Preserve termos em inglês quando forem padrão do mercado (não traduza)
- Mantenha o case original (React, não react; AWS, não aws)

TEXTO DAS VAGAS:
{texto_vagas}

RETORNE APENAS JSON VÁLIDO, SEM TEXTO ADICIONAL!

FORMATO JSON OBRIGATÓRIO:
{{
  "analise_metadados": {{
    "cargo_analisado": "{cargo_objetivo}",
    "area_analisada": "{area_interesse}",
    "total_vagas": {total_vagas},
    "data_analise": "{datetime.now().strftime('%Y-%m-%d')}",
    "total_palavras_unicas": 0
  }},
  "top_10_carolina_martins": [
    {{"termo": "exemplo", "frequencia_absoluta": 85, "frequencia_percentual": 85.0, "categoria": "tecnica"}},
    ...
  ],
  "mpc_completo": {{
    "essenciais": [
      {{"termo": "...", "categoria": "tecnica|ferramentas|comportamental", "frequencia_absoluta": 65, "frequencia_percentual": 65.0}},
      ...
    ],
    "importantes": [
      ...
    ],
    "complementares": [
      ...
    ]
  }},
  "insights_adicionais": {{
    "tendencias_emergentes": ["lista de tecnologias/skills em crescimento"],
    "gaps_identificados": ["competências pouco mencionadas mas potencialmente importantes"],
    "recomendacoes": ["sugestões específicas para o candidato"]
  }}
}}"""
        
        return prompt
    
    def _chamar_claude(self, prompt: str) -> Dict[str, Any]:
        """Chama API do Claude para análise"""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                temperature=0.3,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Extrair JSON da resposta
            texto_resposta = response.content[0].text
            
            # Tentar encontrar JSON na resposta
            inicio = texto_resposta.find('{')
            fim = texto_resposta.rfind('}') + 1
            
            if inicio >= 0 and fim > inicio:
                json_str = texto_resposta[inicio:fim]
                return json.loads(json_str)
            else:
                raise ValueError("JSON não encontrado na resposta")
                
        except Exception as e:
            print(f"Erro ao chamar Claude: {e}")
            raise
    
    def _chamar_gpt4(self, prompt: str) -> Dict[str, Any]:
        """Chama API do GPT-4 para análise"""
        try:
            response = self.openai_client.ChatCompletion.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "Você é um especialista em análise de vagas e extração de palavras-chave. Sempre retorne JSON válido."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=4000,
                response_format={"type": "json_object"}
            )
            
            texto_resposta = response.choices[0].message.content
            return json.loads(texto_resposta)
            
        except Exception as e:
            print(f"Erro ao chamar GPT-4: {e}")
            raise
    
    def _chamar_gemini(self, prompt: str) -> Dict[str, Any]:
        """Chama API do Gemini 2.5 Flash para análise"""
        try:
            # Configuração otimizada para Gemini Pro
            response = self.gemini_model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.3,
                    "max_output_tokens": 4000,  # Limite seguro
                    # Removido response_mime_type que pode causar problemas
                }
            )
            
            # Com response_mime_type, o Gemini 2.5 Flash já retorna JSON estruturado
            texto_resposta = response.text
            
            # Debug: imprimir primeiros caracteres da resposta
            print(f"DEBUG: Resposta Gemini (primeiros 200 chars): {texto_resposta[:200]}")
            
            try:
                # Tenta parse direto já que configuramos JSON output
                return json.loads(texto_resposta)
            except json.JSONDecodeError as e:
                print(f"DEBUG: Erro de JSON na posição {e.pos}: {e.msg}")
                print(f"DEBUG: Contexto do erro: ...{texto_resposta[max(0, e.pos-50):e.pos+50]}...")
                
                # Tenta limpar JSON comum problemas
                # Remove possíveis caracteres extras no início/fim
                texto_limpo = texto_resposta.strip()
                
                # Remove possíveis markdown code blocks
                if texto_limpo.startswith("```json"):
                    texto_limpo = texto_limpo[7:]
                if texto_limpo.startswith("```"):
                    texto_limpo = texto_limpo[3:]
                if texto_limpo.endswith("```"):
                    texto_limpo = texto_limpo[:-3]
                
                # Tenta novamente após limpeza
                try:
                    return json.loads(texto_limpo.strip())
                except json.JSONDecodeError:
                    # Fallback para extração manual se necessário
                    inicio = texto_resposta.find('{')
                    fim = texto_resposta.rfind('}') + 1
                    
                    if inicio >= 0 and fim > inicio:
                        json_str = texto_resposta[inicio:fim]
                        # Última tentativa com JSON extraído
                        try:
                            return json.loads(json_str)
                        except json.JSONDecodeError as e2:
                            print(f"DEBUG: Falha final no parse. Erro: {e2}")
                            print(f"DEBUG: JSON extraído tem {len(json_str)} caracteres")
                            # Salvar resposta para debug
                            with open('gemini_response_debug.json', 'w', encoding='utf-8') as f:
                                f.write(texto_resposta)
                            print("DEBUG: Resposta completa salva em gemini_response_debug.json")
                            raise ValueError(f"JSON inválido na resposta: {e2}")
                    else:
                        raise ValueError("JSON não encontrado na resposta")
                
        except Exception as e:
            print(f"Erro ao chamar Gemini: {e}")
            raise
    
    def _processar_resultado_ia(self, resultado: Dict[str, Any], modelo: str) -> Dict[str, Any]:
        """Processa e valida resultado da IA"""
        # Adicionar metadados
        resultado['analise_metadados']['modelo_ia_usado'] = modelo
        
        # Calcular total de palavras únicas
        todas_palavras = set()
        
        if 'mpc_completo' in resultado:
            for nivel in ['essenciais', 'importantes', 'complementares']:
                if nivel in resultado['mpc_completo']:
                    for palavra in resultado['mpc_completo'][nivel]:
                        todas_palavras.add(palavra['termo'])
        
        resultado['analise_metadados']['total_palavras_unicas'] = len(todas_palavras)
        
        # Validar top 10
        if 'top_10_carolina_martins' not in resultado:
            resultado['top_10_carolina_martins'] = []
        
        return resultado