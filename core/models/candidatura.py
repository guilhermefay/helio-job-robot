from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

# Import unified Base
from .base import Base

class StatusCandidatura(str, Enum):
    PREPARANDO = "preparando"
    ENVIADA = "enviada"
    VISUALIZADA = "visualizada"
    EM_ANDAMENTO = "em_andamento"
    ENTREVISTA_AGENDADA = "entrevista_agendada"
    APROVADA = "aprovada"
    REJEITADA = "rejeitada"
    FINALIZADA = "finalizada"

class TipoEntrevista(str, Enum):
    TRIAGEM = "triagem"
    TECNICA = "tecnica"
    COMPORTAMENTAL = "comportamental"
    FINAL = "final"
    PAINEL = "painel"

class FonteVaga(str, Enum):
    LINKEDIN = "linkedin"
    INDEED = "indeed"
    CATHO = "catho"
    INFOJOBS = "infojobs"
    VAGAS_COM = "vagas_com"
    SITE_EMPRESA = "site_empresa"
    INDICACAO = "indicacao"
    RECRUTADOR = "recrutador"

class Candidatura(Base):
    """Candidaturas do usuário com tracking completo"""
    __tablename__ = "candidaturas"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Dados da vaga
    titulo_vaga = Column(String(200), nullable=False)
    empresa = Column(String(200), nullable=False)
    localizacao = Column(String(200))
    salario_anunciado = Column(String(100))
    regime_trabalho = Column(String(50))  # presencial/hibrido/remoto
    
    # Fonte e aplicação
    fonte = Column(String(50), nullable=False)
    url_vaga = Column(String(500))
    data_aplicacao = Column(DateTime, default=datetime.utcnow)
    
    # Status e tracking
    status = Column(String(50), default=StatusCandidatura.PREPARANDO.value)
    data_ultima_atualizacao = Column(DateTime, default=datetime.utcnow)
    
    # Currículo utilizado
    curriculo_id = Column(Integer, ForeignKey("curriculos.id"))
    
    # Análise de aderência
    score_aderencia = Column(Float, default=0.0)
    requisitos_atendidos = Column(JSON)  # Lista de requisitos matched
    gaps_identificados = Column(JSON)  # Lista de gaps
    
    # Job description original
    descricao_completa = Column(Text)
    requisitos_obrigatorios = Column(JSON)
    requisitos_desejaveis = Column(JSON)
    
    # Personalização aplicada
    palavras_chave_utilizadas = Column(JSON)
    otimizacoes_aplicadas = Column(JSON)
    
    # Feedback e follow-up
    feedback_recebido = Column(Text)
    motivo_rejeicao = Column(String(200))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    usuario = relationship("User", back_populates="candidaturas")
    curriculo = relationship("Curriculo")
    entrevistas = relationship("Entrevista", back_populates="candidatura")
    
    def __repr__(self):
        return f"<Candidatura(titulo='{self.titulo_vaga}', empresa='{self.empresa}', status='{self.status}')>"
    
    def calcular_score_aderencia(self, perfil_usuario: Dict[str, Any]) -> float:
        """Calcula score de aderência baseado na metodologia Carolina Martins (70% mínimo)"""
        if not self.requisitos_obrigatorios:
            return 0.0
        
        score = 0.0
        total_requisitos = len(self.requisitos_obrigatorios)
        
        # Requisitos obrigatórios (peso 2)
        atendidos_obrigatorios = 0
        for req in self.requisitos_obrigatorios:
            if self._usuario_atende_requisito(req, perfil_usuario):
                atendidos_obrigatorios += 1
        
        score_obrigatorios = (atendidos_obrigatorios / total_requisitos) * 0.8
        
        # Requisitos desejáveis (peso 1)
        score_desejaveis = 0.0
        if self.requisitos_desejaveis:
            atendidos_desejaveis = 0
            for req in self.requisitos_desejaveis:
                if self._usuario_atende_requisito(req, perfil_usuario):
                    atendidos_desejaveis += 1
            score_desejaveis = (atendidos_desejaveis / len(self.requisitos_desejaveis)) * 0.2
        
        return min(score_obrigatorios + score_desejaveis, 1.0)
    
    def _usuario_atende_requisito(self, requisito: str, perfil_usuario: Dict[str, Any]) -> bool:
        """Verifica se usuário atende a um requisito específico"""
        # Implementação simplificada - será melhorada com NLP
        req_lower = requisito.lower()
        
        # Verifica experiência
        if perfil_usuario.get('experiencias'):
            for exp in perfil_usuario['experiencias']:
                if req_lower in exp.lower():
                    return True
        
        # Verifica competências
        if perfil_usuario.get('competencias'):
            for comp in perfil_usuario['competencias']:
                if req_lower in comp.lower():
                    return True
        
        return False
    
    def is_aderencia_suficiente(self) -> bool:
        """Verifica se aderência atende critério Carolina Martins (70%)"""
        return self.score_aderencia >= 0.7
    
    def gerar_relatorio_gaps(self) -> Dict[str, Any]:
        """Gera relatório de gaps para melhoria do perfil"""
        return {
            "score_atual": self.score_aderencia,
            "score_objetivo": 0.7,
            "gaps_criticos": self.gaps_identificados or [],
            "recomendacoes": self._gerar_recomendacoes_gaps()
        }
    
    def _gerar_recomendacoes_gaps(self) -> List[str]:
        """Gera recomendações para cobrir gaps identificados"""
        recomendacoes = []
        
        if self.gaps_identificados:
            for gap in self.gaps_identificados:
                if "experiência" in gap.lower():
                    recomendacoes.append(f"Buscar experiência em {gap}")
                elif "curso" in gap.lower():
                    recomendacoes.append(f"Fazer curso de {gap}")
                elif "certificação" in gap.lower():
                    recomendacoes.append(f"Obter certificação em {gap}")
                else:
                    recomendacoes.append(f"Desenvolver competência em {gap}")
        
        return recomendacoes

class Entrevista(Base):
    """Entrevistas agendadas e realizadas"""
    __tablename__ = "entrevistas"
    
    id = Column(Integer, primary_key=True, index=True)
    candidatura_id = Column(Integer, ForeignKey("candidaturas.id"), nullable=False)
    
    # Dados da entrevista
    tipo = Column(String(50), nullable=False)
    data_agendada = Column(DateTime, nullable=False)
    data_realizada = Column(DateTime)
    
    # Entrevistador
    nome_entrevistador = Column(String(200))
    cargo_entrevistador = Column(String(100))
    
    # Formato
    formato = Column(String(50))  # presencial, video, telefone
    plataforma = Column(String(50))  # teams, zoom, etc.
    localizacao = Column(String(200))
    
    # Preparação
    perguntas_preparadas = Column(JSON)
    pontos_fortes_destacar = Column(JSON)
    perguntas_fazer = Column(JSON)
    
    # Realização
    perguntas_recebidas = Column(JSON)
    respostas_dadas = Column(JSON)
    impressoes = Column(Text)
    
    # Resultado
    feedback = Column(Text)
    proxima_etapa = Column(String(100))
    aprovado = Column(Boolean)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    candidatura = relationship("Candidatura", back_populates="entrevistas")
    
    def __repr__(self):
        return f"<Entrevista(tipo='{self.tipo}', data='{self.data_agendada}')>"
    
    def gerar_preparacao_personalizada(self, perfil_usuario: Dict[str, Any]) -> Dict[str, Any]:
        """Gera preparação personalizada baseada no perfil do usuário"""
        preparacao = {
            "pontos_fortes": [],
            "perguntas_esperadas": [],
            "perguntas_fazer": [],
            "stories_star": []
        }
        
        # Baseado no tipo de entrevista
        if self.tipo == TipoEntrevista.COMPORTAMENTAL.value:
            preparacao["perguntas_esperadas"] = [
                "Conte sobre uma situação desafiadora",
                "Como você lida com pressão",
                "Exemplo de trabalho em equipe"
            ]
        elif self.tipo == TipoEntrevista.TECNICA.value:
            preparacao["perguntas_esperadas"] = [
                "Desafios técnicos da sua área",
                "Projetos mais complexos",
                "Como resolve problemas técnicos"
            ]
        
        return preparacao

class ProcessoSeletivo(Base):
    """Tracking completo do processo seletivo"""
    __tablename__ = "processos_seletivos"
    
    id = Column(Integer, primary_key=True, index=True)
    candidatura_id = Column(Integer, ForeignKey("candidaturas.id"), nullable=False)
    
    # Etapas do processo
    etapas_planejadas = Column(JSON)  # Etapas informadas pela empresa
    etapa_atual = Column(String(100))
    
    # Timeline
    data_inicio = Column(DateTime, default=datetime.utcnow)
    data_fim = Column(DateTime)
    duracao_esperada = Column(Integer)  # dias
    
    # Pessoas envolvidas
    recrutador = Column(String(200))
    gestor_contratante = Column(String(200))
    outros_envolvidos = Column(JSON)
    
    # Informações coletadas
    cultura_empresa = Column(Text)
    detalhes_vaga = Column(Text)
    salario_negociado = Column(Float)
    beneficios_oferecidos = Column(JSON)
    
    # Resultado final
    resultado = Column(String(50))  # aprovado, rejeitado, desistiu
    motivo_resultado = Column(Text)
    
    # Learnings
    pontos_melhoria = Column(JSON)
    feedback_processo = Column(Text)
    recomendaria_empresa = Column(Boolean)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<ProcessoSeletivo(etapa_atual='{self.etapa_atual}', resultado='{self.resultado}')>"
    
    def calcular_duracao_processo(self) -> int:
        """Calcula duração total do processo em dias"""
        if self.data_fim:
            return (self.data_fim - self.data_inicio).days
        return (datetime.utcnow() - self.data_inicio).days
    
    def gerar_relatorio_experiencia(self) -> Dict[str, Any]:
        """Gera relatório da experiência no processo"""
        return {
            "duracao_dias": self.calcular_duracao_processo(),
            "etapas_cumpridas": len(self.etapas_planejadas) if self.etapas_planejadas else 0,
            "resultado": self.resultado,
            "pontos_melhoria": self.pontos_melhoria or [],
            "recomendaria": self.recomendaria_empresa,
            "learnings": self.feedback_processo
        }