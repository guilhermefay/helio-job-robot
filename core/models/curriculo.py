from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

Base = declarative_base()

class TipoCurriculo(str, Enum):
    BASE = "base"  # Currículo completo - nunca enviado
    PERSONALIZADO = "personalizado"  # Adaptado para vaga específica

class StatusCurriculo(str, Enum):
    RASCUNHO = "rascunho"
    VALIDADO = "validado"
    ATIVO = "ativo"
    ARQUIVADO = "arquivado"

class Curriculo(Base):
    __tablename__ = "curriculos"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Metadados
    tipo = Column(String(50), default=TipoCurriculo.BASE.value)
    status = Column(String(50), default=StatusCurriculo.RASCUNHO.value)
    nome_arquivo = Column(String(255))
    
    # Campos obrigatórios (estrutura Carolina Martins)
    objetivo = Column(String(200))  # Nome da vaga ou área
    resumo = Column(Text)  # Apresentação + competências + registros
    
    # Dados pessoais (extraídos do usuário)
    nome_completo = Column(String(255))
    telefone = Column(String(20))
    email = Column(String(255))
    linkedin_url = Column(String(500))
    cidade = Column(String(100))
    estado = Column(String(50))
    
    # Configurações de personalização
    vaga_especifica = Column(String(500))  # Job description original
    empresa_alvo = Column(String(200))
    palavras_chave_priorizadas = Column(JSON)  # Keywords da vaga
    
    # Score e validação
    score_qualidade = Column(Float, default=0.0)  # 0-100
    score_aderencia = Column(Float, default=0.0)  # 0-100 (para personalizado)
    
    # Validações automáticas
    validacoes_aprovadas = Column(JSON)  # Lista de validações OK
    validacoes_reprovadas = Column(JSON)  # Lista de validações com erro
    alertas_qualidade = Column(JSON)  # Red flags identificados
    
    # Formatação
    numero_paginas = Column(Integer, default=0)
    fonte_utilizada = Column(String(50), default="Arial")
    tamanho_fonte = Column(Integer, default=11)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    usuario = relationship("User", back_populates="curriculos")
    
    def __repr__(self):
        return f"<Curriculo(id={self.id}, tipo='{self.tipo}', objetivo='{self.objetivo}')>"
    
    def calcular_score_qualidade(self) -> float:
        """Calcula score de qualidade baseado na metodologia Carolina Martins"""
        score = 0.0
        
        # Estrutura (20 pontos)
        if self.objetivo:
            score += 5
        if self.resumo and len(self.resumo.split('\n')) <= 10:
            score += 5
        if self.numero_paginas <= 2:
            score += 5
        if self.fonte_utilizada in ["Arial", "Calibri"]:
            score += 5
        
        # Conteúdo (40 pontos) - verificado através dos relacionamentos
        # Será implementado com dados das experiências e formações
        
        # Honestidade (20 pontos)
        # Validação de consistência será implementada
        
        # Estratégia (20 pontos)
        if self.tipo == TipoCurriculo.PERSONALIZADO.value and self.vaga_especifica:
            score += 10
        if self.palavras_chave_priorizadas:
            score += 5
        
        return min(score, 100.0)
    
    def validar_estrutura_carolina_martins(self) -> Dict[str, Any]:
        """Valida estrutura segundo metodologia Carolina Martins"""
        validacoes = {
            "dados_pessoais": {
                "status": "aprovado" if all([self.nome_completo, self.telefone, self.email, self.linkedin_url]) else "reprovado",
                "detalhes": []
            },
            "objetivo": {
                "status": "aprovado" if self.objetivo else "reprovado",
                "detalhes": []
            },
            "resumo": {
                "status": "pendente",
                "detalhes": []
            },
            "formatacao": {
                "status": "aprovado" if self.fonte_utilizada in ["Arial", "Calibri"] else "reprovado",
                "detalhes": []
            }
        }
        
        # Validações específicas do resumo
        if self.resumo:
            linhas_resumo = len(self.resumo.split('\n'))
            if linhas_resumo <= 10:
                validacoes["resumo"]["status"] = "aprovado"
            else:
                validacoes["resumo"]["status"] = "reprovado"
                validacoes["resumo"]["detalhes"].append(f"Resumo muito extenso: {linhas_resumo} linhas (máx. 10)")
        
        # Validações de dados pessoais
        if not self.nome_completo:
            validacoes["dados_pessoais"]["detalhes"].append("Nome completo obrigatório")
        if not self.telefone:
            validacoes["dados_pessoais"]["detalhes"].append("Telefone obrigatório")
        if not self.email or "@" not in self.email:
            validacoes["dados_pessoais"]["detalhes"].append("Email válido obrigatório")
        if not self.linkedin_url:
            validacoes["dados_pessoais"]["detalhes"].append("LinkedIn obrigatório")
        
        return validacoes
    
    def gerar_alertas_qualidade(self) -> List[str]:
        """Gera alertas baseados nas regras Carolina Martins"""
        alertas = []
        
        # Alertas de formatação
        if self.numero_paginas > 2:
            alertas.append("Currículo muito extenso (>2 páginas)")
        
        # Alertas de conteúdo
        if not self.objetivo:
            alertas.append("Objetivo não definido")
        if not self.resumo:
            alertas.append("Resumo obrigatório")
        
        # Alertas de personalização
        if self.tipo == TipoCurriculo.PERSONALIZADO.value:
            if not self.vaga_especifica:
                alertas.append("Vaga específica não definida para currículo personalizado")
            if not self.palavras_chave_priorizadas:
                alertas.append("Palavras-chave não priorizadas")
        
        return alertas

class ExperienciaProfissional(Base):
    __tablename__ = "experiencias_profissionais"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Dados da experiência
    empresa = Column(String(200), nullable=False)
    cargo = Column(String(100), nullable=False)
    cidade = Column(String(100))
    estado = Column(String(50))
    
    # Período
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime)  # Null se atual
    atual = Column(Boolean, default=False)
    
    # Descrição e responsabilidades
    descricao = Column(Text)
    responsabilidades = Column(JSON)  # Lista de responsabilidades
    resultados = Column(JSON)  # Lista de resultados (tangíveis e intangíveis)
    
    # Palavras-chave da experiência
    palavras_chave = Column(JSON)
    
    # Relevância para objetivos
    relevancia_alta = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    usuario = relationship("User", back_populates="experiencias")
    
    def __repr__(self):
        return f"<ExperienciaProfissional(empresa='{self.empresa}', cargo='{self.cargo}')>"
    
    def calcular_meses_experiencia(self) -> int:
        """Calcula total de meses de experiência"""
        if self.atual:
            fim = datetime.utcnow()
        else:
            fim = self.data_fim or datetime.utcnow()
        
        delta = fim - self.data_inicio
        return int(delta.days / 30.44)  # Média de dias por mês
    
    def validar_consistencia(self) -> Dict[str, Any]:
        """Valida consistência da experiência"""
        validacoes = {
            "periodos": {"status": "aprovado", "detalhes": []},
            "descricao": {"status": "aprovado", "detalhes": []},
            "resultados": {"status": "aprovado", "detalhes": []}
        }
        
        # Validação de períodos
        if self.data_fim and self.data_inicio > self.data_fim:
            validacoes["periodos"]["status"] = "reprovado"
            validacoes["periodos"]["detalhes"].append("Data início posterior à data fim")
        
        # Validação de descrição
        if not self.descricao or len(self.descricao.strip()) < 20:
            validacoes["descricao"]["status"] = "reprovado"
            validacoes["descricao"]["detalhes"].append("Descrição muito curta")
        
        # Validação de resultados
        if not self.resultados or len(self.resultados) == 0:
            validacoes["resultados"]["status"] = "reprovado"
            validacoes["resultados"]["detalhes"].append("Pelo menos 1 resultado obrigatório")
        
        return validacoes

class FormacaoAcademica(Base):
    __tablename__ = "formacoes_academicas"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Dados da formação
    curso = Column(String(200), nullable=False)
    instituicao = Column(String(200), nullable=False)
    cidade = Column(String(100))
    estado = Column(String(50))
    
    # Status e período
    concluido = Column(Boolean, default=False)
    data_inicio = Column(DateTime)
    data_conclusao = Column(DateTime)
    previsao_conclusao = Column(DateTime)
    
    # Tipo de formação
    tipo = Column(String(50))  # graduacao, pos_graduacao, mestrado, doutorado
    
    # Validação Carolina Martins
    percentual_concluido = Column(Float, default=0.0)
    relacionado_objetivo = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    usuario = relationship("User", back_populates="formacoes")
    
    def __repr__(self):
        return f"<FormacaoAcademica(curso='{self.curso}', instituicao='{self.instituicao}')>"
    
    def validar_criterios_inclusao(self) -> bool:
        """Valida critérios Carolina Martins para inclusão no currículo"""
        if self.concluido:
            return True
        
        # Critérios para cursos incompletos
        if self.relacionado_objetivo and self.percentual_concluido > 50:
            return True
        
        return False

class CompetenciaUsuario(Base):
    __tablename__ = "competencias_usuario"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Dados da competência
    nome = Column(String(200), nullable=False)
    categoria = Column(String(50))  # comportamental, tecnica, digital
    nivel = Column(String(50))  # basico, intermediario, avancado
    
    # Validação e comprovação
    comprovada = Column(Boolean, default=False)
    fonte_comprovacao = Column(String(200))  # experiencia, certificacao, curso
    
    # Relevância para objetivos
    relevancia_objetivo = Column(Integer, default=0)  # 0-10
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    usuario = relationship("User", back_populates="competencias")
    
    def __repr__(self):
        return f"<CompetenciaUsuario(nome='{self.nome}', categoria='{self.categoria}', nivel='{self.nivel}')>"