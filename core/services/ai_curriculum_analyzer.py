"""
Analisador de Currículo com IA Real
Usa OpenAI/Anthropic para análise qualitativa baseada na metodologia Carolina Martins
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional
import openai
from anthropic import Anthropic
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class AICurriculumAnalyzer:
    """
    Analisador inteligente que usa IA para avaliar qualidade do currículo
    seguindo a metodologia dos 13 passos da Carolina Martins
    """
    
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        
        # Debug das chaves
        openai_key = os.getenv('OPENAI_API_KEY', '')
        anthropic_key = os.getenv('ANTHROPIC_API_KEY', '')
        
        print(f"🔑 OpenAI Key disponível: {bool(openai_key and 'sk-' in openai_key)}")
        print(f"🔑 Anthropic Key disponível: {bool(anthropic_key and 'sk-' in anthropic_key)}")
        
        # Inicializar clientes de IA
        if openai_key and openai_key != 'your_openai_api_key_here' and 'sk-' in openai_key:
            openai.api_key = openai_key
            self.openai_client = openai
            print("✅ Cliente OpenAI inicializado")
            
        if anthropic_key and anthropic_key != 'your_anthropic_api_key_here' and 'sk-' in anthropic_key:
            self.anthropic_client = Anthropic(api_key=anthropic_key)
            print("✅ Cliente Anthropic inicializado")
    
    async def analisar_curriculo_completo(self, texto_curriculo: str, objetivo_vaga: str = "", palavras_chave_usuario: List[str] = None) -> Dict[str, Any]:
        """
        Análise completa usando IA seguindo metodologia Carolina Martins
        
        Returns:
            Análise detalhada com score real, elementos e recomendações
        """
        
        if palavras_chave_usuario is None:
            palavras_chave_usuario = []
        
        palavras_chave_str = ", ".join(palavras_chave_usuario) if palavras_chave_usuario else "Não fornecidas"
        
        prompt = f"""
# PERSONA E OBJETIVO
Você é Carolina Martins, criadora da metodologia "Carreira Meteórica" e mentora sênior de carreira com 20 anos de experiência. Sua missão é realizar um diagnóstico RIGOROSO e ESTRATÉGICO do currículo, não apenas verificando estrutura, mas avaliando profundamente sua eficácia para passar pela triagem de 6-30 segundos e conquistar a vaga desejada.

# CONTEXTO PARA ANÁLISE
Você receberá três informações cruciais:
1. **Currículo completo**: {texto_curriculo}
2. **Vaga alvo**: {objetivo_vaga if objetivo_vaga else "Não especificada - análise genérica"}
3. **Palavras-chave estratégicas**: [{palavras_chave_str}]

# CRITÉRIOS DE AVALIAÇÃO - OS 3 PILARES DA METODOLOGIA

## PILAR 1: ESTRATÉGIA E ALINHAMENTO (Peso 50%)
**Lei do Desapego em Ação:**
- O currículo foi CLARAMENTE personalizado para esta vaga específica?
- Informações irrelevantes foram ELIMINADAS para dar foco ao que importa?
- O campo "Objetivo" corresponde EXATAMENTE ao título da vaga?
- O Resumo funciona como um "trailer" de filme (máx 10 linhas) que vende o profissional em 6 segundos?
- As palavras-chave foram integradas NATURALMENTE no resumo e experiências?

**VIOLAÇÕES GRAVES DA LEI DO DESAPEGO:**
- CPF, RG, data nascimento, estado civil = demonstra amadorismo
- Endereço completo com CEP = risco de segurança
- Seção de Hobbies = totalmente irrelevante
- Informações pessoais desnecessárias = falta de profissionalismo

## PILAR 2: CONTEÚDO DE IMPACTO E RESULTADOS (Peso 40%)
**A Regra de Ouro - RESULTADOS > TAREFAS:**
- Cada experiência profissional (>8 meses) DEVE apresentar resultados
- Resultados tangíveis: números, percentuais, valores, métricas
- Resultados intangíveis: melhorias de processo, reconhecimentos
- Verbos de ação fortes: liderei, implementei, desenvolvi, alcancei
- Evitar verbos fracos: ajudei, participei, fiz, auxiliei

**Storytelling de Carreira:**
- As experiências contam uma história de evolução profissional?
- Promoções estão claras e bem estruturadas?
- A ordem das seções valoriza os pontos fortes para ESTA vaga?

## PILAR 3: PROFISSIONALISMO E FORMATAÇÃO (Peso 10%)
**Visual que Passa Confiança:**
- Formatação limpa: fundo branco, fonte preta, sem cores ou ícones
- Estrutura clara: seções bem definidas, fácil leitura rápida
- Português impecável: zero erros de digitação ou gramática
- E-mail profissional: gmail/outlook, sem números ou apelidos

# SISTEMA DE PENALIZAÇÕES RIGOROSO

**COMECE com 100 pontos e SUBTRAIA:**

**Violações da Lei do Desapego:**
- CPF/RG presente: -30 pontos
- Data nascimento/idade: -30 pontos
- Estado civil: -30 pontos
- Endereço completo: -30 pontos
- Seção Hobbies: -40 pontos
- Foto no currículo: -40 pontos

**Falhas Metodológicas Graves:**
- Objetivo genérico "busco oportunidade": -40 pontos
- Sem resumo executivo: -40 pontos
- ZERO resultados quantificados: -50 pontos
- Email não profissional (hotmail/números): -20 pontos
- Pretensão salarial: -30 pontos

**Erros de Conteúdo:**
- Linguagem informal (fiz, ajudei): -30 pontos
- Habilidades genéricas (proativo, dinâmico): -20 pontos
- "Pacote Office completo": -10 pontos
- CNH sem ser motorista: -10 pontos
- Cursos irrelevantes de 40h: -10 pontos

**REGRA FINAL**: Se o currículo acumular mais de 150 pontos em penalizações, o score máximo é 20.

# ESTRUTURA DE RESPOSTA (JSON OBRIGATÓRIO)
Sua resposta deve ser um único bloco de código JSON, sem NENHUM texto antes ou depois:

{{
    "penalizacoes_aplicadas": {{
        "violacoes_lei_desapego": [
            {{"item": "CPF presente", "encontrado": true/false, "penalizacao": -30}},
            {{"item": "Data nascimento", "encontrado": true/false, "penalizacao": -30}},
            {{"item": "Estado civil", "encontrado": true/false, "penalizacao": -30}},
            {{"item": "Endereço completo", "encontrado": true/false, "penalizacao": -30}},
            {{"item": "Seção Hobbies", "encontrado": true/false, "penalizacao": -40}},
            {{"item": "Foto no currículo", "encontrado": true/false, "penalizacao": -40}}
        ],
        "falhas_metodologicas": [
            {{"item": "Objetivo genérico", "encontrado": true/false, "penalizacao": -40}},
            {{"item": "Sem resumo executivo", "encontrado": true/false, "penalizacao": -40}},
            {{"item": "Zero resultados", "encontrado": true/false, "penalizacao": -50}},
            {{"item": "Email não profissional", "encontrado": true/false, "penalizacao": -20}},
            {{"item": "Pretensão salarial", "encontrado": true/false, "penalizacao": -30}}
        ],
        "erros_conteudo": [
            {{"item": "Linguagem informal", "encontrado": true/false, "penalizacao": -30}},
            {{"item": "Habilidades genéricas", "encontrado": true/false, "penalizacao": -20}},
            {{"item": "Pacote Office completo", "encontrado": true/false, "penalizacao": -10}},
            {{"item": "CNH irrelevante", "encontrado": true/false, "penalizacao": -10}}
        ],
        "total_penalizacoes": <soma de TODAS as penalizações onde encontrado=true>
    }},
    "score_geral_meteoro": <100 - total_penalizacoes, mínimo 0, máximo 100>,
    "analise_estrategica": {{
        "alinhamento_com_vaga": {{"nota": <0-10>, "feedback": "O currículo foi personalizado para esta vaga específica? Aplica a Lei do Desapego?"}},
        "qualidade_resumo_trailer": {{"nota": <0-10>, "feedback": "O resumo consegue vender o profissional em 6 segundos? Tem no máximo 10 linhas?"}},
        "uso_de_palavras_chave": {{"nota": <0-10>, "feedback": "As palavras-chave foram integradas naturalmente ou estão ausentes/forçadas?"}}
    }},
    "analise_de_conteudo": {{
        "foco_em_resultados": {{"nota": <0-10>, "feedback": "CRÍTICO: Cada experiência apresenta resultados tangíveis ou intangíveis? Usa verbos de ação fortes?"}},
        "storytelling_de_carreira": {{"nota": <0-10>, "feedback": "A progressão de carreira está clara? A ordem das seções é estratégica para esta vaga?"}}
    }},
    "analise_formal": {{
        "formatacao_e_clareza": {{"nota": <0-10>, "feedback": "O currículo tem formatação profissional, limpa e facilita a leitura rápida?"}},
        "validacao_honestidade": {{"nota": <0-10>, "feedback": "As informações são consistentes? Há erros de português ou dados suspeitos?"}}
    }},
    "diagnostico_final_mentor": {{
        "pontos_fortes_meteoro": [
            "Liste 2-3 pontos APENAS se o currículo tem score > 60. Caso contrário: ['Nenhum ponto forte identificado - currículo precisa ser refeito']"
        ],
        "pontos_de_melhoria_urgentes": [
            "Liste as 3 ações MAIS CRÍTICAS para transformar este currículo em meteórico"
        ],
        "red_flags": [
            "Liste TODOS os problemas graves que eliminariam o candidato na triagem"
        ],
        "caminho_para_100": {{
            "explicacao_score": <string explicando por que o score atual>,
            "falhas_criticas": [
                "Lista DINÂMICA das violações graves que zeraram ou reduziram drasticamente o score"
            ],
            "erros_conteudo": [
                "Lista DINÂMICA dos problemas de conteúdo e profissionalismo"
            ],
            "plano_acao_100": {{
                "limpeza_radical": [
                    "Ações específicas de eliminação baseadas nas violações encontradas"
                ],
                "direcionamento_estrategico": [
                    "Ações para personalizar o currículo para a vaga"
                ],
                "foco_em_impacto": [
                    "Como transformar tarefas em resultados quantificados"
                ]
            }},
            "conceitos_metodologia": {{
                "lei_do_desapego": "Como aplicar: [explicação específica para este currículo]",
                "curriculo_trailer": "Como criar: [orientação específica]",
                "resultados_vs_tarefas": "Exemplos práticos: [baseados nas experiências do candidato]",
                "triagem_6_segundos": "O que mostrar primeiro: [sugestões personalizadas]"
            }}
        }}
    }}
}}

        ### CÁLCULO DO SCORE - SISTEMA DE PENALIZAÇÕES OBRIGATÓRIO
        
        **COMECE COM 100 PONTOS E APLIQUE TODAS AS PENALIZAÇÕES:**
        
        **VIOLAÇÕES GRAVES (reduzir imediatamente):**
        - Tem CPF? = -40 pontos
        - Tem data de nascimento? = -40 pontos  
        - Tem estado civil? = -40 pontos
        - Tem seção de HOBBIES? = -30 pontos
        - Tem endereço completo? = -40 pontos
        - Email hotmail/yahoo/números? = -20 pontos
        - Tem pretensão salarial? = -20 pontos
        - Objetivo genérico "busco oportunidade"? = -40 pontos
        
        **FALHAS METODOLÓGICAS:**
        - NÃO tem resumo executivo? = -30 pontos
        - ZERO resultados quantificados? = -50 pontos
        - Usa "fiz", "ajudei", "participei"? = -30 pontos
        - Tem seção "HABILIDADES" genéricas? = -20 pontos
        - Pacote Office completo? = -10 pontos
        - CNH sem ser motorista? = -10 pontos
        
        **CALCULE O SCORE FINAL:**
        1. Identifique TODAS as violações
        2. Some TODAS as penalizações
        3. Subtraia de 100
        4. Se o resultado for negativo, score = 0
        
        **EXEMPLO REAL:**
        Currículo com CPF (-40) + Hobbies (-30) + Email hotmail (-20) + Zero resultados (-50) + "busco oportunidade" (-40) + Habilidades genéricas (-20) = -200 pontos
        Score final: 100 - 200 = 0 (mínimo é 0)
        
        VOCÊ DEVE LISTAR TODAS AS PENALIZAÇÕES APLICADAS!
        
        # EXPLICAÇÃO OBRIGATÓRIA DO SCORE - TOM DE MENTOR
        
        No campo "caminho_para_100", você DEVE agir como Carolina Martins explicando:
        
        1. **explicacao_score**: 
           - Se score = 0: "Seu currículo atual contém múltiplas falhas críticas que o tornam ineficaz para um processo seletivo moderno. A presença desses erros zera o score inicial."
           - Se score < 30: "O currículo apresenta violações graves da metodologia que comprometem severamente suas chances."
           - Se score 30-60: "O currículo tem potencial mas precisa de ajustes significativos para se tornar meteórico."
           - Se score > 60: "Bom trabalho! O currículo está no caminho certo, mas ainda há oportunidades de melhoria."
        
        2. **falhas_criticas**: Liste APENAS as violações que encontrou, não invente. Exemplos:
           - "Violação da Lei do Desapego e LGPD: CPF, data nascimento, estado civil presentes"
           - "Falta de foco estratégico: objetivo genérico e ausência de resumo executivo"
           - "Falta de prova de impacto: zero resultados quantificados"
           - "Conteúdo irrelevante: seção de hobbies, pretensão salarial"
        
        3. **erros_conteudo**: Problemas menos graves mas importantes:
           - "Linguagem fraca: uso de 'fiz', 'ajudei' em vez de verbos de ação"
           - "Habilidades genéricas que não comprovam competência"
           - "Email não profissional (hotmail/yahoo com números)"
        
        4. **plano_acao_100**: Seja ESPECÍFICO e PRÁTICO:
           - limpeza_radical: Baseado nas violações reais encontradas
           - direcionamento_estrategico: Como personalizar para a vaga alvo
           - foco_em_impacto: Exemplos de como quantificar baseado no que está no currículo
        
        5. **conceitos_metodologia**: Explique de forma prática:
           - Como aplicar cada conceito no contexto DESTE currículo específico
           - Não seja genérico, use exemplos do próprio currículo do candidato
        """
        
        try:
            print(f"🔍 Analisando currículo com IA...")
            print(f"📊 Anthropic disponível: {self.anthropic_client is not None}")
            print(f"📊 OpenAI disponível: {self.openai_client is not None}")
            
            if self.anthropic_client:
                print("🤖 Usando Anthropic/Claude para análise...")
                response = await self._chamar_anthropic(prompt)
            elif self.openai_client:
                print("🤖 Usando OpenAI/GPT para análise...")
                response = await self._chamar_openai(prompt)
            else:
                print("⚠️  Nenhuma IA configurada, usando fallback...")
                # Fallback para análise básica se não tiver IA
                return self._analise_basica_fallback(texto_curriculo)
            
            # Limpar resposta para garantir apenas JSON
            response_clean = response.strip()
            
            # Se a resposta começar com texto antes do JSON, extrair apenas o JSON
            if response_clean and not response_clean.startswith('{'):
                # Procurar pelo início do JSON
                json_start = response_clean.find('{')
                if json_start != -1:
                    response_clean = response_clean[json_start:]
            
            # Se houver texto após o JSON, remover
            if response_clean:
                # Contar chaves para encontrar o fim do JSON
                brace_count = 0
                json_end = -1
                for i, char in enumerate(response_clean):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            json_end = i + 1
                            break
                
                if json_end > 0:
                    response_clean = response_clean[:json_end]
            
            # Parse da resposta JSON e adaptar para formato esperado
            try:
                analise_resultado = json.loads(response_clean)
            except json.JSONDecodeError as e:
                print(f"Erro ao parsear JSON: {e}")
                print(f"Resposta recebida: {response_clean[:500]}...")
                raise
            
            # Adaptar para formato compatível com frontend atual
            return self._adaptar_formato_resposta(analise_resultado)
            
        except Exception as e:
            print(f"Erro na análise com IA: {e}")
            return self._analise_basica_fallback(texto_curriculo)
    
    async def _chamar_anthropic(self, prompt: str) -> str:
        """Chama API do Claude/Anthropic"""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=2000,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            raise Exception(f"Erro Anthropic: {e}")
    
    async def _chamar_openai(self, prompt: str) -> str:
        """Chama API do OpenAI"""
        try:
            # Nova sintaxe da OpenAI
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.1
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Erro OpenAI: {e}")
    
    def _analise_basica_fallback(self, texto_curriculo: str) -> Dict[str, Any]:
        """Análise básica quando IA não está disponível"""
        print("⚠️  ATENÇÃO: Usando análise FALLBACK - IA não está configurada!")
        print("❌ Para análise real com IA, configure OPENAI_API_KEY ou ANTHROPIC_API_KEY no arquivo .env")
        
        texto_lower = texto_curriculo.lower()
        
        # Detectar red flags básicos
        red_flags = []
        if any(flag in texto_lower for flag in ['quando dava vontade', 'não lembro', 'acho que', 'número falso']):
            red_flags.append("Linguagem não profissional detectada")
        
        if any(info in texto_lower for info in ['signo', 'time', 'altura', 'peso', 'religião']):
            red_flags.append("Informações pessoais irrelevantes")
        
        # Score fixo de 35 para indicar que é fallback
        score_final = 35
        
        return {
            "score_geral": score_final,
            "elementos_metodologia": {},
            "validacoes_honestidade": {},
            "red_flags": ["⚠️ ANÁLISE SIMPLES - Configure API keys para análise com IA real"] + red_flags,
            "pontos_fortes": [],
            "recomendacoes_prioritarias": ["Configure OPENAI_API_KEY ou ANTHROPIC_API_KEY no arquivo .env para análise completa"],
            "palavras_chave_identificadas": []
        }
    
    def _adaptar_formato_resposta(self, analise_ia: Dict[str, Any]) -> Dict[str, Any]:
        """Adapta o formato da IA para o formato esperado pelo frontend"""
        
        # Extrair dados principais
        score = analise_ia.get('score_geral_meteoro', 0)
        analise_estrategica = analise_ia.get('analise_estrategica', {})
        analise_conteudo = analise_ia.get('analise_de_conteudo', {})
        analise_formal = analise_ia.get('analise_formal', {})
        feedback = analise_ia.get('diagnostico_final_mentor', {})
        penalizacoes = analise_ia.get('penalizacoes_aplicadas', {})
        
        # Simular elementos metodologia para compatibilidade
        elementos_metodologia = {
            'dados_pessoais': {'presente': True, 'qualidade': 8},
            'objetivo_profissional': {
                'presente': analise_estrategica.get('alinhamento_com_vaga', {}).get('nota', 0) > 0,
                'qualidade': analise_estrategica.get('alinhamento_com_vaga', {}).get('nota', 0)
            },
            'resumo_executivo': {
                'presente': analise_estrategica.get('qualidade_resumo_trailer', {}).get('nota', 0) > 0,
                'qualidade': analise_estrategica.get('qualidade_resumo_trailer', {}).get('nota', 0)
            },
            'experiencias': {
                'presente': analise_conteudo.get('foco_em_resultados', {}).get('nota', 0) > 0,
                'qualidade': analise_conteudo.get('foco_em_resultados', {}).get('nota', 0)
            },
            'resultados_quantificados': {
                'presente': analise_conteudo.get('foco_em_resultados', {}).get('nota', 0) > 5,
                'qualidade': analise_conteudo.get('foco_em_resultados', {}).get('nota', 0)
            },
            'formacao': {
                'presente': analise_conteudo.get('storytelling_de_carreira', {}).get('nota', 0) > 0,
                'qualidade': analise_conteudo.get('storytelling_de_carreira', {}).get('nota', 0)
            }
        }
        
        # Validações de honestidade
        validacoes_honestidade = {
            'datas_consistentes': {
                'status': analise_formal.get('validacao_honestidade', {}).get('nota', 0) > 5,
                'observacao': analise_formal.get('validacao_honestidade', {}).get('feedback', '')
            },
            'informacoes_verificaveis': {
                'status': analise_formal.get('validacao_honestidade', {}).get('nota', 0) > 5,
                'observacao': 'Baseado na análise de consistência'
            },
            'detalhamento_adequado': {
                'status': analise_conteudo.get('foco_em_resultados', {}).get('nota', 0) > 5,
                'observacao': analise_conteudo.get('foco_em_resultados', {}).get('feedback', '')
            },
            'verbos_acao': {
                'status': analise_conteudo.get('foco_em_resultados', {}).get('nota', 0) > 3,
                'observacao': 'Baseado na análise das experiências'
            }
        }
        
        # Processar caminho_para_100 e calcular total de penalizações
        caminho_para_100 = feedback.get('caminho_para_100', {})
        
        # Calcular total de penalizações se houver dados de penalizações
        if penalizacoes:
            total_penalizacoes_calculado = 0
            
            # Somar todas as penalizações encontradas
            for categoria in ['violacoes_lei_desapego', 'falhas_metodologicas', 'erros_conteudo']:
                if categoria in penalizacoes:
                    for item in penalizacoes[categoria]:
                        if item.get('encontrado', False):
                            total_penalizacoes_calculado += abs(item.get('penalizacao', 0))
            
            # Atualizar o total no caminho_para_100
            caminho_para_100['total_penalizacoes'] = total_penalizacoes_calculado
            
            # Criar lista de penalizações detalhadas se não existir
            if 'penalizacoes_detalhadas' not in caminho_para_100:
                penalizacoes_detalhadas = []
                for categoria in ['violacoes_lei_desapego', 'falhas_metodologicas', 'erros_conteudo']:
                    if categoria in penalizacoes:
                        for item in penalizacoes[categoria]:
                            if item.get('encontrado', False):
                                penalizacoes_detalhadas.append(f"{item['item']}: {item['penalizacao']} pontos")
                caminho_para_100['penalizacoes_detalhadas'] = penalizacoes_detalhadas
            
            # Adicionar explicação quando há múltiplas falhas críticas
            if total_penalizacoes_calculado >= 100 and score == 0:
                caminho_para_100['explicacao_score'] = "A presença de múltiplas falhas críticas zera o score inicial."
                caminho_para_100['total_penalizacoes_texto'] = f"Total de penalizações: -{total_penalizacoes_calculado} pontos"
            else:
                caminho_para_100['total_penalizacoes_texto'] = f"Total de penalizações: -{total_penalizacoes_calculado} pontos"

        return {
            'score_geral': score,
            'elementos_metodologia': elementos_metodologia,
            'validacoes_honestidade': validacoes_honestidade,
            'red_flags': feedback.get('red_flags', []),
            'pontos_fortes': feedback.get('pontos_fortes_meteoro', []),
            'recomendacoes_prioritarias': feedback.get('pontos_de_melhoria_urgentes', []),
            'palavras_chave_identificadas': [],
            'caminho_para_100': caminho_para_100,  # Usar o objeto processado
            'analise_completa_ia': analise_ia  # Preservar análise completa para debug
        }