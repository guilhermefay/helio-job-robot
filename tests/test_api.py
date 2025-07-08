"""
Testes iniciais da API
"""

import pytest
from fastapi.testclient import TestClient
from api.main import app

# Cliente de teste
client = TestClient(app)


def test_read_root():
    """Teste do endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Robô de Empregos" in data["message"]
    assert data["version"] == "1.0.0"


def test_health_check():
    """Teste do health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "services" in data


def test_list_agents():
    """Teste da listagem de agentes"""
    response = client.get("/agents")
    assert response.status_code == 200
    data = response.json()
    assert "agents" in data
    assert len(data["agents"]) == 5
    
    # Verificar se todos os agentes têm campos obrigatórios
    for agent in data["agents"]:
        assert "id" in agent
        assert "name" in agent
        assert "description" in agent
        assert "status" in agent


def test_api_docs():
    """Teste se a documentação está acessível"""
    response = client.get("/docs")
    assert response.status_code == 200
    
    response = client.get("/redoc")
    assert response.status_code == 200 