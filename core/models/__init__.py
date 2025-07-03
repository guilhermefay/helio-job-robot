"""
Core models para o sistema HELIO - Metodologia Carolina Martins

Este módulo contém todos os modelos de dados baseados na metodologia completa
"Trocando de Emprego" da Carolina Martins, extraída das 89 transcrições.

Estrutura dos modelos:
- user.py: Modelo do usuário e diagnóstico inicial
- curriculo.py: Currículo meteórico com validações metodológicas
- palavras_chave.py: MPC (Mapa de Palavras-Chave) e análise de vagas
- candidatura.py: Tracking de candidaturas e processos seletivos
- linkedin.py: Otimização e estratégia de conteúdo LinkedIn

Cada modelo implementa as regras específicas da metodologia Carolina Martins:
- Validações de honestidade e integridade
- Critérios de qualidade metodológica
- Scores de aderência (70% mínimo)
- Estruturas dos 13 passos do currículo meteórico
- Processo de personalização por vaga
- Ferramenta dos sabotadores
- Estratégias de conteúdo para autoridade
"""

from .user import (
    User,
    SituacaoCarreira,
    StatusEmprego,
    Sabotador,
    NivelSenioridade,
    TipoEmpresa,
    Base as UserBase
)

from .curriculo import (
    Curriculo,
    ExperienciaProfissional,
    FormacaoAcademica,
    CompetenciaUsuario,
    TipoCurriculo,
    StatusCurriculo,
    Base as CurriculoBase
)

from .palavras_chave import (
    MapaPalavrasChave,
    VagaAnalisada,
    PalavraChave,
    ProcessamentoMPC,
    ValidacaoIA,
    CategoriaPalavraChave,
    StatusMPC,
    Base as PalavrasChaveBase
)

from .candidatura import (
    Candidatura,
    Entrevista,
    ProcessoSeletivo,
    StatusCandidatura,
    TipoEntrevista,
    FonteVaga,
    Base as CandidaturaBase
)

from .linkedin import (
    PerfilLinkedIn,
    ExperienciaLinkedIn,
    ConteudoLinkedIn,
    EstrategiaConteudo,
    MetricasLinkedIn,
    StatusPerfilLinkedIn,
    TipoConteudo,
    StatusSSI,
    Base as LinkedInBase
)

# Unifica todas as bases para SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

# Base única para todos os modelos
Base = declarative_base()

# Importa todos os modelos para registro automático
from .user import *
from .curriculo import *
from .palavras_chave import *
from .candidatura import *
from .linkedin import *

__all__ = [
    # User models
    "User",
    "SituacaoCarreira", 
    "StatusEmprego",
    "Sabotador",
    "NivelSenioridade",
    "TipoEmpresa",
    
    # Curriculo models
    "Curriculo",
    "ExperienciaProfissional", 
    "FormacaoAcademica",
    "CompetenciaUsuario",
    "TipoCurriculo",
    "StatusCurriculo",
    
    # Palavras-chave models
    "MapaPalavrasChave",
    "VagaAnalisada",
    "PalavraChave", 
    "ProcessamentoMPC",
    "ValidacaoIA",
    "CategoriaPalavraChave",
    "StatusMPC",
    
    # Candidatura models
    "Candidatura",
    "Entrevista",
    "ProcessoSeletivo", 
    "StatusCandidatura",
    "TipoEntrevista",
    "FonteVaga",
    
    # LinkedIn models
    "PerfilLinkedIn",
    "ExperienciaLinkedIn",
    "ConteudoLinkedIn",
    "EstrategiaConteudo", 
    "MetricasLinkedIn",
    "StatusPerfilLinkedIn",
    "TipoConteudo",
    "StatusSSI",
    
    # Base
    "Base"
]