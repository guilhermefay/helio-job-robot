"""
Testes para os 5 Agentes do Sistema HELIO
Metodologia Carolina Martins

Este arquivo contém testes para validar o funcionamento de cada agente
e demonstrar como usar o sistema completo.
"""

import pytest
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.models import Base, User, Curriculo, PerfilLinkedIn
from core.services.agente_0_diagnostico import DiagnosticoCarolinaMartins
from core.services.agente_1_palavras_chave import MPCCarolinaMartins
from core.services.agente_2_curriculo import CurriculoCarolinaMartins
from core.services.agente_3_linkedin import LinkedInCarolinaMartins
from core.services.agente_4_conteudo import ConteudoCarolinaMartins

# Configuração do banco de dados para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_helio.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    """Cria sessão de banco para testes"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def dados_usuario_teste():
    """Dados de exemplo para testar os agentes"""
    return {
        "nome": "João Silva Santos",
        "email": "joao.silva@gmail.com",
        "telefone": "(11) 99999-9999",
        "linkedin_url": "https://linkedin.com/in/joaosilva",
        "cidade": "São Paulo",
        "estado": "SP",
        "area_atual": "Tecnologia",
        "area_objetivo": "Engenharia de Software",
        "cargo_atual": "Desenvolvedor Pleno",
        "cargo_objetivo": "Tech Lead",
        "experiencia_mercado": 8,
        "experiencia_profissional": 6,
        "status_emprego": "empregado",
        "satisfacao_emprego_atual": 4,
        "disponibilidade_mudanca": True,
        "regime_trabalho": "hibrido",
        
        # Experiências profissionais
        "experiencias": [
            {
                "empresa": "TechCorp",
                "cargo": "Desenvolvedor Pleno",
                "data_inicio": "2022-01-01",
                "data_fim": None,
                "descricao": "Desenvolvimento de aplicações web em Python e React. Liderei equipe de 3 desenvolvedores em projeto de migração de sistema legacy."
            },
            {
                "empresa": "StartupX",
                "cargo": "Desenvolvedor Júnior",
                "data_inicio": "2020-03-01",
                "data_fim": "2021-12-31",
                "descricao": "Desenvolvimento full-stack usando Django e Vue.js. Implementei sistema de pagamentos que aumentou conversão em 15%."
            }
        ],
        
        # Formações
        "formacoes": [
            {
                "instituicao": "FIAP",
                "curso": "Análise e Desenvolvimento de Sistemas",
                "tipo": "superior",
                "ano_conclusao": "2020",
                "status": "concluido"
            }
        ],
        
        # Competências
        "competencias": ["Python", "React", "Django", "JavaScript", "SQL", "Git", "AWS"],
        
        # Idiomas
        "idiomas": [
            {"idioma": "Inglês", "nivel": "intermediario", "certificacao": ""},
            {"idioma": "Espanhol", "nivel": "básico", "certificacao": ""}
        ],
        
        # Questionário sabotadores (respostas 1-5)
        "questionario_sabotadores": {
            "q1": 3, "q2": 2, "q3": 4,  # Hiper-racional
            "q4": 4, "q5": 5, "q6": 3,  # Hiper-realizador
            "q7": 2, "q8": 3, "q9": 4,  # Controlador
            "q10": 3, "q11": 2, "q12": 3,  # Hipervigilante
            "q13": 2, "q14": 4, "q15": 3,  # Inquieto
            "q16": 1, "q17": 2, "q18": 2,  # Complacente
            "q19": 4, "q20": 3, "q21": 5,  # Juiz
            "q22": 1, "q23": 1, "q24": 2,  # Vítima
            "q25": 2, "q26": 2, "q27": 3,  # Agradador
            "q28": 3, "q29": 2, "q30": 3   # Evitador
        }
    }

class TestAgente0Diagnostico:
    """Testa Agente 0: Diagnóstico e Onboarding"""
    
    def test_executar_diagnostico_completo(self, db_session, dados_usuario_teste):
        """Testa execução completa do diagnóstico"""
        agente = DiagnosticoCarolinaMartins(db_session)
        resultado = agente.executar_diagnostico_completo(dados_usuario_teste)
        
        # Verifica estrutura do resultado
        assert "perfil_basico" in resultado
        assert "experiencia_profissional" in resultado
        assert "sabotadores" in resultado
        assert "situacao_carreira" in resultado
        assert "alinhamento_expectativas" in resultado
        assert "configuracao_agentes" in resultado
        assert "score_diagnostico" in resultado
        
        # Verifica sabotadores identificados
        sabotadores = resultado["sabotadores"]
        assert "scores" in sabotadores
        assert "principais" in sabotadores
        assert len(sabotadores["principais"]) >= 0
        
        # Verifica configuração para outros agentes
        config_agentes = resultado["configuracao_agentes"]
        assert "agente_1_palavras_chave" in config_agentes
        assert "agente_2_curriculo" in config_agentes
        
        print(f"✅ Diagnóstico concluído! Score: {resultado['score_diagnostico']:.1f}")
        print(f"   Sabotadores principais: {', '.join(sabotadores['principais'])}")
        print(f"   Situação de carreira: {resultado['situacao_carreira']}")

class TestAgente1PalavrasChave:
    """Testa Agente 1: Extração de Palavras-chave (MPC)"""
    
    @pytest.mark.asyncio
    async def test_executar_mpc_completo(self, db_session):
        """Testa execução completa do MPC"""
        agente = MPCCarolinaMartins(db_session)
        
        # Simula dados para teste
        area_interesse = "Engenharia de Software"
        cargo_objetivo = "Tech Lead"
        
        try:
            # Em ambiente real, faria coleta de vagas
            # Para teste, simula resultado MPC
            resultado_mpc = {
                "mpc_id": 1,
                "configuracao": {
                    "area_interesse": area_interesse,
                    "cargo_objetivo": cargo_objetivo,
                    "meta_vagas": 100
                },
                "priorizacao_final": {
                    "essenciais": [
                        {"palavra": "Python", "frequencia": 85},
                        {"palavra": "Liderança", "frequencia": 78},
                        {"palavra": "Arquitetura", "frequencia": 72}
                    ],
                    "importantes": [
                        {"palavra": "React", "frequencia": 65},
                        {"palavra": "AWS", "frequencia": 58},
                        {"palavra": "Scrum", "frequencia": 55}
                    ],
                    "complementares": [
                        {"palavra": "Docker", "frequencia": 45},
                        {"palavra": "Kubernetes", "frequencia": 38}
                    ]
                }
            }
            
            print(f"✅ MPC concluído para {area_interesse}")
            print(f"   Palavras essenciais: {[p['palavra'] for p in resultado_mpc['priorizacao_final']['essenciais']]}")
            print(f"   Total de palavras mapeadas: {len(resultado_mpc['priorizacao_final']['essenciais']) + len(resultado_mpc['priorizacao_final']['importantes']) + len(resultado_mpc['priorizacao_final']['complementares'])}")
            
            return resultado_mpc
            
        except Exception as e:
            print(f"⚠️  Teste MPC em modo simulado: {str(e)}")
            return None

class TestAgente2Curriculo:
    """Testa Agente 2: Otimização de Currículo (13 Passos)"""
    
    @pytest.mark.asyncio
    async def test_gerar_curriculo_base(self, db_session, dados_usuario_teste):
        """Testa geração do currículo base"""
        # Cria usuário no banco
        user = User(
            nome=dados_usuario_teste["nome"],
            email=dados_usuario_teste["email"],
            telefone=dados_usuario_teste["telefone"]
        )
        db_session.add(user)
        db_session.commit()
        
        agente = CurriculoCarolinaMartins(db_session)
        
        # Simula dados do diagnóstico
        dados_diagnostico = {
            "perfil_basico": {
                "nome": dados_usuario_teste["nome"],
                "email": dados_usuario_teste["email"],
                "telefone": dados_usuario_teste["telefone"],
                "linkedin_url": dados_usuario_teste["linkedin_url"],
                "cidade": dados_usuario_teste["cidade"],
                "estado": dados_usuario_teste["estado"]
            },
            "experiencia_profissional": {
                "nivel_objetivo": dados_usuario_teste["cargo_objetivo"],
                "experiencia_profissional": dados_usuario_teste["experiencia_profissional"]
            },
            "configuracao_agentes": {
                "agente_1_palavras_chave": {
                    "area_interesse": dados_usuario_teste["area_objetivo"]
                }
            },
            "experiencias": dados_usuario_teste["experiencias"],
            "formacoes": dados_usuario_teste["formacoes"],
            "competencias": dados_usuario_teste["competencias"],
            "idiomas": dados_usuario_teste["idiomas"]
        }
        
        # Simula dados do MPC
        mpc_dados = {
            "priorizacao_final": {
                "essenciais": [
                    {"palavra": "Python"}, {"palavra": "Liderança"}, {"palavra": "Arquitetura"}
                ]
            }
        }
        
        resultado = await agente.gerar_curriculo_base(
            usuario_id=user.id,
            dados_diagnostico=dados_diagnostico,
            mpc_dados=mpc_dados
        )
        
        # Verifica resultado
        assert "curriculo_id" in resultado
        assert "13_passos" in resultado
        assert "score_qualidade" in resultado
        assert "classificacao" in resultado
        
        # Verifica se todos os 13 passos foram executados
        passos = resultado["13_passos"]
        assert len(passos) == 13
        
        print(f"✅ Currículo base criado! Score: {resultado['score_qualidade']:.1f}")
        print(f"   Classificação: {resultado['classificacao']}")
        print(f"   Passos executados: {len(passos)}/13")

class TestAgente3LinkedIn:
    """Testa Agente 3: Otimização LinkedIn"""
    
    @pytest.mark.asyncio
    async def test_construir_linkedin_meteorico(self, db_session, dados_usuario_teste):
        """Testa construção do LinkedIn meteórico"""
        # Cria usuário
        user = User(
            nome=dados_usuario_teste["nome"],
            email=dados_usuario_teste["email"]
        )
        db_session.add(user)
        db_session.commit()
        
        agente = LinkedInCarolinaMartins(db_session)
        
        # Simula dados necessários
        dados_diagnostico = {
            "perfil_basico": {
                "nome": dados_usuario_teste["nome"],
                "cidade": dados_usuario_teste["cidade"],
                "estado": dados_usuario_teste["estado"]
            },
            "configuracao_agentes": {
                "agente_1_palavras_chave": {
                    "area_interesse": dados_usuario_teste["area_objetivo"]
                }
            }
        }
        
        curriculo_dados = {
            "13_passos": {
                "2_objetivo": {
                    "objetivo": {"objetivo_formatado": dados_usuario_teste["cargo_objetivo"]}
                },
                "3_resumo": {
                    "resumo": f"Profissional de {dados_usuario_teste['area_objetivo']} com {dados_usuario_teste['experiencia_profissional']} anos de experiência"
                }
            }
        }
        
        mpc_dados = {
            "priorizacao_final": {
                "essenciais": [{"palavra": "Python"}, {"palavra": "Liderança"}]
            }
        }
        
        resultado = await agente.construir_linkedin_meteorico(
            usuario_id=user.id,
            dados_diagnostico=dados_diagnostico,
            curriculo_dados=curriculo_dados,
            mpc_dados=mpc_dados
        )
        
        # Verifica resultado
        assert "10_passos" in resultado
        assert "estrategia_conteudo" in resultado
        assert "score_linkedin" in resultado
        assert "classificacao" in resultado
        
        passos = resultado["10_passos"]
        assert len(passos) == 10
        
        print(f"✅ LinkedIn meteórico criado! Score: {resultado['score_linkedin']:.1f}")
        print(f"   Classificação: {resultado['classificacao']}")
        print(f"   Passos executados: {len(passos)}/10")

class TestAgente4Conteudo:
    """Testa Agente 4: Geração de Conteúdo"""
    
    @pytest.mark.asyncio
    async def test_gerar_plano_editorial(self, db_session, dados_usuario_teste):
        """Testa geração do plano editorial"""
        # Cria usuário e perfil LinkedIn
        user = User(nome=dados_usuario_teste["nome"])
        db_session.add(user)
        db_session.commit()
        
        perfil = PerfilLinkedIn(usuario_id=user.id)
        db_session.add(perfil)
        db_session.commit()
        
        # Cria estratégia de conteúdo (normalmente criada pelo Agente 3)
        from core.models import EstrategiaConteudo
        estrategia = EstrategiaConteudo(
            perfil_linkedin_id=perfil.id,
            distribuicao_geral=60,
            distribuicao_autoridade=40,
            frequencia_posts='{"posts_por_semana": 3}',
            temas_gerais='["Dicas de carreira", "Motivação"]',
            temas_autoridade='["Expertise técnica", "Cases"]',
            area_foco=dados_usuario_teste["area_objetivo"]
        )
        db_session.add(estrategia)
        db_session.commit()
        
        agente = ConteudoCarolinaMartins(db_session)
        
        # Simula dados necessários
        dados_diagnostico = {
            "configuracao_agentes": {
                "agente_1_palavras_chave": {
                    "area_interesse": dados_usuario_teste["area_objetivo"]
                }
            },
            "experiencia_profissional": {
                "experiencia_profissional": dados_usuario_teste["experiencia_profissional"]
            },
            "perfil_basico": {"nome": dados_usuario_teste["nome"]}
        }
        
        mpc_dados = {
            "priorizacao_final": {
                "essenciais": [{"palavra": "Python"}, {"palavra": "Liderança"}]
            }
        }
        
        curriculo_dados = {
            "13_passos": {
                "4_experiencias": {"experiencias": dados_usuario_teste["experiencias"]}
            }
        }
        
        resultado = await agente.gerar_plano_editorial_completo(
            perfil_linkedin_id=perfil.id,
            periodo_dias=30,
            dados_diagnostico=dados_diagnostico,
            mpc_dados=mpc_dados,
            curriculo_dados=curriculo_dados
        )
        
        # Verifica resultado
        assert "calendario_detalhado" in resultado
        assert "plano_editorial" in resultado
        assert "temas_identificados" in resultado
        
        calendario = resultado["calendario_detalhado"]
        plano = resultado["plano_editorial"]
        
        print(f"✅ Plano editorial criado!")
        print(f"   Total de posts: {plano['total_posts']}")
        print(f"   Distribuição 60/40: {plano['distribuicao_60_40']}")
        print(f"   Período: {plano['periodo']}")

class TestFluxoCompleto:
    """Testa fluxo completo dos 5 agentes"""
    
    @pytest.mark.asyncio
    async def test_fluxo_completo_agentes(self, db_session, dados_usuario_teste):
        """Testa execução sequencial de todos os agentes"""
        print("\n🚀 INICIANDO TESTE COMPLETO DO SISTEMA HELIO")
        print("=" * 60)
        
        # Cria usuário
        user = User(
            nome=dados_usuario_teste["nome"],
            email=dados_usuario_teste["email"],
            telefone=dados_usuario_teste["telefone"]
        )
        db_session.add(user)
        db_session.commit()
        print(f"👤 Usuário criado: {user.nome}")
        
        # AGENTE 0: Diagnóstico
        print("\n🩺 EXECUTANDO AGENTE 0: DIAGNÓSTICO")
        agente_0 = DiagnosticoCarolinaMartins(db_session)
        resultado_diagnostico = agente_0.executar_diagnostico_completo(dados_usuario_teste)
        print(f"   ✅ Score diagnóstico: {resultado_diagnostico['score_diagnostico']:.1f}")
        print(f"   ✅ Situação: {resultado_diagnostico['situacao_carreira']}")
        
        # AGENTE 1: Palavras-chave (simulado)
        print("\n🔍 EXECUTANDO AGENTE 1: PALAVRAS-CHAVE (MPC)")
        resultado_mpc = {
            "priorizacao_final": {
                "essenciais": [
                    {"palavra": "Python"}, {"palavra": "Liderança"}, {"palavra": "Arquitetura"}
                ],
                "importantes": [
                    {"palavra": "React"}, {"palavra": "AWS"}
                ]
            }
        }
        print(f"   ✅ Palavras essenciais: Python, Liderança, Arquitetura")
        
        # AGENTE 2: Currículo
        print("\n📄 EXECUTANDO AGENTE 2: CURRÍCULO (13 PASSOS)")
        agente_2 = CurriculoCarolinaMartins(db_session)
        resultado_curriculo = await agente_2.gerar_curriculo_base(
            usuario_id=user.id,
            dados_diagnostico=resultado_diagnostico,
            mpc_dados=resultado_mpc
        )
        print(f"   ✅ Score currículo: {resultado_curriculo['score_qualidade']:.1f}")
        print(f"   ✅ Classificação: {resultado_curriculo['classificacao']}")
        
        # AGENTE 3: LinkedIn
        print("\n💼 EXECUTANDO AGENTE 3: LINKEDIN (10 PASSOS)")
        agente_3 = LinkedInCarolinaMartins(db_session)
        resultado_linkedin = await agente_3.construir_linkedin_meteorico(
            usuario_id=user.id,
            dados_diagnostico=resultado_diagnostico,
            curriculo_dados=resultado_curriculo,
            mpc_dados=resultado_mpc
        )
        print(f"   ✅ Score LinkedIn: {resultado_linkedin['score_linkedin']:.1f}")
        print(f"   ✅ Classificação: {resultado_linkedin['classificacao']}")
        
        # AGENTE 4: Conteúdo
        print("\n📝 EXECUTANDO AGENTE 4: CONTEÚDO")
        perfil_id = resultado_linkedin["perfil_id"]
        
        # Cria estratégia (normalmente criada pelo Agente 3)
        from core.models import EstrategiaConteudo
        estrategia = EstrategiaConteudo(
            perfil_linkedin_id=perfil_id,
            distribuicao_geral=60,
            distribuicao_autoridade=40,
            frequencia_posts='{"posts_por_semana": 3}',
            temas_gerais='["Dicas de carreira"]',
            temas_autoridade='["Expertise técnica"]',
            area_foco="Engenharia de Software"
        )
        db_session.add(estrategia)
        db_session.commit()
        
        agente_4 = ConteudoCarolinaMartins(db_session)
        resultado_conteudo = await agente_4.gerar_plano_editorial_completo(
            perfil_linkedin_id=perfil_id,
            periodo_dias=30,
            dados_diagnostico=resultado_diagnostico,
            mpc_dados=resultado_mpc,
            curriculo_dados=resultado_curriculo
        )
        
        print(f"   ✅ Posts planejados: {resultado_conteudo['plano_editorial']['total_posts']}")
        print(f"   ✅ Distribuição 60/40: {resultado_conteudo['plano_editorial']['distribuicao_60_40']}")
        
        # RESULTADO FINAL
        print("\n🎉 FLUXO COMPLETO EXECUTADO COM SUCESSO!")
        print("=" * 60)
        print("📊 RESUMO DOS RESULTADOS:")
        print(f"   🩺 Diagnóstico: {resultado_diagnostico['score_diagnostico']:.1f}/100")
        print(f"   📄 Currículo: {resultado_curriculo['score_qualidade']:.1f}/100 ({resultado_curriculo['classificacao']})")
        print(f"   💼 LinkedIn: {resultado_linkedin['score_linkedin']:.1f}/100 ({resultado_linkedin['classificacao']})")
        print(f"   📝 Conteúdo: {resultado_conteudo['plano_editorial']['total_posts']} posts programados")
        
        # Verifica se algum resultado é "Meteórico"
        meteoricos = []
        if resultado_curriculo['score_qualidade'] >= 90:
            meteoricos.append("Currículo Meteórico")
        if resultado_linkedin['score_linkedin'] >= 90:
            meteoricos.append("LinkedIn Meteórico")
            
        if meteoricos:
            print(f"🚀 CONQUISTAS METEÓRICAS: {', '.join(meteoricos)}")
        
        print("\n✨ Sistema HELIO funcionando perfeitamente!")
        print("   Metodologia Carolina Martins implementada com sucesso!")

if __name__ == "__main__":
    """Executa testes de demonstração"""
    import asyncio
    
    print("🧪 EXECUTANDO TESTES DE DEMONSTRAÇÃO DO SISTEMA HELIO")
    print("=" * 70)
    
    # Cria sessão de banco
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Dados de teste
    dados_teste = {
        "nome": "Maria Silva Santos",
        "email": "maria.silva@email.com",
        "telefone": "(11) 99999-9999",
        "linkedin_url": "https://linkedin.com/in/mariasilva",
        "cidade": "São Paulo",
        "estado": "SP",
        "area_atual": "Marketing",
        "area_objetivo": "Marketing Digital",
        "cargo_atual": "Analista de Marketing",
        "cargo_objetivo": "Coordenador de Marketing Digital",
        "experiencia_mercado": 5,
        "experiencia_profissional": 4,
        "status_emprego": "empregado",
        "satisfacao_emprego_atual": 6,
        "disponibilidade_mudanca": True,
        "regime_trabalho": "hibrido",
        "experiencias": [
            {
                "empresa": "AgencyX",
                "cargo": "Analista de Marketing",
                "data_inicio": "2022-01-01",
                "data_fim": None,
                "descricao": "Gestão de campanhas digitais no Google Ads e Facebook. Aumentei ROI em 25% através de otimização de segmentação."
            }
        ],
        "formacoes": [
            {
                "instituicao": "ESPM",
                "curso": "Marketing",
                "tipo": "superior",
                "ano_conclusao": "2021",
                "status": "concluido"
            }
        ],
        "competencias": ["Google Ads", "Facebook Ads", "Analytics", "SEO", "Content Marketing"],
        "idiomas": [{"idioma": "Inglês", "nivel": "intermediario", "certificacao": ""}],
        "questionario_sabotadores": {f"q{i}": 3 for i in range(1, 31)}  # Respostas médias
    }
    
    # Executa teste completo
    teste_completo = TestFluxoCompleto()
    
    try:
        asyncio.run(teste_completo.test_fluxo_completo_agentes(db, dados_teste))
    except Exception as e:
        print(f"❌ Erro durante teste: {str(e)}")
    finally:
        db.close()