"""
Agente 0: Diagnóstico e Onboarding - Metodologia Carolina Martins

Este agente implementa o diagnóstico inicial completo baseado na metodologia 
extraída das 89 transcrições. Responsável por:

1. Análise de currículo atual
2. Análise de perfil LinkedIn
3. Questionário de sabotadores
4. Mapeamento de experiência profissional vs mercado
5. Alinhamento de expectativas (70% de aderência)
6. Configuração personalizada para outros agentes
"""

import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from sqlalchemy.orm import Session
from core.models import (
    User, SituacaoCarreira, StatusEmprego, Sabotador, 
    NivelSenioridade, Curriculo, ExperienciaProfissional,
    FormacaoAcademica, CompetenciaUsuario
)

class DiagnosticoCarolinaMartins:
    """Implementação do diagnóstico inicial da metodologia Carolina Martins"""
    
    def __init__(self, db: Session):
        self.db = db
        self.sabotadores_definicoes = self._carregar_sabotadores()
        self.criterios_senioridade = self._carregar_criterios_senioridade()
    
    def executar_diagnostico_completo(self, dados_usuario: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa diagnóstico completo seguindo metodologia Carolina Martins
        
        Retorna:
        - Perfil estruturado
        - Sabotadores identificados
        - Situação de carreira
        - Gaps e pontos fortes
        - Configuração para outros agentes
        """
        resultado = {
            "perfil_basico": self._processar_dados_basicos(dados_usuario),
            "experiencia_profissional": self._analisar_experiencia(dados_usuario),
            "sabotadores": self._identificar_sabotadores(dados_usuario.get("questionario_sabotadores", {})),
            "situacao_carreira": self._determinar_situacao_carreira(dados_usuario),
            "alinhamento_expectativas": self._validar_expectativas(dados_usuario),
            "gaps_e_fortes": self._mapear_gaps_e_fortes(dados_usuario),
            "configuracao_agentes": self._gerar_configuracao_agentes(dados_usuario),
            "score_diagnostico": 0.0,
            "recomendacoes": []
        }
        
        # Calcula score final e gera recomendações
        resultado["score_diagnostico"] = self._calcular_score_diagnostico(resultado)
        resultado["recomendacoes"] = self._gerar_recomendacoes(resultado)
        
        return resultado
    
    def analisar_curriculo_atual(self, arquivo_curriculo: str) -> Dict[str, Any]:
        """
        Analisa currículo atual contra critérios Carolina Martins
        
        Verifica:
        - Estrutura metodológica
        - Presença dos 13 passos
        - Validações de honestidade
        - Formatação adequada
        """
        analise = {
            "estrutura_metodologica": self._verificar_estrutura_metodologica(arquivo_curriculo),
            "validacoes_honestidade": self._verificar_honestidade(arquivo_curriculo),
            "formatacao": self._analisar_formatacao(arquivo_curriculo),
            "palavras_chave_atuais": self._extrair_palavras_chave_atuais(arquivo_curriculo),
            "gaps_estruturais": [],
            "score_qualidade": 0.0
        }
        
        # Identifica gaps estruturais
        analise["gaps_estruturais"] = self._identificar_gaps_estruturais(analise)
        
        # Calcula score baseado na metodologia
        analise["score_qualidade"] = self._calcular_score_curriculo_atual(analise)
        
        return analise
    
    def analisar_perfil_linkedin(self, url_linkedin: str) -> Dict[str, Any]:
        """
        Analisa perfil LinkedIn atual para otimização posterior
        
        Avalia:
        - Completude do perfil
        - Qualidade das descrições
        - Presença de palavras-chave
        - Estratégia de conteúdo atual
        """
        # Implementação será expandida com scraping/API do LinkedIn
        analise_base = {
            "url_valida": self._validar_url_linkedin(url_linkedin),
            "completude_estimada": 0.0,
            "elementos_faltando": [],
            "qualidade_headline": 0.0,
            "qualidade_sobre": 0.0,
            "estrategia_conteudo_atual": "inexistente",
            "ssi_estimado": 0.0,
            "recomendacoes_linkedin": []
        }
        
        return analise_base
    
    def _processar_dados_basicos(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Processa e valida dados básicos do usuário"""
        return {
            "nome": dados.get("nome", "").strip(),
            "email": dados.get("email", "").strip(),
            "telefone": self._formatar_telefone(dados.get("telefone", "")),
            "linkedin_url": self._validar_linkedin_url(dados.get("linkedin_url", "")),
            "cidade": dados.get("cidade", "").strip(),
            "estado": dados.get("estado", "").strip(),
            "disponibilidade_mudanca": dados.get("disponibilidade_mudanca", True),
            "regime_trabalho_preferido": dados.get("regime_trabalho", "hibrido")
        }
    
    def _analisar_experiencia(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa experiência seguindo conceitos Carolina Martins:
        - Experiência profissional (específica da área)
        - Experiência de mercado (total)
        """
        experiencias = dados.get("experiencias", [])
        area_objetivo = dados.get("area_objetivo", "")
        
        experiencia_mercado = 0  # Total em anos
        experiencia_profissional = 0  # Específica da área
        
        for exp in experiencias:
            meses = self._calcular_meses_experiencia(exp.get("data_inicio"), exp.get("data_fim"))
            experiencia_mercado += meses
            
            # Verifica se é experiência específica da área
            if self._experiencia_relevante_para_area(exp, area_objetivo):
                experiencia_profissional += meses
        
        # Converte para anos
        experiencia_mercado = round(experiencia_mercado / 12, 1)
        experiencia_profissional = round(experiencia_profissional / 12, 1)
        
        return {
            "experiencia_mercado": experiencia_mercado,
            "experiencia_profissional": experiencia_profissional,
            "nivel_atual": self._determinar_nivel_atual(experiencia_profissional),
            "nivel_objetivo": dados.get("nivel_objetivo", ""),
            "evolucao_realista": self._validar_evolucao_hierarquica(
                self._determinar_nivel_atual(experiencia_profissional),
                dados.get("nivel_objetivo", "")
            )
        }
    
    def _identificar_sabotadores(self, questionario: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identifica sabotadores baseado no questionário
        
        Sabotadores da metodologia Carolina Martins:
        - Hiper-racional
        - Hiper-realizador
        - Controlador
        - Hipervigilante
        - Inquieto
        - Complacente
        - Juiz
        - Vítima
        - Agradador
        - Evitador
        """
        scores_sabotadores = {}
        
        for sabotador, perguntas in self.sabotadores_definicoes.items():
            score = 0
            total_perguntas = len(perguntas)
            
            for pergunta_id in perguntas:
                resposta = questionario.get(pergunta_id, 0)  # 0-5 escala
                score += resposta
            
            # Normaliza score (0-1)
            scores_sabotadores[sabotador] = score / (total_perguntas * 5)
        
        # Identifica sabotadores principais (score > 0.6)
        sabotadores_principais = [
            sabotador for sabotador, score in scores_sabotadores.items()
            if score > 0.6
        ]
        
        return {
            "scores": scores_sabotadores,
            "principais": sabotadores_principais,
            "recomendacoes_personalizadas": self._gerar_recomendacoes_sabotadores(sabotadores_principais)
        }
    
    def _determinar_situacao_carreira(self, dados: Dict[str, Any]) -> str:
        """
        Determina situação de carreira baseada nos dados coletados
        
        Situações possíveis:
        - primeira_experiencia
        - transicao_area
        - ascensao_hierarquica
        - retorno_mercado
        - empregado_insatisfeito
        - empregado_explorando
        """
        experiencia_total = dados.get("experiencia_mercado", 0)
        area_atual = dados.get("area_atual", "")
        area_objetivo = dados.get("area_objetivo", "")
        status_emprego = dados.get("status_emprego", "")
        tempo_parado = dados.get("tempo_parado_mercado", 0)
        
        # Primeira experiência
        if experiencia_total < 1:
            return SituacaoCarreira.PRIMEIRA_EXPERIENCIA.value
        
        # Retorno ao mercado
        if tempo_parado > 12:  # Mais de 1 ano parado
            return SituacaoCarreira.RETORNO_MERCADO.value
        
        # Transição de área
        if area_atual != area_objetivo and area_atual and area_objetivo:
            return SituacaoCarreira.TRANSICAO_AREA.value
        
        # Desempregado insatisfeito vs explorando
        if status_emprego == StatusEmprego.EMPREGADO.value:
            satisfacao = dados.get("satisfacao_emprego_atual", 5)  # 1-10
            if satisfacao <= 5:
                return SituacaoCarreira.EMPREGADO_INSATISFEITO.value
            else:
                return SituacaoCarreira.EMPREGADO_EXPLORANDO.value
        
        # Ascensão hierárquica (padrão para quem busca crescer na mesma área)
        return SituacaoCarreira.ASCENSAO_HIERARQUICA.value
    
    def _validar_expectativas(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida expectativas baseado no critério Carolina Martins (70% de aderência)
        """
        cargo_objetivo = dados.get("cargo_objetivo", "")
        experiencia_profissional = dados.get("experiencia_profissional", 0)
        competencias_atuais = dados.get("competencias", [])
        
        # Simula requisitos típicos do cargo objetivo
        requisitos_cargo = self._obter_requisitos_tipicos_cargo(cargo_objetivo)
        
        # Calcula aderência
        score_experiencia = self._calcular_score_experiencia(experiencia_profissional, requisitos_cargo)
        score_competencias = self._calcular_score_competencias(competencias_atuais, requisitos_cargo)
        
        aderencia_total = (score_experiencia * 0.6) + (score_competencias * 0.4)
        
        return {
            "score_aderencia": aderencia_total,
            "atende_criterio_70": aderencia_total >= 0.7,
            "gaps_criticos": self._identificar_gaps_criticos(requisitos_cargo, competencias_atuais),
            "pontos_fortes": self._identificar_pontos_fortes(requisitos_cargo, competencias_atuais),
            "recomendacoes_desenvolvimento": self._gerar_plano_desenvolvimento(
                requisitos_cargo, competencias_atuais, aderencia_total
            )
        }
    
    def _mapear_gaps_e_fortes(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Mapeia gaps críticos e pontos fortes do perfil"""
        cargo_objetivo = dados.get("cargo_objetivo", "")
        experiencias = dados.get("experiencias", [])
        formacoes = dados.get("formacoes", [])
        competencias = dados.get("competencias", [])
        
        # Análise baseada no cargo objetivo
        requisitos_ideais = self._obter_requisitos_tipicos_cargo(cargo_objetivo)
        
        gaps_criticos = []
        pontos_fortes = []
        
        # Verifica gaps de experiência
        if not any(self._experiencia_relevante_para_area(exp, cargo_objetivo) for exp in experiencias):
            gaps_criticos.append("experiencia_area_especifica")
        
        # Verifica gaps de formação
        if not any(self._formacao_relevante_para_area(form, cargo_objetivo) for form in formacoes):
            gaps_criticos.append("formacao_area_especifica")
        
        # Verifica competências
        competencias_atuais = [comp.lower() for comp in competencias]
        for req in requisitos_ideais.get("competencias_obrigatorias", []):
            if req.lower() not in competencias_atuais:
                gaps_criticos.append(f"competencia_{req.lower().replace(' ', '_')}")
            else:
                pontos_fortes.append(f"competencia_{req.lower().replace(' ', '_')}")
        
        return {
            "gaps_criticos": gaps_criticos,
            "pontos_fortes": pontos_fortes,
            "prioridade_desenvolvimento": self._priorizar_gaps(gaps_criticos),
            "plano_acao": self._gerar_plano_acao_gaps(gaps_criticos)
        }
    
    def _gerar_configuracao_agentes(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera configuração personalizada para os outros agentes baseada no diagnóstico
        """
        return {
            "agente_1_palavras_chave": {
                "area_interesse": dados.get("area_objetivo", ""),
                "cargo_objetivo": dados.get("cargo_objetivo", ""),
                "nivel_senioridade": dados.get("nivel_objetivo", ""),
                "segmentos_preferenciais": dados.get("segmentos_interesse", []),
                "quantidade_minima_vagas": 50,
                "priorizar_por": "relevancia_experiencia"
            },
            "agente_2_curriculo": {
                "tipo_inicial": "base",
                "foco_experiencias": self._determinar_foco_experiencias(dados),
                "nivel_detalhamento": self._determinar_nivel_detalhamento(dados),
                "palavras_chave_priorizadas": [],  # Será preenchido pelo Agente 1
                "sabotadores_cuidados": dados.get("sabotadores_principais", [])
            },
            "agente_3_linkedin": {
                "estrategia_principal": self._determinar_estrategia_linkedin(dados),
                "frequencia_posts": self._calcular_frequencia_posts_recomendada(dados),
                "foco_networking": self._determinar_foco_networking(dados),
                "ssi_objetivo": self._definir_ssi_objetivo(dados)
            },
            "agente_4_conteudo": {
                "objetivo_conteudo": self._determinar_objetivo_conteudo(dados),
                "temas_autoridade": self._definir_temas_autoridade(dados),
                "distribuicao_conteudo": {"geral": 0.6, "especifico": 0.4},
                "calendario_inicial": self._gerar_calendario_inicial(dados)
            }
        }
    
    # Métodos auxiliares
    
    def _carregar_sabotadores(self) -> Dict[str, List[str]]:
        """Carrega definições dos sabotadores com perguntas do questionário"""
        return {
            Sabotador.HIPER_RACIONAL.value: ["q1", "q2", "q3"],  # IDs das perguntas
            Sabotador.HIPER_REALIZADOR.value: ["q4", "q5", "q6"],
            Sabotador.CONTROLADOR.value: ["q7", "q8", "q9"],
            Sabotador.HIPERVIGILANTE.value: ["q10", "q11", "q12"],
            Sabotador.INQUIETO.value: ["q13", "q14", "q15"],
            Sabotador.COMPLACENTE.value: ["q16", "q17", "q18"],
            Sabotador.JUIZ.value: ["q19", "q20", "q21"],
            Sabotador.VITIMA.value: ["q22", "q23", "q24"],
            Sabotador.AGRADADOR.value: ["q25", "q26", "q27"],
            Sabotador.EVITADOR.value: ["q28", "q29", "q30"]
        }
    
    def _carregar_criterios_senioridade(self) -> Dict[str, Dict[str, Any]]:
        """Carrega critérios de senioridade baseados na metodologia"""
        return {
            NivelSenioridade.ASSISTENTE.value: {"experiencia_min": 0, "experiencia_max": 1},
            NivelSenioridade.ANALISTA_JR.value: {"experiencia_min": 0, "experiencia_max": 2},
            NivelSenioridade.ANALISTA_PLENO.value: {"experiencia_min": 2, "experiencia_max": 5},
            NivelSenioridade.ANALISTA_SR.value: {"experiencia_min": 5, "experiencia_max": 8},
            NivelSenioridade.COORDENADOR.value: {"experiencia_min": 7, "experiencia_max": 12},
            NivelSenioridade.GERENTE.value: {"experiencia_min": 10, "experiencia_max": 20},
            NivelSenioridade.DIRETOR.value: {"experiencia_min": 15, "experiencia_max": None}
        }
    
    def _calcular_meses_experiencia(self, data_inicio: str, data_fim: Optional[str]) -> int:
        """Calcula meses de experiência entre duas datas"""
        try:
            inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
            fim = datetime.strptime(data_fim, "%Y-%m-%d") if data_fim else datetime.now()
            return int((fim - inicio).days / 30.44)
        except:
            return 0
    
    def _experiencia_relevante_para_area(self, experiencia: Dict[str, Any], area_objetivo: str) -> bool:
        """Verifica se experiência é relevante para área objetivo"""
        if not area_objetivo:
            return False
        
        area_obj_lower = area_objetivo.lower()
        cargo = experiencia.get("cargo", "").lower()
        empresa = experiencia.get("empresa", "").lower()
        descricao = experiencia.get("descricao", "").lower()
        
        # Verifica correspondência em cargo, empresa ou descrição
        return (area_obj_lower in cargo or 
                area_obj_lower in empresa or 
                area_obj_lower in descricao)
    
    def _determinar_nivel_atual(self, experiencia_anos: float) -> str:
        """Determina nível hierárquico atual baseado na experiência"""
        for nivel, criterios in self.criterios_senioridade.items():
            exp_min = criterios["experiencia_min"]
            exp_max = criterios["experiencia_max"]
            
            if exp_max is None:  # Diretor
                if experiencia_anos >= exp_min:
                    return nivel
            else:
                if exp_min <= experiencia_anos < exp_max:
                    return nivel
        
        return NivelSenioridade.ASSISTENTE.value
    
    def _validar_evolucao_hierarquica(self, nivel_atual: str, nivel_objetivo: str) -> Dict[str, Any]:
        """
        Valida evolução hierárquica baseada na metodologia Carolina Martins
        Máximo recomendado: 2 níveis de diferença
        """
        niveis_ordem = {
            NivelSenioridade.ASSISTENTE.value: 0,
            NivelSenioridade.ANALISTA_JR.value: 1,
            NivelSenioridade.ANALISTA_PLENO.value: 2,
            NivelSenioridade.ANALISTA_SR.value: 3,
            NivelSenioridade.COORDENADOR.value: 4,
            NivelSenioridade.GERENTE.value: 5,
            NivelSenioridade.DIRETOR.value: 6
        }
        
        atual_idx = niveis_ordem.get(nivel_atual, 0)
        objetivo_idx = niveis_ordem.get(nivel_objetivo, 0)
        diferenca = objetivo_idx - atual_idx
        
        if diferenca <= 0:
            return {"realista": True, "tipo": "lateral_ou_retrocesso", "diferenca": diferenca}
        elif diferenca == 1:
            return {"realista": True, "tipo": "evolucao_natural", "diferenca": diferenca}
        elif diferenca == 2:
            return {"realista": True, "tipo": "evolucao_ambiciosa", "diferenca": diferenca}
        else:
            return {"realista": False, "tipo": "muito_ambicioso", "diferenca": diferenca}
    
    def _obter_requisitos_tipicos_cargo(self, cargo: str) -> Dict[str, List[str]]:
        """Obtém requisitos típicos baseados no cargo objetivo"""
        # Base de conhecimento simplificada - será expandida
        requisitos_base = {
            "analista": {
                "competencias_obrigatorias": ["Excel", "Análise de dados", "Relatórios"],
                "competencias_desejaveis": ["Power BI", "SQL", "Inglês"],
                "experiencia_minima": 2
            },
            "coordenador": {
                "competencias_obrigatorias": ["Gestão de equipe", "Planejamento", "Liderança"],
                "competencias_desejaveis": ["Gestão de projetos", "Orçamento", "Inglês avançado"],
                "experiencia_minima": 5
            },
            "gerente": {
                "competencias_obrigatorias": ["Gestão estratégica", "Orçamento", "Liderança"],
                "competencias_desejaveis": ["MBA", "Inglês fluente", "Gestão de mudança"],
                "experiencia_minima": 8
            }
        }
        
        # Busca correspondência aproximada
        cargo_lower = cargo.lower()
        for tipo, reqs in requisitos_base.items():
            if tipo in cargo_lower:
                return reqs
        
        # Retorno padrão
        return {
            "competencias_obrigatorias": ["Experiência na área"],
            "competencias_desejaveis": ["Inglês", "Excel"],
            "experiencia_minima": 1
        }
    
    def _calcular_score_diagnostico(self, resultado: Dict[str, Any]) -> float:
        """Calcula score geral do diagnóstico"""
        score = 0.0
        
        # Dados básicos completos (20%)
        dados_basicos = resultado["perfil_basico"]
        campos_obrigatorios = ["nome", "email", "telefone", "linkedin_url"]
        completude_basica = sum(1 for campo in campos_obrigatorios if dados_basicos.get(campo)) / len(campos_obrigatorios)
        score += completude_basica * 20
        
        # Experiência adequada (30%)
        exp_data = resultado["experiencia_profissional"]
        if exp_data["evolucao_realista"]["realista"]:
            score += 30
        elif exp_data["evolucao_realista"]["diferenca"] <= 3:
            score += 20
        else:
            score += 10
        
        # Alinhamento de expectativas (30%)
        if resultado["alinhamento_expectativas"]["atende_criterio_70"]:
            score += 30
        else:
            score += resultado["alinhamento_expectativas"]["score_aderencia"] * 30
        
        # Gaps identificados e plano de ação (20%)
        gaps_data = resultado["gaps_e_fortes"]
        if gaps_data["plano_acao"]:
            score += 20
        elif gaps_data["gaps_criticos"]:
            score += 10
        
        return min(score, 100.0)
    
    def _gerar_recomendacoes(self, resultado: Dict[str, Any]) -> List[str]:
        """Gera recomendações personalizadas baseadas no diagnóstico"""
        recomendacoes = []
        
        # Baseado no score de aderência
        if not resultado["alinhamento_expectativas"]["atende_criterio_70"]:
            recomendacoes.append("Desenvolver competências críticas antes de aplicar para o cargo objetivo")
        
        # Baseado na evolução hierárquica
        if not resultado["experiencia_profissional"]["evolucao_realista"]["realista"]:
            recomendacoes.append("Considerar cargo intermediário para evolução gradual")
        
        # Baseado nos sabotadores
        sabotadores = resultado["sabotadores"]["principais"]
        if Sabotador.HIPER_RACIONAL.value in sabotadores:
            recomendacoes.append("Evitar excesso de análise - definir prazo para tomada de decisão")
        if Sabotador.PERFECCIONISTA.value in sabotadores:
            recomendacoes.append("Focar em entregas funcionais ao invés de perfeitas")
        
        # Baseado nos gaps
        gaps = resultado["gaps_e_fortes"]["gaps_criticos"]
        if "experiencia_area_especifica" in gaps:
            recomendacoes.append("Buscar experiência voluntária ou projetos na área objetivo")
        
        return recomendacoes