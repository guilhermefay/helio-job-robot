from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

Base = declarative_base()

class CategoriaPalavraChave(str, Enum):
    COMPORTAMENTAL = "comportamental"
    TECNICA = "tecnica"
    DIGITAL = "digital"

class StatusMPC(str, Enum):
    PENDENTE = "pendente"
    COLETANDO = "coletando"
    PROCESSANDO = "processando"
    CONCLUIDO = "concluido"
    ERRO = "erro"

class MapaPalavrasChave(Base):
    """MPC - Mapa de Palavras-Chave da metodologia Carolina Martins"""
    __tablename__ = "mapas_palavras_chave"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Configuração da busca
    area_interesse = Column(String(100), nullable=False)
    cargo_objetivo = Column(String(100), nullable=False)
    segmentos_alvo = Column(JSON)  # Lista de segmentos de interesse
    
    # Status do processamento
    status = Column(String(50), default=StatusMPC.PENDENTE.value)
    
    # Estatísticas da coleta
    total_vagas_coletadas = Column(Integer, default=0)
    total_palavras_extraidas = Column(Integer, default=0)
    data_ultima_coleta = Column(DateTime)
    
    # Resultados consolidados
    palavras_chave_priorizadas = Column(JSON)  # Top palavras por categoria
    competencias_mapeadas = Column(JSON)  # Competências por frequência
    
    # Validação ChatGPT/IA
    validado_ia = Column(Boolean, default=False)
    sugestoes_ia = Column(JSON)  # Sugestões adicionais da IA
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    usuario = relationship("User")
    vagas_analisadas = relationship("VagaAnalisada", back_populates="mpc")
    palavras_chave = relationship("PalavraChave", back_populates="mpc")
    
    def __repr__(self):
        return f"<MapaPalavrasChave(area='{self.area_interesse}', cargo='{self.cargo_objetivo}')>"
    
    def calcular_score_qualidade(self) -> float:
        """Calcula qualidade do MPC baseado nos critérios Carolina Martins"""
        score = 0.0
        
        # Quantidade de vagas (peso 30%)
        if self.total_vagas_coletadas >= 100:
            score += 30
        elif self.total_vagas_coletadas >= 50:
            score += 20
        elif self.total_vagas_coletadas >= 20:
            score += 10
        
        # Diversidade de palavras (peso 25%)
        if self.total_palavras_extraidas >= 200:
            score += 25
        elif self.total_palavras_extraidas >= 100:
            score += 20
        elif self.total_palavras_extraidas >= 50:
            score += 15
        
        # Validação por IA (peso 20%)
        if self.validado_ia:
            score += 20
        
        # Categorização (peso 15%)
        if self.palavras_chave_priorizadas:
            categorias = len(self.palavras_chave_priorizadas.get('por_categoria', {}))
            if categorias >= 3:
                score += 15
            elif categorias >= 2:
                score += 10
        
        # Atualização recente (peso 10%)
        if self.data_ultima_coleta:
            dias_desde_coleta = (datetime.utcnow() - self.data_ultima_coleta).days
            if dias_desde_coleta <= 30:
                score += 10
            elif dias_desde_coleta <= 60:
                score += 5
        
        return min(score, 100.0)
    
    def get_palavras_essenciais(self) -> List[str]:
        """Retorna palavras-chave essenciais baseadas na frequência"""
        if not self.palavras_chave_priorizadas:
            return []
        
        essenciais = []
        for categoria, palavras in self.palavras_chave_priorizadas.get('por_categoria', {}).items():
            # Top 5 por categoria
            for palavra in palavras[:5]:
                if palavra['frequencia'] >= 0.7:  # Aparece em 70%+ das vagas
                    essenciais.append(palavra['termo'])
        
        return essenciais
    
    def get_palavras_por_prioridade(self) -> Dict[str, List[str]]:
        """Organiza palavras por prioridade: essenciais, importantes, complementares"""
        if not self.palavras_chave_priorizadas:
            return {"essenciais": [], "importantes": [], "complementares": []}
        
        priorizacao = {"essenciais": [], "importantes": [], "complementares": []}
        
        for categoria, palavras in self.palavras_chave_priorizadas.get('por_categoria', {}).items():
            for palavra in palavras:
                termo = palavra['termo']
                freq = palavra['frequencia']
                
                if freq >= 0.7:
                    priorizacao["essenciais"].append(termo)
                elif freq >= 0.4:
                    priorizacao["importantes"].append(termo)
                else:
                    priorizacao["complementares"].append(termo)
        
        return priorizacao

class VagaAnalisada(Base):
    """Vagas coletadas para análise de palavras-chave"""
    __tablename__ = "vagas_analisadas"
    
    id = Column(Integer, primary_key=True, index=True)
    mpc_id = Column(Integer, ForeignKey("mapas_palavras_chave.id"), nullable=False)
    
    # Dados da vaga
    titulo = Column(String(200), nullable=False)
    empresa = Column(String(200))
    localizacao = Column(String(200))
    salario = Column(String(100))
    
    # Conteúdo
    descricao = Column(Text)
    requisitos = Column(Text)
    beneficios = Column(Text)
    
    # Fonte da coleta
    fonte = Column(String(100))  # linkedin, indeed, etc.
    url_original = Column(String(500))
    
    # Processamento
    processada = Column(Boolean, default=False)
    palavras_extraidas = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    mpc = relationship("MapaPalavrasChave", back_populates="vagas_analisadas")
    
    def __repr__(self):
        return f"<VagaAnalisada(titulo='{self.titulo}', empresa='{self.empresa}')>"
    
    def extrair_palavras_chave(self) -> Dict[str, List[str]]:
        """Extrai palavras-chave categorizadas da descrição da vaga"""
        # Implementação será feita com NLP
        texto_completo = f"{self.descricao} {self.requisitos}".lower()
        
        # Palavras-chave por categoria (exemplo)
        comportamentais = ["liderança", "comunicação", "trabalho em equipe", "proatividade"]
        tecnicas = ["gestão", "análise", "planejamento", "controle"]
        digitais = ["excel", "power bi", "sql", "python", "sap"]
        
        encontradas = {
            "comportamental": [p for p in comportamentais if p in texto_completo],
            "tecnica": [p for p in tecnicas if p in texto_completo],
            "digital": [p for p in digitais if p in texto_completo]
        }
        
        return encontradas

class PalavraChave(Base):
    """Palavras-chave individuais com estatísticas"""
    __tablename__ = "palavras_chave"
    
    id = Column(Integer, primary_key=True, index=True)
    mpc_id = Column(Integer, ForeignKey("mapas_palavras_chave.id"), nullable=False)
    
    # Dados da palavra-chave
    termo = Column(String(200), nullable=False)
    categoria = Column(String(50), nullable=False)
    sinonimos = Column(JSON)  # Lista de sinônimos
    
    # Estatísticas
    frequencia_absoluta = Column(Integer, default=0)
    frequencia_relativa = Column(Float, default=0.0)
    importancia = Column(Float, default=0.0)  # Score de importância
    
    # Contexto
    contextos_uso = Column(JSON)  # Contextos onde aparece
    empresas_que_usam = Column(JSON)  # Empresas que mencionam
    
    # Validação
    validada_ia = Column(Boolean, default=False)
    recomendada_ia = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    mpc = relationship("MapaPalavrasChave", back_populates="palavras_chave")
    
    def __repr__(self):
        return f"<PalavraChave(termo='{self.termo}', categoria='{self.categoria}', freq={self.frequencia_relativa})>"
    
    def calcular_score_relevancia(self, experiencia_usuario: List[str]) -> float:
        """Calcula relevância da palavra-chave para o usuário"""
        score = self.frequencia_relativa * 0.6  # Base: frequência no mercado
        
        # Bonus se usuário já tem experiência
        if any(exp.lower() in self.termo.lower() for exp in experiencia_usuario):
            score += 0.3
        
        # Bonus se validada por IA
        if self.validada_ia:
            score += 0.1
        
        return min(score, 1.0)

class ProcessamentoMPC(Base):
    """Log de processamento do MPC"""
    __tablename__ = "processamentos_mpc"
    
    id = Column(Integer, primary_key=True, index=True)
    mpc_id = Column(Integer, ForeignKey("mapas_palavras_chave.id"), nullable=False)
    
    # Dados do processamento
    etapa = Column(String(100))  # coleta, extracao, categorizacao, validacao
    status = Column(String(50))  # executando, concluido, erro
    
    # Resultados
    vagas_processadas = Column(Integer, default=0)
    palavras_encontradas = Column(Integer, default=0)
    tempo_processamento = Column(Float)  # segundos
    
    # Erro (se houver)
    erro = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<ProcessamentoMPC(etapa='{self.etapa}', status='{self.status}')>"

class ValidacaoIA(Base):
    """Validações e sugestões da IA para o MPC"""
    __tablename__ = "validacoes_ia"
    
    id = Column(Integer, primary_key=True, index=True)
    mpc_id = Column(Integer, ForeignKey("mapas_palavras_chave.id"), nullable=False)
    
    # Dados da validação
    modelo_ia = Column(String(100))  # gpt-4, claude, etc.
    prompt_utilizado = Column(Text)
    
    # Resultados
    palavras_aprovadas = Column(JSON)
    palavras_rejeitadas = Column(JSON)
    sugestoes_adicionais = Column(JSON)
    
    # Qualidade da validação
    confianca = Column(Float, default=0.0)  # 0-1
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ValidacaoIA(modelo='{self.modelo_ia}', confianca={self.confianca})>"