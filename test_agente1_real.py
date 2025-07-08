#!/usr/bin/env python3
"""
Teste REAL do Agente 1 para verificar se está funcionando corretamente
"""

import asyncio
import sys
import os

# Adiciona o path do projeto
sys.path.append('/Users/Guilherme_1/HELIO')

from core.services.agente_1_palavras_chave import MPCCarolinaMartins
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def test_extracao_palavras():
    """Testa a extração de palavras-chave com dados reais"""
    
    # Cria uma sessão mock para teste
    engine = create_engine('sqlite:///:memory:')
    Session = sessionmaker(bind=engine)
    db = Session()
    
    # Cria instância do MPC
    mpc = MPCCarolinaMartins(db)
    
    # Texto exemplo de vaga real de Product Manager
    texto_vaga_real = """
    O Nubank está procurando um Product Manager Sênior para liderar produtos digitais inovadores.
    
    Responsabilidades:
    • Definir e executar roadmap de produtos
    • Trabalhar com dados e métricas (SQL, Google Analytics)
    • Colaborar com times de engenharia e design
    • Conduzir pesquisas com usuários
    • Gerenciar stakeholders internos
    • Implementar metodologias ágeis (Scrum, Kanban)
    
    Requisitos:
    • Experiência mínima 5 anos em product management
    • Conhecimento em metodologias ágeis
    • Análise de dados (SQL, Excel, Power BI)
    • Inglês avançado
    • Experiência com ferramentas: Jira, Confluence, Figma
    • MBA ou pós-graduação (desejável)
    
    Oferecemos ambiente inovador, stock options e crescimento acelerado.
    """
    
    print("🧪 TESTE REAL DO EXTRATOR DE PALAVRAS-CHAVE")
    print("="*60)
    print("📝 Texto da vaga:")
    print(texto_vaga_real[:200] + "...")
    
    # Testa método antigo
    print("\n❌ MÉTODO ANTIGO:")
    palavras_antigas = mpc._extrair_palavras_texto(texto_vaga_real)
    print(f"   Palavras extraídas: {len(palavras_antigas)}")
    print(f"   Primeiras 10: {palavras_antigas[:10]}")
    
    # Testa método novo
    print("\n✅ MÉTODO NOVO (APRIMORADO):")
    palavras_novas = mpc._extrair_palavras_texto_detalhado(texto_vaga_real)
    print(f"   Palavras extraídas: {len(palavras_novas)}")
    print(f"   Primeiras 20: {palavras_novas[:20]}")
    
    # Compara
    print(f"\n📊 COMPARAÇÃO:")
    print(f"   Método antigo: {len(palavras_antigas)} palavras")
    print(f"   Método novo: {len(palavras_novas)} palavras")
    print(f"   Melhoria: {len(palavras_novas) - len(palavras_antigas)} palavras a mais")
    
    # Mostra termos compostos encontrados
    termos_compostos = mpc._identificar_termos_compostos_expandido(texto_vaga_real)
    print(f"\n🔗 TERMOS COMPOSTOS IDENTIFICADOS ({len(termos_compostos)}):")
    for termo in termos_compostos:
        print(f"   • {termo}")
    
    print("\n" + "="*60)
    
    if len(palavras_novas) > len(palavras_antigas):
        print("✅ TESTE PASSOU - Método aprimorado funcionando!")
        return True
    else:
        print("❌ TESTE FALHOU - Método não melhorou")
        return False

if __name__ == "__main__":
    sucesso = test_extracao_palavras()
    sys.exit(0 if sucesso else 1)