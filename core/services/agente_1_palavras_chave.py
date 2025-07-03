"""
Agente 1: Extração de Palavras-chave (MPC) - Metodologia Carolina Martins

Este agente implementa a Ferramenta MPC (Mapa de Palavras-Chave) mencionada
em múltiplas aulas como pré-requisito para o currículo meteórico.

Processo baseado nas transcrições:
1. Coleta de 50-100 vagas relevantes da área
2. Extração automática de palavras-chave
3. Categorização (comportamental, técnica, digital)
4. Validação no ChatGPT (mencionado na Aula 6)
5. Priorização por frequência
6. Output: Guia estruturado para aplicar no currículo
"""

import re
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from collections import Counter, defaultdict
from sqlalchemy.orm import Session
from core.models import (
    MapaPalavrasChave, VagaAnalisada, PalavraChave, 
    ProcessamentoMPC, ValidacaoIA, StatusMPC, CategoriaPalavraChave
)

class MPCCarolinaMartins:
    """
    Implementação da Ferramenta MPC (Mapa de Palavras-Chave)
    baseada na metodologia Carolina Martins
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.palavras_base = self._carregar_palavras_base()
        self.stop_words = self._carregar_stop_words()
        self.padroes_limpeza = self._configurar_padroes_limpeza()
    
    async def executar_mpc_completo(
        self, 
        area_interesse: str, 
        cargo_objetivo: str,
        segmentos_alvo: List[str] = None,
        usuario_id: int = None
    ) -> Dict[str, Any]:
        """
        Executa processo MPC completo seguindo metodologia Carolina Martins
        
        Etapas:
        1. Configuração inicial
        2. Coleta de vagas
        3. Extração de palavras-chave
        4. Categorização automática
        5. Validação com IA
        6. Priorização final
        """
        # Cria registro MPC
        mpc = MapaPalavrasChave(
            usuario_id=usuario_id,
            area_interesse=area_interesse,
            cargo_objetivo=cargo_objetivo,
            segmentos_alvo=segmentos_alvo or [],
            status=StatusMPC.COLETANDO.value
        )
        self.db.add(mpc)
        self.db.commit()
        
        resultado = {
            "mpc_id": mpc.id,
            "configuracao": {
                "area_interesse": area_interesse,
                "cargo_objetivo": cargo_objetivo,
                "segmentos_alvo": segmentos_alvo,
                "meta_vagas": 100
            },
            "coleta_vagas": {},
            "extracao_palavras": {},
            "categorizacao": {},
            "validacao_ia": {},
            "priorizacao_final": {},
            "mpc_final": {}
        }
        
        try:
            # Etapa 1: Coleta de vagas
            mpc.status = StatusMPC.COLETANDO.value
            self.db.commit()
            
            resultado["coleta_vagas"] = await self._coletar_vagas(
                mpc, area_interesse, cargo_objetivo, segmentos_alvo
            )
            
            # Etapa 2: Extração de palavras-chave
            mpc.status = StatusMPC.PROCESSANDO.value
            self.db.commit()
            
            resultado["extracao_palavras"] = await self._extrair_palavras_chave(mpc)
            
            # Etapa 3: Categorização
            resultado["categorizacao"] = await self._categorizar_palavras_chave(mpc)
            
            # Etapa 4: Validação com IA
            resultado["validacao_ia"] = await self._validar_com_ia(mpc, area_interesse, cargo_objetivo)
            
            # Etapa 5: Priorização final
            resultado["priorizacao_final"] = await self._priorizar_palavras_chave(mpc)
            
            # Etapa 6: Consolidação do MPC
            resultado["mpc_final"] = self._consolidar_mpc(mpc)
            
            # Finaliza processo
            mpc.status = StatusMPC.CONCLUIDO.value
            mpc.data_ultima_coleta = datetime.utcnow()
            self.db.commit()
            
            return resultado
            
        except Exception as e:
            mpc.status = StatusMPC.ERRO.value
            self.db.commit()
            
            # Log do erro
            log_erro = ProcessamentoMPC(
                mpc_id=mpc.id,
                etapa="execucao_completa",
                status="erro",
                erro=str(e)
            )
            self.db.add(log_erro)
            self.db.commit()
            
            raise e
    
    async def _coletar_vagas(
        self, 
        mpc: MapaPalavrasChave, 
        area: str, 
        cargo: str, 
        segmentos: List[str]
    ) -> Dict[str, Any]:
        """
        Coleta vagas de múltiplas fontes para análise
        
        Objetivo Carolina Martins: 50-100 vagas relevantes
        """
        log_coleta = ProcessamentoMPC(
            mpc_id=mpc.id,
            etapa="coleta_vagas",
            status="executando"
        )
        self.db.add(log_coleta)
        self.db.commit()
        
        vagas_coletadas = []
        fontes_utilizadas = ["linkedin", "indeed", "catho", "infojobs"]
        
        # Simula coleta de vagas (integração real seria implementada)
        for fonte in fontes_utilizadas:
            vagas_fonte = await self._coletar_vagas_fonte(fonte, area, cargo, segmentos)
            vagas_coletadas.extend(vagas_fonte)
        
        # Salva vagas no banco
        total_salvas = 0
        for vaga_data in vagas_coletadas:
            vaga = VagaAnalisada(
                mpc_id=mpc.id,
                titulo=vaga_data["titulo"],
                empresa=vaga_data.get("empresa", ""),
                localizacao=vaga_data.get("localizacao", ""),
                descricao=vaga_data.get("descricao", ""),
                requisitos=vaga_data.get("requisitos", ""),
                fonte=vaga_data.get("fonte", ""),
                url_original=vaga_data.get("url", "")
            )
            self.db.add(vaga)
            total_salvas += 1
        
        self.db.commit()
        
        # Atualiza estatísticas do MPC
        mpc.total_vagas_coletadas = total_salvas
        self.db.commit()
        
        # Atualiza log
        log_coleta.status = "concluido"
        log_coleta.vagas_processadas = total_salvas
        self.db.commit()
        
        return {
            "total_coletadas": total_salvas,
            "fontes_utilizadas": fontes_utilizadas,
            "meta_atingida": total_salvas >= 50,
            "qualidade_coleta": "boa" if total_salvas >= 100 else "adequada" if total_salvas >= 50 else "insuficiente"
        }
    
    async def _coletar_vagas_fonte(
        self, 
        fonte: str, 
        area: str, 
        cargo: str, 
        segmentos: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Simula coleta de vagas de uma fonte específica
        Na implementação real, seria integração com APIs/scraping
        """
        # Dados simulados baseados na metodologia
        vagas_simuladas = [
            {
                "titulo": f"{cargo} - {area}",
                "empresa": f"Empresa {i}",
                "localizacao": "São Paulo, SP",
                "descricao": f"Oportunidade para atuar como {cargo} na área de {area}. Buscamos profissional com experiência em gestão de projetos, liderança de equipe e conhecimento em Excel avançado.",
                "requisitos": "Superior completo, experiência mínima de 3 anos, Excel avançado, inglês intermediário, gestão de projetos",
                "fonte": fonte,
                "url": f"https://{fonte}.com/vaga-{i}"
            }
            for i in range(1, 26)  # 25 vagas por fonte
        ]
        
        return vagas_simuladas
    
    async def _extrair_palavras_chave(self, mpc: MapaPalavrasChave) -> Dict[str, Any]:
        """
        Extrai palavras-chave de todas as vagas coletadas
        
        Processo Carolina Martins:
        1. Análise de descrições e requisitos
        2. Limpeza e normalização
        3. Contagem de frequência
        4. Identificação de padrões
        """
        log_extracao = ProcessamentoMPC(
            mpc_id=mpc.id,
            etapa="extracao_palavras",
            status="executando"
        )
        self.db.add(log_extracao)
        self.db.commit()
        
        # Busca todas as vagas do MPC
        vagas = self.db.query(VagaAnalisada).filter(VagaAnalisada.mpc_id == mpc.id).all()
        
        todas_palavras = []
        vagas_processadas = 0
        
        for vaga in vagas:
            # Combina descrição e requisitos
            texto_completo = f"{vaga.descricao} {vaga.requisitos}".lower()
            
            # Extrai palavras-chave
            palavras_vaga = self._extrair_palavras_texto(texto_completo)
            
            # Salva palavras da vaga
            vaga.palavras_extraidas = palavras_vaga
            vaga.processada = True
            
            todas_palavras.extend(palavras_vaga)
            vagas_processadas += 1
        
        self.db.commit()
        
        # Conta frequências
        contador_palavras = Counter(todas_palavras)
        total_palavras_unicas = len(contador_palavras)
        
        # Atualiza MPC
        mpc.total_palavras_extraidas = total_palavras_unicas
        self.db.commit()
        
        # Atualiza log
        log_extracao.status = "concluido"
        log_extracao.vagas_processadas = vagas_processadas
        log_extracao.palavras_encontradas = total_palavras_unicas
        self.db.commit()
        
        return {
            "vagas_processadas": vagas_processadas,
            "palavras_unicas": total_palavras_unicas,
            "palavras_mais_frequentes": contador_palavras.most_common(20),
            "qualidade_extracao": self._avaliar_qualidade_extracao(contador_palavras)
        }
    
    def _extrair_palavras_texto(self, texto: str) -> List[str]:
        """
        Extrai palavras-chave relevantes de um texto
        
        Aplica:
        - Limpeza de caracteres especiais
        - Remoção de stop words
        - Identificação de termos compostos
        - Normalização
        """
        # Limpeza inicial
        texto = re.sub(r'[^\w\s]', ' ', texto)
        texto = re.sub(r'\s+', ' ', texto).strip()
        
        # Identifica termos compostos primeiro
        termos_compostos = self._identificar_termos_compostos(texto)
        
        # Extrai palavras individuais
        palavras = [
            palavra.strip() 
            for palavra in texto.split()
            if len(palavra.strip()) > 2 
            and palavra.strip().lower() not in self.stop_words
        ]
        
        # Combina termos compostos e palavras individuais
        todas_palavras = termos_compostos + palavras
        
        # Remove duplicatas e normaliza
        palavras_normalizadas = list(set([
            self._normalizar_palavra(palavra)
            for palavra in todas_palavras
            if self._e_palavra_relevante(palavra)
        ]))
        
        return palavras_normalizadas
    
    def _identificar_termos_compostos(self, texto: str) -> List[str]:
        """
        Identifica termos compostos relevantes para área profissional
        Ex: "gestão de projetos", "excel avançado", "power bi"
        """
        termos_compostos = []
        
        # Padrões de termos compostos conhecidos
        padroes_compostos = [
            r'excel\s+(avançado|intermediário|básico)',
            r'power\s+bi',
            r'gestão\s+de\s+(projetos|equipe|pessoas|processos)',
            r'análise\s+de\s+(dados|negócio|mercado)',
            r'controle\s+de\s+(qualidade|estoque|custos)',
            r'planejamento\s+(estratégico|financeiro|operacional)',
            r'relacionamento\s+com\s+cliente',
            r'trabalho\s+em\s+equipe',
            r'tomada\s+de\s+decisão',
            r'resolução\s+de\s+(problemas|conflitos)',
            r'comunicação\s+(oral|escrita|interpessoal)',
            r'pensamento\s+(analítico|crítico|estratégico)'
        ]
        
        for padrao in padroes_compostos:
            matches = re.findall(padrao, texto, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    termo_completo = re.search(padrao, texto, re.IGNORECASE).group()
                else:
                    termo_completo = match
                termos_compostos.append(termo_completo.lower().strip())
        
        return list(set(termos_compostos))
    
    def _normalizar_palavra(self, palavra: str) -> str:
        """Normaliza palavra removendo acentos e padronizando"""
        import unicodedata
        
        # Remove acentos
        palavra = unicodedata.normalize('NFD', palavra).encode('ascii', 'ignore').decode('ascii')
        
        # Converte para minúsculo
        palavra = palavra.lower().strip()
        
        # Aplica normalizações específicas
        normalizacoes = {
            'excel': 'excel',
            'powerbi': 'power bi',
            'power-bi': 'power bi',
            'sql': 'sql',
            'crm': 'crm',
            'erp': 'erp',
            'sap': 'sap',
            'lideranca': 'liderança',
            'gestao': 'gestão',
            'analise': 'análise'
        }
        
        return normalizacoes.get(palavra, palavra)
    
    def _e_palavra_relevante(self, palavra: str) -> bool:
        """Verifica se palavra é relevante para contexto profissional"""
        # Filtros de relevância
        if len(palavra) < 3:
            return False
        
        if palavra.lower() in self.stop_words:
            return False
        
        # Palavras irrelevantes específicas
        irrelevantes = [
            'empresa', 'oportunidade', 'vaga', 'profissional', 'area',
            'conhecimento', 'experiencia', 'habilidade', 'competencia',
            'requisito', 'diferencial', 'atividade', 'responsabilidade'
        ]
        
        if palavra.lower() in irrelevantes:
            return False
        
        return True
    
    async def _categorizar_palavras_chave(self, mpc: MapaPalavrasChave) -> Dict[str, Any]:
        """
        Categoriza palavras-chave em: Comportamental, Técnica, Digital
        baseado na metodologia Carolina Martins
        """
        # Busca todas as palavras extraídas
        vagas = self.db.query(VagaAnalisada).filter(VagaAnalisada.mpc_id == mpc.id).all()
        
        # Coleta todas as palavras com frequência
        contador_geral = Counter()
        for vaga in vagas:
            if vaga.palavras_extraidas:
                contador_geral.update(vaga.palavras_extraidas)
        
        # Categoriza cada palavra
        palavras_categorizadas = {
            "comportamental": [],
            "tecnica": [],
            "digital": []
        }
        
        for palavra, frequencia in contador_geral.items():
            categoria = self._determinar_categoria_palavra(palavra)
            
            # Calcula frequência relativa
            freq_relativa = frequencia / mpc.total_vagas_coletadas
            
            # Cria registro de palavra-chave
            palavra_obj = PalavraChave(
                mpc_id=mpc.id,
                termo=palavra,
                categoria=categoria,
                frequencia_absoluta=frequencia,
                frequencia_relativa=freq_relativa,
                importancia=self._calcular_importancia_palavra(palavra, categoria, freq_relativa)
            )
            self.db.add(palavra_obj)
            
            # Adiciona à categoria correspondente
            palavras_categorizadas[categoria].append({
                "termo": palavra,
                "frequencia_absoluta": frequencia,
                "frequencia_relativa": freq_relativa,
                "importancia": palavra_obj.importancia
            })
        
        self.db.commit()
        
        # Ordena por importância
        for categoria in palavras_categorizadas:
            palavras_categorizadas[categoria].sort(
                key=lambda x: x["importancia"], 
                reverse=True
            )
        
        return {
            "total_por_categoria": {
                cat: len(palavras) for cat, palavras in palavras_categorizadas.items()
            },
            "palavras_categorizadas": palavras_categorizadas,
            "qualidade_categorizacao": self._avaliar_qualidade_categorizacao(palavras_categorizadas)
        }
    
    def _determinar_categoria_palavra(self, palavra: str) -> str:
        """
        Determina categoria da palavra baseado na metodologia Carolina Martins
        
        Categorias:
        - Comportamental: soft skills, competências interpessoais
        - Técnica: conhecimentos específicos da área
        - Digital: ferramentas, softwares, tecnologias
        """
        palavra_lower = palavra.lower()
        
        # Palavras digitais/tecnológicas
        if any(tech in palavra_lower for tech in [
            'excel', 'power bi', 'sql', 'python', 'java', 'sap', 'oracle',
            'crm', 'erp', 'tableau', 'autocad', 'photoshop', 'word',
            'powerpoint', 'access', 'outlook', 'teams', 'slack',
            'jira', 'confluence', 'git', 'agile', 'scrum', 'kanban'
        ]):
            return CategoriaPalavraChave.DIGITAL.value
        
        # Palavras comportamentais
        if any(comp in palavra_lower for comp in [
            'liderança', 'comunicação', 'trabalho em equipe', 'proatividade',
            'organização', 'planejamento', 'negociação', 'relacionamento',
            'criatividade', 'inovação', 'adaptabilidade', 'flexibilidade',
            'responsabilidade', 'comprometimento', 'iniciativa', 'empatia',
            'colaboração', 'motivação', 'persuasão', 'networking'
        ]):
            return CategoriaPalavraChave.COMPORTAMENTAL.value
        
        # Palavras técnicas (padrão)
        return CategoriaPalavraChave.TECNICA.value
    
    def _calcular_importancia_palavra(
        self, 
        palavra: str, 
        categoria: str, 
        freq_relativa: float
    ) -> float:
        """
        Calcula importância da palavra baseado em múltiplos fatores
        
        Fatores:
        - Frequência relativa (50%)
        - Categoria (20%) - digitais têm peso maior
        - Especificidade (20%) - termos mais específicos têm peso maior
        - Tamanho (10%) - termos compostos têm peso maior
        """
        score = freq_relativa * 0.5
        
        # Peso por categoria
        if categoria == CategoriaPalavraChave.DIGITAL.value:
            score += 0.2
        elif categoria == CategoriaPalavraChave.COMPORTAMENTAL.value:
            score += 0.15
        else:  # técnica
            score += 0.1
        
        # Peso por especificidade (termos compostos são mais específicos)
        if ' ' in palavra:  # termo composto
            score += 0.2
        elif len(palavra) > 8:  # palavra longa/específica
            score += 0.15
        else:
            score += 0.1
        
        # Peso por tamanho
        if len(palavra.split()) > 1:  # termo composto
            score += 0.1
        elif len(palavra) > 6:
            score += 0.08
        else:
            score += 0.05
        
        return min(score, 1.0)
    
    async def _validar_com_ia(
        self, 
        mpc: MapaPalavrasChave, 
        area_interesse: str, 
        cargo_objetivo: str
    ) -> Dict[str, Any]:
        """
        Valida palavras-chave com IA seguindo menção da Aula 6
        "Validação no ChatGPT"
        """
        # Busca top palavras por categoria
        palavras_top = self.db.query(PalavraChave)\
            .filter(PalavraChave.mpc_id == mpc.id)\
            .order_by(PalavraChave.importancia.desc())\
            .limit(50)\
            .all()
        
        # Prepara dados para validação
        palavras_por_categoria = defaultdict(list)
        for palavra in palavras_top:
            palavras_por_categoria[palavra.categoria].append(palavra.termo)
        
        # Simula validação com IA (integração real seria implementada)
        validacao_resultado = await self._simular_validacao_ia(
            palavras_por_categoria, area_interesse, cargo_objetivo
        )
        
        # Salva resultado da validação
        validacao_ia = ValidacaoIA(
            mpc_id=mpc.id,
            modelo_ia="gpt-4",
            prompt_utilizado=validacao_resultado["prompt_usado"],
            palavras_aprovadas=validacao_resultado["aprovadas"],
            palavras_rejeitadas=validacao_resultado["rejeitadas"],
            sugestoes_adicionais=validacao_resultado["sugestoes"],
            confianca=validacao_resultado["confianca"]
        )
        self.db.add(validacao_ia)
        
        # Marca palavras como validadas
        for palavra in palavras_top:
            if palavra.termo in validacao_resultado["aprovadas"]:
                palavra.validada_ia = True
                palavra.recomendada_ia = True
            elif palavra.termo in validacao_resultado["rejeitadas"]:
                palavra.validada_ia = True
                palavra.recomendada_ia = False
        
        # Marca MPC como validado
        mpc.validado_ia = True
        mpc.sugestoes_ia = validacao_resultado["sugestoes"]
        
        self.db.commit()
        
        return validacao_resultado
    
    async def _simular_validacao_ia(
        self, 
        palavras_por_categoria: Dict[str, List[str]], 
        area: str, 
        cargo: str
    ) -> Dict[str, Any]:
        """
        Simula validação com IA
        Na implementação real, seria chamada para API do ChatGPT/Claude
        """
        prompt = f"""
        Analise as seguintes palavras-chave extraídas para a posição de {cargo} na área de {area}.
        
        Comportamentais: {palavras_por_categoria.get('comportamental', [])}
        Técnicas: {palavras_por_categoria.get('tecnica', [])}
        Digitais: {palavras_por_categoria.get('digital', [])}
        
        Valide quais são relevantes e sugira melhorias.
        """
        
        # Simulação de resultado
        todas_palavras = []
        for palavras in palavras_por_categoria.values():
            todas_palavras.extend(palavras)
        
        # 80% aprovadas, 20% rejeitadas
        total = len(todas_palavras)
        aprovadas = todas_palavras[:int(total * 0.8)]
        rejeitadas = todas_palavras[int(total * 0.8):]
        
        sugestoes = [
            "Incluir 'Excel avançado' se não estiver presente",
            "Considerar adicionar competências de comunicação",
            "Verificar se 'gestão de projetos' é relevante para o cargo"
        ]
        
        return {
            "prompt_usado": prompt,
            "aprovadas": aprovadas,
            "rejeitadas": rejeitadas,
            "sugestoes": sugestoes,
            "confianca": 0.85
        }
    
    async def _priorizar_palavras_chave(self, mpc: MapaPalavrasChave) -> Dict[str, Any]:
        """
        Prioriza palavras-chave seguindo critério Carolina Martins
        
        Priorização:
        - Essenciais: aparecem em 70%+ das vagas
        - Importantes: aparecem em 40-69% das vagas  
        - Complementares: aparecem em menos de 40%
        """
        palavras = self.db.query(PalavraChave)\
            .filter(PalavraChave.mpc_id == mpc.id)\
            .filter(PalavraChave.validada_ia == True)\
            .filter(PalavraChave.recomendada_ia == True)\
            .all()
        
        priorizacao = {
            "essenciais": [],
            "importantes": [],
            "complementares": []
        }
        
        for palavra in palavras:
            freq = palavra.frequencia_relativa
            
            item = {
                "termo": palavra.termo,
                "categoria": palavra.categoria,
                "frequencia": freq,
                "importancia": palavra.importancia
            }
            
            if freq >= 0.7:
                priorizacao["essenciais"].append(item)
            elif freq >= 0.4:
                priorizacao["importantes"].append(item)
            else:
                priorizacao["complementares"].append(item)
        
        # Ordena cada categoria por importância
        for categoria in priorizacao:
            priorizacao[categoria].sort(key=lambda x: x["importancia"], reverse=True)
        
        # Salva no MPC
        mpc.palavras_chave_priorizadas = {
            "por_prioridade": priorizacao,
            "por_categoria": self._organizar_por_categoria(palavras)
        }
        self.db.commit()
        
        return {
            "priorizacao": priorizacao,
            "total_essenciais": len(priorizacao["essenciais"]),
            "total_importantes": len(priorizacao["importantes"]),
            "total_complementares": len(priorizacao["complementares"]),
            "recomendacao_uso": self._gerar_recomendacao_uso(priorizacao)
        }
    
    def _consolidar_mpc(self, mpc: MapaPalavrasChave) -> Dict[str, Any]:
        """
        Consolida MPC final com todas as informações
        Output: Guia estruturado para aplicar no currículo
        """
        # Calcula score de qualidade
        score_qualidade = mpc.calcular_score_qualidade()
        
        # Busca dados para consolidação
        priorizacao = mpc.palavras_chave_priorizadas.get("por_prioridade", {})
        
        mpc_final = {
            "id": mpc.id,
            "configuracao": {
                "area_interesse": mpc.area_interesse,
                "cargo_objetivo": mpc.cargo_objetivo,
                "segmentos_alvo": mpc.segmentos_alvo
            },
            "estatisticas": {
                "total_vagas_analisadas": mpc.total_vagas_coletadas,
                "total_palavras_extraidas": mpc.total_palavras_extraidas,
                "score_qualidade": score_qualidade,
                "validado_ia": mpc.validado_ia
            },
            "palavras_essenciais": priorizacao.get("essenciais", [])[:10],
            "palavras_importantes": priorizacao.get("importantes", [])[:15],
            "palavras_complementares": priorizacao.get("complementares", [])[:20],
            "guia_aplicacao": self._gerar_guia_aplicacao(priorizacao),
            "recomendacoes": self._gerar_recomendacoes_finais(mpc, score_qualidade)
        }
        
        return mpc_final
    
    def _gerar_guia_aplicacao(self, priorizacao: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """
        Gera guia prático para aplicar palavras-chave no currículo
        baseado na metodologia Carolina Martins
        """
        essenciais = priorizacao.get("essenciais", [])
        importantes = priorizacao.get("importantes", [])
        
        return {
            "resumo_profissional": {
                "incluir_obrigatoriamente": [p["termo"] for p in essenciais[:5]],
                "incluir_preferencialmente": [p["termo"] for p in importantes[:3]],
                "instrucoes": "Use estas palavras-chave no resumo de forma natural"
            },
            "experiencias_profissionais": {
                "distribuir_por_experiencia": [p["termo"] for p in essenciais + importantes[:5]],
                "instrucoes": "Distribua as palavras-chave nas descrições das experiências"
            },
            "competencias": {
                "listar_explicitamente": [p["termo"] for p in essenciais if p["categoria"] == "digital"],
                "instrucoes": "Liste competências digitais/técnicas explicitamente"
            },
            "personalizacao": {
                "palavras_vaga_especifica": "Use palavras-chave exatas da job description",
                "instrucoes": "Sempre personalize com palavras-chave específicas da vaga"
            }
        }
    
    def _gerar_recomendacoes_finais(
        self, 
        mpc: MapaPalavrasChave, 
        score_qualidade: float
    ) -> List[str]:
        """Gera recomendações finais baseadas na qualidade do MPC"""
        recomendacoes = []
        
        if score_qualidade >= 80:
            recomendacoes.append("MPC de alta qualidade - pronto para uso no currículo")
        elif score_qualidade >= 60:
            recomendacoes.append("MPC de qualidade adequada - considere coletar mais vagas")
        else:
            recomendacoes.append("MPC necessita melhorias - colete mais vagas e refaça análise")
        
        if mpc.total_vagas_coletadas < 50:
            recomendacoes.append("Recomenda-se coletar pelo menos 50 vagas para maior precisão")
        
        if not mpc.validado_ia:
            recomendacoes.append("Valide palavras-chave com IA para maior assertividade")
        
        return recomendacoes
    
    # Métodos auxiliares
    
    def _carregar_palavras_base(self) -> Dict[str, List[str]]:
        """Carrega base de palavras-chave por categoria"""
        return {
            "comportamental": [
                "liderança", "comunicação", "trabalho em equipe", "proatividade",
                "organização", "planejamento", "negociação", "relacionamento"
            ],
            "tecnica": [
                "gestão", "análise", "controle", "desenvolvimento", "implementação",
                "coordenação", "supervisão", "operação"
            ],
            "digital": [
                "excel", "power bi", "sql", "sap", "crm", "erp", "word",
                "powerpoint", "outlook", "teams"
            ]
        }
    
    def _carregar_stop_words(self) -> List[str]:
        """Carrega lista de stop words em português"""
        return [
            "de", "da", "do", "das", "dos", "e", "em", "para", "com", "por",
            "ser", "ter", "estar", "fazer", "ir", "vir", "dar", "ver",
            "o", "a", "os", "as", "um", "uma", "uns", "umas",
            "que", "qual", "quais", "quando", "onde", "como", "porque",
            "mas", "ou", "se", "então", "assim", "também", "ainda",
            "já", "não", "sim", "muito", "mais", "menos", "bem", "mal"
        ]
    
    def _configurar_padroes_limpeza(self) -> List[str]:
        """Configura padrões regex para limpeza de texto"""
        return [
            r'\b(anos?|meses?|dias?)\b',  # unidades de tempo
            r'\b(r\$|\$|€|£)\s*\d+', # valores monetários
            r'\b\d{1,2}[hH]\d{2}\b',  # horários
            r'\b\d+[kg|km|m²|%]\b'    # unidades de medida
        ]
    
    def _avaliar_qualidade_extracao(self, contador: Counter) -> str:
        """Avalia qualidade da extração baseada nas palavras encontradas"""
        total_palavras = len(contador)
        palavras_relevantes = sum(1 for palavra in contador.keys() if self._e_palavra_relevante(palavra))
        
        proporcao_relevantes = palavras_relevantes / total_palavras if total_palavras > 0 else 0
        
        if proporcao_relevantes >= 0.7:
            return "excelente"
        elif proporcao_relevantes >= 0.5:
            return "boa"
        elif proporcao_relevantes >= 0.3:
            return "adequada"
        else:
            return "insuficiente"
    
    def _avaliar_qualidade_categorizacao(self, palavras_cat: Dict[str, List]) -> str:
        """Avalia distribuição das categorias"""
        total = sum(len(palavras) for palavras in palavras_cat.values())
        
        if total == 0:
            return "insuficiente"
        
        # Verifica se há palavras em todas as categorias
        categorias_com_palavras = sum(1 for palavras in palavras_cat.values() if len(palavras) > 0)
        
        if categorias_com_palavras == 3:
            return "completa"
        elif categorias_com_palavras >= 2:
            return "adequada"
        else:
            return "incompleta"
    
    def _organizar_por_categoria(self, palavras: List[PalavraChave]) -> Dict[str, List[Dict]]:
        """Organiza palavras por categoria"""
        por_categoria = defaultdict(list)
        
        for palavra in palavras:
            if palavra.recomendada_ia:
                por_categoria[palavra.categoria].append({
                    "termo": palavra.termo,
                    "frequencia": palavra.frequencia_relativa,
                    "importancia": palavra.importancia
                })
        
        # Ordena cada categoria
        for categoria in por_categoria:
            por_categoria[categoria].sort(key=lambda x: x["importancia"], reverse=True)
        
        return dict(por_categoria)
    
    def _gerar_recomendacao_uso(self, priorizacao: Dict[str, List]) -> Dict[str, str]:
        """Gera recomendações de uso das palavras-chave"""
        total_essenciais = len(priorizacao.get("essenciais", []))
        total_importantes = len(priorizacao.get("importantes", []))
        
        recomendacoes = {}
        
        if total_essenciais >= 5:
            recomendacoes["essenciais"] = "Use todas as palavras essenciais no resumo e experiências"
        elif total_essenciais >= 3:
            recomendacoes["essenciais"] = "Use pelo menos 3 palavras essenciais no resumo"
        else:
            recomendacoes["essenciais"] = "Poucas palavras essenciais - revise o MPC"
        
        if total_importantes >= 10:
            recomendacoes["importantes"] = "Distribua palavras importantes nas experiências"
        else:
            recomendacoes["importantes"] = "Use palavras importantes como complemento"
        
        recomendacoes["geral"] = "Sempre personalize com palavras-chave específicas da vaga"
        
        return recomendacoes