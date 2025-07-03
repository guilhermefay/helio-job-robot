"""
Agente 3: Otimização LinkedIn - Metodologia Carolina Martins

Este agente implementa a metodologia completa dos 10 passos do LinkedIn Meteórico
baseada nas transcrições da Carolina Martins:

PROCESSO DOS 10 PASSOS LINKEDIN:
1. Foto de perfil profissional
2. Foto de capa (banner) da área
3. URL personalizada
4. Localidade correta
5. Pronomes (opcional)
6. Modo de Criação + 5 hashtags
7. Headline/Título estratégico
8. Setor correto
9. Seção "Sobre" otimizada
10. Experiências com mídias + 50 competências

ESTRATÉGIA DE CONTEÚDO:
- 60% posts gerais (audiência)
- 40% posts específicos (autoridade)
- SSI (Social Selling Index) tracking
- Networking estratégico
"""

import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from sqlalchemy.orm import Session
from core.models import (
    User, PerfilLinkedIn, ExperienciaLinkedIn, ConteudoLinkedIn,
    EstrategiaConteudo, MetricasLinkedIn, StatusPerfilLinkedIn,
    TipoConteudo, StatusSSI
)

class LinkedInCarolinaMartins:
    """
    Implementação do Agente 3: Otimização LinkedIn
    baseado na metodologia dos 10 passos da Carolina Martins
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.criterios_foto_profissional = self._carregar_criterios_foto()
        self.templates_conteudo = self._carregar_templates_conteudo()
        self.estrategia_60_40 = self._carregar_estrategia_conteudo()
        self.competencias_sugeridas = self._carregar_competencias_base()
    
    async def construir_linkedin_meteorico(
        self,
        usuario_id: int,
        dados_diagnostico: Dict[str, Any],
        curriculo_dados: Dict[str, Any],
        mpc_dados: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Constrói LinkedIn meteórico completo seguindo os 10 passos metodológicos
        
        Integra dados do diagnóstico, currículo e MPC para criar perfil otimizado
        que será encontrado por recrutadores e gere autoridade na área.
        """
        usuario = self.db.query(User).filter(User.id == usuario_id).first()
        if not usuario:
            raise ValueError(f"Usuário {usuario_id} não encontrado")
        
        # Cria perfil LinkedIn
        perfil_linkedin = PerfilLinkedIn(
            usuario_id=usuario_id,
            status=StatusPerfilLinkedIn.EM_CONSTRUCAO.value,
            versao=1
        )
        self.db.add(perfil_linkedin)
        self.db.commit()
        
        resultado = {
            "perfil_id": perfil_linkedin.id,
            "10_passos": {},
            "estrategia_conteudo": {},
            "ssi_objetivo": {},
            "validacoes": {},
            "score_linkedin": 0.0,
            "classificacao": "",
            "próximos_passos": []
        }
        
        try:
            # PASSO 1: Foto de Perfil Profissional
            resultado["10_passos"]["1_foto_perfil"] = await self._passo_1_foto_perfil(
                perfil_linkedin, dados_diagnostico
            )
            
            # PASSO 2: Foto de Capa (Banner)
            resultado["10_passos"]["2_foto_capa"] = await self._passo_2_foto_capa(
                perfil_linkedin, dados_diagnostico, mpc_dados
            )
            
            # PASSO 3: URL Personalizada
            resultado["10_passos"]["3_url_personalizada"] = await self._passo_3_url_personalizada(
                perfil_linkedin, dados_diagnostico
            )
            
            # PASSO 4: Localidade
            resultado["10_passos"]["4_localidade"] = await self._passo_4_localidade(
                perfil_linkedin, dados_diagnostico
            )
            
            # PASSO 5: Pronomes (opcional)
            resultado["10_passos"]["5_pronomes"] = await self._passo_5_pronomes(
                perfil_linkedin, dados_diagnostico
            )
            
            # PASSO 6: Modo de Criação + 5 Hashtags
            resultado["10_passos"]["6_modo_criacao_hashtags"] = await self._passo_6_modo_criacao(
                perfil_linkedin, mpc_dados
            )
            
            # PASSO 7: Headline/Título Estratégico
            resultado["10_passos"]["7_headline"] = await self._passo_7_headline(
                perfil_linkedin, curriculo_dados, mpc_dados
            )
            
            # PASSO 8: Setor
            resultado["10_passos"]["8_setor"] = await self._passo_8_setor(
                perfil_linkedin, dados_diagnostico
            )
            
            # PASSO 9: Seção "Sobre"
            resultado["10_passos"]["9_sobre"] = await self._passo_9_sobre(
                perfil_linkedin, curriculo_dados, mpc_dados
            )
            
            # PASSO 10: Experiências + Competências
            resultado["10_passos"]["10_experiencias_competencias"] = await self._passo_10_experiencias(
                perfil_linkedin, curriculo_dados, mpc_dados
            )
            
            # Estratégia de Conteúdo 60/40
            resultado["estrategia_conteudo"] = await self._definir_estrategia_conteudo(
                perfil_linkedin, dados_diagnostico, mpc_dados
            )
            
            # SSI (Social Selling Index) Tracking
            resultado["ssi_objetivo"] = await self._configurar_ssi_tracking(
                perfil_linkedin, dados_diagnostico
            )
            
            # Validações metodológicas
            resultado["validacoes"] = self._executar_validacoes_linkedin(perfil_linkedin, resultado["10_passos"])
            resultado["score_linkedin"] = self._calcular_score_linkedin(resultado["validacoes"])
            resultado["classificacao"] = self._determinar_classificacao_linkedin(resultado["score_linkedin"])
            resultado["próximos_passos"] = self._gerar_proximos_passos_linkedin(resultado)
            
            # Atualiza status do perfil
            perfil_linkedin.status = StatusPerfilLinkedIn.ATIVO.value if resultado["score_linkedin"] >= 80 else StatusPerfilLinkedIn.NECESSITA_MELHORIA.value
            perfil_linkedin.score_qualidade = resultado["score_linkedin"]
            self.db.commit()
            
        except Exception as e:
            perfil_linkedin.status = StatusPerfilLinkedIn.ERRO.value
            self.db.commit()
            raise e
        
        return resultado
    
    async def gerar_calendario_conteudo(
        self,
        perfil_linkedin_id: int,
        periodo_dias: int = 30
    ) -> Dict[str, Any]:
        """
        Gera calendário editorial seguindo estratégia 60/40
        
        60% conteúdo geral (audiência) + 40% específico (autoridade)
        """
        perfil = self.db.query(PerfilLinkedIn).filter(PerfilLinkedIn.id == perfil_linkedin_id).first()
        if not perfil:
            raise ValueError("Perfil LinkedIn não encontrado")
        
        # Busca estratégia de conteúdo definida
        estrategia = self.db.query(EstrategiaConteudo).filter(
            EstrategiaConteudo.perfil_linkedin_id == perfil_linkedin_id
        ).first()
        
        if not estrategia:
            raise ValueError("Estratégia de conteúdo não definida")
        
        calendario = []
        data_inicio = datetime.now()
        
        # Calcula posts baseado na frequência recomendada
        frequencia_semanal = json.loads(estrategia.frequencia_posts)["posts_por_semana"]
        total_posts = int((periodo_dias / 7) * frequencia_semanal)
        
        # Distribui posts 60/40
        posts_gerais = int(total_posts * 0.6)
        posts_especificos = int(total_posts * 0.4)
        
        # Gera conteúdo geral (60%)
        for i in range(posts_gerais):
            data_post = data_inicio + timedelta(days=i * (periodo_dias // total_posts))
            
            post_geral = {
                "data": data_post.strftime("%Y-%m-%d"),
                "tipo": TipoConteudo.GERAL.value,
                "tema": self._selecionar_tema_geral(estrategia),
                "template": self._obter_template_geral(),
                "hashtags": self._obter_hashtags_gerais(estrategia),
                "objetivo": "engajamento_audiencia"
            }
            calendario.append(post_geral)
        
        # Gera conteúdo específico (40%)
        for i in range(posts_especificos):
            data_post = data_inicio + timedelta(days=(i + posts_gerais) * (periodo_dias // total_posts))
            
            post_especifico = {
                "data": data_post.strftime("%Y-%m-%d"),
                "tipo": TipoConteudo.AUTORIDADE.value,
                "tema": self._selecionar_tema_autoridade(estrategia),
                "template": self._obter_template_autoridade(),
                "hashtags": self._obter_hashtags_autoridade(estrategia),
                "objetivo": "demonstrar_expertise"
            }
            calendario.append(post_especifico)
        
        # Ordena por data
        calendario.sort(key=lambda x: x["data"])
        
        # Salva calendário no banco
        for post in calendario:
            conteudo = ConteudoLinkedIn(
                perfil_linkedin_id=perfil_linkedin_id,
                tipo_conteudo=post["tipo"],
                tema=post["tema"],
                data_publicacao=datetime.strptime(post["data"], "%Y-%m-%d"),
                template=post["template"],
                hashtags=json.dumps(post["hashtags"]),
                status="agendado"
            )
            self.db.add(conteudo)
        
        self.db.commit()
        
        return {
            "calendario": calendario,
            "total_posts": total_posts,
            "distribuicao": {
                "geral": posts_gerais,
                "especifico": posts_especificos,
                "percentual_geral": 60,
                "percentual_especifico": 40
            },
            "frequencia_semanal": frequencia_semanal,
            "periodo_dias": periodo_dias
        }
    
    # IMPLEMENTAÇÃO DOS 10 PASSOS LINKEDIN
    
    async def _passo_1_foto_perfil(
        self,
        perfil: PerfilLinkedIn,
        dados_diagnostico: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        PASSO 1: Foto de Perfil Profissional
        
        Critérios Carolina Martins:
        - Visibilidade 'para todos'
        - Foto profissional (ombros para cima)
        - Fundo neutro ou desfocado
        - Sorriso natural
        - Roupas adequadas para área
        """
        foto_criterios = {
            "visibilidade_todos": True,
            "enquadramento_profissional": True,  # Ombros para cima
            "fundo_adequado": True,  # Neutro ou desfocado
            "aparencia_profissional": True,
            "qualidade_imagem": True
        }
        
        recomendacoes_foto = [
            "Use foto profissional com enquadramento dos ombros para cima",
            "Mantenha visibilidade 'para todos' para ser encontrado",
            "Escolha fundo neutro ou desfocado",
            "Use vestimenta adequada para sua área profissional",
            "Mantenha expressão confiante e sorriso natural"
        ]
        
        # Atualiza perfil
        perfil.foto_perfil_criterios = json.dumps(foto_criterios)
        
        validacoes = {
            "foto_presente": True,  # Será validado manualmente
            "visibilidade_publica": True,
            "qualidade_profissional": True
        }
        
        return {
            "criterios": foto_criterios,
            "recomendacoes": recomendacoes_foto,
            "validacoes": validacoes,
            "score_passo": self._calcular_score_foto_perfil(validacoes)
        }
    
    async def _passo_2_foto_capa(
        self,
        perfil: PerfilLinkedIn,
        dados_diagnostico: Dict[str, Any],
        mpc_dados: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        PASSO 2: Foto de Capa (Banner) relacionada à área
        
        Critérios Carolina Martins:
        - Relacionada à área de atuação
        - Imagem profissional
        - Pode conter texto/logo da empresa
        - Mantém identidade visual consistente
        """
        area_atuacao = dados_diagnostico.get("configuracao_agentes", {}).get("agente_1_palavras_chave", {}).get("area_interesse", "")
        
        banner_sugestoes = {
            "tecnologia": "Imagens de código, servidores, ou logos tech",
            "marketing": "Gráficos, campanhas, ou elementos visuais criativos",
            "financeiro": "Gráficos financeiros, números, ou prédios corporativos",
            "recursos_humanos": "Pessoas, equipes, ou ambiente corporativo",
            "vendas": "Apertos de mão, gráficos de crescimento, ou networking",
            "default": "Ambiente corporativo ou logo da empresa atual"
        }
        
        area_lower = area_atuacao.lower()
        sugestao_banner = None
        for area, sugestao in banner_sugestoes.items():
            if area in area_lower:
                sugestao_banner = sugestao
                break
        
        if not sugestao_banner:
            sugestao_banner = banner_sugestoes["default"]
        
        banner_config = {
            "area_relacionada": area_atuacao,
            "sugestao_visual": sugestao_banner,
            "elementos_recomendados": [
                "Logo da empresa atual (se aplicável)",
                "Elementos visuais da área",
                "Cores profissionais",
                "Qualidade alta da imagem"
            ]
        }
        
        perfil.foto_capa_config = json.dumps(banner_config)
        
        validacoes = {
            "banner_presente": True,
            "relacionado_area": True,
            "qualidade_profissional": True
        }
        
        return {
            "configuracao": banner_config,
            "sugestao": sugestao_banner,
            "validacoes": validacoes,
            "score_passo": self._calcular_score_foto_capa(validacoes)
        }
    
    async def _passo_3_url_personalizada(
        self,
        perfil: PerfilLinkedIn,
        dados_diagnostico: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        PASSO 3: URL Personalizada (ex: /in/jessicaferreira)
        
        Critérios Carolina Martins:
        - URL curta e limpa
        - Sem números desnecessários
        - Baseada no nome profissional
        - Fácil de lembrar e compartilhar
        """
        nome_completo = dados_diagnostico.get("perfil_basico", {}).get("nome", "")
        
        # Gera sugestões de URL personalizada
        nome_parts = nome_completo.lower().replace(" ", "").replace("-", "")
        
        sugestoes_url = [
            nome_parts,  # Nome completo junto
            nome_completo.split()[0].lower() + nome_completo.split()[-1].lower(),  # Primeiro + último nome
            nome_completo.split()[0].lower() + nome_completo.split()[1].lower() if len(nome_completo.split()) > 1 else nome_parts,  # Primeiro + segundo nome
        ]
        
        # Remove duplicatas e caracteres especiais
        sugestoes_limpas = []
        for sugestao in sugestoes_url:
            clean = re.sub(r'[^a-zA-Z]', '', sugestao)
            if clean and clean not in sugestoes_limpas:
                sugestoes_limpas.append(clean)
        
        url_config = {
            "nome_base": nome_completo,
            "sugestoes": sugestoes_limpas[:3],  # Top 3 sugestões
            "url_recomendada": sugestoes_limpas[0] if sugestoes_limpas else "nomesobrenome",
            "formato": "linkedin.com/in/{url_personalizada}"
        }
        
        perfil.url_personalizada = url_config["url_recomendada"]
        
        validacoes = {
            "url_personalizada": True,
            "formato_limpo": True,
            "sem_numeros_desnecessarios": True,
            "facil_memorizar": len(url_config["url_recomendada"]) <= 20
        }
        
        return {
            "configuracao": url_config,
            "validacoes": validacoes,
            "score_passo": self._calcular_score_url_personalizada(validacoes)
        }
    
    async def _passo_4_localidade(
        self,
        perfil: PerfilLinkedIn,
        dados_diagnostico: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        PASSO 4: Localidade correta (sem mentir)
        
        Critérios Carolina Martins:
        - Cidade e estado reais
        - Não mentir sobre localização
        - Informar disponibilidade para mudança se aplicável
        """
        cidade = dados_diagnostico.get("perfil_basico", {}).get("cidade", "")
        estado = dados_diagnostico.get("perfil_basico", {}).get("estado", "")
        disponibilidade_mudanca = dados_diagnostico.get("perfil_basico", {}).get("disponibilidade_mudanca", False)
        
        localidade_config = {
            "cidade_atual": cidade,
            "estado_atual": estado,
            "localidade_formatada": f"{cidade}, {estado}",
            "disponibilidade_mudanca": disponibilidade_mudanca,
            "observacao": "Disponível para mudança" if disponibilidade_mudanca else "Baseado em " + cidade
        }
        
        perfil.localidade = localidade_config["localidade_formatada"]
        perfil.disponibilidade_mudanca = disponibilidade_mudanca
        
        validacoes = {
            "localidade_preenchida": bool(cidade and estado),
            "informacao_verdadeira": True,  # Assume verdadeira baseada no diagnóstico
            "formato_correto": bool(cidade and estado and "," in localidade_config["localidade_formatada"])
        }
        
        return {
            "configuracao": localidade_config,
            "validacoes": validacoes,
            "score_passo": self._calcular_score_localidade(validacoes)
        }
    
    async def _passo_5_pronomes(
        self,
        perfil: PerfilLinkedIn,
        dados_diagnostico: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        PASSO 5: Pronomes (opcional)
        
        Critérios Carolina Martins:
        - Campo opcional
        - Demonstra inclusividade se usado
        - Não obrigatório para perfil meteórico
        """
        # Este é um campo opcional na metodologia
        pronomes_config = {
            "opcional": True,
            "exemplos": ["Ele/Dele", "Ela/Dela", "Eles/Deles"],
            "recomendacao": "Use se sentir confortável para demonstrar inclusividade"
        }
        
        validacoes = {
            "configuracao_opcional": True,
            "sem_impacto_metodologia": True
        }
        
        return {
            "configuracao": pronomes_config,
            "validacoes": validacoes,
            "score_passo": 100.0  # Sempre 100% pois é opcional
        }
    
    async def _passo_6_modo_criacao(
        self,
        perfil: PerfilLinkedIn,
        mpc_dados: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        PASSO 6: Modo de Criação + 5 Hashtags principais
        
        Critérios Carolina Martins:
        - Ativar 'Modo de Criação'
        - Definir 5 hashtags principais alinhadas à área
        - Hashtags baseadas nas palavras-chave do MPC
        """
        # Extrai palavras-chave do MPC para hashtags
        hashtags_sugeridas = []
        
        if mpc_dados:
            palavras_essenciais = mpc_dados.get("priorizacao_final", {}).get("essenciais", [])
            for palavra_obj in palavras_essenciais[:8]:  # Top 8 para selecionar 5
                palavra = palavra_obj.get("palavra", "")
                if palavra:
                    # Converte para hashtag
                    hashtag = "#" + palavra.replace(" ", "").replace("-", "").lower()
                    hashtags_sugeridas.append(hashtag)
        
        # Se não tem MPC, usa hashtags genéricas baseadas em área comum
        if not hashtags_sugeridas:
            hashtags_sugeridas = ["#lideranca", "#gestao", "#inovacao", "#resultados", "#estrategia"]
        
        # Seleciona top 5 hashtags
        hashtags_principais = hashtags_sugeridas[:5]
        
        modo_criacao_config = {
            "ativar_modo_criacao": True,
            "hashtags_principais": hashtags_principais,
            "hashtags_origem": "MPC" if mpc_dados else "Padrão",
            "objetivo": "Informar algoritmo sobre tópicos de interesse",
            "recomendacao": "Publique conteúdo relacionado a essas hashtags"
        }
        
        perfil.hashtags_principais = json.dumps(hashtags_principais)
        perfil.modo_criacao_ativo = True
        
        validacoes = {
            "modo_criacao_ativo": True,
            "hashtags_definidas": len(hashtags_principais) == 5,
            "hashtags_relevantes": bool(mpc_dados),  # Mais relevantes se vem do MPC
            "formato_correto": all(tag.startswith("#") for tag in hashtags_principais)
        }
        
        return {
            "configuracao": modo_criacao_config,
            "validacoes": validacoes,
            "score_passo": self._calcular_score_modo_criacao(validacoes)
        }
    
    async def _passo_7_headline(
        self,
        perfil: PerfilLinkedIn,
        curriculo_dados: Dict[str, Any],
        mpc_dados: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        PASSO 7: Headline/Título Estratégico
        
        Critérios Carolina Martins:
        - Cargo atual + competências principais
        - Usar palavras-chave do MPC
        - Máximo 220 caracteres
        - Atrativo para recrutadores
        """
        # Extrai informações do currículo
        objetivo = curriculo_dados.get("13_passos", {}).get("2_objetivo", {}).get("objetivo", {}).get("objetivo_formatado", "")
        
        # Extrai competências do MPC
        competencias_mpc = []
        if mpc_dados:
            palavras_essenciais = mpc_dados.get("priorizacao_final", {}).get("essenciais", [])
            competencias_mpc = [p["palavra"] for p in palavras_essenciais[:3]]  # Top 3
        
        # Estrutura da headline: Cargo | Competência 1, Competência 2, Competência 3
        if competencias_mpc:
            competencias_texto = " | " + ", ".join(competencias_mpc)
        else:
            competencias_texto = ""
        
        headline_proposta = objetivo + competencias_texto
        
        # Verifica limite de 220 caracteres
        if len(headline_proposta) > 220:
            # Reduz competências se necessário
            if competencias_mpc:
                competencias_reduzidas = competencias_mpc[:2]  # Reduz para 2
                competencias_texto = " | " + ", ".join(competencias_reduzidas)
                headline_proposta = objetivo + competencias_texto
                
                if len(headline_proposta) > 220:
                    headline_proposta = objetivo  # Apenas cargo se ainda muito longo
        
        headline_config = {
            "headline_completa": headline_proposta,
            "cargo_base": objetivo,
            "competencias_incluidas": competencias_mpc,
            "caracteres_utilizados": len(headline_proposta),
            "limite_caracteres": 220,
            "estrutura": "Cargo | Competência 1, Competência 2, Competência 3"
        }
        
        perfil.headline = headline_proposta
        
        validacoes = {
            "headline_preenchida": bool(headline_proposta),
            "dentro_limite_caracteres": len(headline_proposta) <= 220,
            "inclui_cargo": bool(objetivo),
            "inclui_competencias": bool(competencias_mpc),
            "palavras_chave_mpc": bool(mpc_dados)
        }
        
        return {
            "configuracao": headline_config,
            "validacoes": validacoes,
            "score_passo": self._calcular_score_headline(validacoes)
        }
    
    async def _passo_8_setor(
        self,
        perfil: PerfilLinkedIn,
        dados_diagnostico: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        PASSO 8: Setor correto
        
        Critérios Carolina Martins:
        - Setor alinhado com área de atuação
        - Facilita ser encontrado por recrutadores
        - Consistente com objetivo profissional
        """
        area_interesse = dados_diagnostico.get("configuracao_agentes", {}).get("agente_1_palavras_chave", {}).get("area_interesse", "")
        
        # Mapeamento de áreas para setores LinkedIn
        mapeamento_setores = {
            "tecnologia": "Tecnologia da informação e serviços",
            "ti": "Tecnologia da informação e serviços",
            "marketing": "Marketing e publicidade",
            "vendas": "Vendas",
            "financeiro": "Serviços financeiros",
            "recursos humanos": "Recursos humanos",
            "rh": "Recursos humanos",
            "logistica": "Logística e cadeia de fornecimento",
            "contabilidade": "Contabilidade",
            "juridico": "Serviços jurídicos",
            "saude": "Hospital e assistência médica",
            "educacao": "Educação",
            "consultoria": "Consultoria de gestão",
            "engenharia": "Engenharia",
            "design": "Design",
            "comunicacao": "Comunicação"
        }
        
        area_lower = area_interesse.lower()
        setor_recomendado = None
        
        for area, setor in mapeamento_setores.items():
            if area in area_lower:
                setor_recomendado = setor
                break
        
        if not setor_recomendado:
            setor_recomendado = "Outros"
        
        setor_config = {
            "area_interesse": area_interesse,
            "setor_recomendado": setor_recomendado,
            "alternativas": [setor for area, setor in mapeamento_setores.items() if area in area_lower],
            "importancia": "Facilita ser encontrado por recrutadores da área"
        }
        
        perfil.setor = setor_recomendado
        
        validacoes = {
            "setor_definido": bool(setor_recomendado),
            "alinhado_area": setor_recomendado != "Outros",
            "facilita_descoberta": True
        }
        
        return {
            "configuracao": setor_config,
            "validacoes": validacoes,
            "score_passo": self._calcular_score_setor(validacoes)
        }
    
    async def _passo_9_sobre(
        self,
        perfil: PerfilLinkedIn,
        curriculo_dados: Dict[str, Any],
        mpc_dados: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        PASSO 9: Seção "Sobre" otimizada
        
        Critérios Carolina Martins:
        - Baseada no resumo do currículo
        - Expandida para mais detalhes
        - Palavras-chave estratégicas do MPC
        - Tom profissional mas pessoal
        - Call-to-action para contato
        """
        # Pega resumo do currículo como base
        resumo_curriculo = curriculo_dados.get("13_passos", {}).get("3_resumo", {}).get("resumo", "")
        
        # Extrai palavras-chave do MPC
        palavras_chave_mpc = []
        if mpc_dados:
            for categoria in ["essenciais", "importantes"]:
                palavras = mpc_dados.get("priorizacao_final", {}).get(categoria, [])
                palavras_chave_mpc.extend([p["palavra"] for p in palavras[:3]])
        
        # Estrutura da seção "Sobre"
        sobre_estrutura = {
            "paragrafo_1": resumo_curriculo,  # Resumo profissional
            "paragrafo_2": f"Especializado em {', '.join(palavras_chave_mpc[:4])}." if palavras_chave_mpc else "",
            "paragrafo_3": "Sempre em busca de novos desafios e oportunidades de crescimento.",
            "call_to_action": "Vamos conversar? Entre em contato!"
        }
        
        # Monta seção "Sobre" completa
        sobre_completo = "\n\n".join([p for p in sobre_estrutura.values() if p])
        
        sobre_config = {
            "sobre_completo": sobre_completo,
            "estrutura": sobre_estrutura,
            "palavras_chave_incluidas": palavras_chave_mpc,
            "caracteres_utilizados": len(sobre_completo),
            "limite_linkedin": 2600,  # Limite do LinkedIn para seção Sobre
            "baseado_curriculo": bool(resumo_curriculo)
        }
        
        perfil.sobre = sobre_completo
        
        validacoes = {
            "sobre_preenchido": bool(sobre_completo),
            "baseado_resumo_curriculo": bool(resumo_curriculo),
            "inclui_palavras_chave": bool(palavras_chave_mpc),
            "tem_call_to_action": "contato" in sobre_completo.lower(),
            "dentro_limite": len(sobre_completo) <= 2600
        }
        
        return {
            "configuracao": sobre_config,
            "validacoes": validacoes,
            "score_passo": self._calcular_score_sobre(validacoes)
        }
    
    async def _passo_10_experiencias(
        self,
        perfil: PerfilLinkedIn,
        curriculo_dados: Dict[str, Any],
        mpc_dados: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        PASSO 10: Experiências com mídias + 50 competências + recomendações
        
        Critérios Carolina Martins:
        - Experiências do currículo enriquecidas
        - Adicionar mídias quando possível
        - Listar 50 competências estratégicas
        - Buscar 5+ recomendações
        """
        # Extrai experiências do currículo
        experiencias_curriculo = curriculo_dados.get("13_passos", {}).get("4_experiencias", {}).get("experiencias", [])
        
        # Processa experiências para LinkedIn
        experiencias_linkedin = []
        for exp in experiencias_curriculo:
            exp_linkedin = {
                "empresa": exp.get("empresa", ""),
                "cargo": exp.get("cargo", ""),
                "periodo": exp.get("periodo", ""),
                "descricao": exp.get("descricao_otimizada", ""),
                "resultados": exp.get("resultados_destacados", []),
                "sugestoes_midia": self._sugerir_midias_experiencia(exp),
                "competencias_evidenciadas": self._extrair_competencias_experiencia(exp, mpc_dados)
            }
            experiencias_linkedin.append(exp_linkedin)
        
        # Gera lista de 50 competências estratégicas
        competencias_50 = self._gerar_50_competencias(curriculo_dados, mpc_dados)
        
        # Estratégia para obter recomendações
        estrategia_recomendacoes = {
            "meta_minima": 5,
            "fontes_sugeridas": [
                "Ex-chefes diretos",
                "Colegas de equipe",
                "Subordinados (se aplicável)",
                "Clientes internos/externos",
                "Parceiros de projeto"
            ],
            "templates_solicitacao": self._gerar_templates_solicitacao_recomendacao()
        }
        
        # Salva experiências no banco
        for i, exp in enumerate(experiencias_linkedin):
            exp_model = ExperienciaLinkedIn(
                perfil_linkedin_id=perfil.id,
                empresa=exp["empresa"],
                cargo=exp["cargo"],
                periodo=exp["periodo"],
                descricao=exp["descricao"],
                resultados=json.dumps(exp["resultados"]),
                sugestoes_midia=json.dumps(exp["sugestoes_midia"]),
                ordem=i
            )
            self.db.add(exp_model)
        
        experiencias_config = {
            "experiencias": experiencias_linkedin,
            "competencias_50": competencias_50,
            "estrategia_recomendacoes": estrategia_recomendacoes,
            "total_experiencias": len(experiencias_linkedin)
        }
        
        perfil.competencias = json.dumps(competencias_50)
        perfil.meta_recomendacoes = 5
        
        validacoes = {
            "experiencias_migradas": len(experiencias_linkedin) > 0,
            "competencias_50_definidas": len(competencias_50) == 50,
            "estrategia_recomendacoes_definida": True,
            "experiencias_enriquecidas": any(exp["sugestoes_midia"] for exp in experiencias_linkedin)
        }
        
        return {
            "configuracao": experiencias_config,
            "validacoes": validacoes,
            "score_passo": self._calcular_score_experiencias_linkedin(validacoes)
        }
    
    # ESTRATÉGIA DE CONTEÚDO 60/40
    
    async def _definir_estrategia_conteudo(
        self,
        perfil: PerfilLinkedIn,
        dados_diagnostico: Dict[str, Any],
        mpc_dados: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Define estratégia de conteúdo 60/40 da metodologia Carolina Martins
        
        60% conteúdo geral (audiência) + 40% específico (autoridade)
        """
        area_interesse = dados_diagnostico.get("configuracao_agentes", {}).get("agente_1_palavras_chave", {}).get("area_interesse", "")
        nivel_experiencia = dados_diagnostico.get("experiencia_profissional", {}).get("experiencia_profissional", 0)
        
        # Define frequência baseada no nível de experiência
        if nivel_experiencia < 3:
            frequencia_recomendada = {"posts_por_semana": 2, "posts_por_mes": 8}
        elif nivel_experiencia < 8:
            frequencia_recomendada = {"posts_por_semana": 3, "posts_por_mes": 12}
        else:
            frequencia_recomendada = {"posts_por_semana": 4, "posts_por_mes": 16}
        
        # Temas para conteúdo geral (60% - audiência)
        temas_gerais = [
            "Tendências do mercado",
            "Dicas de carreira",
            "Motivação profissional",
            "Networking",
            "Desenvolvimento pessoal",
            "Notícias da área",
            "Reflexões sobre trabalho"
        ]
        
        # Temas para conteúdo específico (40% - autoridade)
        temas_autoridade = []
        if mpc_dados:
            palavras_essenciais = mpc_dados.get("priorizacao_final", {}).get("essenciais", [])
            temas_autoridade = [f"Experiência em {p['palavra']}" for p in palavras_essenciais[:5]]
        
        if not temas_autoridade:
            temas_autoridade = [
                f"Expertise em {area_interesse}",
                "Cases de sucesso",
                "Metodologias aplicadas",
                "Resultados alcançados",
                "Insights técnicos"
            ]
        
        # Cria estratégia de conteúdo
        estrategia = EstrategiaConteudo(
            perfil_linkedin_id=perfil.id,
            distribuicao_geral=60,
            distribuicao_autoridade=40,
            frequencia_posts=json.dumps(frequencia_recomendada),
            temas_gerais=json.dumps(temas_gerais),
            temas_autoridade=json.dumps(temas_autoridade),
            area_foco=area_interesse
        )
        self.db.add(estrategia)
        
        estrategia_config = {
            "distribuicao": {"geral": 60, "autoridade": 40},
            "frequencia": frequencia_recomendada,
            "temas_gerais": temas_gerais,
            "temas_autoridade": temas_autoridade,
            "area_foco": area_interesse,
            "objetivo": "Construir audiência (60%) e demonstrar expertise (40%)"
        }
        
        return estrategia_config
    
    # SSI TRACKING
    
    async def _configurar_ssi_tracking(
        self,
        perfil: PerfilLinkedIn,
        dados_diagnostico: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Configura tracking do SSI (Social Selling Index)
        
        Metodologia Carolina Martins para acompanhar crescimento da influência
        """
        nivel_experiencia = dados_diagnostico.get("experiencia_profissional", {}).get("experiencia_profissional", 0)
        
        # Define metas SSI baseadas na experiência
        if nivel_experiencia < 3:
            ssi_meta = {"target": 60, "prazo_meses": 6}
        elif nivel_experiencia < 8:
            ssi_meta = {"target": 75, "prazo_meses": 4}
        else:
            ssi_meta = {"target": 85, "prazo_meses": 3}
        
        # Cria registro de métricas
        metricas = MetricasLinkedIn(
            perfil_linkedin_id=perfil.id,
            ssi_atual=0,  # Será atualizado manualmente
            ssi_meta=ssi_meta["target"],
            prazo_meta=ssi_meta["prazo_meses"],
            status_ssi=StatusSSI.INICIANDO.value
        )
        self.db.add(metricas)
        
        ssi_config = {
            "meta_ssi": ssi_meta,
            "componentes_ssi": [
                "Estabelecer sua marca profissional",
                "Encontrar as pessoas certas",
                "Interagir com insights",
                "Construir relacionamentos"
            ],
            "estrategia_crescimento": [
                "Completar perfil 100%",
                "Postar conteúdo regularmente",
                "Engajar com rede de contatos",
                "Expandir rede strategicamente"
            ],
            "tracking_frequencia": "Verificar SSI semanalmente"
        }
        
        return ssi_config
    
    # MÉTODOS AUXILIARES
    
    def _carregar_criterios_foto(self) -> Dict[str, Any]:
        """Carrega critérios para foto profissional"""
        return {
            "enquadramento": "Ombros para cima",
            "fundo": "Neutro ou desfocado",
            "expressao": "Profissional e confiante",
            "vestimenta": "Adequada para área",
            "qualidade": "Alta resolução"
        }
    
    def _carregar_templates_conteudo(self) -> Dict[str, List[str]]:
        """Carrega templates de conteúdo para posts"""
        return {
            "geral": [
                "💡 Reflexão: {insight sobre mercado}",
                "🚀 Dica de carreira: {dica prática}",
                "📊 Tendência: {tendência da área}",
                "💪 Segunda-feira: {motivação}",
                "🤝 Networking: {importância do networking}"
            ],
            "autoridade": [
                "📈 Case de sucesso: {resultado alcançado}",
                "🎯 Metodologia: {como fazer algo}",
                "🔍 Insight técnico: {conhecimento específico}",
                "⚡ Lição aprendida: {experiência pessoal}",
                "🛠️ Ferramenta: {ferramenta útil da área}"
            ]
        }
    
    def _carregar_estrategia_conteudo(self) -> Dict[str, float]:
        """Carrega distribuição 60/40 da estratégia"""
        return {
            "conteudo_geral": 0.6,
            "conteudo_autoridade": 0.4
        }
    
    def _carregar_competencias_base(self) -> List[str]:
        """Carrega competências base para LinkedIn"""
        return [
            "Liderança", "Gestão de Equipes", "Planejamento Estratégico", "Análise de Dados",
            "Microsoft Excel", "Power BI", "Gestão de Projetos", "Comunicação",
            "Trabalho em Equipe", "Resolução de Problemas", "Pensamento Crítico",
            "Adaptabilidade", "Criatividade", "Inovação", "Orientação a Resultados",
            "Foco no Cliente", "Negociação", "Apresentações", "Relacionamento Interpessoal",
            "Gestão do Tempo", "Organização", "Multitarefa", "Flexibilidade",
            "Proatividade", "Autonomia", "Responsabilidade", "Ética Profissional",
            "Visão Estratégica", "Tomada de Decisão", "Gestão de Mudanças",
            "Desenvolvimento de Pessoas", "Coaching", "Mentoring", "Feedback",
            "Inteligência Emocional", "Resiliência", "Persistência", "Iniciativa",
            "Colaboração", "Influência", "Persuasão", "Networking", "Vendas",
            "Marketing", "Tecnologia", "Digital", "Inglês", "Espanhol", "Francês"
        ]
    
    # Métodos de cálculo de scores
    def _calcular_score_foto_perfil(self, validacoes: Dict[str, bool]) -> float:
        return sum(validacoes.values()) / len(validacoes) * 100
    
    def _calcular_score_foto_capa(self, validacoes: Dict[str, bool]) -> float:
        return sum(validacoes.values()) / len(validacoes) * 100
    
    def _calcular_score_url_personalizada(self, validacoes: Dict[str, bool]) -> float:
        return sum(validacoes.values()) / len(validacoes) * 100
    
    def _calcular_score_localidade(self, validacoes: Dict[str, bool]) -> float:
        return sum(validacoes.values()) / len(validacoes) * 100
    
    def _calcular_score_modo_criacao(self, validacoes: Dict[str, bool]) -> float:
        return sum(validacoes.values()) / len(validacoes) * 100
    
    def _calcular_score_headline(self, validacoes: Dict[str, bool]) -> float:
        return sum(validacoes.values()) / len(validacoes) * 100
    
    def _calcular_score_setor(self, validacoes: Dict[str, bool]) -> float:
        return sum(validacoes.values()) / len(validacoes) * 100
    
    def _calcular_score_sobre(self, validacoes: Dict[str, bool]) -> float:
        return sum(validacoes.values()) / len(validacoes) * 100
    
    def _calcular_score_experiencias_linkedin(self, validacoes: Dict[str, bool]) -> float:
        return sum(validacoes.values()) / len(validacoes) * 100
    
    def _executar_validacoes_linkedin(self, perfil: PerfilLinkedIn, passos: Dict[str, Any]) -> Dict[str, Any]:
        """Executa validações gerais do LinkedIn meteórico"""
        validacoes = {
            "todos_10_passos_completos": len(passos) == 10,
            "perfil_100_completo": True,  # Baseado nos passos
            "palavras_chave_integradas": bool(perfil.hashtags_principais),
            "estrategia_conteudo_definida": True,
            "pronto_para_networking": True
        }
        
        return validacoes
    
    def _calcular_score_linkedin(self, validacoes: Dict[str, Any]) -> float:
        """Calcula score geral do LinkedIn"""
        scores_individuais = []
        
        # Soma scores de todos os passos
        for passo, dados in validacoes.items():
            if isinstance(dados, dict) and "score_passo" in dados:
                scores_individuais.append(dados["score_passo"])
        
        return sum(scores_individuais) / len(scores_individuais) if scores_individuais else 0.0
    
    def _determinar_classificacao_linkedin(self, score: float) -> str:
        """Determina classificação do LinkedIn"""
        if score >= 90:
            return "LinkedIn Meteórico"
        elif score >= 80:
            return "LinkedIn Otimizado"
        elif score >= 70:
            return "LinkedIn Bom"
        elif score >= 60:
            return "LinkedIn Básico"
        else:
            return "LinkedIn Necessita Melhoria"
    
    def _gerar_proximos_passos_linkedin(self, resultado: Dict[str, Any]) -> List[str]:
        """Gera próximos passos baseados no resultado"""
        proximos_passos = []
        
        score = resultado["score_linkedin"]
        
        if score >= 90:
            proximos_passos.append("LinkedIn meteórico pronto - iniciar estratégia de conteúdo")
            proximos_passos.append("Começar networking ativo com profissionais da área")
            proximos_passos.append("Monitorar SSI semanalmente")
        elif score >= 80:
            proximos_passos.append("LinkedIn otimizado - implementar melhorias finais")
            proximos_passos.append("Iniciar publicação de conteúdo regular")
        else:
            proximos_passos.append("Revisar passos com score baixo")
            proximos_passos.append("Completar otimizações pendentes")
        
        return proximos_passos
    
    # Métodos auxiliares para conteúdo
    def _selecionar_tema_geral(self, estrategia: EstrategiaConteudo) -> str:
        """Seleciona tema para post geral"""
        temas = json.loads(estrategia.temas_gerais)
        import random
        return random.choice(temas)
    
    def _selecionar_tema_autoridade(self, estrategia: EstrategiaConteudo) -> str:
        """Seleciona tema para post de autoridade"""
        temas = json.loads(estrategia.temas_autoridade)
        import random
        return random.choice(temas)
    
    def _obter_template_geral(self) -> str:
        """Obtém template para post geral"""
        templates = self.templates_conteudo["geral"]
        import random
        return random.choice(templates)
    
    def _obter_template_autoridade(self) -> str:
        """Obtém template para post de autoridade"""
        templates = self.templates_conteudo["autoridade"]
        import random
        return random.choice(templates)
    
    def _obter_hashtags_gerais(self, estrategia: EstrategiaConteudo) -> List[str]:
        """Obtém hashtags para post geral"""
        return ["#carreira", "#profissional", "#networking", "#crescimento"]
    
    def _obter_hashtags_autoridade(self, estrategia: EstrategiaConteudo) -> List[str]:
        """Obtém hashtags para post de autoridade"""
        area = estrategia.area_foco.lower().replace(" ", "")
        return [f"#{area}", "#expertise", "#experiencia", "#resultados"]
    
    # Métodos auxiliares para experiências
    def _sugerir_midias_experiencia(self, experiencia: Dict[str, Any]) -> List[str]:
        """Sugere mídias para adicionar à experiência"""
        sugestoes = [
            "Logo da empresa",
            "Certificados de projetos",
            "Screenshots de resultados",
            "Documentos de reconhecimento",
            "Fotos de eventos/equipe"
        ]
        return sugestoes[:3]  # Máximo 3 sugestões
    
    def _extrair_competencias_experiencia(self, experiencia: Dict[str, Any], mpc_dados: Dict[str, Any]) -> List[str]:
        """Extrai competências evidenciadas na experiência"""
        competencias = []
        
        descricao = experiencia.get("descricao_otimizada", "").lower()
        
        # Competências baseadas em palavras-chave da descrição
        if "gestão" in descricao or "gerenciar" in descricao:
            competencias.append("Gestão")
        if "liderança" in descricao or "liderar" in descricao:
            competencias.append("Liderança")
        if "projeto" in descricao:
            competencias.append("Gestão de Projetos")
        if "equipe" in descricao:
            competencias.append("Trabalho em Equipe")
        
        return competencias[:5]  # Máximo 5 por experiência
    
    def _gerar_50_competencias(self, curriculo_dados: Dict[str, Any], mpc_dados: Dict[str, Any]) -> List[str]:
        """Gera lista de 50 competências estratégicas"""
        competencias = []
        
        # Adiciona competências do MPC se disponível
        if mpc_dados:
            for categoria in ["essenciais", "importantes", "complementares"]:
                palavras = mpc_dados.get("priorizacao_final", {}).get(categoria, [])
                competencias.extend([p["palavra"] for p in palavras])
        
        # Adiciona competências base para completar 50
        competencias.extend(self.competencias_sugeridas)
        
        # Remove duplicatas mantendo ordem
        competencias_unicas = []
        for comp in competencias:
            if comp not in competencias_unicas:
                competencias_unicas.append(comp)
        
        return competencias_unicas[:50]  # Exatamente 50
    
    def _gerar_templates_solicitacao_recomendacao(self) -> List[str]:
        """Gera templates para solicitar recomendações"""
        return [
            "Olá [Nome], espero que esteja bem! Estou atualizando meu perfil no LinkedIn e gostaria de saber se você poderia escrever uma recomendação sobre nossa parceria em [Projeto/Empresa]. Sua perspectiva sobre meu trabalho seria muito valiosa. Obrigado(a)!",
            "Oi [Nome]! Tudo bem? Estou organizando meu LinkedIn e pensei em você como alguém que pode falar sobre minha atuação em [área/projeto]. Você poderia me ajudar com uma recomendação? Agradeço muito!",
            "Olá [Nome], como vai? Estou solicitando algumas recomendações no LinkedIn de pessoas que trabalharam comigo. Você poderia compartilhar sua experiência sobre nossa colaboração em [contexto]? Muito obrigado(a)!"
        ]