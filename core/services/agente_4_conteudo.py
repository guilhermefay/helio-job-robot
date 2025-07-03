"""
Agente 4: Geração de Conteúdo - Metodologia Carolina Martins

Este agente implementa a geração automática de conteúdo estratégico para LinkedIn
baseada na metodologia completa da Carolina Martins:

ESTRATÉGIA EDITORIAL 60/40:
- 60% Conteúdo Geral (Audiência): engajamento, carreira, motivação
- 40% Conteúdo Específico (Autoridade): expertise, cases, metodologias

TIPOS DE CONTEÚDO:
- Posts de experiência profissional
- Posts de insight técnico
- Posts motivacionais
- Posts de dicas de carreira
- Posts de casos de sucesso
- Posts de reflexão

CRONOGRAMA ESTRATÉGICO:
- Frequência baseada na senioridade
- Distribuição balanceada ao longo da semana
- Integração de palavras-chave do MPC
- Call-to-actions estratégicos
"""

import json
import re
from datetime import datetime, timedelta, time
from typing import Dict, List, Optional, Any, Tuple
from sqlalchemy.orm import Session
from core.models import (
    User, PerfilLinkedIn, ConteudoLinkedIn, EstrategiaConteudo,
    TipoConteudo, MapaPalavrasChave
)

class ConteudoCarolinaMartins:
    """
    Implementação do Agente 4: Geração de Conteúdo
    baseado na metodologia de autoridade e audiência da Carolina Martins
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.templates_conteudo = self._carregar_templates_completos()
        self.estrategia_60_40 = {"geral": 0.6, "autoridade": 0.4}
        self.horarios_otimos = self._carregar_horarios_otimos()
        self.call_to_actions = self._carregar_call_to_actions()
    
    async def gerar_plano_editorial_completo(
        self,
        perfil_linkedin_id: int,
        periodo_dias: int = 30,
        dados_diagnostico: Dict[str, Any] = None,
        mpc_dados: Dict[str, Any] = None,
        curriculo_dados: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Gera plano editorial completo seguindo metodologia Carolina Martins
        
        Integra todos os dados dos agentes anteriores para criar calendário
        estratégico personalizado que constrói audiência e autoridade.
        """
        perfil = self.db.query(PerfilLinkedIn).filter(PerfilLinkedIn.id == perfil_linkedin_id).first()
        if not perfil:
            raise ValueError("Perfil LinkedIn não encontrado")
        
        # Busca estratégia de conteúdo definida no Agente 3
        estrategia = self.db.query(EstrategiaConteudo).filter(
            EstrategiaConteudo.perfil_linkedin_id == perfil_linkedin_id
        ).first()
        
        if not estrategia:
            raise ValueError("Estratégia de conteúdo não configurada. Execute Agente 3 primeiro.")
        
        resultado = {
            "plano_editorial": {},
            "calendario_detalhado": [],
            "temas_identificados": {},
            "personas_audiencia": {},
            "estrategia_hashtags": {},
            "kpis_conteudo": {},
            "templates_personalizados": {},
            "cronograma_publicacao": {}
        }
        
        try:
            # Análise de perfil e contexto
            resultado["personas_audiencia"] = await self._identificar_personas_audiencia(
                dados_diagnostico, mpc_dados
            )
            
            # Estratégia de temas baseada no MPC
            resultado["temas_identificados"] = await self._mapear_temas_estrategicos(
                mpc_dados, curriculo_dados, estrategia
            )
            
            # Geração de templates personalizados
            resultado["templates_personalizados"] = await self._gerar_templates_personalizados(
                dados_diagnostico, mpc_dados, curriculo_dados
            )
            
            # Estratégia de hashtags por tipo de conteúdo
            resultado["estrategia_hashtags"] = await self._definir_estrategia_hashtags(
                mpc_dados, estrategia
            )
            
            # Calendário editorial detalhado
            resultado["calendario_detalhado"] = await self._gerar_calendario_editorial(
                perfil_linkedin_id, periodo_dias, estrategia, resultado["temas_identificados"],
                resultado["templates_personalizados"]
            )
            
            # Cronograma de publicação otimizado
            resultado["cronograma_publicacao"] = await self._otimizar_cronograma_publicacao(
                resultado["calendario_detalhado"], estrategia
            )
            
            # KPIs e métricas de acompanhamento
            resultado["kpis_conteudo"] = await self._definir_kpis_conteudo(
                estrategia, resultado["calendario_detalhado"]
            )
            
            # Plano editorial consolidado
            resultado["plano_editorial"] = {
                "periodo": f"{periodo_dias} dias",
                "total_posts": len(resultado["calendario_detalhado"]),
                "distribuicao_60_40": self._calcular_distribuicao_real(resultado["calendario_detalhado"]),
                "frequencia_semanal": json.loads(estrategia.frequencia_posts)["posts_por_semana"],
                "objetivos": ["Construir audiência", "Demonstrar autoridade", "Gerar networking"],
                "status": "Ativo"
            }
            
        except Exception as e:
            raise e
        
        return resultado
    
    async def gerar_conteudo_individual(
        self,
        tipo_conteudo: str,
        tema: str,
        template_base: str,
        dados_contexto: Dict[str, Any],
        palavras_chave: List[str] = None
    ) -> Dict[str, Any]:
        """
        Gera post individual completo com base nos parâmetros fornecidos
        
        Tipo: 'geral' (60% audiência) ou 'autoridade' (40% expertise)
        """
        if tipo_conteudo not in ["geral", "autoridade"]:
            raise ValueError("Tipo deve ser 'geral' ou 'autoridade'")
        
        # Personaliza template com dados do contexto
        post_personalizado = await self._personalizar_template(
            template_base, tema, dados_contexto, palavras_chave
        )
        
        # Adiciona elementos estratégicos
        post_com_elementos = await self._adicionar_elementos_estrategicos(
            post_personalizado, tipo_conteudo, tema
        )
        
        # Define hashtags otimizadas
        hashtags_otimizadas = await self._definir_hashtags_post(
            tipo_conteudo, tema, palavras_chave
        )
        
        # Adiciona call-to-action
        call_to_action = await self._selecionar_call_to_action(tipo_conteudo, tema)
        
        # Monta post final
        post_final = {
            "conteudo_principal": post_com_elementos,
            "hashtags": hashtags_otimizadas,
            "call_to_action": call_to_action,
            "tipo": tipo_conteudo,
            "tema": tema,
            "objetivo": "audiencia" if tipo_conteudo == "geral" else "autoridade",
            "caracteristicas": {
                "palavras_chave_incluidas": len(palavras_chave) if palavras_chave else 0,
                "tom": self._determinar_tom_post(tipo_conteudo),
                "formato": self._determinar_formato_post(template_base),
                "engajamento_esperado": self._estimar_engajamento(tipo_conteudo, tema)
            }
        }
        
        return post_final
    
    async def analisar_performance_conteudo(
        self,
        perfil_linkedin_id: int,
        periodo_analise_dias: int = 30
    ) -> Dict[str, Any]:
        """
        Analisa performance do conteúdo publicado e sugere otimizações
        
        Baseado na metodologia Carolina Martins de monitoramento contínuo
        """
        # Busca conteúdos publicados no período
        data_inicio = datetime.now() - timedelta(days=periodo_analise_dias)
        
        conteudos = self.db.query(ConteudoLinkedIn).filter(
            ConteudoLinkedIn.perfil_linkedin_id == perfil_linkedin_id,
            ConteudoLinkedIn.data_publicacao >= data_inicio,
            ConteudoLinkedIn.status == "publicado"
        ).all()
        
        if not conteudos:
            return {"erro": "Nenhum conteúdo encontrado no período"}
        
        # Análise por tipo de conteúdo
        analise_tipos = {
            "geral": {"total": 0, "engajamento_medio": 0, "melhor_performance": None},
            "autoridade": {"total": 0, "engajamento_medio": 0, "melhor_performance": None}
        }
        
        # Análise por tema
        analise_temas = {}
        
        # Análise por horário
        analise_horarios = {}
        
        for conteudo in conteudos:
            tipo = conteudo.tipo_conteudo
            tema = conteudo.tema
            
            # Simula métricas (em implementação real viria da API do LinkedIn)
            engajamento_simulado = self._simular_engajamento_post(conteudo)
            
            # Atualiza análise por tipo
            if tipo in analise_tipos:
                analise_tipos[tipo]["total"] += 1
                analise_tipos[tipo]["engajamento_medio"] += engajamento_simulado
            
            # Atualiza análise por tema
            if tema not in analise_temas:
                analise_temas[tema] = {"total": 0, "engajamento_total": 0}
            analise_temas[tema]["total"] += 1
            analise_temas[tema]["engajamento_total"] += engajamento_simulado
            
            # Atualiza análise por horário
            horario = conteudo.data_publicacao.hour
            if horario not in analise_horarios:
                analise_horarios[horario] = {"total": 0, "engajamento_total": 0}
            analise_horarios[horario]["total"] += 1
            analise_horarios[horario]["engajamento_total"] += engajamento_simulado
        
        # Calcula médias
        for tipo_info in analise_tipos.values():
            if tipo_info["total"] > 0:
                tipo_info["engajamento_medio"] = tipo_info["engajamento_medio"] / tipo_info["total"]
        
        # Identifica padrões e recomendações
        recomendacoes = await self._gerar_recomendacoes_performance(
            analise_tipos, analise_temas, analise_horarios
        )
        
        resultado_analise = {
            "periodo_analisado": f"{periodo_analise_dias} dias",
            "total_posts": len(conteudos),
            "analise_tipos": analise_tipos,
            "temas_mais_engajados": sorted(
                [(tema, info["engajamento_total"]/info["total"]) for tema, info in analise_temas.items()],
                key=lambda x: x[1], reverse=True
            )[:5],
            "melhores_horarios": sorted(
                [(hora, info["engajamento_total"]/info["total"]) for hora, info in analise_horarios.items()],
                key=lambda x: x[1], reverse=True
            )[:3],
            "distribuicao_60_40": self._verificar_distribuicao_60_40(conteudos),
            "recomendacoes": recomendacoes,
            "kpis": {
                "engajamento_medio_geral": sum(info["engajamento_medio"] for info in analise_tipos.values()) / 2,
                "consistencia_publicacao": len(conteudos) / (periodo_analise_dias / 7) * 100,  # % da meta semanal
                "balanceamento_conteudo": abs(50 - (analise_tipos["geral"]["total"] / len(conteudos) * 100))  # Distância do ideal 50/50
            }
        }
        
        return resultado_analise
    
    # MÉTODOS DE GERAÇÃO DE CONTEÚDO
    
    async def _identificar_personas_audiencia(
        self,
        dados_diagnostico: Dict[str, Any],
        mpc_dados: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Identifica personas da audiência baseado no perfil e área de atuação
        """
        area_interesse = dados_diagnostico.get("configuracao_agentes", {}).get("agente_1_palavras_chave", {}).get("area_interesse", "")
        nivel_experiencia = dados_diagnostico.get("experiencia_profissional", {}).get("experiencia_profissional", 0)
        
        # Define personas baseadas na área e experiência
        personas = {
            "profissionais_area": {
                "descricao": f"Profissionais de {area_interesse}",
                "interesses": ["tendências da área", "networking", "oportunidades"],
                "conteudo_preferido": "insights técnicos e cases",
                "percentual_audiencia": 40
            },
            "aspirantes_area": {
                "descricao": f"Pessoas que querem entrar em {area_interesse}",
                "interesses": ["dicas de carreira", "como começar", "competências necessárias"],
                "conteudo_preferido": "conteúdo educativo e motivacional",
                "percentual_audiencia": 30
            },
            "recrutadores_hr": {
                "descricao": "Recrutadores e profissionais de RH",
                "interesses": ["talentos", "competências", "tendências de mercado"],
                "conteudo_preferido": "demonstração de expertise e resultados",
                "percentual_audiencia": 20
            },
            "network_geral": {
                "descricao": "Rede profissional geral",
                "interesses": ["carreira", "motivação", "crescimento profissional"],
                "conteudo_preferido": "conteúdo motivacional e reflexivo",
                "percentual_audiencia": 10
            }
        }
        
        return personas
    
    async def _mapear_temas_estrategicos(
        self,
        mpc_dados: Dict[str, Any],
        curriculo_dados: Dict[str, Any],
        estrategia: EstrategiaConteudo
    ) -> Dict[str, Any]:
        """
        Mapeia temas estratégicos baseados no MPC e experiências
        """
        temas_autoridade = []
        temas_gerais = []
        
        # Temas de autoridade baseados no MPC
        if mpc_dados:
            palavras_essenciais = mpc_dados.get("priorizacao_final", {}).get("essenciais", [])
            for palavra_obj in palavras_essenciais[:5]:
                tema = f"Expertise em {palavra_obj.get('palavra', '')}"
                temas_autoridade.append(tema)
        
        # Temas baseados em experiências do currículo
        if curriculo_dados:
            experiencias = curriculo_dados.get("13_passos", {}).get("4_experiencias", {}).get("experiencias", [])
            for exp in experiencias[:3]:  # Top 3 experiências
                if exp.get("resultados_destacados"):
                    tema = f"Case: {exp.get('empresa', 'Empresa')}"
                    temas_autoridade.append(tema)
        
        # Temas gerais (60%)
        temas_gerais = [
            "Tendências do mercado",
            "Dicas de carreira",
            "Motivação profissional",
            "Networking eficaz",
            "Desenvolvimento pessoal",
            "Liderança",
            "Gestão do tempo",
            "Inovação",
            "Produtividade",
            "Soft skills"
        ]
        
        return {
            "autoridade": temas_autoridade,
            "gerais": temas_gerais,
            "mix_recomendado": {
                "autoridade_percentual": 40,
                "geral_percentual": 60
            }
        }
    
    async def _gerar_templates_personalizados(
        self,
        dados_diagnostico: Dict[str, Any],
        mpc_dados: Dict[str, Any],
        curriculo_dados: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """
        Gera templates personalizados baseados no perfil específico
        """
        area_interesse = dados_diagnostico.get("configuracao_agentes", {}).get("agente_1_palavras_chave", {}).get("area_interesse", "")
        nome_usuario = dados_diagnostico.get("perfil_basico", {}).get("nome", "").split()[0]
        
        # Templates gerais personalizados
        templates_gerais = [
            f"💡 Reflexão sobre {area_interesse}: {{insight}}",
            f"🚀 Dica de carreira em {area_interesse}: {{dica_pratica}}",
            f"📊 O mercado de {area_interesse} está mudando: {{tendencia}}",
            f"💪 Segunda-feira motivacional: {{motivacao}}",
            f"🤝 Networking em {area_interesse}: {{importancia_networking}}",
            f"⏰ Gestão de tempo para profissionais de {area_interesse}: {{dica_tempo}}",
            f"🎯 Meta de carreira em {area_interesse}: {{meta_carreira}}",
            f"📈 Crescimento profissional: {{crescimento}}",
            f"🧠 Aprendizado contínuo em {area_interesse}: {{aprendizado}}",
            f"✨ Inovação em {area_interesse}: {{inovacao}}"
        ]
        
        # Templates de autoridade personalizados
        templates_autoridade = [
            f"📈 Case de sucesso: Como {{resultado_especifico}} em {{projeto}}",
            f"🎯 Metodologia que uso em {area_interesse}: {{metodologia}}",
            f"🔍 Insight técnico de {area_interesse}: {{conhecimento_especifico}}",
            f"⚡ Lição aprendida nos meus {{anos_exp}} anos em {area_interesse}: {{licao}}",
            f"🛠️ Ferramenta indispensável para {area_interesse}: {{ferramenta}}",
            f"📊 Resultado que alcancei: {{resultado_tangivel}}",
            f"🎪 Erro que cometi e o que aprendi: {{erro_aprendizado}}",
            f"🚀 Como resolvi {{problema_especifico}} usando {{solucao}}",
            f"💼 Experiência em {{empresa}}: {{experiencia_relevante}}",
            f"🏆 Conquista profissional: {{conquista}}"
        ]
        
        return {
            "gerais": templates_gerais,
            "autoridade": templates_autoridade,
            "personalizacao": {
                "area": area_interesse,
                "nome": nome_usuario,
                "tom": "profissional_acessivel"
            }
        }
    
    async def _definir_estrategia_hashtags(
        self,
        mpc_dados: Dict[str, Any],
        estrategia: EstrategiaConteudo
    ) -> Dict[str, Any]:
        """
        Define estratégia de hashtags otimizada por tipo de conteúdo
        """
        area_foco = estrategia.area_foco.lower().replace(" ", "")
        
        # Hashtags específicas do MPC
        hashtags_mpc = []
        if mpc_dados:
            palavras_essenciais = mpc_dados.get("priorizacao_final", {}).get("essenciais", [])
            for palavra_obj in palavras_essenciais[:5]:
                palavra = palavra_obj.get("palavra", "")
                hashtag = "#" + palavra.replace(" ", "").replace("-", "").lower()
                hashtags_mpc.append(hashtag)
        
        # Hashtags por tipo de conteúdo
        estrategia_hashtags = {
            "geral": {
                "principais": [f"#{area_foco}", "#carreira", "#profissional", "#networking", "#crescimento"],
                "secundarias": ["#dicas", "#motivacao", "#lideranca", "#gestao", "#inovacao"],
                "quantidade_recomendada": 5,
                "mix_recomendado": "3 principais + 2 secundárias"
            },
            "autoridade": {
                "principais": hashtags_mpc[:3] if hashtags_mpc else [f"#{area_foco}", "#expertise", "#experiencia"],
                "secundarias": ["#resultados", "#metodologia", "#case", "#insights", "#conhecimento"],
                "quantidade_recomendada": 5,
                "mix_recomendado": "3 MPC/área + 2 autoridade"
            },
            "diretrizes": {
                "evitar_hashtags_genericas": ["#trabalho", "#emprego", "#job"],
                "priorizar_hashtags_nicho": True,
                "variar_hashtags": "Não usar sempre as mesmas",
                "pesquisar_hashtags_trending": "Incluir 1-2 trending por semana"
            }
        }
        
        return estrategia_hashtags
    
    async def _gerar_calendario_editorial(
        self,
        perfil_linkedin_id: int,
        periodo_dias: int,
        estrategia: EstrategiaConteudo,
        temas: Dict[str, Any],
        templates: Dict[str, List[str]]
    ) -> List[Dict[str, Any]]:
        """
        Gera calendário editorial completo seguindo distribuição 60/40
        """
        frequencia = json.loads(estrategia.frequencia_posts)["posts_por_semana"]
        total_posts = int((periodo_dias / 7) * frequencia)
        
        # Calcula distribuição 60/40
        posts_gerais = int(total_posts * 0.6)
        posts_autoridade = int(total_posts * 0.4)
        
        calendario = []
        data_inicio = datetime.now()
        
        # Gera posts gerais (60%)
        for i in range(posts_gerais):
            dias_offset = i * (periodo_dias // total_posts)
            data_post = data_inicio + timedelta(days=dias_offset)
            
            # Seleciona tema e template
            tema = self._selecionar_tema_aleatorio(temas["gerais"])
            template = self._selecionar_template_aleatorio(templates["gerais"])
            
            post = {
                "data": data_post.strftime("%Y-%m-%d"),
                "hora_sugerida": self._sugerir_horario_otimo(data_post.weekday()),
                "tipo": TipoConteudo.GERAL.value,
                "tema": tema,
                "template": template,
                "objetivo": "Engajar audiência",
                "prioridade": "media",
                "status": "planejado"
            }
            calendario.append(post)
        
        # Gera posts de autoridade (40%)
        for i in range(posts_autoridade):
            dias_offset = (i + posts_gerais) * (periodo_dias // total_posts)
            data_post = data_inicio + timedelta(days=dias_offset)
            
            # Seleciona tema e template
            tema = self._selecionar_tema_aleatorio(temas["autoridade"])
            template = self._selecionar_template_aleatorio(templates["autoridade"])
            
            post = {
                "data": data_post.strftime("%Y-%m-%d"),
                "hora_sugerida": self._sugerir_horario_otimo(data_post.weekday()),
                "tipo": TipoConteudo.AUTORIDADE.value,
                "tema": tema,
                "template": template,
                "objetivo": "Demonstrar expertise",
                "prioridade": "alta",
                "status": "planejado"
            }
            calendario.append(post)
        
        # Ordena por data
        calendario.sort(key=lambda x: x["data"])
        
        # Salva no banco de dados
        for post in calendario:
            conteudo = ConteudoLinkedIn(
                perfil_linkedin_id=perfil_linkedin_id,
                tipo_conteudo=post["tipo"],
                tema=post["tema"],
                data_publicacao=datetime.strptime(f"{post['data']} {post['hora_sugerida']}", "%Y-%m-%d %H:%M"),
                template=post["template"],
                status="planejado"
            )
            self.db.add(conteudo)
        
        self.db.commit()
        
        return calendario
    
    async def _otimizar_cronograma_publicacao(
        self,
        calendario: List[Dict[str, Any]],
        estrategia: EstrategiaConteudo
    ) -> Dict[str, Any]:
        """
        Otimiza cronograma de publicação baseado em melhores práticas
        """
        # Analisa distribuição ao longo da semana
        distribuicao_semanal = {
            0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []  # Segunda a Domingo
        }
        
        for post in calendario:
            data_post = datetime.strptime(post["data"], "%Y-%m-%d")
            dia_semana = data_post.weekday()
            distribuicao_semanal[dia_semana].append(post)
        
        # Recomendações de otimização
        recomendacoes = []
        
        # Verifica se há posts em fins de semana (menos engajamento)
        if len(distribuicao_semanal[5]) + len(distribuicao_semanal[6]) > 0:
            recomendacoes.append("Considere reduzir posts em fins de semana para melhor engajamento")
        
        # Verifica concentração em dias específicos
        posts_por_dia = [len(posts) for posts in distribuicao_semanal.values()]
        if max(posts_por_dia) > min(posts_por_dia) * 2:
            recomendacoes.append("Distribua posts mais uniformemente ao longo da semana")
        
        # Horários otimizados por tipo de post
        horarios_otimizados = {
            "geral": ["08:00", "12:00", "18:00"],  # Horários de maior audiência geral
            "autoridade": ["09:00", "14:00", "19:00"]  # Horários de maior audiência profissional
        }
        
        cronograma_otimizado = {
            "distribuicao_semanal": {
                f"dia_{i}": len(posts) for i, posts in distribuicao_semanal.items()
            },
            "horarios_recomendados": horarios_otimizados,
            "recomendacoes": recomendacoes,
            "melhor_dia_engajamento": "terça-feira",  # Baseado em estudos do LinkedIn
            "pior_dia_engajamento": "domingo",
            "frequencia_ideal": json.loads(estrategia.frequencia_posts)["posts_por_semana"]
        }
        
        return cronograma_otimizado
    
    async def _definir_kpis_conteudo(
        self,
        estrategia: EstrategiaConteudo,
        calendario: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Define KPIs e métricas de acompanhamento do conteúdo
        """
        frequencia_semanal = json.loads(estrategia.frequencia_posts)["posts_por_semana"]
        
        kpis = {
            "metricas_quantitativas": {
                "posts_planejados": len(calendario),
                "posts_por_semana_meta": frequencia_semanal,
                "distribuicao_60_40": {
                    "geral_meta": 60,
                    "autoridade_meta": 40,
                    "geral_atual": len([p for p in calendario if p["tipo"] == "geral"]) / len(calendario) * 100,
                    "autoridade_atual": len([p for p in calendario if p["tipo"] == "autoridade"]) / len(calendario) * 100
                }
            },
            "metricas_engajamento": {
                "likes_meta_por_post": {"geral": 20, "autoridade": 35},
                "comentarios_meta_por_post": {"geral": 3, "autoridade": 8},
                "compartilhamentos_meta_por_post": {"geral": 2, "autoridade": 5},
                "visualizacoes_meta_por_post": {"geral": 500, "autoridade": 800}
            },
            "metricas_crescimento": {
                "novos_seguidores_meta_mensal": 50,
                "conexoes_novas_meta_mensal": 30,
                "mensagens_inbox_meta_mensal": 10,
                "oportunidades_geradas_meta_mensal": 2
            },
            "metricas_autoridade": {
                "mencoes_como_especialista": 5,
                "convites_para_eventos": 2,
                "solicitacoes_colaboracao": 3,
                "reconhecimento_industria": 1
            }
        }
        
        return kpis
    
    # MÉTODOS AUXILIARES
    
    def _carregar_templates_completos(self) -> Dict[str, List[str]]:
        """Carrega biblioteca completa de templates"""
        return {
            "geral_motivacional": [
                "🌟 Segunda-feira inspiradora: {motivacao}",
                "💪 Desafio da semana: {desafio}",
                "✨ Reflexão: {reflexao}",
                "🚀 Meta alcançada: {meta}"
            ],
            "geral_carreira": [
                "📈 Dica de carreira: {dica}",
                "🎯 Estratégia profissional: {estrategia}",
                "🤝 Networking: {networking}",
                "📚 Aprendizado: {aprendizado}"
            ],
            "autoridade_case": [
                "📊 Case de sucesso: {case}",
                "⚡ Resultado alcançado: {resultado}",
                "🛠️ Metodologia aplicada: {metodologia}",
                "🎪 Erro e aprendizado: {erro}"
            ],
            "autoridade_insight": [
                "🔍 Insight técnico: {insight}",
                "💡 Descoberta: {descoberta}",
                "⚙️ Ferramenta útil: {ferramenta}",
                "📈 Tendência identificada: {tendencia}"
            ]
        }
    
    def _carregar_horarios_otimos(self) -> Dict[str, List[str]]:
        """Carrega horários ótimos para publicação"""
        return {
            "segunda": ["08:00", "12:00", "17:00"],
            "terca": ["09:00", "13:00", "18:00"],
            "quarta": ["08:30", "12:30", "17:30"],
            "quinta": ["09:00", "13:00", "18:00"],
            "sexta": ["08:00", "12:00", "16:00"],
            "sabado": ["10:00", "14:00"],
            "domingo": ["19:00"]
        }
    
    def _carregar_call_to_actions(self) -> Dict[str, List[str]]:
        """Carrega call-to-actions por tipo de conteúdo"""
        return {
            "geral": [
                "O que vocês acham? Comentem aí! 👇",
                "Qual sua experiência com isso? 🤔",
                "Concordam? Discordam? Vamos debater! 💬",
                "Marquem alguém que precisa ver isso! 👥"
            ],
            "autoridade": [
                "Já passaram por situação similar? Como resolveram? 🤝",
                "Que outras estratégias vocês usariam? 💡",
                "Vamos trocar experiências nos comentários! 📈",
                "Conectem comigo para trocarmos insights! 🚀"
            ]
        }
    
    def _selecionar_tema_aleatorio(self, temas: List[str]) -> str:
        """Seleciona tema aleatório da lista"""
        import random
        return random.choice(temas) if temas else "Tema padrão"
    
    def _selecionar_template_aleatorio(self, templates: List[str]) -> str:
        """Seleciona template aleatório da lista"""
        import random
        return random.choice(templates) if templates else "Template padrão: {conteudo}"
    
    def _sugerir_horario_otimo(self, dia_semana: int) -> str:
        """Sugere horário ótimo baseado no dia da semana"""
        dias = ["segunda", "terca", "quarta", "quinta", "sexta", "sabado", "domingo"]
        dia_nome = dias[dia_semana]
        horarios = self.horarios_otimos.get(dia_nome, ["12:00"])
        import random
        return random.choice(horarios)
    
    def _calcular_distribuicao_real(self, calendario: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calcula distribuição real 60/40 do calendário"""
        total = len(calendario)
        if total == 0:
            return {"geral": 0, "autoridade": 0}
        
        geral_count = len([p for p in calendario if p.get("tipo") == "geral"])
        autoridade_count = len([p for p in calendario if p.get("tipo") == "autoridade"])
        
        return {
            "geral": round(geral_count / total * 100, 1),
            "autoridade": round(autoridade_count / total * 100, 1)
        }
    
    def _verificar_distribuicao_60_40(self, conteudos: List) -> Dict[str, Any]:
        """Verifica se distribuição está próxima do ideal 60/40"""
        total = len(conteudos)
        if total == 0:
            return {"status": "sem_dados"}
        
        geral_count = len([c for c in conteudos if c.tipo_conteudo == "geral"])
        geral_percent = geral_count / total * 100
        
        # Tolerância de 10% para considerar "dentro do ideal"
        if 50 <= geral_percent <= 70:
            status = "ideal"
        elif geral_percent > 70:
            status = "muito_geral"
        else:
            status = "muito_autoridade"
        
        return {
            "status": status,
            "geral_atual": round(geral_percent, 1),
            "autoridade_atual": round(100 - geral_percent, 1),
            "geral_ideal": 60,
            "autoridade_ideal": 40
        }
    
    def _simular_engajamento_post(self, conteudo) -> float:
        """Simula engajamento do post (em implementação real viria da API)"""
        # Simulação baseada no tipo de conteúdo
        base_score = 15.0  # Score base
        
        if conteudo.tipo_conteudo == "autoridade":
            base_score *= 1.5  # Posts de autoridade tendem a ter mais engajamento
        
        # Adiciona variação aleatória
        import random
        variation = random.uniform(0.5, 2.0)
        
        return base_score * variation
    
    async def _gerar_recomendacoes_performance(
        self,
        analise_tipos: Dict[str, Any],
        analise_temas: Dict[str, Any],
        analise_horarios: Dict[str, Any]
    ) -> List[str]:
        """Gera recomendações baseadas na análise de performance"""
        recomendacoes = []
        
        # Recomendações baseadas em tipos
        if analise_tipos["geral"]["engajamento_medio"] > analise_tipos["autoridade"]["engajamento_medio"]:
            recomendacoes.append("Posts gerais estão performando melhor - considere aumentar ligeiramente a proporção")
        else:
            recomendacoes.append("Posts de autoridade estão gerando bom engajamento - mantenha foco na expertise")
        
        # Recomendações baseadas em temas
        if analise_temas:
            melhor_tema = max(analise_temas.items(), key=lambda x: x[1]["engajamento_total"]/x[1]["total"])
            recomendacoes.append(f"Tema '{melhor_tema[0]}' tem melhor performance - explore mais variações")
        
        # Recomendações baseadas em horários
        if analise_horarios:
            melhor_horario = max(analise_horarios.items(), key=lambda x: x[1]["engajamento_total"]/x[1]["total"])
            recomendacoes.append(f"Horário {melhor_horario[0]}h tem melhor engajamento - priorize este período")
        
        return recomendacoes
    
    # Métodos de personalização avançada
    async def _personalizar_template(
        self,
        template: str,
        tema: str,
        dados_contexto: Dict[str, Any],
        palavras_chave: List[str] = None
    ) -> str:
        """Personaliza template com dados contextuais"""
        # Substitui placeholders básicos
        template_personalizado = template.format(
            tema=tema,
            area=dados_contexto.get("area", ""),
            nome=dados_contexto.get("nome", ""),
            **dados_contexto
        )
        
        # Adiciona palavras-chave naturalmente se fornecidas
        if palavras_chave:
            # Implementação seria mais sofisticada na versão real
            palavras_contexto = ", ".join(palavras_chave[:2])
            if "{palavras_chave}" in template_personalizado:
                template_personalizado = template_personalizado.replace("{palavras_chave}", palavras_contexto)
        
        return template_personalizado
    
    async def _adicionar_elementos_estrategicos(
        self,
        post: str,
        tipo_conteudo: str,
        tema: str
    ) -> str:
        """Adiciona elementos estratégicos ao post"""
        elementos_adicionais = []
        
        # Adiciona contexto baseado no tipo
        if tipo_conteudo == "autoridade":
            elementos_adicionais.append("\n\n💼 Baseado na minha experiência prática:")
        elif tipo_conteudo == "geral":
            elementos_adicionais.append("\n\n🤝 Na minha opinião:")
        
        # Adiciona chamada para engajamento
        if "dica" in tema.lower():
            elementos_adicionais.append("\n\n📌 Qual dica vocês dariam?")
        elif "caso" in tema.lower() or "case" in tema.lower():
            elementos_adicionais.append("\n\n🎯 Já enfrentaram desafio similar?")
        
        return post + "".join(elementos_adicionais)
    
    async def _definir_hashtags_post(
        self,
        tipo_conteudo: str,
        tema: str,
        palavras_chave: List[str] = None
    ) -> List[str]:
        """Define hashtags otimizadas para o post específico"""
        hashtags = []
        
        # Hashtags baseadas no tipo
        if tipo_conteudo == "geral":
            hashtags.extend(["#carreira", "#profissional", "#networking"])
        else:
            hashtags.extend(["#expertise", "#experiencia", "#resultados"])
        
        # Hashtags baseadas no tema
        tema_lower = tema.lower()
        if "motivação" in tema_lower or "motivacao" in tema_lower:
            hashtags.append("#motivacao")
        if "dica" in tema_lower:
            hashtags.append("#dicas")
        if "case" in tema_lower or "caso" in tema_lower:
            hashtags.append("#case")
        
        # Adiciona palavras-chave como hashtags se fornecidas
        if palavras_chave:
            for palavra in palavras_chave[:2]:  # Máximo 2 do MPC
                hashtag = "#" + palavra.replace(" ", "").replace("-", "").lower()
                if hashtag not in hashtags:
                    hashtags.append(hashtag)
        
        return hashtags[:5]  # Máximo 5 hashtags
    
    async def _selecionar_call_to_action(
        self,
        tipo_conteudo: str,
        tema: str
    ) -> str:
        """Seleciona call-to-action apropriado"""
        ctas = self.call_to_actions.get(tipo_conteudo, self.call_to_actions["geral"])
        
        # Personaliza baseado no tema
        if "experiencia" in tema.lower() or "case" in tema.lower():
            return "Já passaram por situação similar? Como resolveram? 🤝"
        elif "dica" in tema.lower():
            return "Que outras dicas vocês dariam? 💡"
        else:
            import random
            return random.choice(ctas)
    
    def _determinar_tom_post(self, tipo_conteudo: str) -> str:
        """Determina tom apropriado para o post"""
        return "inspiracional_acessivel" if tipo_conteudo == "geral" else "profissional_tecnico"
    
    def _determinar_formato_post(self, template: str) -> str:
        """Determina formato do post baseado no template"""
        if "💡" in template:
            return "insight"
        elif "📊" in template or "📈" in template:
            return "dados_case"
        elif "🚀" in template or "💪" in template:
            return "motivacional"
        else:
            return "reflexivo"
    
    def _estimar_engajamento(self, tipo_conteudo: str, tema: str) -> str:
        """Estima nível de engajamento esperado"""
        if tipo_conteudo == "autoridade":
            return "alto" if "case" in tema.lower() else "medio_alto"
        else:
            return "medio" if "motivacao" in tema.lower() else "medio_baixo"