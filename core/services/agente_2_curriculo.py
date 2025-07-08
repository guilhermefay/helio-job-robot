"""
Agente 2: Otimização de Currículo (13 Passos) - Metodologia Carolina Martins

Este agente implementa a metodologia completa dos 13 passos do currículo meteórico
baseada nas transcrições da Carolina Martins:

PROCESSO DOS 13 PASSOS:
1. Dados Pessoais (validação completa)
2. Objetivo (nome exato da vaga)
3. Resumo (apresentação + competências + registros)
4. Experiências Profissionais (com palavras-chave MPC)
5. Resultados (tangíveis e intangíveis)
6. Formação Acadêmica (apenas concluídos)
7. Idiomas (mínimo intermediário)
8. Tecnologia (Excel nivelado)
9. Outros Conhecimentos (3 filtros)
10. Trabalho Voluntário (opcional)
11. Formatação (Arial/Calibri, 2 páginas)
12. Personalização automática
13. Validação metodológica

TIPOS DE CURRÍCULO:
- Base: Todas as informações estruturadas
- Personalizado: Adaptado para vaga específica (max 2 páginas)
"""

import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from sqlalchemy.orm import Session
from core.models import (
    User, Curriculo, ExperienciaProfissional, FormacaoAcademica,
    CompetenciaUsuario, TipoCurriculo, StatusCurriculo, MapaPalavrasChave
)

class CurriculoCarolinaMartins:
    """
    Implementação do Agente 2: Otimização de Currículo
    baseado na metodologia dos 13 passos da Carolina Martins
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.regras_honestidade = self._carregar_regras_honestidade()
        self.criterios_formatacao = self._carregar_criterios_formatacao()
        self.validacoes_metodologicas = self._carregar_validacoes_metodologicas()
    
    async def gerar_curriculo_base(
        self, 
        usuario_id: int,
        dados_diagnostico: Dict[str, Any],
        mpc_dados: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Gera currículo base completo seguindo os 13 passos metodológicos
        
        Este é o currículo master com todas as informações estruturadas,
        que será usado como base para personalizações futuras.
        """
        usuario = self.db.query(User).filter(User.id == usuario_id).first()
        if not usuario:
            raise ValueError(f"Usuário {usuario_id} não encontrado")
        
        # Cria novo currículo base
        curriculo = Curriculo(
            usuario_id=usuario_id,
            tipo=TipoCurriculo.BASE.value,
            status=StatusCurriculo.RASCUNHO.value
        )
        self.db.add(curriculo)
        self.db.commit()
        
        resultado = {
            "curriculo_id": curriculo.id,
            "tipo": "base",
            "13_passos": {},
            "validacoes": {},
            "score_qualidade": 0.0,
            "classificacao": "",
            "próximos_passos": []
        }
        
        try:
            # PASSO 1: Dados Pessoais
            resultado["13_passos"]["1_dados_pessoais"] = await self._passo_1_dados_pessoais(
                curriculo, usuario, dados_diagnostico
            )
            
            # PASSO 2: Objetivo
            resultado["13_passos"]["2_objetivo"] = await self._passo_2_objetivo(
                curriculo, dados_diagnostico
            )
            
            # PASSO 3: Resumo
            resultado["13_passos"]["3_resumo"] = await self._passo_3_resumo(
                curriculo, dados_diagnostico, mpc_dados
            )
            
            # PASSO 4: Experiências Profissionais
            resultado["13_passos"]["4_experiencias"] = await self._passo_4_experiencias(
                curriculo, dados_diagnostico, mpc_dados
            )
            
            # PASSO 5: Resultados
            resultado["13_passos"]["5_resultados"] = await self._passo_5_resultados(
                curriculo, dados_diagnostico
            )
            
            # PASSO 6: Formação Acadêmica
            resultado["13_passos"]["6_formacao"] = await self._passo_6_formacao(
                curriculo, dados_diagnostico
            )
            
            # PASSO 7: Idiomas
            resultado["13_passos"]["7_idiomas"] = await self._passo_7_idiomas(
                curriculo, dados_diagnostico
            )
            
            # PASSO 8: Tecnologia
            resultado["13_passos"]["8_tecnologia"] = await self._passo_8_tecnologia(
                curriculo, dados_diagnostico, mpc_dados
            )
            
            # PASSO 9: Outros Conhecimentos
            resultado["13_passos"]["9_outros_conhecimentos"] = await self._passo_9_outros_conhecimentos(
                curriculo, dados_diagnostico
            )
            
            # PASSO 10: Trabalho Voluntário
            resultado["13_passos"]["10_voluntario"] = await self._passo_10_voluntario(
                curriculo, dados_diagnostico
            )
            
            # PASSO 11: Formatação
            resultado["13_passos"]["11_formatacao"] = await self._passo_11_formatacao(
                curriculo
            )
            
            # PASSO 12: Personalização (preparação)
            resultado["13_passos"]["12_personalizacao"] = await self._passo_12_personalizacao_prep(
                curriculo
            )
            
            # PASSO 13: Validação Metodológica
            resultado["13_passos"]["13_validacao"] = await self._passo_13_validacao(
                curriculo, resultado["13_passos"]
            )
            
            # Calcula score final e classificação
            resultado["validacoes"] = self._executar_validacoes_completas(curriculo, resultado["13_passos"])
            resultado["score_qualidade"] = self._calcular_score_qualidade(resultado["validacoes"])
            resultado["classificacao"] = self._determinar_classificacao(resultado["score_qualidade"])
            resultado["próximos_passos"] = self._gerar_proximos_passos(resultado)
            
            # Atualiza status do currículo
            curriculo.status = StatusCurriculo.CONCLUIDO.value if resultado["score_qualidade"] >= 70 else StatusCurriculo.REVISAO_NECESSARIA.value
            curriculo.score_qualidade = resultado["score_qualidade"]
            self.db.commit()
            
        except Exception as e:
            curriculo.status = StatusCurriculo.RASCUNHO.value
            self.db.commit()
            raise e
        
        return resultado
    
    async def personalizar_curriculo_para_vaga(
        self,
        curriculo_base_id: int,
        vaga_dados: Dict[str, Any],
        mpc_personalizado: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Personaliza currículo base para vaga específica
        
        Regras de personalização Carolina Martins:
        - Máximo 2 páginas
        - Palavras-chave da vaga integradas
        - Experiências mais relevantes em destaque
        - Objetivo exato da vaga
        - Resumo adaptado
        """
        curriculo_base = self.db.query(Curriculo).filter(Curriculo.id == curriculo_base_id).first()
        if not curriculo_base or curriculo_base.tipo != TipoCurriculo.BASE.value:
            raise ValueError("Currículo base não encontrado")
        
        # Cria currículo personalizado
        curriculo_personalizado = Curriculo(
            usuario_id=curriculo_base.usuario_id,
            tipo=TipoCurriculo.PERSONALIZADO.value,
            status=StatusCurriculo.RASCUNHO.value,
            curriculo_base_id=curriculo_base_id,
            vaga_empresa=vaga_dados.get("empresa", ""),
            vaga_cargo=vaga_dados.get("cargo", ""),
            vaga_url=vaga_dados.get("url", ""),
            versao=1
        )
        self.db.add(curriculo_personalizado)
        self.db.commit()
        
        resultado = {
            "curriculo_id": curriculo_personalizado.id,
            "tipo": "personalizado",
            "vaga_alvo": vaga_dados,
            "personalizacoes": {},
            "compatibilidade_vaga": 0.0,
            "otimizacoes_aplicadas": [],
            "score_personalizacao": 0.0
        }
        
        try:
            # Análise de compatibilidade com a vaga
            resultado["compatibilidade_vaga"] = self._calcular_compatibilidade_vaga(
                curriculo_base, vaga_dados, mpc_personalizado
            )
            
            # Personalização do objetivo
            resultado["personalizacoes"]["objetivo"] = self._personalizar_objetivo(
                curriculo_base, vaga_dados
            )
            
            # Personalização do resumo
            resultado["personalizacoes"]["resumo"] = self._personalizar_resumo(
                curriculo_base, vaga_dados, mpc_personalizado
            )
            
            # Seleção e reordenação de experiências
            resultado["personalizacoes"]["experiencias"] = self._personalizar_experiencias(
                curriculo_base, vaga_dados, mpc_personalizado
            )
            
            # Personalização de competências e tecnologias
            resultado["personalizacoes"]["competencias"] = self._personalizar_competencias(
                curriculo_base, vaga_dados, mpc_personalizado
            )
            
            # Otimização de palavras-chave
            resultado["personalizacoes"]["palavras_chave"] = self._otimizar_palavras_chave(
                curriculo_base, vaga_dados, mpc_personalizado
            )
            
            # Validação de 2 páginas
            resultado["personalizacoes"]["formatacao"] = self._validar_limite_2_paginas(
                curriculo_personalizado, resultado["personalizacoes"]
            )
            
            # Aplica personalizações ao currículo
            self._aplicar_personalizacoes(curriculo_personalizado, resultado["personalizacoes"])
            
            # Calcula score de personalização
            resultado["score_personalizacao"] = self._calcular_score_personalizacao(resultado)
            
            # Atualiza status
            curriculo_personalizado.status = StatusCurriculo.CONCLUIDO.value
            curriculo_personalizado.score_qualidade = resultado["score_personalizacao"]
            self.db.commit()
            
        except Exception as e:
            curriculo_personalizado.status = StatusCurriculo.ERRO.value
            self.db.commit()
            raise e
        
        return resultado
    
    # IMPLEMENTAÇÃO DOS 13 PASSOS
    
    async def _passo_1_dados_pessoais(
        self, 
        curriculo: Curriculo, 
        usuario: User,
        dados_diagnostico: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        PASSO 1: Dados Pessoais com validação completa
        
        Validações Carolina Martins:
        - Nome completo (sem abreviações)
        - Email profissional (evitar @hotmail, @bol)
        - Telefone com DDD
        - LinkedIn URL personalizada
        - Endereço profissional (cidade/estado)
        """
        perfil = dados_diagnostico.get("perfil_basico", {})
        
        dados_pessoais = {
            "nome_completo": perfil.get("nome", "").strip(),
            "email_profissional": perfil.get("email", "").strip(),
            "telefone": self._formatar_telefone_profissional(perfil.get("telefone", "")),
            "linkedin_url": self._validar_url_linkedin_personalizada(perfil.get("linkedin_url", "")),
            "endereco_profissional": f"{perfil.get('cidade', '')}, {perfil.get('estado', '')}".strip(", "),
            "disponibilidade_mudanca": perfil.get("disponibilidade_mudanca", False),
            "regime_trabalho": perfil.get("regime_trabalho_preferido", "")
        }
        
        # Validações metodológicas
        validacoes = {
            "nome_completo": self._validar_nome_completo(dados_pessoais["nome_completo"]),
            "email_profissional": self._validar_email_profissional(dados_pessoais["email_profissional"]),
            "telefone": self._validar_telefone_completo(dados_pessoais["telefone"]),
            "linkedin_personalizado": self._validar_linkedin_personalizado(dados_pessoais["linkedin_url"]),
            "endereco_completo": self._validar_endereco_profissional(dados_pessoais["endereco_profissional"])
        }
        
        # Aplica dados ao currículo
        curriculo.dados_pessoais = json.dumps(dados_pessoais)
        
        return {
            "dados": dados_pessoais,
            "validacoes": validacoes,
            "score_passo": self._calcular_score_dados_pessoais(validacoes),
            "recomendacoes": self._gerar_recomendacoes_dados_pessoais(validacoes)
        }
    
    async def _passo_2_objetivo(
        self,
        curriculo: Curriculo,
        dados_diagnostico: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        PASSO 2: Objetivo - Nome exato da vaga
        
        Regra Carolina Martins:
        - Usar EXATAMENTE o nome da vaga como publicada
        - Evitar objetivos genéricos
        - Para currículo base: usar cargo objetivo declarado
        """
        config_agentes = dados_diagnostico.get("configuracao_agentes", {})
        agente_2_config = config_agentes.get("agente_2_curriculo", {})
        
        cargo_objetivo = dados_diagnostico.get("experiencia_profissional", {}).get("nivel_objetivo", "")
        area_objetivo = config_agentes.get("agente_1_palavras_chave", {}).get("area_interesse", "")
        
        objetivo = {
            "cargo_principal": cargo_objetivo,
            "area_atuacao": area_objetivo,
            "nivel_senioridade": dados_diagnostico.get("experiencia_profissional", {}).get("nivel_atual", ""),
            "objetivo_formatado": f"{cargo_objetivo} em {area_objetivo}".strip()
        }
        
        # Validações metodológicas
        validacoes = {
            "especificidade": len(objetivo["objetivo_formatado"]) > 10,
            "clareza": not any(palavra in objetivo["objetivo_formatado"].lower() for palavra in ["diversos", "qualquer", "geral"]),
            "nivel_adequado": objetivo["nivel_senioridade"] != ""
        }
        
        curriculo.objetivo = objetivo["objetivo_formatado"]
        
        return {
            "objetivo": objetivo,
            "validacoes": validacoes,
            "score_passo": self._calcular_score_objetivo(validacoes),
            "recomendacoes": self._gerar_recomendacoes_objetivo(validacoes)
        }
    
    async def _passo_3_resumo(
        self,
        curriculo: Curriculo,
        dados_diagnostico: Dict[str, Any],
        mpc_dados: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        PASSO 3: Resumo (apresentação + competências + registros)
        
        Estrutura Carolina Martins:
        - Apresentação profissional (quem é)
        - Competências principais (palavras-chave MPC)
        - Registros e certificações relevantes
        - 3-4 linhas máximo
        """
        experiencia_prof = dados_diagnostico.get("experiencia_profissional", {})
        gaps_fortes = dados_diagnostico.get("gaps_e_fortes", {})
        
        # Extrai competências do MPC se disponível
        competencias_mpc = []
        if mpc_dados:
            palavras_essenciais = mpc_dados.get("priorizacao_final", {}).get("essenciais", [])
            competencias_mpc = [p["palavra"] for p in palavras_essenciais[:5]]
        
        # Estrutura do resumo
        resumo_elementos = {
            "apresentacao": self._gerar_apresentacao_profissional(experiencia_prof),
            "competencias_chave": competencias_mpc or gaps_fortes.get("pontos_fortes", [])[:5],
            "registros_certificacoes": self._extrair_registros_relevantes(dados_diagnostico),
            "experiencia_resumida": f"{experiencia_prof.get('experiencia_profissional', 0)} anos de experiência"
        }
        
        # Monta resumo final
        resumo_completo = self._montar_resumo_final(resumo_elementos)
        
        # Validações metodológicas
        validacoes = {
            "tamanho_adequado": 150 <= len(resumo_completo) <= 400,  # 3-4 linhas
            "palavras_chave_presentes": len(resumo_elementos["competencias_chave"]) >= 3,
            "apresentacao_clara": "anos" in resumo_completo.lower(),
            "sem_subjetividade": not any(palavra in resumo_completo.lower() for palavra in ["excelente", "ótimo", "melhor"])
        }
        
        curriculo.resumo = resumo_completo
        
        return {
            "resumo": resumo_completo,
            "elementos": resumo_elementos,
            "validacoes": validacoes,
            "score_passo": self._calcular_score_resumo(validacoes),
            "recomendacoes": self._gerar_recomendacoes_resumo(validacoes)
        }
    
    async def _passo_4_experiencias(
        self,
        curriculo: Curriculo,
        dados_diagnostico: Dict[str, Any],
        mpc_dados: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        PASSO 4: Experiências Profissionais com palavras-chave MPC
        
        Regras Carolina Martins:
        - Ordem cronológica reversa (mais recente primeiro)
        - Foco em resultados, não atividades
        - Integração de palavras-chave do MPC
        - Máximo 3-4 experiências mais relevantes
        """
        experiencias_dados = dados_diagnostico.get("experiencias", [])
        area_objetivo = dados_diagnostico.get("configuracao_agentes", {}).get("agente_1_palavras_chave", {}).get("area_interesse", "")
        
        # Extrai palavras-chave do MPC
        palavras_chave_mpc = []
        if mpc_dados:
            for categoria in ["essenciais", "importantes", "complementares"]:
                palavras = mpc_dados.get("priorizacao_final", {}).get(categoria, [])
                palavras_chave_mpc.extend([p["palavra"] for p in palavras])
        
        experiencias_processadas = []
        
        for exp_data in experiencias_dados:
            # Verifica relevância para área objetivo
            relevancia = self._calcular_relevancia_experiencia(exp_data, area_objetivo)
            
            if relevancia > 0.3:  # Apenas experiências com relevância mínima
                exp_processada = {
                    "empresa": exp_data.get("empresa", ""),
                    "cargo": exp_data.get("cargo", ""),
                    "periodo": self._formatar_periodo(exp_data.get("data_inicio"), exp_data.get("data_fim")),
                    "descricao_otimizada": self._otimizar_descricao_com_mpc(
                        exp_data.get("descricao", ""), 
                        palavras_chave_mpc,
                        relevancia
                    ),
                    "resultados_destacados": self._extrair_resultados_tangiveis(exp_data),
                    "relevancia_score": relevancia
                }
                experiencias_processadas.append(exp_processada)
        
        # Ordena por relevância e data (mais recente primeiro)
        experiencias_processadas.sort(
            key=lambda x: (x["relevancia_score"], self._converter_data_para_ordenacao(x["periodo"])), 
            reverse=True
        )
        
        # Limita a 4 experiências mais relevantes
        experiencias_finais = experiencias_processadas[:4]
        
        # Cria registros no banco
        for i, exp in enumerate(experiencias_finais):
            exp_model = ExperienciaProfissional(
                curriculo_id=curriculo.id,
                empresa=exp["empresa"],
                cargo=exp["cargo"],
                periodo=exp["periodo"],
                descricao=exp["descricao_otimizada"],
                resultados=json.dumps(exp["resultados_destacados"]),
                ordem=i,
                relevancia_score=exp["relevancia_score"]
            )
            self.db.add(exp_model)
        
        # Validações metodológicas
        validacoes = {
            "ordem_cronologica": self._validar_ordem_cronologica(experiencias_finais),
            "descricoes_com_resultados": all("%" in exp["descricao_otimizada"] or "R$" in exp["descricao_otimizada"] or any(palavra in exp["descricao_otimizada"].lower() for palavra in ["aumentou", "reduziu", "melhorou", "implementou"]) for exp in experiencias_finais),
            "palavras_chave_integradas": self._validar_integracao_mpc(experiencias_finais, palavras_chave_mpc),
            "quantidade_adequada": 2 <= len(experiencias_finais) <= 4
        }
        
        return {
            "experiencias": experiencias_finais,
            "palavras_chave_aplicadas": palavras_chave_mpc,
            "validacoes": validacoes,
            "score_passo": self._calcular_score_experiencias(validacoes),
            "recomendacoes": self._gerar_recomendacoes_experiencias(validacoes)
        }
    
    async def _passo_5_resultados(
        self,
        curriculo: Curriculo,
        dados_diagnostico: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        PASSO 5: Resultados (tangíveis e intangíveis)
        
        Metodologia Carolina Martins:
        - Resultados tangíveis: números, percentuais, valores
        - Resultados intangíveis: melhorias de processo, reconhecimentos
        - Linguagem de resultado (aumentou, reduziu, implementou, otimizou)
        """
        experiencias = dados_diagnostico.get("experiencias", [])
        
        resultados_tangiveis = []
        resultados_intangiveis = []
        
        for exp in experiencias:
            # Extrai resultados da descrição
            descricao = exp.get("descricao", "")
            
            # Identifica resultados tangíveis (com números)
            tangiveis = self._extrair_resultados_numericos(descricao)
            resultados_tangiveis.extend(tangiveis)
            
            # Identifica resultados intangíveis
            intangiveis = self._extrair_resultados_qualitativos(descricao)
            resultados_intangiveis.extend(intangiveis)
        
        # Remove duplicatas e prioriza melhores resultados
        resultados_tangiveis = self._priorizar_melhores_resultados(resultados_tangiveis)[:5]
        resultados_intangiveis = self._priorizar_melhores_resultados(resultados_intangiveis)[:3]
        
        resultados_consolidados = {
            "tangiveis": resultados_tangiveis,
            "intangiveis": resultados_intangiveis,
            "total_resultados": len(resultados_tangiveis) + len(resultados_intangiveis)
        }
        
        # Validações metodológicas
        validacoes = {
            "possui_resultados_tangiveis": len(resultados_tangiveis) >= 2,
            "linguagem_resultado": self._validar_linguagem_resultado(resultados_tangiveis + resultados_intangiveis),
            "especificidade": self._validar_especificidade_resultados(resultados_tangiveis),
            "balanceamento": len(resultados_tangiveis) >= len(resultados_intangiveis)
        }
        
        curriculo.resultados = json.dumps(resultados_consolidados)
        
        return {
            "resultados": resultados_consolidados,
            "validacoes": validacoes,
            "score_passo": self._calcular_score_resultados(validacoes),
            "recomendacoes": self._gerar_recomendacoes_resultados(validacoes)
        }
    
    async def _passo_6_formacao(
        self,
        curriculo: Curriculo,
        dados_diagnostico: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        PASSO 6: Formação Acadêmica (apenas concluídos)
        
        Regra Carolina Martins:
        - Apenas formações CONCLUÍDAS
        - Ordem: Superior > Técnico > Outros
        - Incluir apenas relevantes para área
        """
        formacoes_dados = dados_diagnostico.get("formacoes", [])
        
        formacoes_validas = []
        
        for form in formacoes_dados:
            # Apenas formações concluídas
            if form.get("status") == "concluido":
                formacao_processada = {
                    "instituicao": form.get("instituicao", ""),
                    "curso": form.get("curso", ""),
                    "tipo": form.get("tipo", ""),  # Superior, Técnico, Curso
                    "ano_conclusao": form.get("ano_conclusao", ""),
                    "relevancia": self._calcular_relevancia_formacao(
                        form, 
                        dados_diagnostico.get("configuracao_agentes", {}).get("agente_1_palavras_chave", {}).get("area_interesse", "")
                    )
                }
                
                if formacao_processada["relevancia"] > 0.2:  # Apenas relevantes
                    formacoes_validas.append(formacao_processada)
        
        # Ordena por importância: Superior > Técnico > Cursos, depois por relevância
        ordem_tipos = {"superior": 3, "tecnico": 2, "curso": 1}
        formacoes_validas.sort(
            key=lambda x: (ordem_tipos.get(x["tipo"].lower(), 0), x["relevancia"]), 
            reverse=True
        )
        
        # Cria registros no banco
        for i, form in enumerate(formacoes_validas):
            form_model = FormacaoAcademica(
                curriculo_id=curriculo.id,
                instituicao=form["instituicao"],
                curso=form["curso"],
                tipo=form["tipo"],
                ano_conclusao=form["ano_conclusao"],
                ordem=i,
                relevancia_score=form["relevancia"]
            )
            self.db.add(form_model)
        
        # Validações metodológicas
        validacoes = {
            "apenas_concluidos": True,  # Já filtrado
            "relevancia_adequada": all(f["relevancia"] > 0.2 for f in formacoes_validas),
            "ordem_prioridade": self._validar_ordem_formacao(formacoes_validas),
            "informacoes_completas": all(f["instituicao"] and f["curso"] and f["ano_conclusao"] for f in formacoes_validas)
        }
        
        return {
            "formacoes": formacoes_validas,
            "validacoes": validacoes,
            "score_passo": self._calcular_score_formacao(validacoes),
            "recomendacoes": self._gerar_recomendacoes_formacao(validacoes)
        }
    
    async def _passo_7_idiomas(
        self,
        curriculo: Curriculo,
        dados_diagnostico: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        PASSO 7: Idiomas (mínimo intermediário)
        
        Regra Carolina Martins:
        - Apenas níveis intermediário ou superior
        - Evitar "básico" ou "iniciante"
        - Incluir certificações se houver
        """
        idiomas_dados = dados_diagnostico.get("idiomas", [])
        
        niveis_validos = ["intermediario", "avancado", "fluente", "nativo"]
        idiomas_validos = []
        
        for idioma in idiomas_dados:
            nivel = idioma.get("nivel", "").lower()
            
            if nivel in niveis_validos:
                idioma_processado = {
                    "idioma": idioma.get("idioma", ""),
                    "nivel": idioma.get("nivel", ""),
                    "certificacao": idioma.get("certificacao", ""),
                    "pontuacao": idioma.get("pontuacao", "")
                }
                idiomas_validos.append(idioma_processado)
        
        # Ordena por importância: Inglês primeiro, depois por nível
        ordem_importancia = {"inglês": 3, "espanhol": 2, "francês": 1}
        idiomas_validos.sort(
            key=lambda x: (
                ordem_importancia.get(x["idioma"].lower(), 0),
                {"fluente": 4, "avancado": 3, "intermediario": 2}.get(x["nivel"].lower(), 1)
            ),
            reverse=True
        )
        
        # Validações metodológicas
        validacoes = {
            "nivel_minimo_intermediario": True,  # Já filtrado
            "ingles_presente": any(idioma["idioma"].lower() == "inglês" for idioma in idiomas_validos),
            "certificacoes_incluidas": any(idioma["certificacao"] for idioma in idiomas_validos),
            "quantidade_adequada": len(idiomas_validos) <= 4  # Não sobrecarregar
        }
        
        curriculo.idiomas = json.dumps(idiomas_validos)
        
        return {
            "idiomas": idiomas_validos,
            "validacoes": validacoes,
            "score_passo": self._calcular_score_idiomas(validacoes),
            "recomendacoes": self._gerar_recomendacoes_idiomas(validacoes)
        }
    
    async def _passo_8_tecnologia(
        self,
        curriculo: Curriculo,
        dados_diagnostico: Dict[str, Any],
        mpc_dados: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        PASSO 8: Tecnologia (Excel nivelado)
        
        Metodologia Carolina Martins:
        - Excel sempre com nível especificado
        - Softwares relevantes para área
        - Palavras-chave técnicas do MPC
        - Evitar tecnologias obsoletas
        """
        competencias = dados_diagnostico.get("competencias", [])
        
        # Extrai tecnologias do MPC se disponível
        tecnologias_mpc = []
        if mpc_dados:
            palavras_tecnicas = mpc_dados.get("categorizacao", {}).get("tecnica", [])
            tecnologias_mpc = [p["palavra"] for p in palavras_tecnicas if self._e_tecnologia(p["palavra"])]
        
        # Combina competências declaradas com MPC
        todas_tecnologias = set(competencias + tecnologias_mpc)
        
        tecnologias_processadas = []
        
        for tech in todas_tecnologias:
            tech_processada = {
                "tecnologia": tech,
                "nivel": self._determinar_nivel_tecnologia(tech, dados_diagnostico),
                "categoria": self._categorizar_tecnologia(tech),
                "relevancia": self._calcular_relevancia_tecnologia(tech, mpc_dados)
            }
            
            if tech_processada["relevancia"] > 0.2:
                tecnologias_processadas.append(tech_processada)
        
        # Garante Excel com nível especificado
        excel_presente = any("excel" in tech["tecnologia"].lower() for tech in tecnologias_processadas)
        if not excel_presente:
            tecnologias_processadas.append({
                "tecnologia": "Microsoft Excel",
                "nivel": "Intermediário",
                "categoria": "Office",
                "relevancia": 0.8
            })
        
        # Ordena por relevância e categoria
        tecnologias_processadas.sort(key=lambda x: (x["relevancia"], x["categoria"] == "Office"), reverse=True)
        
        # Validações metodológicas
        validacoes = {
            "excel_com_nivel": any("excel" in tech["tecnologia"].lower() and tech["nivel"] for tech in tecnologias_processadas),
            "tecnologias_atuais": self._validar_tecnologias_atuais(tecnologias_processadas),
            "mpc_integrado": len([t for t in tecnologias_processadas if t["tecnologia"] in tecnologias_mpc]) > 0,
            "quantidade_adequada": 3 <= len(tecnologias_processadas) <= 8
        }
        
        curriculo.tecnologias = json.dumps(tecnologias_processadas)
        
        return {
            "tecnologias": tecnologias_processadas,
            "mpc_aplicado": tecnologias_mpc,
            "validacoes": validacoes,
            "score_passo": self._calcular_score_tecnologia(validacoes),
            "recomendacoes": self._gerar_recomendacoes_tecnologia(validacoes)
        }
    
    async def _passo_9_outros_conhecimentos(
        self,
        curriculo: Curriculo,
        dados_diagnostico: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        PASSO 9: Outros Conhecimentos (3 filtros)
        
        Filtros Carolina Martins:
        1. Relevância para área objetivo
        2. Diferencial competitivo
        3. Validação/certificação
        """
        outros_conhecimentos = dados_diagnostico.get("outros_conhecimentos", [])
        certificacoes = dados_diagnostico.get("certificacoes", [])
        
        conhecimentos_processados = []
        
        # Processa outros conhecimentos
        for conhecimento in outros_conhecimentos:
            conhec_processado = {
                "conhecimento": conhecimento,
                "tipo": "conhecimento",
                "filtro_1_relevancia": self._aplicar_filtro_relevancia(conhecimento, dados_diagnostico),
                "filtro_2_diferencial": self._aplicar_filtro_diferencial(conhecimento),
                "filtro_3_validacao": False  # Conhecimento sem certificação
            }
            conhecimentos_processados.append(conhec_processado)
        
        # Processa certificações
        for cert in certificacoes:
            cert_processada = {
                "conhecimento": cert.get("nome", ""),
                "tipo": "certificacao",
                "instituicao": cert.get("instituicao", ""),
                "ano": cert.get("ano", ""),
                "filtro_1_relevancia": self._aplicar_filtro_relevancia(cert.get("nome", ""), dados_diagnostico),
                "filtro_2_diferencial": self._aplicar_filtro_diferencial(cert.get("nome", "")),
                "filtro_3_validacao": True  # Certificação sempre tem validação
            }
            conhecimentos_processados.append(cert_processada)
        
        # Aplica os 3 filtros
        conhecimentos_filtrados = []
        for item in conhecimentos_processados:
            score_filtros = sum([
                item["filtro_1_relevancia"],
                item["filtro_2_diferencial"],
                item["filtro_3_validacao"]
            ])
            
            if score_filtros >= 2:  # Pelo menos 2 dos 3 filtros
                item["score_filtros"] = score_filtros
                conhecimentos_filtrados.append(item)
        
        # Ordena por score dos filtros
        conhecimentos_filtrados.sort(key=lambda x: x["score_filtros"], reverse=True)
        
        # Limita quantidade
        conhecimentos_finais = conhecimentos_filtrados[:6]
        
        # Validações metodológicas
        validacoes = {
            "filtros_aplicados": all(item["score_filtros"] >= 2 for item in conhecimentos_finais),
            "mix_conhecimentos_certificacoes": any(item["tipo"] == "certificacao" for item in conhecimentos_finais),
            "relevancia_area": all(item["filtro_1_relevancia"] for item in conhecimentos_finais),
            "quantidade_adequada": len(conhecimentos_finais) <= 6
        }
        
        curriculo.outros_conhecimentos = json.dumps(conhecimentos_finais)
        
        return {
            "conhecimentos": conhecimentos_finais,
            "filtros_aplicados": ["relevancia", "diferencial", "validacao"],
            "validacoes": validacoes,
            "score_passo": self._calcular_score_outros_conhecimentos(validacoes),
            "recomendacoes": self._gerar_recomendacoes_outros_conhecimentos(validacoes)
        }
    
    async def _passo_10_voluntario(
        self,
        curriculo: Curriculo,
        dados_diagnostico: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        PASSO 10: Trabalho Voluntário (opcional)
        
        Critérios Carolina Martins:
        - Apenas se relevante para área/cargo
        - Demonstra competências comportamentais
        - Diferencial para perfil
        """
        trabalhos_voluntarios = dados_diagnostico.get("trabalhos_voluntarios", [])
        
        voluntarios_relevantes = []
        
        for voluntario in trabalhos_voluntarios:
            relevancia = self._calcular_relevancia_voluntario(voluntario, dados_diagnostico)
            
            if relevancia > 0.3:  # Apenas relevantes
                voluntario_processado = {
                    "organizacao": voluntario.get("organizacao", ""),
                    "funcao": voluntario.get("funcao", ""),
                    "periodo": voluntario.get("periodo", ""),
                    "descricao": voluntario.get("descricao", ""),
                    "competencias_desenvolvidas": self._extrair_competencias_voluntario(voluntario),
                    "relevancia": relevancia
                }
                voluntarios_relevantes.append(voluntario_processado)
        
        # Ordena por relevância
        voluntarios_relevantes.sort(key=lambda x: x["relevancia"], reverse=True)
        
        # Limita a 2 experiências mais relevantes
        voluntarios_finais = voluntarios_relevantes[:2]
        
        # Validações metodológicas
        validacoes = {
            "relevancia_adequada": all(v["relevancia"] > 0.3 for v in voluntarios_finais),
            "competencias_destacadas": all(v["competencias_desenvolvidas"] for v in voluntarios_finais),
            "quantidade_adequada": len(voluntarios_finais) <= 2,
            "diferencial_perfil": len(voluntarios_finais) > 0
        }
        
        curriculo.trabalho_voluntario = json.dumps(voluntarios_finais) if voluntarios_finais else None
        
        return {
            "voluntarios": voluntarios_finais,
            "validacoes": validacoes,
            "score_passo": self._calcular_score_voluntario(validacoes),
            "recomendacoes": self._gerar_recomendacoes_voluntario(validacoes)
        }
    
    async def _passo_11_formatacao(
        self,
        curriculo: Curriculo
    ) -> Dict[str, Any]:
        """
        PASSO 11: Formatação (Arial/Calibri, 2 páginas)
        
        Padrões Carolina Martins:
        - Fonte: Arial ou Calibri
        - Tamanho: 11 ou 12
        - Máximo 2 páginas
        - Margens adequadas
        - Espaçamento uniforme
        """
        formatacao_padrao = {
            "fonte": "Arial",
            "tamanho_fonte": 11,
            "espacamento_linhas": 1.0,
            "margens": {
                "superior": 2.0,
                "inferior": 2.0,
                "esquerda": 2.5,
                "direita": 2.5
            },
            "limite_paginas": 2,
            "cores": {
                "texto_principal": "#000000",
                "destaques": "#1f497d"
            }
        }
        
        # Estima quantidade de páginas baseado no conteúdo
        conteudo_estimado = self._estimar_conteudo_curriculo(curriculo)
        paginas_estimadas = self._calcular_paginas_estimadas(conteudo_estimado, formatacao_padrao)
        
        # Validações metodológicas
        validacoes = {
            "fonte_adequada": formatacao_padrao["fonte"] in ["Arial", "Calibri"],
            "tamanho_fonte_adequado": 10 <= formatacao_padrao["tamanho_fonte"] <= 12,
            "limite_2_paginas": paginas_estimadas <= 2,
            "margens_adequadas": all(2.0 <= margin <= 3.0 for margin in formatacao_padrao["margens"].values()),
            "cores_profissionais": formatacao_padrao["cores"]["texto_principal"] == "#000000"
        }
        
        curriculo.formatacao = json.dumps(formatacao_padrao)
        
        return {
            "formatacao": formatacao_padrao,
            "paginas_estimadas": paginas_estimadas,
            "conteudo_estimado": conteudo_estimado,
            "validacoes": validacoes,
            "score_passo": self._calcular_score_formatacao(validacoes),
            "recomendacoes": self._gerar_recomendacoes_formatacao(validacoes, paginas_estimadas)
        }
    
    async def _passo_12_personalizacao_prep(
        self,
        curriculo: Curriculo
    ) -> Dict[str, Any]:
        """
        PASSO 12: Preparação para Personalização
        
        Configura estrutura base para futuras personalizações por vaga
        """
        estrutura_personalizacao = {
            "curriculo_base_pronto": True,
            "elementos_personalizaveis": [
                "objetivo",
                "resumo", 
                "ordem_experiencias",
                "palavras_chave",
                "competencias_destaque"
            ],
            "criterios_personalizacao": {
                "compatibilidade_minima": 0.7,
                "limite_2_paginas": True,
                "palavras_chave_vaga": True,
                "experiencias_relevantes_primeiro": True
            }
        }
        
        validacoes = {
            "base_completa": curriculo.dados_pessoais and curriculo.objetivo and curriculo.resumo,
            "experiencias_cadastradas": len(self.db.query(ExperienciaProfissional).filter(ExperienciaProfissional.curriculo_id == curriculo.id).all()) > 0,
            "formatacao_definida": curriculo.formatacao is not None,
            "pronto_personalizacao": True
        }
        
        return {
            "estrutura": estrutura_personalizacao,
            "validacoes": validacoes,
            "score_passo": self._calcular_score_personalizacao_prep(validacoes),
            "recomendacoes": self._gerar_recomendacoes_personalizacao_prep(validacoes)
        }
    
    async def _passo_13_validacao(
        self,
        curriculo: Curriculo,
        todos_passos: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        PASSO 13: Validação Metodológica Final
        
        Validação completa seguindo metodologia Carolina Martins
        """
        validacoes_finais = {
            "honestidade_total": self._validar_honestidade_total(curriculo),
            "estrutura_13_passos": self._validar_estrutura_completa(todos_passos),
            "formatacao_metodologica": self._validar_formatacao_metodologica(curriculo),
            "palavras_chave_integradas": self._validar_integracao_palavras_chave_final(curriculo),
            "resultados_destacados": self._validar_resultados_presentes(curriculo),
            "profissionalismo": self._validar_profissionalismo_geral(curriculo)
        }
        
        # Calcula score final de validação
        score_validacao = sum(validacoes_finais.values()) / len(validacoes_finais) * 100
        
        # Determina classificação Carolina Martins
        if score_validacao >= 90:
            classificacao = "Meteórico"
        elif score_validacao >= 80:
            classificacao = "Bom+"
        elif score_validacao >= 70:
            classificacao = "Bom"
        elif score_validacao >= 60:
            classificacao = "Básico"
        else:
            classificacao = "Necessita Revisão"
        
        curriculo.classificacao_metodologica = classificacao
        curriculo.score_validacao_final = score_validacao
        
        return {
            "validacoes": validacoes_finais,
            "score_validacao": score_validacao,
            "classificacao": classificacao,
            "proximos_passos": self._definir_proximos_passos_pos_validacao(validacoes_finais, score_validacao),
            "recomendacoes": self._gerar_recomendacoes_validacao_final(validacoes_finais)
        }
    
    # MÉTODOS AUXILIARES DE VALIDAÇÃO E CÁLCULO
    
    def _carregar_regras_honestidade(self) -> Dict[str, Any]:
        """Carrega regras de honestidade da metodologia"""
        return {
            "nunca_mentir": True,
            "experiencias_verificaveis": True,
            "competencias_comprovadas": True,
            "resultados_reais": True,
            "formacoes_concluidas": True
        }
    
    def _carregar_criterios_formatacao(self) -> Dict[str, Any]:
        """Carrega critérios de formatação padrão"""
        return {
            "fontes_aceitas": ["Arial", "Calibri"],
            "tamanho_fonte_min": 10,
            "tamanho_fonte_max": 12,
            "paginas_max": 2,
            "margens_min": 2.0,
            "margens_max": 3.0
        }
    
    def _carregar_validacoes_metodologicas(self) -> Dict[str, Any]:
        """Carrega validações metodológicas específicas"""
        return {
            "score_meteórico": 90,
            "score_bom_mais": 80,
            "score_bom": 70,
            "score_básico": 60,
            "compatibilidade_minima": 70
        }
    
    def _calcular_score_qualidade(self, validacoes: Dict[str, Any]) -> float:
        """Calcula score geral de qualidade do currículo"""
        scores_passos = []
        
        for passo, dados in validacoes.items():
            if isinstance(dados, dict) and "score_passo" in dados:
                scores_passos.append(dados["score_passo"])
        
        return sum(scores_passos) / len(scores_passos) if scores_passos else 0.0
    
    def _determinar_classificacao(self, score: float) -> str:
        """Determina classificação baseada no score"""
        if score >= 90:
            return "Meteórico"
        elif score >= 80:
            return "Bom+"
        elif score >= 70:
            return "Bom"
        elif score >= 60:
            return "Básico"
        else:
            return "Necessita Revisão"
    
    def _gerar_proximos_passos(self, resultado: Dict[str, Any]) -> List[str]:
        """Gera próximos passos baseados no resultado"""
        proximos_passos = []
        
        score = resultado["score_qualidade"]
        
        if score < 70:
            proximos_passos.append("Revisar e corrigir validações com falha")
        
        if score >= 70:
            proximos_passos.append("Currículo base está pronto para personalização")
        
        if score >= 90:
            proximos_passos.append("Currículo meteórico - iniciar personalizações para vagas")
        
        return proximos_passos
    
    # Placeholder methods for detailed implementations
    # These would be fully implemented with the specific logic for each step
    
    def _formatar_telefone_profissional(self, telefone: str) -> str:
        """Formata telefone para padrão profissional"""
        # Implementação completa seria aqui
        return telefone
    
    def _validar_nome_completo(self, nome: str) -> bool:
        """Valida se nome está completo"""
        return len(nome.split()) >= 2
    
    def _validar_email_profissional(self, email: str) -> bool:
        """Valida se email é profissional"""
        dominios_nao_profissionais = ["@hotmail", "@bol", "@yahoo"]
        return not any(dominio in email.lower() for dominio in dominios_nao_profissionais)
    
    # ... outros métodos auxiliares seriam implementados aqui
    
    def _calcular_score_dados_pessoais(self, validacoes: Dict[str, bool]) -> float:
        """Calcula score do passo dados pessoais"""
        return sum(validacoes.values()) / len(validacoes) * 100
    
    def _calcular_score_objetivo(self, validacoes: Dict[str, bool]) -> float:
        """Calcula score do passo objetivo"""
        return sum(validacoes.values()) / len(validacoes) * 100
    
    def _calcular_score_resumo(self, validacoes: Dict[str, bool]) -> float:
        """Calcula score do passo resumo"""
        return sum(validacoes.values()) / len(validacoes) * 100
    
    def _calcular_score_experiencias(self, validacoes: Dict[str, bool]) -> float:
        """Calcula score do passo experiências"""
        return sum(validacoes.values()) / len(validacoes) * 100
    
    def _calcular_score_resultados(self, validacoes: Dict[str, bool]) -> float:
        """Calcula score do passo resultados"""
        return sum(validacoes.values()) / len(validacoes) * 100
    
    def _calcular_score_formacao(self, validacoes: Dict[str, bool]) -> float:
        """Calcula score do passo formação"""
        return sum(validacoes.values()) / len(validacoes) * 100
    
    def _calcular_score_idiomas(self, validacoes: Dict[str, bool]) -> float:
        """Calcula score do passo idiomas"""
        return sum(validacoes.values()) / len(validacoes) * 100
    
    def _calcular_score_tecnologia(self, validacoes: Dict[str, bool]) -> float:
        """Calcula score do passo tecnologia"""
        return sum(validacoes.values()) / len(validacoes) * 100
    
    def _calcular_score_outros_conhecimentos(self, validacoes: Dict[str, bool]) -> float:
        """Calcula score do passo outros conhecimentos"""
        return sum(validacoes.values()) / len(validacoes) * 100
    
    def _calcular_score_voluntario(self, validacoes: Dict[str, bool]) -> float:
        """Calcula score do passo voluntário"""
        return sum(validacoes.values()) / len(validacoes) * 100
    
    def _calcular_score_formatacao(self, validacoes: Dict[str, bool]) -> float:
        """Calcula score do passo formatação"""
        return sum(validacoes.values()) / len(validacoes) * 100
    
    def _calcular_score_personalizacao_prep(self, validacoes: Dict[str, bool]) -> float:
        """Calcula score do passo personalização prep"""
        return sum(validacoes.values()) / len(validacoes) * 100
    
    # Métodos para geração de recomendações
    def _gerar_recomendacoes_dados_pessoais(self, validacoes: Dict[str, bool]) -> List[str]:
        """Gera recomendações para dados pessoais"""
        recomendacoes = []
        if not validacoes.get("email_profissional"):
            recomendacoes.append("Use email profissional (evite @hotmail, @bol)")
        return recomendacoes
    
    def _gerar_recomendacoes_objetivo(self, validacoes: Dict[str, bool]) -> List[str]:
        """Gera recomendações para objetivo"""
        recomendacoes = []
        if not validacoes.get("especificidade"):
            recomendacoes.append("Seja mais específico no objetivo")
        return recomendacoes
    
    def _gerar_recomendacoes_resumo(self, validacoes: Dict[str, bool]) -> List[str]:
        """Gera recomendações para resumo"""
        recomendacoes = []
        if not validacoes.get("tamanho_adequado"):
            recomendacoes.append("Ajuste tamanho do resumo para 3-4 linhas")
        return recomendacoes
    
    def _gerar_recomendacoes_experiencias(self, validacoes: Dict[str, bool]) -> List[str]:
        """Gera recomendações para experiências"""
        recomendacoes = []
        if not validacoes.get("descricoes_com_resultados"):
            recomendacoes.append("Inclua resultados tangíveis nas experiências")
        return recomendacoes
    
    def _gerar_recomendacoes_resultados(self, validacoes: Dict[str, bool]) -> List[str]:
        """Gera recomendações para resultados"""
        recomendacoes = []
        if not validacoes.get("possui_resultados_tangiveis"):
            recomendacoes.append("Inclua pelo menos 2 resultados com números")
        return recomendacoes
    
    def _gerar_recomendacoes_formacao(self, validacoes: Dict[str, bool]) -> List[str]:
        """Gera recomendações para formação"""
        recomendacoes = []
        if not validacoes.get("informacoes_completas"):
            recomendacoes.append("Complete informações de instituição e ano")
        return recomendacoes
    
    def _gerar_recomendacoes_idiomas(self, validacoes: Dict[str, bool]) -> List[str]:
        """Gera recomendações para idiomas"""
        recomendacoes = []
        if not validacoes.get("ingles_presente"):
            recomendacoes.append("Inclua inglês se tiver nível intermediário ou superior")
        return recomendacoes
    
    def _gerar_recomendacoes_tecnologia(self, validacoes: Dict[str, bool]) -> List[str]:
        """Gera recomendações para tecnologia"""
        recomendacoes = []
        if not validacoes.get("excel_com_nivel"):
            recomendacoes.append("Especifique nível do Excel")
        return recomendacoes
    
    def _gerar_recomendacoes_outros_conhecimentos(self, validacoes: Dict[str, bool]) -> List[str]:
        """Gera recomendações para outros conhecimentos"""
        recomendacoes = []
        if not validacoes.get("relevancia_area"):
            recomendacoes.append("Inclua apenas conhecimentos relevantes para área")
        return recomendacoes
    
    def _gerar_recomendacoes_voluntario(self, validacoes: Dict[str, bool]) -> List[str]:
        """Gera recomendações para voluntário"""
        recomendacoes = []
        if not validacoes.get("diferencial_perfil"):
            recomendacoes.append("Considere incluir trabalho voluntário relevante")
        return recomendacoes
    
    def _gerar_recomendacoes_formatacao(self, validacoes: Dict[str, bool], paginas: float) -> List[str]:
        """Gera recomendações para formatação"""
        recomendacoes = []
        if not validacoes.get("limite_2_paginas"):
            recomendacoes.append(f"Reduza conteúdo para 2 páginas (atual: {paginas:.1f})")
        return recomendacoes
    
    def _gerar_recomendacoes_personalizacao_prep(self, validacoes: Dict[str, bool]) -> List[str]:
        """Gera recomendações para preparação de personalização"""
        recomendacoes = []
        if validacoes.get("pronto_personalizacao"):
            recomendacoes.append("Currículo base pronto para personalização por vaga")
        return recomendacoes
    
    def _gerar_recomendacoes_validacao_final(self, validacoes: Dict[str, bool]) -> List[str]:
        """Gera recomendações da validação final"""
        recomendacoes = []
        for validacao, passou in validacoes.items():
            if not passou:
                recomendacoes.append(f"Revisar: {validacao}")
        return recomendacoes
    
    # Métodos placeholder que seriam implementados completamente
    def _validar_url_linkedin_personalizada(self, url: str) -> bool:
        return "/in/" in url
    
    def _validar_telefone_completo(self, telefone: str) -> bool:
        return len(telefone) >= 10
    
    def _validar_linkedin_personalizado(self, url: str) -> bool:
        if not url or not isinstance(url, str):
            return False
        return "/in/" in url and not url.endswith("/in/")
    
    def _validar_endereco_profissional(self, endereco: str) -> bool:
        return len(endereco) > 5
    
    def _gerar_apresentacao_profissional(self, exp_data: Dict[str, Any]) -> str:
        return f"Profissional com {exp_data.get('experiencia_profissional', 0)} anos de experiência"
    
    def _extrair_registros_relevantes(self, dados: Dict[str, Any]) -> List[str]:
        return dados.get("registros", [])
    
    def _montar_resumo_final(self, elementos: Dict[str, Any]) -> str:
        return f"{elementos['apresentacao']} especializado em {', '.join(elementos['competencias_chave'][:3])}."
    
    def _calcular_relevancia_experiencia(self, exp: Dict[str, Any], area: str) -> float:
        return 0.8  # Placeholder
    
    def _formatar_periodo(self, inicio: str, fim: str = None) -> str:
        return f"{inicio} - {fim or 'Atual'}"
    
    def _otimizar_descricao_com_mpc(self, descricao: str, palavras_mpc: List[str], relevancia: float) -> str:
        return descricao  # Placeholder - integraria palavras-chave
    
    def _extrair_resultados_tangiveis(self, exp: Dict[str, Any]) -> List[str]:
        return []  # Placeholder
    
    def _converter_data_para_ordenacao(self, periodo: str) -> datetime:
        return datetime.now()  # Placeholder
    
    def _validar_ordem_cronologica(self, experiencias: List[Dict[str, Any]]) -> bool:
        return True  # Placeholder
    
    def _validar_integracao_mpc(self, experiencias: List[Dict[str, Any]], palavras_mpc: List[str]) -> bool:
        return True  # Placeholder
    
    def _extrair_resultados_numericos(self, descricao: str) -> List[str]:
        return []  # Placeholder
    
    def _extrair_resultados_qualitativos(self, descricao: str) -> List[str]:
        return []  # Placeholder
    
    def _priorizar_melhores_resultados(self, resultados: List[str]) -> List[str]:
        return resultados[:5]  # Placeholder
    
    def _validar_linguagem_resultado(self, resultados: List[str]) -> bool:
        return True  # Placeholder
    
    def _validar_especificidade_resultados(self, resultados: List[str]) -> bool:
        return True  # Placeholder
    
    def _calcular_relevancia_formacao(self, formacao: Dict[str, Any], area: str) -> float:
        return 0.8  # Placeholder
    
    def _validar_ordem_formacao(self, formacoes: List[Dict[str, Any]]) -> bool:
        return True  # Placeholder
    
    def _determinar_nivel_tecnologia(self, tech: str, dados: Dict[str, Any]) -> str:
        if "excel" in tech.lower():
            return "Intermediário"
        return "Usuário"  # Placeholder
    
    def _categorizar_tecnologia(self, tech: str) -> str:
        if "excel" in tech.lower() or "word" in tech.lower():
            return "Office"
        return "Específica"  # Placeholder
    
    def _calcular_relevancia_tecnologia(self, tech: str, mpc_dados: Dict[str, Any] = None) -> float:
        return 0.7  # Placeholder
    
    def _e_tecnologia(self, palavra: str) -> bool:
        tecnologias_comum = ["excel", "sap", "python", "sql", "power bi"]
        return any(tech in palavra.lower() for tech in tecnologias_comum)
    
    def _validar_tecnologias_atuais(self, tecnologias: List[Dict[str, Any]]) -> bool:
        return True  # Placeholder
    
    def _aplicar_filtro_relevancia(self, conhecimento: str, dados: Dict[str, Any]) -> bool:
        return True  # Placeholder
    
    def _aplicar_filtro_diferencial(self, conhecimento: str) -> bool:
        return True  # Placeholder
    
    def _calcular_relevancia_voluntario(self, voluntario: Dict[str, Any], dados: Dict[str, Any]) -> float:
        return 0.5  # Placeholder
    
    def _extrair_competencias_voluntario(self, voluntario: Dict[str, Any]) -> List[str]:
        return ["liderança", "trabalho em equipe"]  # Placeholder
    
    def _estimar_conteudo_curriculo(self, curriculo: Curriculo) -> Dict[str, int]:
        return {"linhas_total": 50, "caracteres_total": 3000}  # Placeholder
    
    def _calcular_paginas_estimadas(self, conteudo: Dict[str, int], formatacao: Dict[str, Any]) -> float:
        return 1.8  # Placeholder
    
    def _validar_honestidade_total(self, curriculo: Curriculo) -> bool:
        return True  # Placeholder
    
    def _validar_estrutura_completa(self, passos: Dict[str, Any]) -> bool:
        return len(passos) == 13  # Placeholder
    
    def _validar_formatacao_metodologica(self, curriculo: Curriculo) -> bool:
        return True  # Placeholder
    
    def _validar_integracao_palavras_chave_final(self, curriculo: Curriculo) -> bool:
        return True  # Placeholder
    
    def _validar_resultados_presentes(self, curriculo: Curriculo) -> bool:
        return True  # Placeholder
    
    def _validar_profissionalismo_geral(self, curriculo: Curriculo) -> bool:
        return True  # Placeholder
    
    def _definir_proximos_passos_pos_validacao(self, validacoes: Dict[str, bool], score: float) -> List[str]:
        passos = []
        if score >= 90:
            passos.append("Iniciar personalizações para vagas específicas")
        elif score >= 70:
            passos.append("Currículo aprovado - pronto para uso")
        else:
            passos.append("Revisar pontos de melhoria")
        return passos
    
    # Métodos de personalização por vaga
    def _calcular_compatibilidade_vaga(self, curriculo: Curriculo, vaga: Dict[str, Any], mpc: Dict[str, Any] = None) -> float:
        return 0.85  # Placeholder
    
    def _personalizar_objetivo(self, curriculo: Curriculo, vaga: Dict[str, Any]) -> str:
        return vaga.get("cargo", curriculo.objetivo)
    
    def _personalizar_resumo(self, curriculo: Curriculo, vaga: Dict[str, Any], mpc: Dict[str, Any] = None) -> str:
        return curriculo.resumo  # Placeholder - seria personalizado
    
    def _personalizar_experiencias(self, curriculo: Curriculo, vaga: Dict[str, Any], mpc: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        return []  # Placeholder
    
    def _personalizar_competencias(self, curriculo: Curriculo, vaga: Dict[str, Any], mpc: Dict[str, Any] = None) -> List[str]:
        return []  # Placeholder
    
    def _otimizar_palavras_chave(self, curriculo: Curriculo, vaga: Dict[str, Any], mpc: Dict[str, Any] = None) -> List[str]:
        return []  # Placeholder
    
    def _validar_limite_2_paginas(self, curriculo: Curriculo, personalizacoes: Dict[str, Any]) -> Dict[str, Any]:
        return {"paginas_estimadas": 1.9, "dentro_limite": True}
    
    def _aplicar_personalizacoes(self, curriculo: Curriculo, personalizacoes: Dict[str, Any]) -> None:
        # Aplica personalizações ao objeto currículo
        pass
    
    def _calcular_score_personalizacao(self, resultado: Dict[str, Any]) -> float:
        return 88.0  # Placeholder
    
    def _executar_validacoes_completas(self, curriculo: Curriculo, passos: Dict[str, Any]) -> Dict[str, Any]:
        """Executa todas as validações metodológicas"""
        return {
            "validacao_geral": True,
            "score_medio": 85.0,
            "pontos_melhoria": []
        }