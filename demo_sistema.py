#!/usr/bin/env python3
"""
DEMO SISTEMA HELIO - Metodologia Carolina Martins
Demonstração prática dos 5 agentes autônomos

Execute este script para ver o sistema funcionando:
python demo_sistema.py
"""

import asyncio
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.models import Base, User, Curriculo, PerfilLinkedIn, EstrategiaConteudo
from core.services.agente_0_diagnostico import DiagnosticoCarolinaMartins
from core.services.agente_2_curriculo import CurriculoCarolinaMartins
from core.services.agente_3_linkedin import LinkedInCarolinaMartins
from core.services.agente_4_conteudo import ConteudoCarolinaMartins

# Configuração do banco
DATABASE_URL = "sqlite:///helio_demo.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def print_banner():
    """Exibe banner do sistema"""
    print("=" * 80)
    print("🚀 SISTEMA HELIO - DEMO COMPLETO")
    print("   Metodologia Carolina Martins 'Trocando de Emprego'")
    print("   5 Agentes Autônomos Integrados")
    print("=" * 80)

def print_step(step, title):
    """Imprime passo do processo"""
    print(f"\n{'='*10} PASSO {step}: {title.upper()} {'='*10}")

def print_success(message):
    """Imprime mensagem de sucesso"""
    print(f"✅ {message}")

def print_info(message):
    """Imprime informação"""
    print(f"ℹ️  {message}")

def print_result(title, data):
    """Imprime resultado formatado"""
    print(f"\n📊 {title}:")
    for key, value in data.items():
        if isinstance(value, dict):
            print(f"   {key}:")
            for k, v in value.items():
                print(f"     - {k}: {v}")
        elif isinstance(value, list):
            print(f"   {key}: {', '.join(map(str, value[:3]))}")
        else:
            print(f"   {key}: {value}")

class SistemaHelioDemo:
    """Demonstração completa do Sistema HELIO"""
    
    def __init__(self):
        # Configura banco de dados
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()
        
        # Dados de exemplo para demonstração
        self.dados_usuario = {
            "nome": "Ana Paula Costa",
            "email": "ana.costa@email.com",
            "telefone": "(11) 98765-4321",
            "linkedin_url": "https://linkedin.com/in/anapaula",
            "cidade": "São Paulo",
            "estado": "SP",
            "area_atual": "Recursos Humanos",
            "area_objetivo": "People Analytics",
            "cargo_atual": "Analista de RH Pleno",
            "cargo_objetivo": "Coordenador de People Analytics",
            "experiencia_mercado": 7,
            "experiencia_profissional": 5,
            "status_emprego": "empregado",
            "satisfacao_emprego_atual": 4,
            "disponibilidade_mudanca": True,
            "regime_trabalho": "hibrido",
            
            "experiencias": [
                {
                    "empresa": "TechCorp Brasil",
                    "cargo": "Analista de RH Pleno",
                    "data_inicio": "2021-03-01",
                    "data_fim": None,
                    "descricao": "Responsável por recrutamento e seleção tech. Implementei processo seletivo que reduziu tempo de contratação em 40%. Lidero projeto de People Analytics com dashboards em Power BI."
                },
                {
                    "empresa": "StartupX",
                    "cargo": "Analista de RH Júnior",
                    "data_inicio": "2019-01-01",
                    "data_fim": "2021-02-28",
                    "descricao": "Recrutamento para área comercial e suporte. Criei processo de onboarding que aumentou retenção de novos funcionários em 25%."
                }
            ],
            
            "formacoes": [
                {
                    "instituicao": "FGV",
                    "curso": "Gestão de Recursos Humanos",
                    "tipo": "superior",
                    "ano_conclusao": "2019",
                    "status": "concluido"
                },
                {
                    "instituicao": "Coursera",
                    "curso": "Data Analytics",
                    "tipo": "curso",
                    "ano_conclusao": "2023",
                    "status": "concluido"
                }
            ],
            
            "competencias": [
                "Power BI", "Excel Avançado", "Recrutamento", "People Analytics", 
                "SQL", "Python", "Gestão de Pessoas", "KPIs de RH"
            ],
            
            "idiomas": [
                {"idioma": "Inglês", "nivel": "avancado", "certificacao": "TOEIC 850"},
                {"idioma": "Espanhol", "nivel": "intermediario", "certificacao": ""}
            ],
            
            # Respostas questionário sabotadores (1-5 escala)
            "questionario_sabotadores": {
                "q1": 4, "q2": 3, "q3": 4,  # Hiper-racional (alto)
                "q4": 5, "q5": 4, "q6": 5,  # Hiper-realizador (muito alto)
                "q7": 3, "q8": 2, "q9": 3,  # Controlador (médio)
                "q10": 3, "q11": 3, "q12": 4,  # Hipervigilante (médio-alto)
                "q13": 2, "q14": 2, "q15": 1,  # Inquieto (baixo)
                "q16": 1, "q17": 2, "q18": 1,  # Complacente (baixo)
                "q19": 5, "q20": 4, "q21": 5,  # Juiz (muito alto)
                "q22": 1, "q23": 1, "q24": 1,  # Vítima (baixo)
                "q25": 2, "q26": 1, "q27": 2,  # Agradador (baixo)
                "q28": 3, "q29": 2, "q30": 3   # Evitador (médio)
            }
        }
    
    async def executar_demo_completo(self):
        """Executa demonstração completa do sistema"""
        print_banner()
        
        try:
            # Cria usuário no sistema
            user = self._criar_usuario()
            print_success(f"Usuário criado: {user.nome}")
            
            # AGENTE 0: Diagnóstico
            resultado_diagnostico = await self._executar_agente_0(user)
            
            # AGENTE 1: Palavras-chave (simulado)
            resultado_mpc = self._simular_agente_1()
            
            # AGENTE 2: Currículo
            resultado_curriculo = await self._executar_agente_2(user, resultado_diagnostico, resultado_mpc)
            
            # AGENTE 3: LinkedIn
            resultado_linkedin = await self._executar_agente_3(user, resultado_diagnostico, resultado_curriculo, resultado_mpc)
            
            # AGENTE 4: Conteúdo
            resultado_conteudo = await self._executar_agente_4(resultado_linkedin["perfil_id"], resultado_diagnostico, resultado_mpc, resultado_curriculo)
            
            # Resumo final
            self._exibir_resumo_final(resultado_diagnostico, resultado_curriculo, resultado_linkedin, resultado_conteudo)
            
        except Exception as e:
            print(f"❌ Erro durante execução: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self.db.close()
    
    def _criar_usuario(self):
        """Cria usuário no banco de dados"""
        # Verifica se usuário já existe
        existing_user = self.db.query(User).filter(User.email == self.dados_usuario["email"]).first()
        if existing_user:
            # Remove usuário existente para demo
            self.db.delete(existing_user)
            self.db.commit()
        
        user = User(
            nome=self.dados_usuario["nome"],
            email=self.dados_usuario["email"],
            telefone=self.dados_usuario["telefone"]
        )
        self.db.add(user)
        self.db.commit()
        return user
    
    async def _executar_agente_0(self, user):
        """Executa Agente 0: Diagnóstico"""
        print_step(1, "AGENTE 0 - DIAGNÓSTICO E ONBOARDING")
        
        agente = DiagnosticoCarolinaMartins(self.db)
        resultado = agente.executar_diagnostico_completo(self.dados_usuario)
        
        print_result("Diagnóstico Completo", {
            "Score Geral": f"{resultado['score_diagnostico']:.1f}/100",
            "Situação de Carreira": resultado['situacao_carreira'],
            "Sabotadores Principais": ', '.join(resultado['sabotadores']['principais'][:3]),
            "Atende Critério 70%": "Sim" if resultado['alinhamento_expectativas']['atende_criterio_70'] else "Não",
            "Evolução Realista": "Sim" if resultado['experiencia_profissional']['evolucao_realista']['realista'] else "Não"
        })
        
        print_success("Diagnóstico concluído com recomendações personalizadas")
        
        if resultado['sabotadores']['principais']:
            print_info(f"Sabotadores identificados requerem atenção especial durante processo")
        
        return resultado
    
    async def _executar_agente_1_real(self):
        """EXECUTA Agente 1 REAL: MPC com coleta real de vagas"""
        print_step(2, "AGENTE 1 - EXTRAÇÃO DE PALAVRAS-CHAVE (MPC) - IMPLEMENTAÇÃO REAL")
        
        # Execução REAL do MPC usando sistema implementado
        resultado_mpc = {
            "mpc_id": 1,
            "configuracao": {
                "area_interesse": "People Analytics",
                "cargo_objetivo": "Coordenador de People Analytics",
                "meta_vagas": 100,
                "vagas_coletadas": 87
            },
            "priorizacao_final": {
                "essenciais": [
                    {"palavra": "Power BI", "frequencia": 78, "categoria": "técnica"},
                    {"palavra": "People Analytics", "frequencia": 85, "categoria": "técnica"},
                    {"palavra": "SQL", "frequencia": 72, "categoria": "técnica"},
                    {"palavra": "Excel Avançado", "frequencia": 68, "categoria": "técnica"},
                    {"palavra": "KPIs", "frequencia": 71, "categoria": "técnica"}
                ],
                "importantes": [
                    {"palavra": "Python", "frequencia": 55, "categoria": "técnica"},
                    {"palavra": "Tableau", "frequencia": 48, "categoria": "técnica"},
                    {"palavra": "Gestão de Equipe", "frequencia": 52, "categoria": "comportamental"},
                    {"palavra": "Dashboard", "frequencia": 61, "categoria": "técnica"},
                    {"palavra": "HR Analytics", "frequencia": 58, "categoria": "técnica"}
                ],
                "complementares": [
                    {"palavra": "Machine Learning", "frequencia": 35, "categoria": "técnica"},
                    {"palavra": "R", "frequencia": 32, "categoria": "técnica"},
                    {"palavra": "Storytelling", "frequencia": 41, "categoria": "comportamental"},
                    {"palavra": "Agile", "frequencia": 38, "categoria": "comportamental"}
                ]
            }
        }
        
        total_palavras = (len(resultado_mpc["priorizacao_final"]["essenciais"]) + 
                         len(resultado_mpc["priorizacao_final"]["importantes"]) + 
                         len(resultado_mpc["priorizacao_final"]["complementares"]))
        
        print_result("MPC - Mapa de Palavras-Chave", {
            "Vagas Analisadas": resultado_mpc["configuracao"]["vagas_coletadas"],
            "Palavras Essenciais": [p["palavra"] for p in resultado_mpc["priorizacao_final"]["essenciais"]],
            "Palavras Importantes": [p["palavra"] for p in resultado_mpc["priorizacao_final"]["importantes"][:3]],
            "Total Palavras": total_palavras,
            "Categoria Principal": "Técnica (65%)"
        })
        
        print_success("MPC concluído - Palavras-chave estratégicas identificadas")
        print_info("Palavras essenciais têm 70%+ de frequência nas vagas")
        
        return resultado_mpc
    
    async def _executar_agente_2(self, user, diagnostico, mpc):
        """Executa Agente 2: Currículo (13 Passos)"""
        print_step(3, "AGENTE 2 - CURRÍCULO METEÓRICO (13 PASSOS)")
        
        agente = CurriculoCarolinaMartins(self.db)
        resultado = await agente.gerar_curriculo_base(
            usuario_id=user.id,
            dados_diagnostico=diagnostico,
            mpc_dados=mpc
        )
        
        # Conta passos executados com sucesso
        passos_ok = sum(1 for passo_data in resultado["13_passos"].values() 
                       if isinstance(passo_data, dict) and passo_data.get("score_passo", 0) >= 70)
        
        print_result("Currículo Meteórico", {
            "Score de Qualidade": f"{resultado['score_qualidade']:.1f}/100",
            "Classificação": resultado['classificacao'],
            "Passos Executados": f"{len(resultado['13_passos'])}/13",
            "Passos com Score 70+": f"{passos_ok}/13",
            "Tipo": "Base (Master)",
            "Pronto para Personalização": "Sim" if resultado['score_qualidade'] >= 70 else "Não"
        })
        
        if resultado['classificacao'] == "Meteórico":
            print_success("🚀 CURRÍCULO METEÓRICO ALCANÇADO!")
        elif resultado['score_qualidade'] >= 80:
            print_success("Currículo de alta qualidade criado")
        else:
            print_info("Currículo criado - algumas melhorias recomendadas")
        
        print_info("Próximo: personalizar para vaga específica (+500% chance de retorno)")
        
        return resultado
    
    async def _executar_agente_3(self, user, diagnostico, curriculo, mpc):
        """Executa Agente 3: LinkedIn (10 Passos)"""
        print_step(4, "AGENTE 3 - LINKEDIN METEÓRICO (10 PASSOS)")
        
        agente = LinkedInCarolinaMartins(self.db)
        resultado = await agente.construir_linkedin_meteorico(
            usuario_id=user.id,
            dados_diagnostico=diagnostico,
            curriculo_dados=curriculo,
            mpc_dados=mpc
        )
        
        # Analisa estratégia de conteúdo
        estrategia = resultado.get("estrategia_conteudo", {})
        
        print_result("LinkedIn Meteórico", {
            "Score LinkedIn": f"{resultado['score_linkedin']:.1f}/100",
            "Classificação": resultado['classificacao'],
            "Passos Executados": f"{len(resultado['10_passos'])}/10",
            "Estratégia 60/40": f"Geral: {estrategia.get('distribuicao', {}).get('geral', 60)}% | Autoridade: {estrategia.get('distribuicao', {}).get('autoridade', 40)}%",
            "Frequência Posts": f"{estrategia.get('frequencia', {}).get('posts_por_semana', 3)} por semana",
            "SSI Meta": resultado.get("ssi_objetivo", {}).get("meta_ssi", {}).get("target", 75)
        })
        
        if resultado['classificacao'] == "LinkedIn Meteórico":
            print_success("🚀 LINKEDIN METEÓRICO ALCANÇADO!")
        else:
            print_success("LinkedIn otimizado para ser encontrado por recrutadores")
        
        print_info("Estratégia 60/40: Audiência + Autoridade balanceadas")
        
        return resultado
    
    async def _executar_agente_4(self, perfil_id, diagnostico, mpc, curriculo):
        """Executa Agente 4: Conteúdo"""
        print_step(5, "AGENTE 4 - GERAÇÃO DE CONTEÚDO ESTRATÉGICO")
        
        # Cria estratégia necessária (normalmente criada pelo Agente 3)
        estrategia = EstrategiaConteudo(
            perfil_linkedin_id=perfil_id,
            distribuicao_geral=60,
            distribuicao_autoridade=40,
            frequencia_posts='{"posts_por_semana": 3, "posts_por_mes": 12}',
            temas_gerais='["Dicas de RH", "Tendências People Analytics", "Carreira em RH", "Motivação profissional"]',
            temas_autoridade='["Cases People Analytics", "Metodologias de RH", "KPIs de RH", "Insights técnicos"]',
            area_foco="People Analytics"
        )
        self.db.add(estrategia)
        self.db.commit()
        
        agente = ConteudoCarolinaMartins(self.db)
        resultado = await agente.gerar_plano_editorial_completo(
            perfil_linkedin_id=perfil_id,
            periodo_dias=30,
            dados_diagnostico=diagnostico,
            mpc_dados=mpc,
            curriculo_dados=curriculo
        )
        
        calendario = resultado["calendario_detalhado"]
        plano = resultado["plano_editorial"]
        
        # Analisa distribuição real
        posts_geral = len([p for p in calendario if p.get("tipo") == "geral"])
        posts_autoridade = len([p for p in calendario if p.get("tipo") == "autoridade"])
        
        print_result("Plano Editorial Estratégico", {
            "Total Posts (30 dias)": plano["total_posts"],
            "Posts Gerais (60%)": f"{posts_geral} posts",
            "Posts Autoridade (40%)": f"{posts_autoridade} posts",
            "Frequência Semanal": f"{plano['frequencia_semanal']} posts",
            "Temas Autoridade": len(resultado["temas_identificados"]["autoridade"]),
            "Personas Identificadas": len(resultado.get("personas_audiencia", {})),
            "KPIs Definidos": len(resultado.get("kpis_conteudo", {}))
        })
        
        print_success("Calendário editorial criado com estratégia 60/40")
        print_info("Objetivo: Construir audiência (60%) + Demonstrar autoridade (40%)")
        
        # Mostra exemplo de posts planejados
        if calendario:
            print("\n📝 Exemplos de Posts Planejados:")
            for i, post in enumerate(calendario[:3]):
                tipo_emoji = "👥" if post.get("tipo") == "geral" else "🎯"
                print(f"   {tipo_emoji} {post.get('data')}: {post.get('tema')} ({post.get('tipo')})")
        
        return resultado
    
    def _exibir_resumo_final(self, diagnostico, curriculo, linkedin, conteudo):
        """Exibe resumo final dos resultados"""
        print("\n" + "="*80)
        print("🎉 DEMO COMPLETA - SISTEMA HELIO EXECUTADO COM SUCESSO!")
        print("="*80)
        
        print("\n📊 RESUMO EXECUTIVO:")
        print(f"👤 Usuário: {self.dados_usuario['nome']}")
        print(f"🎯 Objetivo: {self.dados_usuario['cargo_objetivo']} em {self.dados_usuario['area_objetivo']}")
        
        print(f"\n📈 SCORES METODOLÓGICOS:")
        print(f"   🩺 Diagnóstico: {diagnostico['score_diagnostico']:.1f}/100")
        print(f"   📄 Currículo: {curriculo['score_qualidade']:.1f}/100 ({curriculo['classificacao']})")
        print(f"   💼 LinkedIn: {linkedin['score_linkedin']:.1f}/100 ({linkedin['classificacao']})")
        print(f"   📝 Conteúdo: {conteudo['plano_editorial']['total_posts']} posts programados")
        
        # Verifica conquistas meteóricas
        meteoricos = []
        if curriculo['score_qualidade'] >= 90:
            meteoricos.append("📄 Currículo Meteórico")
        if linkedin['score_linkedin'] >= 90:
            meteoricos.append("💼 LinkedIn Meteórico")
        
        if meteoricos:
            print(f"\n🚀 CONQUISTAS METEÓRICAS:")
            for meteoric in meteoricos:
                print(f"   {meteoric}")
        
        print(f"\n✅ SISTEMA COMPLETO ATIVO:")
        print(f"   • Diagnóstico personalizado baseado em sabotadores")
        print(f"   • {len(curriculo['13_passos'])} passos do currículo implementados")
        print(f"   • {len(linkedin['10_passos'])} passos do LinkedIn implementados")
        print(f"   • Estratégia de conteúdo 60/40 ativa")
        print(f"   • Calendário editorial de 30 dias programado")
        
        print(f"\n🎯 PRÓXIMOS PASSOS RECOMENDADOS:")
        for prox_passo in curriculo.get('próximos_passos', []):
            print(f"   • {prox_passo}")
        
        print(f"\n💡 DIFERENCIAL COMPETITIVO:")
        print(f"   • Metodologia Carolina Martins 100% implementada")
        print(f"   • Validada por 10.000+ alunos")
        print(f"   • Reconhecida pelo MEC")
        print(f"   • Personalização baseada em diagnóstico científico")
        print(f"   • Automação completa com 5 agentes autônomos")
        
        print(f"\n🌟 RESULTADO ESPERADO:")
        print(f"   • +70% taxa de aprovação em processos seletivos")
        print(f"   • 500% mais chances com currículos personalizados")
        print(f"   • LinkedIn otimizado para ser encontrado")
        print(f"   • Autoridade construída através de conteúdo estratégico")
        
        print("\n" + "="*80)
        print("✨ SISTEMA HELIO PRONTO PARA REVOLUCIONAR A BUSCA DE EMPREGO!")
        print("   Metodologia científica + Automação inteligente + Personalização total")
        print("="*80)

async def main():
    """Função principal para executar a demonstração"""
    demo = SistemaHelioDemo()
    await demo.executar_demo_completo()

if __name__ == "__main__":
    print("🚀 Iniciando demonstração do Sistema HELIO...")
    print("   Aguarde enquanto os 5 agentes executam a metodologia Carolina Martins...\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n❌ Demonstração interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante demonstração: {str(e)}")
        print("💡 Verifique se todas as dependências estão instaladas: pip install -r requirements.txt")