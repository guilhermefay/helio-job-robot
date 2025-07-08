"""
Robô de Empregos - API Principal
Sistema de IA para automatizar o método Trocando de Emprego
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from core.config import settings
from core.models.base import Base
from core.services.agente_0_diagnostico import DiagnosticoCarolinaMartins

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do banco de dados
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Criar instância do FastAPI
app = FastAPI(
    title="Robô de Empregos API",
    description="Sistema de IA com agentes autônomos para automatizar transições de carreira",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Dependency para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React frontend
        "http://127.0.0.1:3000",
        os.getenv("FRONTEND_URL", "http://localhost:3000")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas básicas
@app.get("/")
async def root():
    """Endpoint raiz da API"""
    return {
        "message": "🤖 Robô de Empregos API",
        "version": "1.0.0",
        "status": "active",
        "method": "Trocando de Emprego - Carolina Martins"
    }

@app.get("/health")
async def health_check():
    """Verificação de saúde da API"""
    return {
        "status": "healthy",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "services": {
            "api": "running",
            "database": "pending",  # Será atualizado quando conectar DB
            "redis": "pending"      # Será atualizado quando conectar Redis
        }
    }

# Placeholder para rotas dos agentes
@app.get("/agents")
async def list_agents():
    """Lista todos os agentes disponíveis"""
    return {
        "agents": [
            {
                "id": "agent_0",
                "name": "Diagnóstico e Onboarding",
                "description": "Coleta e análise de dados do usuário",
                "status": "development"
            },
            {
                "id": "agent_1", 
                "name": "Extração de Palavras-chave",
                "description": "Análise de vagas e extração de keywords",
                "status": "development"
            },
            {
                "id": "agent_2",
                "name": "Otimização de Currículo", 
                "description": "Reestruturação seguindo método da Carol",
                "status": "development"
            },
            {
                "id": "agent_3",
                "name": "Otimização do LinkedIn",
                "description": "Otimização completa do perfil",
                "status": "development"
            },
            {
                "id": "agent_4",
                "name": "Geração de Conteúdo",
                "description": "Estratégia de conteúdo personalizada", 
                "status": "development"
            }
        ]
    }

@app.post("/agents/diagnostic")
async def run_diagnostic_agent(dados_usuario: dict, db: Session = Depends(get_db)):
    """Executa o agente de Diagnóstico e Onboarding"""
    try:
        agent = DiagnosticoCarolinaMartins(db)
        resultado = agent.executar_diagnostico_completo(dados_usuario)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar agente de diagnóstico: {str(e)}")

# Handler para erros não capturados
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handler geral para exceções"""
    return JSONResponse(
        status_code=500,
        content={
            "message": "Erro interno do servidor",
            "detail": str(exc) if os.getenv("ENVIRONMENT") == "development" else "Contate o suporte"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0", 
        port=8000,
        reload=True if os.getenv("ENVIRONMENT") == "development" else False
    ) 