from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

Base = declarative_base()

class SituacaoCarreira(str, Enum):
    PRIMEIRA_EXPERIENCIA = "primeira_experiencia"
    TRANSICAO_AREA = "transicao_area"
    ASCENSAO_HIERARQUICA = "ascensao_hierarquica"
    RETORNO_MERCADO = "retorno_mercado"
    EMPREGADO_INSATISFEITO = "empregado_insatisfeito"
    EMPREGADO_EXPLORANDO = "empregado_explorando"

class StatusEmprego(str, Enum):
    EMPREGADO = "empregado"
    DESEMPREGADO = "desempregado"
    FREELANCER = "freelancer"
    ESTUDANTE = "estudante"

class Sabotador(str, Enum):
    HIPER_RACIONAL = "hiper_racional"
    HIPER_REALIZADOR = "hiper_realizador"
    CONTROLADOR = "controlador"
    HIPERVIGILANTE = "hipervigilante"
    INQUIETO = "inquieto"
    COMPLACENTE = "complacente"
    JUIZ = "juiz"
    VITIMA = "vitima"
    AGRADADOR = "agradador"
    EVITADOR = "evitador"

class NivelSenioridade(str, Enum):
    ASSISTENTE = "assistente"
    ANALISTA_JR = "analista_jr"
    ANALISTA_PLENO = "analista_pleno"
    ANALISTA_SR = "analista_sr"
    COORDENADOR = "coordenador"
    GERENTE = "gerente"
    DIRETOR = "diretor"

class TipoEmpresa(str, Enum):
    STARTUP = "startup"
    CORPORACAO = "corporacao"
    MULTINACIONAL = "multinacional"
    PUBLICA = "publica"
    ONG = "ong"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    telefone = Column(String(20))
    linkedin_url = Column(String(500))
    cidade = Column(String(100))
    estado = Column(String(50))
    
    # Situação profissional atual
    status_emprego = Column(String(50), default=StatusEmprego.EMPREGADO.value)
    situacao_carreira = Column(String(50), default=SituacaoCarreira.EMPREGADO_EXPLORANDO.value)
    
    # Experiência profissional
    experiencia_mercado = Column(Integer, default=0)  # Anos totais no mercado
    experiencia_profissional = Column(Integer, default=0)  # Anos na área específica
    
    # Carreira atual
    area_atual = Column(String(100))
    cargo_atual = Column(String(100))
    empresa_atual = Column(String(200))
    salario_atual = Column(Float)
    tempo_emprego_atual = Column(Integer)  # Meses
    
    # Objetivos de carreira
    area_objetivo = Column(String(100))
    cargo_objetivo = Column(String(100))
    nivel_atual = Column(String(50))
    nivel_objetivo = Column(String(50))
    pretensao_salarial = Column(Float)
    
    # Sabotadores identificados
    sabotadores_principais = Column(JSON)  # Lista de sabotadores
    
    # Gaps e pontos fortes
    gaps_criticos = Column(JSON)  # Lista de competências em falta
    pontos_fortes = Column(JSON)  # Lista de pontos fortes
    
    # Configurações de busca
    regime_trabalho = Column(String(50), default="hibrido")  # presencial/hibrido/remoto
    disponibilidade_mudanca = Column(Boolean, default=True)
    urgencia = Column(String(20), default="media")  # baixa/media/alta
    
    # Recursos disponíveis
    tempo_diario_job_hunting = Column(Integer, default=60)  # minutos
    orcamento_desenvolvimento = Column(Float, default=0)
    flexibilidade_geografica = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    curriculos = relationship("Curriculo", back_populates="usuario")
    experiencias = relationship("ExperienciaProfissional", back_populates="usuario")
    formacoes = relationship("FormacaoAcademica", back_populates="usuario")
    competencias = relationship("CompetenciaUsuario", back_populates="usuario")
    candidaturas = relationship("Candidatura", back_populates="usuario")
    
    def __repr__(self):
        return f"<User(nome='{self.nome}', area_atual='{self.area_atual}', cargo_atual='{self.cargo_atual}')>"
    
    def calcular_compatibilidade_nivel(self, nivel_objetivo: str) -> float:
        """Calcula compatibilidade com nível hierárquico baseado na experiência"""
        niveis_ordem = {
            "assistente": 0,
            "analista_jr": 1,
            "analista_pleno": 2,
            "analista_sr": 3,
            "coordenador": 4,
            "gerente": 5,
            "diretor": 6
        }
        
        atual_idx = niveis_ordem.get(self.nivel_atual, 0)
        objetivo_idx = niveis_ordem.get(nivel_objetivo, 0)
        
        # Máximo de 2 níveis de salto recomendado
        if objetivo_idx - atual_idx > 2:
            return 0.2  # Muito ambicioso
        elif objetivo_idx - atual_idx == 2:
            return 0.6  # Ambicioso mas possível
        elif objetivo_idx - atual_idx <= 1:
            return 0.9  # Realista
        else:
            return 0.8  # Retrocesso (possível em transições)
    
    def get_score_aderencia_base(self) -> float:
        """Score base de aderência baseado na experiência"""
        if self.experiencia_profissional >= 7:
            return 0.8
        elif self.experiencia_profissional >= 3:
            return 0.7
        elif self.experiencia_profissional >= 1:
            return 0.6
        else:
            return 0.4