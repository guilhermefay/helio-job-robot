from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

# Import unified Base
from .base import Base

class StatusPerfilLinkedIn(str, Enum):
    BASICO = "basico"
    INTERMEDIARIO = "intermediario"
    OTIMIZADO = "otimizado"
    METEÓRICO = "meteorico"

class TipoConteudo(str, Enum):
    GERAL = "geral"  # Para audiência
    ESPECIFICO = "especifico"  # Para autoridade
    EXPERIENCIA = "experiencia"
    INSIGHT = "insight"
    CONQUISTA = "conquista"
    APRENDIZADO = "aprendizado"

class StatusSSI(str, Enum):
    BAIXO = "baixo"  # 0-40
    MEDIO = "medio"  # 41-65
    ALTO = "alto"  # 66-100

class PerfilLinkedIn(Base):
    """Perfil LinkedIn do usuário com otimizações"""
    __tablename__ = "perfis_linkedin"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # URL e identificação
    url_perfil = Column(String(500), nullable=False)
    url_personalizada = Column(String(500))
    
    # Headline e sobre
    headline_atual = Column(String(220))
    headline_otimizada = Column(String(220))
    sobre_atual = Column(Text)
    sobre_otimizado = Column(Text)
    
    # Configurações de otimização
    palavras_chave_seo = Column(JSON)  # Palavras-chave para SEO
    segmentos_alvo = Column(JSON)  # Segmentos para targeting
    
    # Métricas atuais
    conexoes_count = Column(Integer, default=0)
    seguidores_count = Column(Integer, default=0)
    visualizacoes_perfil = Column(Integer, default=0)
    
    # SSI (Social Selling Index)
    ssi_score = Column(Float, default=0.0)
    ssi_brand = Column(Float, default=0.0)  # Marca pessoal
    ssi_people = Column(Float, default=0.0)  # Encontrar pessoas
    ssi_insights = Column(Float, default=0.0)  # Compartilhar insights
    ssi_relationship = Column(Float, default=0.0)  # Construir relacionamentos
    
    # Status de otimização
    status_otimizacao = Column(String(50), default=StatusPerfilLinkedIn.BASICO.value)
    
    # Análise de completude
    completude_perfil = Column(Float, default=0.0)  # 0-100%
    elementos_faltando = Column(JSON)  # Lista de elementos a completar
    
    # Estratégia de conteúdo
    estrategia_conteudo = Column(JSON)  # Plano de conteúdo
    frequencia_posts = Column(Integer, default=0)  # Posts por semana
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    usuario = relationship("User")
    experiencias_linkedin = relationship("ExperienciaLinkedIn", back_populates="perfil")
    conteudos = relationship("ConteudoLinkedIn", back_populates="perfil")
    
    def __repr__(self):
        return f"<PerfilLinkedIn(url='{self.url_perfil}', status='{self.status_otimizacao}')>"
    
    def calcular_score_otimizacao(self) -> float:
        """Calcula score de otimização baseado na metodologia Carolina Martins"""
        score = 0.0
        
        # Elementos básicos (30 pontos)
        if self.headline_otimizada:
            score += 10
        if self.sobre_otimizado:
            score += 10
        if self.url_personalizada:
            score += 10
        
        # Completude do perfil (25 pontos)
        score += self.completude_perfil * 0.25
        
        # Palavras-chave SEO (20 pontos)
        if self.palavras_chave_seo and len(self.palavras_chave_seo) >= 10:
            score += 20
        elif self.palavras_chave_seo and len(self.palavras_chave_seo) >= 5:
            score += 15
        
        # SSI Score (15 pontos)
        if self.ssi_score >= 70:
            score += 15
        elif self.ssi_score >= 50:
            score += 10
        elif self.ssi_score >= 30:
            score += 5
        
        # Estratégia de conteúdo (10 pontos)
        if self.estrategia_conteudo and self.frequencia_posts >= 3:
            score += 10
        elif self.estrategia_conteudo:
            score += 5
        
        return min(score, 100.0)
    
    def gerar_headline_otimizada(self, cargo_objetivo: str, palavras_chave: List[str]) -> str:
        """Gera headline otimizada baseada no cargo objetivo e palavras-chave"""
        # Estrutura Carolina Martins: Cargo | Competência 1 | Competência 2
        if len(palavras_chave) >= 2:
            return f"{cargo_objetivo} | {palavras_chave[0]} | {palavras_chave[1]}"
        elif len(palavras_chave) >= 1:
            return f"{cargo_objetivo} | {palavras_chave[0]}"
        else:
            return cargo_objetivo
    
    def adaptar_resumo_para_sobre(self, resumo_curriculo: str) -> str:
        """Adapta resumo do currículo para seção Sobre do LinkedIn"""
        # Transforma resumo em formato mais pessoal para LinkedIn
        linhas = resumo_curriculo.split('\n')
        
        # Primeira linha mais pessoal
        if linhas:
            primeira_linha = linhas[0].replace("Profissional", "Sou um profissional")
            sobre_adaptado = primeira_linha + "\n\n" + "\n".join(linhas[1:])
            return sobre_adaptado
        
        return resumo_curriculo
    
    def identificar_elementos_faltando(self) -> List[str]:
        """Identifica elementos faltando no perfil"""
        elementos_faltando = []
        
        if not self.headline_otimizada:
            elementos_faltando.append("Headline otimizada")
        if not self.sobre_otimizado:
            elementos_faltando.append("Seção Sobre")
        if not self.url_personalizada:
            elementos_faltando.append("URL personalizada")
        if not self.palavras_chave_seo:
            elementos_faltando.append("Palavras-chave SEO")
        if self.conexoes_count < 500:
            elementos_faltando.append("Rede de conexões (min 500)")
        if not self.estrategia_conteudo:
            elementos_faltando.append("Estratégia de conteúdo")
        
        return elementos_faltando

class ExperienciaLinkedIn(Base):
    """Experiências profissionais otimizadas para LinkedIn"""
    __tablename__ = "experiencias_linkedin"
    
    id = Column(Integer, primary_key=True, index=True)
    perfil_id = Column(Integer, ForeignKey("perfis_linkedin.id"), nullable=False)
    experiencia_id = Column(Integer, ForeignKey("experiencias_profissionais.id"))
    
    # Dados básicos
    titulo = Column(String(200), nullable=False)
    empresa = Column(String(200), nullable=False)
    localizacao = Column(String(200))
    
    # Período
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime)
    atual = Column(Boolean, default=False)
    
    # Descrição otimizada para LinkedIn
    descricao_otimizada = Column(Text)
    palavras_chave_incluidas = Column(JSON)
    
    # Métricas e resultados
    resultados_quantificados = Column(JSON)
    conquistas_destaque = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    perfil = relationship("PerfilLinkedIn", back_populates="experiencias_linkedin")
    
    def __repr__(self):
        return f"<ExperienciaLinkedIn(titulo='{self.titulo}', empresa='{self.empresa}')>"
    
    def otimizar_para_linkedin(self, palavras_chave: List[str]) -> str:
        """Otimiza descrição da experiência para LinkedIn"""
        if not self.descricao_otimizada:
            return ""
        
        # Adiciona palavras-chave estrategicamente
        descricao = self.descricao_otimizada
        
        # Inclui palavras-chave no início da descrição
        if palavras_chave:
            primeira_competencia = palavras_chave[0]
            if primeira_competencia.lower() not in descricao.lower():
                descricao = f"Responsável por {primeira_competencia.lower()} e {descricao.lower()}"
        
        return descricao

class ConteudoLinkedIn(Base):
    """Conteúdo para estratégia de autoridade no LinkedIn"""
    __tablename__ = "conteudos_linkedin"
    
    id = Column(Integer, primary_key=True, index=True)
    perfil_id = Column(Integer, ForeignKey("perfis_linkedin.id"), nullable=False)
    
    # Dados do conteúdo
    titulo = Column(String(200))
    corpo = Column(Text, nullable=False)
    tipo = Column(String(50), nullable=False)
    
    # Estratégia
    objetivo = Column(String(100))  # audiencia, autoridade, networking
    palavras_chave = Column(JSON)
    hashtags = Column(JSON)
    
    # Programação
    data_programada = Column(DateTime)
    publicado = Column(Boolean, default=False)
    data_publicacao = Column(DateTime)
    
    # Métricas
    visualizacoes = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comentarios = Column(Integer, default=0)
    compartilhamentos = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    perfil = relationship("PerfilLinkedIn", back_populates="conteudos")
    
    def __repr__(self):
        return f"<ConteudoLinkedIn(titulo='{self.titulo}', tipo='{self.tipo}')>"
    
    def calcular_engagement(self) -> float:
        """Calcula taxa de engajamento do conteúdo"""
        if self.visualizacoes == 0:
            return 0.0
        
        total_interacoes = self.likes + self.comentarios + self.compartilhamentos
        return (total_interacoes / self.visualizacoes) * 100

class EstrategiaConteudo(Base):
    """Estratégia de conteúdo personalizada para LinkedIn"""
    __tablename__ = "estrategias_conteudo"
    
    id = Column(Integer, primary_key=True, index=True)
    perfil_id = Column(Integer, ForeignKey("perfis_linkedin.id"), nullable=False)
    
    # Objetivos da estratégia
    objetivo_principal = Column(String(100))  # autoridade, networking, job_search
    area_expertise = Column(String(100))
    publico_alvo = Column(JSON)
    
    # Planejamento
    frequencia_posts = Column(Integer, default=3)  # Por semana
    temas_principais = Column(JSON)  # Temas baseados em palavras-chave
    
    # Distribuição de conteúdo
    percentual_geral = Column(Float, default=0.6)  # 60% para audiência
    percentual_especifico = Column(Float, default=0.4)  # 40% para autoridade
    
    # Templates de conteúdo
    templates_posts = Column(JSON)
    storytelling_pessoal = Column(JSON)
    
    # Cronograma
    calendario_editorial = Column(JSON)
    
    # Métricas objetivo
    meta_conexoes = Column(Integer, default=1000)
    meta_seguidores = Column(Integer, default=500)
    meta_visualizacoes = Column(Integer, default=1000)
    
    # Status
    ativa = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<EstrategiaConteudo(objetivo='{self.objetivo_principal}', area='{self.area_expertise}')>"
    
    def gerar_calendario_semanal(self, palavras_chave: List[str]) -> Dict[str, Any]:
        """Gera calendário editorial semanal baseado nas palavras-chave"""
        calendario = {
            "segunda": {
                "tipo": "experiencia",
                "tema": f"Aprendizado da semana sobre {palavras_chave[0] if palavras_chave else 'sua área'}"
            },
            "quarta": {
                "tipo": "insight",
                "tema": f"Dica prática sobre {palavras_chave[1] if len(palavras_chave) > 1 else 'sua especialidade'}"
            },
            "sexta": {
                "tipo": "conquista",
                "tema": "Resultado ou projeto concluído"
            }
        }
        
        return calendario
    
    def gerar_templates_personalizados(self, experiencias: List[str]) -> Dict[str, str]:
        """Gera templates de posts baseados na experiência do usuário"""
        templates = {
            "experiencia": f"""
Há [X] anos atrás, eu estava [SITUAÇÃO INICIAL].
Hoje, após trabalhar em {experiencias[0] if experiencias else '[ÁREA]'}, aprendi que [LIÇÃO APRENDIDA].
O que mais me marca é [INSIGHT PESSOAL].
E você, qual foi seu maior aprendizado na área?
""",
            "insight": f"""
3 dicas que aplicei em {experiencias[0] if experiencias else '[ÁREA]'} e que transformaram meus resultados:
1. [DICA 1]
2. [DICA 2]  
3. [DICA 3]
Qual dessas você já aplica no seu dia a dia?
""",
            "conquista": f"""
Que semana! Acabei de [CONQUISTA/RESULTADO].
O projeto envolveu [DESAFIO TÉCNICO] e [DESAFIO COMPORTAMENTAL].
O resultado foi [MÉTRICA/IMPACTO].
Gratidão por trabalhar com [RECONHECIMENTO EQUIPE].
"""
        }
        
        return templates

class MetricasLinkedIn(Base):
    """Métricas e analytics do perfil LinkedIn"""
    __tablename__ = "metricas_linkedin"
    
    id = Column(Integer, primary_key=True, index=True)
    perfil_id = Column(Integer, ForeignKey("perfis_linkedin.id"), nullable=False)
    
    # Período da métrica
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=False)
    
    # Métricas de perfil
    visualizacoes_perfil = Column(Integer, default=0)
    buscas_apareceu = Column(Integer, default=0)
    conexoes_aceitas = Column(Integer, default=0)
    
    # Métricas de conteúdo
    impressoes_posts = Column(Integer, default=0)
    clicks_posts = Column(Integer, default=0)
    likes_recebidos = Column(Integer, default=0)
    comentarios_recebidos = Column(Integer, default=0)
    
    # SSI histórico
    ssi_historico = Column(JSON)
    
    # Crescimento
    crescimento_conexoes = Column(Float, default=0.0)
    crescimento_seguidores = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<MetricasLinkedIn(periodo='{self.data_inicio} - {self.data_fim}')>"
    
    def calcular_taxa_crescimento(self, metricas_anteriores: 'MetricasLinkedIn') -> Dict[str, float]:
        """Calcula taxas de crescimento comparando com período anterior"""
        if not metricas_anteriores:
            return {"conexoes": 0.0, "visualizacoes": 0.0}
        
        crescimento = {}
        
        # Crescimento de conexões
        if metricas_anteriores.conexoes_aceitas > 0:
            crescimento["conexoes"] = ((self.conexoes_aceitas - metricas_anteriores.conexoes_aceitas) / metricas_anteriores.conexoes_aceitas) * 100
        else:
            crescimento["conexoes"] = 0.0
        
        # Crescimento de visualizações
        if metricas_anteriores.visualizacoes_perfil > 0:
            crescimento["visualizacoes"] = ((self.visualizacoes_perfil - metricas_anteriores.visualizacoes_perfil) / metricas_anteriores.visualizacoes_perfil) * 100
        else:
            crescimento["visualizacoes"] = 0.0
        
        return crescimento