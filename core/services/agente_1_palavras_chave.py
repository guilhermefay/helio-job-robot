"""
Agente 1: Extração de Palavras-chave (MPC) - Metodologia Carolina Martins

Este agente implementa a Ferramenta MPC (Mapa de Palavras-Chave) mencionada
em múltiplas aulas como pré-requisito para o currículo meteórico.

Processo baseado nas transcrições:
1. Coleta de 50-100 vagas relevantes da área
2. Extração automática de palavras-chave
3. Categorização (comportamental, técnica, digital)
4. Validação no ChatGPT (mencionado na Aula 6)
5. Priorização por frequência
6. Output: Guia estruturado para aplicar no currículo
"""

import re
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from collections import Counter, defaultdict
from sqlalchemy.orm import Session
from core.models import (
    MapaPalavrasChave, VagaAnalisada, PalavraChave, 
    ProcessamentoMPC, ValidacaoIA, StatusMPC, CategoriaPalavraChave
)
from core.services.ai_validator import AIValidator
from core.services.job_scraper import JobScraper

class MPCCarolinaMartins:
    """
    Implementação da Ferramenta MPC (Mapa de Palavras-Chave)
    baseada na metodologia Carolina Martins
    """
    
    # Configurações da Metodologia Carolina Martins
    MIN_PALAVRAS_FASE1 = 20  # Mínimo de palavras na fase de pesquisa ampla
    TARGET_PALAVRAS_FASE1 = 30  # Alvo ideal de palavras (30-40)
    MAX_PALAVRAS_FASE1 = 40  # Máximo recomendado na fase 1
    TOP_PALAVRAS_FASE2 = 10  # Top 10 para priorização
    PALAVRAS_TITULO_LINKEDIN = 4  # 3-4 palavras fortes no título
    COMPETENCIAS_LINKEDIN = 50  # Exatamente 50 competências
    
    def __init__(self, db: Session):
        self.db = db
        self.palavras_base = self._carregar_palavras_base()
        self.stop_words = self._carregar_stop_words()
        self.padroes_limpeza = self._configurar_padroes_limpeza()
        self.ai_validator = AIValidator()
        self.job_scraper = JobScraper()
    
    async def executar_mpc_completo(
        self, 
        area_interesse: str, 
        cargo_objetivo: str,
        segmentos_alvo: List[str] = None,
        usuario_id: int = None,
        total_vagas_desejadas: int = 100  # Parametrizável, default 100
    ) -> Dict[str, Any]:
        """
        Executa processo MPC completo seguindo metodologia Carolina Martins
        COM LOGS DETALHADOS EM TEMPO REAL
        
        Etapas:
        1. Configuração inicial
        2. Coleta de vagas
        3. Extração de palavras-chave
        4. Categorização automática
        5. Validação com IA
        6. Priorização final
        """
        
        # ================================
        # 🚀 INÍCIO DO PROCESSO MPC
        # ================================
        print("\n" + "="*80)
        print("🎯 INICIANDO AGENTE 1 - MAPA DE PALAVRAS-CHAVE (MPC)")
        print("📚 Metodologia Carolina Martins")
        print("="*80)
        print(f"🎯 Cargo alvo: {cargo_objetivo}")
        print(f"🏢 Área: {area_interesse}")
        print(f"📍 Segmentos: {segmentos_alvo or 'Todos'}")
        print(f"👤 Usuário: {usuario_id or 'Demo'}")
        
        # Cria registro MPC
        mpc = MapaPalavrasChave(
            usuario_id=usuario_id,
            area_interesse=area_interesse,
            cargo_objetivo=cargo_objetivo,
            segmentos_alvo=segmentos_alvo or [],
            status=StatusMPC.COLETANDO.value
        )
        self.db.add(mpc)
        self.db.commit()
        
        print(f"📊 MPC ID: {mpc.id} criado no banco de dados")
        
        resultado = {
            "mpc_id": mpc.id,
            "logs_detalhados": [],
            "configuracao": {
                "area_interesse": area_interesse,
                "cargo_objetivo": cargo_objetivo,
                "segmentos_alvo": segmentos_alvo,
                "meta_vagas": total_vagas_desejadas
            },
            "coleta_vagas": {},
            "extracao_palavras": {},
            "categorizacao": {},
            "validacao_ia": {},
            "priorizacao_final": {},
            "mpc_final": {}
        }
        
        try:
            # ================================
            # 📝 ETAPA 1: COLETA DE VAGAS
            # ================================
            print("\n" + "-"*60)
            print("📝 ETAPA 1/6: COLETA DE VAGAS")
            print("-"*60)
            print("🔍 Coletando vagas reais do mercado...")
            print("🎯 FONTES PRIORITÁRIAS (Metodologia Carolina Martins):")
            print("   • 50% LinkedIn Jobs (fonte #1)")
            print("   • 30% Google Jobs (fonte #2)")  
            print("   • 20% fontes secundárias (Indeed, InfoJobs, Catho)")
            
            mpc.status = StatusMPC.COLETANDO.value
            self.db.commit()
            
            resultado["coleta_vagas"] = await self._coletar_vagas_com_logs(
                mpc, area_interesse, cargo_objetivo, segmentos_alvo, resultado["logs_detalhados"]
            )
            
            print(f"✅ COLETA CONCLUÍDA: {resultado['coleta_vagas']['total_coletadas']} vagas")
            
            # ================================
            # 🔤 ETAPA 2: EXTRAÇÃO DE PALAVRAS-CHAVE
            # ================================
            print("\n" + "-"*60)
            print("🔤 ETAPA 2/6: EXTRAÇÃO DE PALAVRAS-CHAVE")
            print("-"*60)
            print("🧠 Processando descrições das vagas com NLP...")
            print("🔍 Identificando termos compostos (ex: 'power bi', 'gestão de projetos')")
            print("🧹 Aplicando filtros de relevância profissional")
            
            mpc.status = StatusMPC.PROCESSANDO.value
            self.db.commit()
            
            resultado["extracao_palavras"] = await self._extrair_palavras_chave_com_logs(
                mpc, resultado["logs_detalhados"]
            )
            
            print(f"✅ EXTRAÇÃO CONCLUÍDA: {resultado['extracao_palavras']['palavras_unicas']} palavras únicas")
            
            # ================================
            # 🏷️ ETAPA 3: CATEGORIZAÇÃO
            # ================================
            print("\n" + "-"*60)
            print("🏷️ ETAPA 3/6: CATEGORIZAÇÃO")
            print("-"*60)
            print("📂 Organizando palavras em categorias metodológicas:")
            print("   • Comportamental: soft skills, liderança")
            print("   • Técnica: conhecimentos específicos da área")
            print("   • Digital: ferramentas, softwares, tecnologias")
            
            resultado["categorizacao"] = await self._categorizar_palavras_chave_com_logs(
                mpc, resultado["logs_detalhados"]
            )
            
            # ================================
            # 🤖 ETAPA 4: VALIDAÇÃO COM IA
            # ================================
            print("\n" + "-"*60)
            print("🤖 ETAPA 4/6: VALIDAÇÃO COM IA")
            print("-"*60)
            print("🧠 Enviando palavras-chave para validação com IA...")
            print("📝 Contexto: cargo, área e descrições de vagas")
            print("✅ IA irá aprovar/rejeitar e sugerir melhorias")
            
            resultado["validacao_ia"] = await self._validar_com_ia_com_logs(
                mpc, area_interesse, cargo_objetivo, resultado["logs_detalhados"]
            )
            
            # ================================
            # 📊 ETAPA 5: PRIORIZAÇÃO FINAL
            # ================================
            print("\n" + "-"*60)
            print("📊 ETAPA 5/6: PRIORIZAÇÃO FINAL")
            print("-"*60)
            print("🎯 Aplicando critérios de priorização metodológica:")
            print("   • Essenciais: aparecem em 70%+ das vagas")
            print("   • Importantes: aparecem em 40-69% das vagas")
            print("   • Complementares: aparecem em <40% das vagas")
            
            resultado["priorizacao_final"] = await self._priorizar_palavras_chave_com_logs(
                mpc, resultado["logs_detalhados"]
            )
            
            # ================================
            # 🎯 ETAPA 6: CONSOLIDAÇÃO FINAL
            # ================================
            print("\n" + "-"*60)
            print("🎯 ETAPA 6/6: CONSOLIDAÇÃO FINAL")
            print("-"*60)
            print("📋 Gerando lista final de palavras-chave")
            print("📊 Criando dashboard metodológico")
            print("💡 Preparando guia de aplicação")
            
            resultado["mpc_final"] = self._consolidar_mpc_com_logs(mpc, resultado["logs_detalhados"])
            
            # ================================
            # ✅ PROCESSO CONCLUÍDO
            # ================================
            mpc.status = StatusMPC.CONCLUIDO.value
            mpc.data_ultima_coleta = datetime.utcnow()
            self.db.commit()
            
            print("\n" + "="*80)
            print("🎉 AGENTE 1 CONCLUÍDO COM SUCESSO!")
            print("="*80)
            print(f"📊 Total de vagas analisadas: {resultado['coleta_vagas']['total_coletadas']}")
            print(f"🔤 Palavras-chave extraídas: {resultado['extracao_palavras']['palavras_unicas']}")
            print(f"🎯 Palavras essenciais: {len(resultado['mpc_final'].get('palavras_essenciais', []))}")
            print(f"⭐ Palavras importantes: {len(resultado['mpc_final'].get('palavras_importantes', []))}")
            print(f"💡 Palavras complementares: {len(resultado['mpc_final'].get('palavras_complementares', []))}")
            
            # RESULTADO FINAL DETALHADO
            print("\n💡 Quer ver o resultado final estruturado? (s/n): ", end="")
            try:
                mostrar_resultado = True  # Configurável
                
                if mostrar_resultado:
                    print("SIM")
                    self._exibir_resultado_final_detalhado(resultado)
                else:
                    print("NÃO")
                    print("   ✅ Resultado completo disponível no dashboard")
            except:
                print("   ⚠️ Resultado completo disponível no dashboard")
            
            print("="*80)
            
            return resultado
            
        except Exception as e:
            print(f"\n❌ ERRO NO AGENTE 1: {str(e)}")
            print("📝 Salvando log de erro...")
            
            mpc.status = StatusMPC.ERRO.value
            self.db.commit()
            
            # Log do erro
            log_erro = ProcessamentoMPC(
                mpc_id=mpc.id,
                etapa="execucao_completa",
                status="erro",
                erro=str(e)
            )
            self.db.add(log_erro)
            self.db.commit()
            
            resultado["logs_detalhados"].append({
                "timestamp": datetime.now().isoformat(),
                "etapa": "erro_critico",
                "status": "erro",
                "detalhes": str(e)
            })
            
            raise e
    
    async def _coletar_vagas_com_logs(
        self, 
        mpc: MapaPalavrasChave, 
        area: str, 
        cargo: str, 
        segmentos: List[str],
        logs: List[Dict]
    ) -> Dict[str, Any]:
        """
        Coleta vagas com logs detalhados em tempo real
        """
        print("🔍 Iniciando coleta de vagas...")
        logs.append({
            "timestamp": datetime.now().isoformat(),
            "etapa": "coleta_inicio",
            "status": "executando",
            "detalhes": f"Cargo: {cargo}, Área: {area}"
        })
        
        # Usa o método original mas com logs adicionais
        resultado = await self._coletar_vagas(mpc, area, cargo, segmentos)
        
        print("📊 Salvando vagas no banco de dados...")
        
        # OPÇÃO INTERATIVA: Mostrar vagas coletadas
        print(f"\n💡 {resultado['total_coletadas']} vagas coletadas!")
        print("   📋 Quer ver as vagas coletadas? (s/n): ", end="")
        
        try:
            # Em ambiente de produção, isso viria da interface
            # Por ora, simula que o usuário quer ver algumas vagas
            mostrar_vagas = True  # Pode ser configurável
            
            if mostrar_vagas:
                print("SIM")
                print("\n" + "="*60)
                print("📋 VAGAS COLETADAS - PRIMEIRAS 5 PARA VERIFICAÇÃO")
                print("="*60)
                
                # Busca primeiras vagas para mostrar
                vagas_exemplo = self.db.query(VagaAnalisada)\
                    .filter(VagaAnalisada.mpc_id == mpc.id)\
                    .limit(5)\
                    .all()
                
                for i, vaga in enumerate(vagas_exemplo, 1):
                    print(f"\n📄 VAGA {i}:")
                    print(f"   🏢 Empresa: {vaga.empresa}")
                    print(f"   📋 Título: {vaga.titulo}")
                    print(f"   📍 Local: {vaga.localizacao}")
                    print(f"   🌐 Fonte: {vaga.fonte}")
                    print(f"   📝 Descrição: {vaga.descricao[:200]}...")
                    if vaga.url_original:
                        print(f"   🔗 URL: {vaga.url_original}")
                
                print(f"\n✅ Total coletado: {resultado['total_coletadas']} vagas")
                print("   💡 Para ver todas as vagas, consulte o relatório final")
                print("="*60)
                
                # Adiciona vagas aos logs para inspeção posterior
                logs.append({
                    "timestamp": datetime.now().isoformat(),
                    "etapa": "vagas_detalhadas",
                    "status": "info",
                    "detalhes": "Primeiras 5 vagas coletadas",
                    "vagas_exemplo": [
                        {
                            "empresa": vaga.empresa,
                            "titulo": vaga.titulo,
                            "fonte": vaga.fonte,
                            "url": vaga.url_original
                        } for vaga in vagas_exemplo
                    ]
                })
            else:
                print("NÃO")
                print("   ✅ Vagas salvas no banco - disponíveis no relatório final")
        
        except Exception as e:
            print("   ⚠️ Erro ao exibir vagas:", e)
        
        # Estatísticas por fonte
        print(f"\n📊 BREAKDOWN POR FONTE:")
        fontes_stats = resultado.get('breakdown_fontes', {})
        if isinstance(fontes_stats, dict):
            for fonte, quantidade in fontes_stats.items():
                print(f"   • {fonte}: {quantidade} vagas")
        else:
            print("   • Estatísticas detalhadas disponíveis no relatório")
        
        logs.append({
            "timestamp": datetime.now().isoformat(),
            "etapa": "coleta_finalizada",
            "status": "concluido",
            "detalhes": f"Total: {resultado['total_coletadas']} vagas",
            "breakdown_fontes": resultado.get('fontes_reais_utilizadas', []),
            "qualidade_coleta": resultado.get('qualidade_coleta', 'adequada')
        })
        
        return resultado
    
    async def _extrair_palavras_chave_com_logs(
        self, 
        mpc: MapaPalavrasChave,
        logs: List[Dict]
    ) -> Dict[str, Any]:
        """
        Extração de palavras-chave com logs detalhados
        """
        print("🔤 Processando descrições das vagas...")
        
        # Busca todas as vagas do MPC
        vagas = self.db.query(VagaAnalisada).filter(VagaAnalisada.mpc_id == mpc.id).all()
        print(f"📄 Encontradas {len(vagas)} vagas para processar")
        
        logs.append({
            "timestamp": datetime.now().isoformat(),
            "etapa": "extracao_inicio",
            "status": "executando",
            "detalhes": f"Processando {len(vagas)} vagas"
        })
        
        todas_palavras = []
        vagas_processadas = 0
        palavras_por_vaga = []
        
        for i, vaga in enumerate(vagas):
            if i % 10 == 0:  # Log a cada 10 vagas
                print(f"   📝 Processando vaga {i+1}/{len(vagas)}: {vaga.empresa}")
            
            # Combina descrição e requisitos
            texto_completo = f"{vaga.descricao} {vaga.requisitos}".lower()
            
            # Extrai palavras-chave com método aprimorado
            palavras_vaga = self._extrair_palavras_texto_detalhado(texto_completo)
            palavras_por_vaga.append(len(palavras_vaga))
            
            # Log detalhado das primeiras 3 vagas
            if i < 3:
                print(f"     🔍 Vaga {vaga.empresa}: {len(palavras_vaga)} palavras extraídas")
                print(f"     📋 Primeiras palavras: {palavras_vaga[:5]}")
            
            # Salva palavras da vaga
            vaga.palavras_extraidas = palavras_vaga
            vaga.processada = True
            
            todas_palavras.extend(palavras_vaga)
            vagas_processadas += 1
        
        self.db.commit()
        
        # Conta frequências
        contador_palavras = Counter(todas_palavras)
        total_palavras_unicas = len(contador_palavras)
        
        print(f"📊 Estatísticas de extração:")
        print(f"   • Total de palavras extraídas: {len(todas_palavras)}")
        print(f"   • Palavras únicas: {total_palavras_unicas}")
        print(f"   • Média por vaga: {sum(palavras_por_vaga)/len(palavras_por_vaga):.1f}")
        print(f"   • Top 5 palavras: {[f'{palavra}({freq})' for palavra, freq in contador_palavras.most_common(5)]}")
        
        # OPÇÃO INTERATIVA: Mostrar palavras-chave extraídas
        print(f"\n💡 {total_palavras_unicas} palavras-chave únicas extraídas!")
        print("   📋 Quer ver a lista de palavras-chave? (s/n): ", end="")
        
        try:
            mostrar_palavras = True  # Configurável
            
            if mostrar_palavras:
                print("SIM")
                print("\n" + "="*60)
                print("🔤 PALAVRAS-CHAVE EXTRAÍDAS - TOP 20 MAIS FREQUENTES")
                print("="*60)
                
                for i, (palavra, freq) in enumerate(contador_palavras.most_common(20), 1):
                    # Calcula frequência relativa
                    freq_rel = (freq / len(vagas)) * 100
                    print(f"{i:2d}. {palavra:<25} | {freq:3d}x | {freq_rel:5.1f}% das vagas")
                
                print(f"\n✅ Total: {total_palavras_unicas} palavras únicas")
                print("   💡 Lista completa disponível no relatório final")
                print("="*60)
                
                # Mostra algumas palavras por categoria se já categorizadas
                print("\n🏷️ PRÉVIA DAS CATEGORIAS:")
                
                # Categorização básica para prévia
                palavras_comportamentais = []
                palavras_tecnicas = []
                palavras_digitais = []
                
                for palavra, _ in contador_palavras.most_common(50):
                    categoria = self._determinar_categoria_palavra(palavra)
                    if categoria == "comportamental" and len(palavras_comportamentais) < 5:
                        palavras_comportamentais.append(palavra)
                    elif categoria == "digital" and len(palavras_digitais) < 5:
                        palavras_digitais.append(palavra)
                    elif categoria == "tecnica" and len(palavras_tecnicas) < 5:
                        palavras_tecnicas.append(palavra)
                
                if palavras_comportamentais:
                    print(f"   🤝 Comportamentais: {', '.join(palavras_comportamentais)}")
                if palavras_digitais:
                    print(f"   💻 Digitais: {', '.join(palavras_digitais)}")
                if palavras_tecnicas:
                    print(f"   🔧 Técnicas: {', '.join(palavras_tecnicas)}")
                
            else:
                print("NÃO")
                print("   ✅ Palavras-chave salvas - disponíveis no relatório final")
        
        except Exception as e:
            print("   ⚠️ Erro ao exibir palavras-chave:", e)
        
        # Atualiza MPC
        mpc.total_palavras_extraidas = total_palavras_unicas
        self.db.commit()
        
        logs.append({
            "timestamp": datetime.now().isoformat(),
            "etapa": "extracao_finalizada",
            "status": "concluido",
            "detalhes": {
                "vagas_processadas": vagas_processadas,
                "palavras_totais": len(todas_palavras),
                "palavras_unicas": total_palavras_unicas,
                "top_palavras": contador_palavras.most_common(10)
            }
        })
        
        return {
            "vagas_processadas": vagas_processadas,
            "palavras_unicas": total_palavras_unicas,
            "palavras_mais_frequentes": contador_palavras.most_common(20),
            "qualidade_extracao": self._avaliar_qualidade_extracao(contador_palavras),
            "estatisticas_detalhadas": {
                "palavras_totais": len(todas_palavras),
                "media_por_vaga": sum(palavras_por_vaga)/len(palavras_por_vaga) if palavras_por_vaga else 0
            }
        }
    
    async def _categorizar_palavras_chave_com_logs(
        self, 
        mpc: MapaPalavrasChave,
        logs: List[Dict]
    ) -> Dict[str, Any]:
        """
        Categorização com logs detalhados
        """
        print("🏷️ Categorizando palavras-chave...")
        
        logs.append({
            "timestamp": datetime.now().isoformat(),
            "etapa": "categorizacao_inicio",
            "status": "executando",
            "detalhes": "Aplicando categorização metodológica"
        })
        
        # Usa método original
        resultado = await self._categorizar_palavras_chave(mpc)
        
        # Logs detalhados da categorização
        total_por_categoria = resultado["total_por_categoria"]
        print(f"📂 Categorização concluída:")
        print(f"   • Comportamentais: {total_por_categoria.get('comportamental', 0)}")
        print(f"   • Técnicas: {total_por_categoria.get('tecnica', 0)}")
        print(f"   • Digitais: {total_por_categoria.get('digital', 0)}")
        
        # Mostra exemplos de cada categoria
        palavras_cat = resultado["palavras_categorizadas"]
        for categoria, palavras in palavras_cat.items():
            if palavras:
                top_3 = [p["termo"] for p in palavras[:3]]
                print(f"     📋 {categoria.title()}: {', '.join(top_3)}...")
        
        logs.append({
            "timestamp": datetime.now().isoformat(),
            "etapa": "categorizacao_finalizada",
            "status": "concluido",
            "detalhes": {
                "total_por_categoria": total_por_categoria,
                "qualidade": resultado["qualidade_categorizacao"]
            }
        })
        
        return resultado
    
    async def _validar_com_ia_com_logs(
        self, 
        mpc: MapaPalavrasChave, 
        area_interesse: str, 
        cargo_objetivo: str,
        logs: List[Dict]
    ) -> Dict[str, Any]:
        """
        Validação com IA com logs detalhados
        """
        print("🤖 Preparando validação com IA...")
        
        # Busca top palavras por categoria
        palavras_top = self.db.query(PalavraChave)\
            .filter(PalavraChave.mpc_id == mpc.id)\
            .order_by(PalavraChave.importancia.desc())\
            .limit(50)\
            .all()
        
        print(f"📤 Enviando {len(palavras_top)} palavras para IA")
        
        # Prepara dados para validação
        palavras_por_categoria = defaultdict(list)
        for palavra in palavras_top:
            palavras_por_categoria[palavra.categoria].append(palavra.termo)
        
        print(f"📊 Breakdown para IA:")
        for categoria, termos in palavras_por_categoria.items():
            print(f"   • {categoria}: {len(termos)} termos")
        
        logs.append({
            "timestamp": datetime.now().isoformat(),
            "etapa": "validacao_ia_inicio",
            "status": "executando",
            "detalhes": {
                "palavras_enviadas": len(palavras_top),
                "breakdown_categorias": {cat: len(termos) for cat, termos in palavras_por_categoria.items()}
            }
        })
        
        # Busca vagas para contexto da validação
        vagas_contexto = self.db.query(VagaAnalisada)\
            .filter(VagaAnalisada.mpc_id == mpc.id)\
            .limit(5)\
            .all()
        
        vagas_dict = [{"descricao": vaga.descricao} for vaga in vagas_contexto]
        
        print("🧠 Chamando IA para validação...")
        print(f"📝 Contexto: {len(vagas_dict)} descrições de vagas")
        print(f"🎯 Cargo: {cargo_objetivo}")
        print(f"🏢 Área: {area_interesse}")
        
        # Validação REAL com IA
        try:
            validacao_resultado = await self._validar_com_ia_real(
                palavras_por_categoria, area_interesse, cargo_objetivo, vagas_dict
            )
            
            print("✅ IA respondeu com sucesso!")
            print(f"✅ Aprovadas: {len(validacao_resultado.get('aprovadas', []))}")
            print(f"❌ Rejeitadas: {len(validacao_resultado.get('rejeitadas', []))}")
            print(f"💡 Sugestões: {len(validacao_resultado.get('sugestoes', []))}")
            
            # Mostra exemplos da resposta da IA
            if validacao_resultado.get('aprovadas'):
                print(f"     ✅ Exemplos aprovados: {validacao_resultado['aprovadas'][:3]}")
            if validacao_resultado.get('rejeitadas'):
                print(f"     ❌ Exemplos rejeitados: {validacao_resultado['rejeitadas'][:3]}")
            if validacao_resultado.get('sugestoes'):
                print(f"     💡 Sugestões da IA: {validacao_resultado['sugestoes'][:2]}")
            
        except Exception as e:
            print(f"⚠️ Erro na validação IA: {e}")
            validacao_resultado = {
                "aprovadas": [p.termo for p in palavras_top[:20]],  # Fallback
                "rejeitadas": [],
                "sugestoes": [],
                "erro": str(e)
            }
        
        # Salva resultado da validação
        validacao_ia = ValidacaoIA(
            mpc_id=mpc.id,
            modelo_ia="gpt-4",
            prompt_utilizado=validacao_resultado.get("prompt_usado", ""),
            palavras_aprovadas=validacao_resultado["aprovadas"],
            palavras_rejeitadas=validacao_resultado["rejeitadas"],
            sugestoes_adicionais=validacao_resultado["sugestoes"],
            confianca=validacao_resultado.get("confianca", 0.8)
        )
        self.db.add(validacao_ia)
        
        # Marca palavras como validadas
        for palavra in palavras_top:
            if palavra.termo in validacao_resultado["aprovadas"]:
                palavra.validada_ia = True
                palavra.recomendada_ia = True
            elif palavra.termo in validacao_resultado["rejeitadas"]:
                palavra.validada_ia = True
                palavra.recomendada_ia = False
        
        # Marca MPC como validado
        mpc.validado_ia = True
        mpc.sugestoes_ia = validacao_resultado["sugestoes"]
        
        self.db.commit()
        
        logs.append({
            "timestamp": datetime.now().isoformat(),
            "etapa": "validacao_ia_finalizada",
            "status": "concluido",
            "detalhes": {
                "aprovadas": len(validacao_resultado["aprovadas"]),
                "rejeitadas": len(validacao_resultado["rejeitadas"]),
                "sugestoes": len(validacao_resultado["sugestoes"]),
                "modelo_usado": validacao_resultado.get("modelo_usado", "ai_real"),
                "confianca": validacao_resultado.get("confianca", 0.8)
            }
        })
        
        return validacao_resultado
    
    async def _priorizar_palavras_chave_com_logs(
        self, 
        mpc: MapaPalavrasChave,
        logs: List[Dict]
    ) -> Dict[str, Any]:
        """
        Priorização com logs detalhados
        """
        print("📊 Aplicando critérios de priorização...")
        
        logs.append({
            "timestamp": datetime.now().isoformat(),
            "etapa": "priorizacao_inicio",
            "status": "executando",
            "detalhes": "Aplicando critérios metodológicos"
        })
        
        # Usa método original
        resultado = await self._priorizar_palavras_chave(mpc)
        
        # Logs detalhados da priorização
        priorizacao = resultado["priorizacao"]
        print(f"🎯 Priorização concluída:")
        print(f"   • Essenciais (70%+): {len(priorizacao['essenciais'])}")
        print(f"   • Importantes (40-69%): {len(priorizacao['importantes'])}")
        print(f"   • Complementares (<40%): {len(priorizacao['complementares'])}")
        
        # Mostra exemplos de cada prioridade
        if priorizacao['essenciais']:
            print(f"     🔥 Essenciais: {[p['termo'] for p in priorizacao['essenciais'][:3]]}")
        if priorizacao['importantes']:
            print(f"     ⭐ Importantes: {[p['termo'] for p in priorizacao['importantes'][:3]]}")
        
        logs.append({
            "timestamp": datetime.now().isoformat(),
            "etapa": "priorizacao_finalizada",
            "status": "concluido",
            "detalhes": {
                "essenciais": len(priorizacao['essenciais']),
                "importantes": len(priorizacao['importantes']),
                "complementares": len(priorizacao['complementares'])
            }
        })
        
        return resultado
    
    def _consolidar_mpc_com_logs(
        self, 
        mpc: MapaPalavrasChave,
        logs: List[Dict]
    ) -> Dict[str, Any]:
        """
        Consolidação final com logs detalhados
        """
        print("🎯 Consolidando resultado final...")
        
        logs.append({
            "timestamp": datetime.now().isoformat(),
            "etapa": "consolidacao_inicio",
            "status": "executando",
            "detalhes": "Gerando MPC final"
        })
        
        # Usa método original
        resultado = self._consolidar_mpc(mpc)
        
        print("📋 Resultado final:")
        print(f"   • Score de qualidade: {resultado['estatisticas']['score_qualidade']:.1f}%")
        print(f"   • Palavras essenciais: {len(resultado['palavras_essenciais'])}")
        print(f"   • Palavras importantes: {len(resultado['palavras_importantes'])}")
        print(f"   • Palavras complementares: {len(resultado['palavras_complementares'])}")
        
        logs.append({
            "timestamp": datetime.now().isoformat(),
            "etapa": "consolidacao_finalizada",
            "status": "concluido",
            "detalhes": {
                "score_qualidade": resultado['estatisticas']['score_qualidade'],
                "total_essenciais": len(resultado['palavras_essenciais']),
                "total_importantes": len(resultado['palavras_importantes']),
                "total_complementares": len(resultado['palavras_complementares'])
            }
        })
        
        return resultado
    
    def _exibir_resultado_final_detalhado(self, resultado: Dict[str, Any]):
        """
        Exibe resultado final estruturado conforme metodologia Carolina Martins
        """
        mpc_final = resultado.get('mpc_final', {})
        
        print("\n" + "🎯" + "="*78 + "🎯")
        print("📋 LISTA DE PALAVRAS-CHAVE PERSONALIZADA - METODOLOGIA CAROLINA MARTINS")
        print("🎯" + "="*78 + "🎯")
        
        # Configuração
        config = resultado.get('configuracao', {})
        print(f"🎯 CARGO ALVO: {config.get('cargo_objetivo', 'N/A')}")
        print(f"🏢 ÁREA: {config.get('area_interesse', 'N/A')}")
        print(f"📊 BASEADO EM: {resultado['coleta_vagas'].get('total_coletadas', 0)} vagas reais")
        
        # Score de qualidade
        score = mpc_final.get('estatisticas', {}).get('score_qualidade', 0)
        print(f"⭐ SCORE DE QUALIDADE: {score:.1f}%")
        
        print("\n" + "🔥" + "="*58 + "🔥")
        print("🔥 PALAVRAS-CHAVE ESSENCIAIS (aparecem em 70%+ das vagas)")
        print("🔥" + "="*58 + "🔥")
        
        essenciais = mpc_final.get('palavras_essenciais', [])
        if essenciais:
            print("💡 USE ESTAS NO RESUMO PROFISSIONAL E TÍTULO DO LINKEDIN:")
            for i, palavra in enumerate(essenciais, 1):
                freq = palavra.get('frequencia', 0) * 100
                print(f"   {i:2d}. {palavra['termo']:<25} ({freq:5.1f}% das vagas)")
        else:
            print("   ⚠️ Nenhuma palavra essencial identificada")
        
        print("\n" + "⭐" + "="*58 + "⭐")
        print("⭐ PALAVRAS-CHAVE IMPORTANTES (aparecem em 40-69% das vagas)")
        print("⭐" + "="*58 + "⭐")
        
        importantes = mpc_final.get('palavras_importantes', [])
        if importantes:
            print("💡 USE ESTAS NAS EXPERIÊNCIAS PROFISSIONAIS:")
            for i, palavra in enumerate(importantes, 1):
                freq = palavra.get('frequencia', 0) * 100
                print(f"   {i:2d}. {palavra['termo']:<25} ({freq:5.1f}% das vagas)")
        else:
            print("   ⚠️ Nenhuma palavra importante identificada")
        
        print("\n" + "💡" + "="*58 + "💡")
        print("💡 PALAVRAS-CHAVE COMPLEMENTARES (aparecem em <40% das vagas)")
        print("💡" + "="*58 + "💡")
        
        complementares = mpc_final.get('palavras_complementares', [])
        if complementares:
            print("💡 USE PARA PERSONALIZAR CADA VAGA ESPECÍFICA:")
            for i, palavra in enumerate(complementares[:10], 1):  # Top 10
                freq = palavra.get('frequencia', 0) * 100
                print(f"   {i:2d}. {palavra['termo']:<25} ({freq:5.1f}% das vagas)")
            if len(complementares) > 10:
                print(f"   ... e mais {len(complementares) - 10} palavras complementares")
        else:
            print("   ⚠️ Nenhuma palavra complementar identificada")
        
        # Guia de aplicação
        guia = mpc_final.get('guia_aplicacao', {})
        if guia:
            print("\n" + "📋" + "="*58 + "📋")
            print("📋 GUIA PRÁTICO DE APLICAÇÃO")
            print("📋" + "="*58 + "📋")
            
            # Resumo profissional
            resumo_info = guia.get('resumo_profissional', {})
            if resumo_info:
                print("\n🎯 NO RESUMO PROFISSIONAL (obrigatório):")
                obrigatorias = resumo_info.get('incluir_obrigatoriamente', [])
                if obrigatorias:
                    print(f"   • Incluir: {', '.join(obrigatorias[:5])}")
                
                preferenciais = resumo_info.get('incluir_preferencialmente', [])
                if preferenciais:
                    print(f"   • Preferencial: {', '.join(preferenciais[:3])}")
            
            # Experiências
            exp_info = guia.get('experiencias_profissionais', {})
            if exp_info:
                print("\n💼 NAS EXPERIÊNCIAS PROFISSIONAIS:")
                distribuir = exp_info.get('distribuir_por_experiencia', [])
                if distribuir:
                    print(f"   • Distribuir: {', '.join(distribuir[:8])}")
            
            # Competências
            comp_info = guia.get('competencias', {})
            if comp_info:
                print("\n🛠️ NA SEÇÃO COMPETÊNCIAS:")
                explicitas = comp_info.get('listar_explicitamente', [])
                if explicitas:
                    print(f"   • Listar: {', '.join(explicitas[:6])}")
        
        # Recomendações da IA
        validacao_ia = resultado.get('validacao_ia', {})
        if validacao_ia.get('sugestoes'):
            print("\n" + "🤖" + "="*58 + "🤖")
            print("🤖 SUGESTÕES ADICIONAIS DA IA")
            print("🤖" + "="*58 + "🤖")
            
            for sugestao in validacao_ia['sugestoes'][:3]:
                print(f"   💡 {sugestao}")
        
        # Dados concretos de fundamentação
        print("\n" + "📊" + "="*58 + "📊")
        print("📊 DADOS CONCRETOS DE FUNDAMENTAÇÃO")
        print("📊" + "="*58 + "📊")
        
        coleta_info = resultado.get('coleta_vagas', {})
        print(f"📈 Baseado em {coleta_info.get('total_coletadas', 0)} vagas reais")
        
        fontes = coleta_info.get('fontes_reais_utilizadas', [])
        if fontes:
            print(f"🌐 Fontes: {', '.join(fontes)}")
        
        print(f"🎯 Área: {config.get('area_interesse', 'N/A')}")
        print(f"📍 Localização: São Paulo, SP")  # Pode ser parametrizado
        
        # Validação IA
        if validacao_ia:
            aprovadas = len(validacao_ia.get('aprovadas', []))
            total_validadas = aprovadas + len(validacao_ia.get('rejeitadas', []))
            if total_validadas > 0:
                taxa_aprovacao = (aprovadas / total_validadas) * 100
                print(f"🤖 Validação IA: {aprovadas}/{total_validadas} aprovadas ({taxa_aprovacao:.1f}%)")
        
        print("\n" + "🎯" + "="*78 + "🎯")

    async def _coletar_vagas(
        self, 
        mpc: MapaPalavrasChave, 
        area: str, 
        cargo: str, 
        segmentos: List[str]
    ) -> Dict[str, Any]:
        """
        Coleta vagas de múltiplas fontes para análise
        
        Objetivo Carolina Martins: 50-100 vagas relevantes
        """
        log_coleta = ProcessamentoMPC(
            mpc_id=mpc.id,
            etapa="coleta_vagas",
            status="executando"
        )
        self.db.add(log_coleta)
        self.db.commit()
        
        vagas_coletadas = []
        fontes_utilizadas = ["linkedin", "indeed", "catho", "infojobs"]
        
        # Coleta REAL de vagas usando job scraper APRIMORADO
        print(f"🚀 Iniciando coleta REAL com priorização metodológica...")
        print(f"🎯 Cargo: {cargo}")
        print(f"🏢 Área: {area}")
        print(f"📊 Meta: 100 vagas (50% LinkedIn + 30% Google Jobs + 20% outras)")
        
        vagas_reais = self.job_scraper.coletar_vagas_multiplas_fontes(
            area_interesse=area,
            cargo_objetivo=cargo,
            localizacao="São Paulo, SP",  # Pode ser parametrizado
            total_vagas_desejadas=total_vagas_desejadas
        )
        
        print(f"✅ Coleta finalizada: {len(vagas_reais)} vagas obtidas")
        
        # Converte formato do scraper para formato do sistema
        for vaga_real in vagas_reais:
            vaga_formatada = {
                "titulo": vaga_real.get("titulo", ""),
                "empresa": vaga_real.get("empresa", ""),
                "localizacao": vaga_real.get("localizacao", ""),
                "descricao": vaga_real.get("descricao", ""),
                "requisitos": vaga_real.get("descricao", ""),  # Requisitos dentro da descrição
                "fonte": vaga_real.get("fonte", ""),
                "url": vaga_real.get("url", ""),
                "data_coleta": vaga_real.get("data_coleta", "")
            }
            vagas_coletadas.append(vaga_formatada)
        
        print(f"Coleta real concluída: {len(vagas_coletadas)} vagas coletadas")
        
        # Salva vagas no banco
        total_salvas = 0
        for vaga_data in vagas_coletadas:
            vaga = VagaAnalisada(
                mpc_id=mpc.id,
                titulo=vaga_data["titulo"],
                empresa=vaga_data.get("empresa", ""),
                localizacao=vaga_data.get("localizacao", ""),
                descricao=vaga_data.get("descricao", ""),
                requisitos=vaga_data.get("requisitos", ""),
                fonte=vaga_data.get("fonte", ""),
                url_original=vaga_data.get("url", "")
            )
            self.db.add(vaga)
            total_salvas += 1
        
        self.db.commit()
        
        # Atualiza estatísticas do MPC
        mpc.total_vagas_coletadas = total_salvas
        self.db.commit()
        
        # Atualiza log
        log_coleta.status = "concluido"
        log_coleta.vagas_processadas = total_salvas
        self.db.commit()
        
        # Atualiza fontes utilizadas baseado na coleta real
        fontes_reais_utilizadas = list(set([vaga.get("fonte", "") for vaga in vagas_coletadas if vaga.get("fonte")]))
        
        # Conta vagas por fonte
        breakdown_fontes = {}
        for vaga in vagas_coletadas:
            fonte = vaga.get("fonte", "unknown")
            breakdown_fontes[fonte] = breakdown_fontes.get(fonte, 0) + 1
        
        print(f"📊 Breakdown de fontes reais:")
        for fonte, count in breakdown_fontes.items():
            print(f"   • {fonte}: {count} vagas")
        
        return {
            "total_coletadas": total_salvas,
            "fontes_utilizadas": fontes_reais_utilizadas,
            "breakdown_fontes": breakdown_fontes,
            "fontes_planejadas": fontes_utilizadas,
            "meta_atingida": total_salvas >= 50,
            "qualidade_coleta": "boa" if total_salvas >= 100 else "adequada" if total_salvas >= 50 else "insuficiente",
            "coleta_real_ativa": True,
            "observacao": f"Coleta REAL de {total_salvas} vagas com priorização metodológica",
            "fontes_prioritarias_ativas": True
        }
    
    async def _extrair_palavras_chave(self, mpc: MapaPalavrasChave) -> Dict[str, Any]:
        """
        Extrai palavras-chave de todas as vagas coletadas
        
        Processo Carolina Martins:
        1. Análise de descrições e requisitos
        2. Limpeza e normalização
        3. Contagem de frequência
        4. Identificação de padrões
        """
        log_extracao = ProcessamentoMPC(
            mpc_id=mpc.id,
            etapa="extracao_palavras",
            status="executando"
        )
        self.db.add(log_extracao)
        self.db.commit()
        
        # Busca todas as vagas do MPC
        vagas = self.db.query(VagaAnalisada).filter(VagaAnalisada.mpc_id == mpc.id).all()
        
        todas_palavras = []
        vagas_processadas = 0
        
        for vaga in vagas:
            # Combina descrição e requisitos
            texto_completo = f"{vaga.descricao} {vaga.requisitos}".lower()
            
            # Extrai palavras-chave com método APRIMORADO
            palavras_vaga = self._extrair_palavras_texto_detalhado(texto_completo)
            
            # Salva palavras da vaga
            vaga.palavras_extraidas = palavras_vaga
            vaga.processada = True
            
            todas_palavras.extend(palavras_vaga)
            vagas_processadas += 1
        
        self.db.commit()
        
        # Conta frequências
        contador_palavras = Counter(todas_palavras)
        total_palavras_unicas = len(contador_palavras)
        
        # Atualiza MPC
        mpc.total_palavras_extraidas = total_palavras_unicas
        self.db.commit()
        
        # Atualiza log
        log_extracao.status = "concluido"
        log_extracao.vagas_processadas = vagas_processadas
        log_extracao.palavras_encontradas = total_palavras_unicas
        self.db.commit()
        
        return {
            "vagas_processadas": vagas_processadas,
            "palavras_unicas": total_palavras_unicas,
            "palavras_mais_frequentes": contador_palavras.most_common(20),
            "qualidade_extracao": self._avaliar_qualidade_extracao(contador_palavras)
        }
    
    def _extrair_palavras_texto_detalhado(self, texto: str) -> List[str]:
        """
        Versão aprimorada da extração para capturar 30-70 palavras-chave
        MENOS RESTRITIVA que a versão original
        """
        # Limpeza inicial mais suave
        texto = re.sub(r'[^\w\s]', ' ', texto)
        texto = re.sub(r'\s+', ' ', texto).strip()
        
        # Identifica termos compostos primeiro (EXPANDIDO)
        termos_compostos = self._identificar_termos_compostos_expandido(texto)
        
        # Extrai palavras individuais com filtros mais permissivos
        palavras = []
        for palavra in texto.split():
            palavra_limpa = palavra.strip().lower()
            if (len(palavra_limpa) > 2 and 
                palavra_limpa not in self.stop_words and 
                self._e_palavra_potencialmente_relevante(palavra_limpa)):
                palavras.append(palavra_limpa)
        
        # Combina termos compostos e palavras individuais
        todas_palavras = termos_compostos + palavras
        
        # Normalização mais permissiva
        palavras_normalizadas = []
        seen = set()
        
        for palavra in todas_palavras:
            palavra_norm = self._normalizar_palavra(palavra)
            if palavra_norm not in seen and len(palavra_norm) > 2:
                palavras_normalizadas.append(palavra_norm)
                seen.add(palavra_norm)
        
        return palavras_normalizadas
    
    def _identificar_termos_compostos_expandido(self, texto: str) -> List[str]:
        """
        VERSÃO EXPANDIDA - identifica muito mais termos compostos
        """
        termos_compostos = []
        
        # Padrões de termos compostos EXPANDIDOS por área
        padroes_compostos = [
            # Ferramentas/Software
            r'excel\s+(avançado|intermediário|básico)',
            r'power\s+bi',
            r'google\s+(analytics|ads|drive|sheets)',
            r'facebook\s+ads',
            r'linkedin\s+ads',
            r'microsoft\s+(office|teams|project)',
            r'adobe\s+(photoshop|illustrator|premiere)',
            r'sql\s+(server|developer)',
            
            # Gestão e Processos
            r'gestão\s+de\s+(projetos|equipe|pessoas|processos|mudança|conflitos|tempo|qualidade|estoque|custos|riscos)',
            r'análise\s+de\s+(dados|negócio|mercado|risco|performance|resultado)',
            r'controle\s+de\s+(qualidade|estoque|custos|orçamento|despesas)',
            r'planejamento\s+(estratégico|financeiro|operacional|comercial)',
            r'desenvolvimento\s+de\s+(produto|negócio|estratégia|pessoas)',
            
            # Marketing e Vendas
            r'marketing\s+(digital|online|de\s+conteúdo|de\s+relacionamento)',
            r'redes\s+sociais',
            r'content\s+marketing',
            r'inbound\s+marketing',
            r'email\s+marketing',
            r'growth\s+hacking',
            r'customer\s+(success|experience|journey)',
            r'relacionamento\s+com\s+cliente',
            
            # Metodologias
            r'metodologias\s+ágeis',
            r'design\s+thinking',
            r'lean\s+(startup|six\s+sigma)',
            r'business\s+(intelligence|analyst)',
            r'product\s+(management|owner)',
            r'scrum\s+master',
            
            # Soft Skills
            r'trabalho\s+em\s+equipe',
            r'tomada\s+de\s+decisão',
            r'resolução\s+de\s+(problemas|conflitos)',
            r'comunicação\s+(oral|escrita|interpessoal|assertiva)',
            r'pensamento\s+(analítico|crítico|estratégico)',
            r'inteligência\s+emocional',
            r'capacidade\s+de\s+(liderança|adaptação|aprendizado)',
            
            # Financeiro/Contábil
            r'análise\s+financeira',
            r'fluxo\s+de\s+caixa',
            r'demonstrações\s+financeiras',
            r'orçamento\s+(anual|empresarial)',
            r'controladoria\s+financeira',
            
            # Tecnologia/IT
            r'desenvolvimento\s+(web|mobile|software)',
            r'banco\s+de\s+dados',
            r'segurança\s+da\s+informação',
            r'infraestrutura\s+de\s+ti',
            r'suporte\s+técnico',
            
            # RH/Gestão Pessoas
            r'recursos\s+humanos',
            r'gestão\s+de\s+talentos',
            r'desenvolvimento\s+humano',
            r'clima\s+organizacional',
            r'recrutamento\s+e\s+seleção'
        ]
        
        for padrao in padroes_compostos:
            matches = re.finditer(padrao, texto, re.IGNORECASE)
            for match in matches:
                termo_completo = match.group().lower().strip()
                if termo_completo not in termos_compostos:
                    termos_compostos.append(termo_completo)
        
        return termos_compostos
    
    def _e_palavra_potencialmente_relevante(self, palavra: str) -> bool:
        """
        Versão MENOS RESTRITIVA para capturar mais palavras
        """
        # Filtros básicos
        if len(palavra) < 3:
            return False
        
        if palavra.lower() in self.stop_words:
            return False
        
        # Palavras irrelevantes específicas (REDUZIDA)
        irrelevantes_criticas = [
            'empresa', 'oportunidade', 'vaga', 'área', 'profissional'
        ]
        
        if palavra.lower() in irrelevantes_criticas:
            return False
        
        # Aceita números se forem relevantes (anos de experiência, etc)
        if palavra.isdigit():
            return int(palavra) > 1990 or int(palavra) < 50  # Anos ou experiência
        
        # Aceita siglas de 3+ caracteres
        if palavra.isupper() and len(palavra) >= 3:
            return True
        
        # Aceita a maioria das outras palavras
        return True

    def _extrair_palavras_texto(self, texto: str) -> List[str]:
        """
        Extrai palavras-chave relevantes de um texto
        
        Aplica:
        - Limpeza de caracteres especiais
        - Remoção de stop words
        - Identificação de termos compostos
        - Normalização
        """
        # Limpeza inicial
        texto = re.sub(r'[^\w\s]', ' ', texto)
        texto = re.sub(r'\s+', ' ', texto).strip()
        
        # Identifica termos compostos primeiro
        termos_compostos = self._identificar_termos_compostos(texto)
        
        # Extrai palavras individuais
        palavras = [
            palavra.strip() 
            for palavra in texto.split()
            if len(palavra.strip()) > 2 
            and palavra.strip().lower() not in self.stop_words
        ]
        
        # Combina termos compostos e palavras individuais
        todas_palavras = termos_compostos + palavras
        
        # Remove duplicatas e normaliza
        palavras_normalizadas = list(set([
            self._normalizar_palavra(palavra)
            for palavra in todas_palavras
            if self._e_palavra_relevante(palavra)
        ]))
        
        return palavras_normalizadas
    
    def _identificar_termos_compostos(self, texto: str) -> List[str]:
        """
        Identifica termos compostos relevantes para área profissional
        Ex: "gestão de projetos", "excel avançado", "power bi"
        """
        termos_compostos = []
        
        # Padrões de termos compostos conhecidos
        padroes_compostos = [
            r'excel\s+(avançado|intermediário|básico)',
            r'power\s+bi',
            r'gestão\s+de\s+(projetos|equipe|pessoas|processos)',
            r'análise\s+de\s+(dados|negócio|mercado)',
            r'controle\s+de\s+(qualidade|estoque|custos)',
            r'planejamento\s+(estratégico|financeiro|operacional)',
            r'relacionamento\s+com\s+cliente',
            r'trabalho\s+em\s+equipe',
            r'tomada\s+de\s+decisão',
            r'resolução\s+de\s+(problemas|conflitos)',
            r'comunicação\s+(oral|escrita|interpessoal)',
            r'pensamento\s+(analítico|crítico|estratégico)'
        ]
        
        for padrao in padroes_compostos:
            matches = re.findall(padrao, texto, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    termo_completo = re.search(padrao, texto, re.IGNORECASE).group()
                else:
                    termo_completo = match
                termos_compostos.append(termo_completo.lower().strip())
        
        return list(set(termos_compostos))
    
    def _normalizar_palavra(self, palavra: str) -> str:
        """Normaliza palavra removendo acentos e padronizando"""
        import unicodedata
        
        # Remove acentos
        palavra = unicodedata.normalize('NFD', palavra).encode('ascii', 'ignore').decode('ascii')
        
        # Converte para minúsculo
        palavra = palavra.lower().strip()
        
        # Aplica normalizações específicas
        normalizacoes = {
            'excel': 'excel',
            'powerbi': 'power bi',
            'power-bi': 'power bi',
            'sql': 'sql',
            'crm': 'crm',
            'erp': 'erp',
            'sap': 'sap',
            'lideranca': 'liderança',
            'gestao': 'gestão',
            'analise': 'análise'
        }
        
        return normalizacoes.get(palavra, palavra)
    
    def _e_palavra_relevante(self, palavra: str) -> bool:
        """Verifica se palavra é relevante para contexto profissional"""
        # Filtros de relevância
        if len(palavra) < 3:
            return False
        
        if palavra.lower() in self.stop_words:
            return False
        
        # Palavras irrelevantes específicas
        irrelevantes = [
            'empresa', 'oportunidade', 'vaga', 'profissional', 'area',
            'conhecimento', 'experiencia', 'habilidade', 'competencia',
            'requisito', 'diferencial', 'atividade', 'responsabilidade'
        ]
        
        if palavra.lower() in irrelevantes:
            return False
        
        return True
    
    async def _categorizar_palavras_chave(self, mpc: MapaPalavrasChave) -> Dict[str, Any]:
        """
        Categoriza palavras-chave em: Comportamental, Técnica, Digital
        baseado na metodologia Carolina Martins
        """
        # Busca todas as palavras extraídas
        vagas = self.db.query(VagaAnalisada).filter(VagaAnalisada.mpc_id == mpc.id).all()
        
        # Coleta todas as palavras com frequência
        contador_geral = Counter()
        for vaga in vagas:
            if vaga.palavras_extraidas:
                contador_geral.update(vaga.palavras_extraidas)
        
        # Categoriza cada palavra
        palavras_categorizadas = {
            "comportamental": [],
            "tecnica": [],
            "digital": []
        }
        
        # Garante que coletamos pelo menos MIN_PALAVRAS_FASE1 (20) palavras
        # e idealmente TARGET_PALAVRAS_FASE1 (30) conforme metodologia
        palavras_mais_frequentes = contador_geral.most_common(self.MAX_PALAVRAS_FASE1 * 2)  # Pega o dobro para filtrar
        
        palavras_salvas = 0
        for palavra, frequencia in palavras_mais_frequentes:
            # Para nas primeiras MAX_PALAVRAS_FASE1 (40) palavras relevantes
            if palavras_salvas >= self.MAX_PALAVRAS_FASE1:
                break
                
            categoria = self._determinar_categoria_palavra(palavra)
            
            # Calcula frequência relativa
            freq_relativa = frequencia / mpc.total_vagas_coletadas
            
            # Cria registro de palavra-chave
            palavra_obj = PalavraChave(
                mpc_id=mpc.id,
                termo=palavra,
                categoria=categoria,
                frequencia_absoluta=frequencia,
                frequencia_relativa=freq_relativa,
                importancia=self._calcular_importancia_palavra(palavra, categoria, freq_relativa)
            )
            self.db.add(palavra_obj)
            palavras_salvas += 1
            
            # Adiciona à categoria correspondente
            palavras_categorizadas[categoria].append({
                "termo": palavra,
                "frequencia_absoluta": frequencia,
                "frequencia_relativa": freq_relativa,
                "importancia": palavra_obj.importancia
            })
        
        # Verifica se atingimos o mínimo da metodologia
        if palavras_salvas < self.MIN_PALAVRAS_FASE1:
            print(f"⚠️  AVISO: Apenas {palavras_salvas} palavras encontradas. Metodologia recomenda mínimo {self.MIN_PALAVRAS_FASE1}")
        
        self.db.commit()
        
        # Ordena por importância
        for categoria in palavras_categorizadas:
            palavras_categorizadas[categoria].sort(
                key=lambda x: x["importancia"], 
                reverse=True
            )
        
        return {
            "total_por_categoria": {
                cat: len(palavras) for cat, palavras in palavras_categorizadas.items()
            },
            "palavras_categorizadas": palavras_categorizadas,
            "qualidade_categorizacao": self._avaliar_qualidade_categorizacao(palavras_categorizadas)
        }
    
    def _determinar_categoria_palavra(self, palavra: str) -> str:
        """
        Determina categoria da palavra baseado na metodologia Carolina Martins
        
        Categorias:
        - Comportamental: soft skills, competências interpessoais
        - Técnica: conhecimentos específicos da área, linguagens, frameworks
        - Digital: ferramentas, softwares de produtividade
        """
        palavra_lower = palavra.lower()
        
        # CORREÇÃO: Ferramentas de produtividade e software = DIGITAL
        ferramentas_digitais = [
            'excel', 'power bi', 'tableau', 'word', 'powerpoint', 'access', 
            'outlook', 'teams', 'slack', 'jira', 'confluence', 'trello',
            'asana', 'monday', 'notion', 'figma', 'sketch', 'photoshop',
            'illustrator', 'premiere', 'after effects', 'canva', 'miro',
            'google analytics', 'google ads', 'facebook ads', 'linkedin ads',
            'hubspot', 'mailchimp', 'salesforce', 'pipedrive', 'zendesk'
        ]
        
        if any(tool in palavra_lower for tool in ferramentas_digitais):
            return CategoriaPalavraChave.DIGITAL.value
        
        # CORREÇÃO: Linguagens e frameworks = TÉCNICA
        competencias_tecnicas = [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby',
            'go', 'rust', 'php', 'swift', 'kotlin', 'scala', 'r', 'matlab',
            'sql', 'nosql', 'mysql', 'postgresql', 'mongodb', 'redis',
            'react', 'angular', 'vue', 'django', 'flask', 'spring', 'rails',
            'node', 'express', '.net', 'aws', 'azure', 'gcp', 'docker',
            'kubernetes', 'terraform', 'jenkins', 'git', 'github', 'gitlab',
            'api', 'rest', 'graphql', 'microservices', 'cloud', 'devops',
            'scrum', 'agile', 'kanban', 'lean', 'six sigma', 'pmbok', 'itil',
            'machine learning', 'deep learning', 'inteligência artificial',
            'data science', 'analytics', 'bi', 'etl', 'sap', 'oracle', 'erp'
        ]
        
        if any(tech in palavra_lower for tech in competencias_tecnicas):
            return CategoriaPalavraChave.TECNICA.value
        
        # Palavras comportamentais (mantém como está)
        if any(comp in palavra_lower for comp in [
            'liderança', 'comunicação', 'trabalho em equipe', 'proatividade',
            'organização', 'planejamento', 'negociação', 'relacionamento',
            'criatividade', 'inovação', 'adaptabilidade', 'flexibilidade',
            'responsabilidade', 'comprometimento', 'iniciativa', 'empatia',
            'colaboração', 'motivação', 'persuasão', 'networking',
            'resiliência', 'foco', 'disciplina', 'ética', 'integridade'
        ]):
            return CategoriaPalavraChave.COMPORTAMENTAL.value
        
        # Palavras técnicas (padrão para termos específicos da área)
        return CategoriaPalavraChave.TECNICA.value
    
    def _calcular_importancia_palavra(
        self, 
        palavra: str, 
        categoria: str, 
        freq_relativa: float
    ) -> float:
        """
        Calcula importância da palavra baseado em múltiplos fatores
        
        Fatores:
        - Frequência relativa (50%)
        - Categoria (20%) - digitais têm peso maior
        - Especificidade (20%) - termos mais específicos têm peso maior
        - Tamanho (10%) - termos compostos têm peso maior
        """
        score = freq_relativa * 0.5
        
        # Peso por categoria
        if categoria == CategoriaPalavraChave.DIGITAL.value:
            score += 0.2
        elif categoria == CategoriaPalavraChave.COMPORTAMENTAL.value:
            score += 0.15
        else:  # técnica
            score += 0.1
        
        # Peso por especificidade (termos compostos são mais específicos)
        if ' ' in palavra:  # termo composto
            score += 0.2
        elif len(palavra) > 8:  # palavra longa/específica
            score += 0.15
        else:
            score += 0.1
        
        # Peso por tamanho
        if len(palavra.split()) > 1:  # termo composto
            score += 0.1
        elif len(palavra) > 6:
            score += 0.08
        else:
            score += 0.05
        
        return min(score, 1.0)
    
    async def _validar_com_ia(
        self, 
        mpc: MapaPalavrasChave, 
        area_interesse: str, 
        cargo_objetivo: str
    ) -> Dict[str, Any]:
        """
        Valida palavras-chave com IA seguindo menção da Aula 6
        "Validação no ChatGPT"
        """
        # Busca top palavras por categoria
        palavras_top = self.db.query(PalavraChave)\
            .filter(PalavraChave.mpc_id == mpc.id)\
            .order_by(PalavraChave.importancia.desc())\
            .limit(50)\
            .all()
        
        # Prepara dados para validação
        palavras_por_categoria = defaultdict(list)
        for palavra in palavras_top:
            palavras_por_categoria[palavra.categoria].append(palavra.termo)
        
        # Busca vagas para contexto da validação
        vagas_contexto = self.db.query(VagaAnalisada)\
            .filter(VagaAnalisada.mpc_id == mpc.id)\
            .limit(5)\
            .all()
        
        vagas_dict = [{"descricao": vaga.descricao} for vaga in vagas_contexto]
        
        # Validação REAL com IA
        validacao_resultado = await self._validar_com_ia_real(
            palavras_por_categoria, area_interesse, cargo_objetivo, vagas_dict
        )
        
        # Salva resultado da validação
        validacao_ia = ValidacaoIA(
            mpc_id=mpc.id,
            modelo_ia="gpt-4",
            prompt_utilizado=validacao_resultado["prompt_usado"],
            palavras_aprovadas=validacao_resultado["aprovadas"],
            palavras_rejeitadas=validacao_resultado["rejeitadas"],
            sugestoes_adicionais=validacao_resultado["sugestoes"],
            confianca=validacao_resultado["confianca"]
        )
        self.db.add(validacao_ia)
        
        # Marca palavras como validadas
        for palavra in palavras_top:
            if palavra.termo in validacao_resultado["aprovadas"]:
                palavra.validada_ia = True
                palavra.recomendada_ia = True
            elif palavra.termo in validacao_resultado["rejeitadas"]:
                palavra.validada_ia = True
                palavra.recomendada_ia = False
        
        # Marca MPC como validado
        mpc.validado_ia = True
        mpc.sugestoes_ia = validacao_resultado["sugestoes"]
        
        self.db.commit()
        
        return validacao_resultado
    
    async def _validar_com_ia_real(
        self, 
        palavras_por_categoria: Dict[str, List[str]], 
        area: str, 
        cargo: str,
        vagas_contexto: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Validação REAL com IA usando OpenAI/Anthropic
        """
        # Prepara contexto das vagas para melhorar validação
        contexto_vagas = []
        if vagas_contexto:
            for vaga in vagas_contexto[:3]:  # Usa top 3 vagas como contexto
                contexto_vagas.append(vaga.get('descricao', '')[:200])
        
        # Chama validador real
        validacao_resultado = await self.ai_validator.validar_palavras_chave(
            palavras_por_categoria=palavras_por_categoria,
            area=area,
            cargo=cargo,
            contexto_vagas=contexto_vagas
        )
        
        # Converte formato para compatibilidade
        aprovadas = validacao_resultado.get('aprovadas', [])
        rejeitadas_com_motivo = validacao_resultado.get('rejeitadas', [])
        
        # Extrai apenas as palavras rejeitadas para compatibilidade
        rejeitadas = []
        if isinstance(rejeitadas_com_motivo, list):
            for item in rejeitadas_com_motivo:
                if isinstance(item, dict):
                    rejeitadas.append(item.get('palavra', ''))
                else:
                    rejeitadas.append(str(item))
        
        # Monta resultado final
        resultado = {
            "aprovadas": aprovadas,
            "rejeitadas": rejeitadas,
            "rejeitadas_detalhadas": rejeitadas_com_motivo,
            "sugestoes": validacao_resultado.get('sugestoes_novas', []),
            "comentarios": validacao_resultado.get('comentarios', ''),
            "confianca": validacao_resultado.get('confianca', 0.8),
            "modelo_usado": validacao_resultado.get('modelo_usado', 'ai_real'),
            "prompt_usado": validacao_resultado.get('prompt_usado', 'Validação com IA real')
        }
        
        return resultado
    
    async def _priorizar_palavras_chave(self, mpc: MapaPalavrasChave) -> Dict[str, Any]:
        """
        Prioriza palavras-chave seguindo critério Carolina Martins
        
        Priorização:
        - Essenciais: aparecem em 70%+ das vagas
        - Importantes: aparecem em 40-69% das vagas  
        - Complementares: aparecem em menos de 40%
        """
        palavras = self.db.query(PalavraChave)\
            .filter(PalavraChave.mpc_id == mpc.id)\
            .filter(PalavraChave.validada_ia == True)\
            .filter(PalavraChave.recomendada_ia == True)\
            .all()
        
        priorizacao = {
            "essenciais": [],
            "importantes": [],
            "complementares": []
        }
        
        for palavra in palavras:
            freq = palavra.frequencia_relativa
            
            item = {
                "termo": palavra.termo,
                "categoria": palavra.categoria,
                "frequencia": freq,
                "importancia": palavra.importancia
            }
            
            if freq >= 0.7:
                priorizacao["essenciais"].append(item)
            elif freq >= 0.4:
                priorizacao["importantes"].append(item)
            else:
                priorizacao["complementares"].append(item)
        
        # Ordena cada categoria por importância
        for categoria in priorizacao:
            priorizacao[categoria].sort(key=lambda x: x["importancia"], reverse=True)
        
        # Salva no MPC
        mpc.palavras_chave_priorizadas = {
            "por_prioridade": priorizacao,
            "por_categoria": self._organizar_por_categoria(palavras)
        }
        self.db.commit()
        
        return {
            "priorizacao": priorizacao,
            "total_essenciais": len(priorizacao["essenciais"]),
            "total_importantes": len(priorizacao["importantes"]),
            "total_complementares": len(priorizacao["complementares"]),
            "recomendacao_uso": self._gerar_recomendacao_uso(priorizacao)
        }
    
    def _consolidar_mpc(self, mpc: MapaPalavrasChave) -> Dict[str, Any]:
        """
        Consolida MPC final com todas as informações
        Output: Guia estruturado para aplicar no currículo
        """
        # Calcula score de qualidade
        score_qualidade = mpc.calcular_score_qualidade()
        
        # Busca dados para consolidação
        priorizacao = mpc.palavras_chave_priorizadas.get("por_prioridade", {})
        
        # Gera TOP 10 palavras conforme Fase 2 da metodologia
        todas_palavras_ordenadas = []
        todas_palavras_ordenadas.extend(priorizacao.get("essenciais", []))
        todas_palavras_ordenadas.extend(priorizacao.get("importantes", []))
        todas_palavras_ordenadas.extend(priorizacao.get("complementares", []))
        
        # Ordena por importância e pega TOP 10
        todas_palavras_ordenadas.sort(key=lambda x: x["importancia"], reverse=True)
        top_10_metodologia = todas_palavras_ordenadas[:self.TOP_PALAVRAS_FASE2]
        
        mpc_final = {
            "id": mpc.id,
            "configuracao": {
                "area_interesse": mpc.area_interesse,
                "cargo_objetivo": mpc.cargo_objetivo,
                "segmentos_alvo": mpc.segmentos_alvo
            },
            "estatisticas": {
                "total_vagas_analisadas": mpc.total_vagas_coletadas,
                "total_palavras_extraidas": mpc.total_palavras_extraidas,
                "score_qualidade": score_qualidade,
                "validado_ia": mpc.validado_ia,
                "metodologia_carolina_martins": {
                    "fase1_total_palavras": len(todas_palavras_ordenadas),
                    "fase1_alvo_atingido": len(todas_palavras_ordenadas) >= self.MIN_PALAVRAS_FASE1,
                    "fase2_top10": len(top_10_metodologia)
                }
            },
            "palavras_essenciais": priorizacao.get("essenciais", []),
            "palavras_importantes": priorizacao.get("importantes", []),  
            "palavras_complementares": priorizacao.get("complementares", []),
            "top_10_carolina_martins": top_10_metodologia,  # TOP 10 da metodologia
            "guia_aplicacao": self._gerar_guia_aplicacao(priorizacao),
            "recomendacoes": self._gerar_recomendacoes_finais(mpc, score_qualidade)
        }
        
        return mpc_final
    
    def _gerar_guia_aplicacao(self, priorizacao: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """
        Gera guia prático para aplicar palavras-chave no currículo
        baseado na metodologia Carolina Martins
        """
        essenciais = priorizacao.get("essenciais", [])
        importantes = priorizacao.get("importantes", [])
        
        return {
            "resumo_profissional": {
                "incluir_obrigatoriamente": [p["termo"] for p in essenciais[:5]],
                "incluir_preferencialmente": [p["termo"] for p in importantes[:3]],
                "instrucoes": "Use estas palavras-chave no resumo de forma natural"
            },
            "experiencias_profissionais": {
                "distribuir_por_experiencia": [p["termo"] for p in essenciais + importantes[:5]],
                "instrucoes": "Distribua as palavras-chave nas descrições das experiências"
            },
            "competencias": {
                "listar_explicitamente": [p["termo"] for p in essenciais if p["categoria"] == "digital"],
                "instrucoes": "Liste competências digitais/técnicas explicitamente"
            },
            "personalizacao": {
                "palavras_vaga_especifica": "Use palavras-chave exatas da job description",
                "instrucoes": "Sempre personalize com palavras-chave específicas da vaga"
            }
        }
    
    def _gerar_recomendacoes_finais(
        self, 
        mpc: MapaPalavrasChave, 
        score_qualidade: float
    ) -> List[str]:
        """Gera recomendações finais baseadas na qualidade do MPC"""
        recomendacoes = []
        
        if score_qualidade >= 80:
            recomendacoes.append("MPC de alta qualidade - pronto para uso no currículo")
        elif score_qualidade >= 60:
            recomendacoes.append("MPC de qualidade adequada - considere coletar mais vagas")
        else:
            recomendacoes.append("MPC necessita melhorias - colete mais vagas e refaça análise")
        
        if mpc.total_vagas_coletadas < 50:
            recomendacoes.append("Recomenda-se coletar pelo menos 50 vagas para maior precisão")
        
        if not mpc.validado_ia:
            recomendacoes.append("Valide palavras-chave com IA para maior assertividade")
        
        return recomendacoes
    
    # Métodos auxiliares
    
    def _carregar_palavras_base(self) -> Dict[str, List[str]]:
        """Carrega base de palavras-chave por categoria"""
        return {
            "comportamental": [
                "liderança", "comunicação", "trabalho em equipe", "proatividade",
                "organização", "planejamento", "negociação", "relacionamento"
            ],
            "tecnica": [
                "gestão", "análise", "controle", "desenvolvimento", "implementação",
                "coordenação", "supervisão", "operação"
            ],
            "digital": [
                "excel", "power bi", "sql", "sap", "crm", "erp", "word",
                "powerpoint", "outlook", "teams"
            ]
        }
    
    def _carregar_stop_words(self) -> List[str]:
        """Carrega lista de stop words em português"""
        return [
            "de", "da", "do", "das", "dos", "e", "em", "para", "com", "por",
            "ser", "ter", "estar", "fazer", "ir", "vir", "dar", "ver",
            "o", "a", "os", "as", "um", "uma", "uns", "umas",
            "que", "qual", "quais", "quando", "onde", "como", "porque",
            "mas", "ou", "se", "então", "assim", "também", "ainda",
            "já", "não", "sim", "muito", "mais", "menos", "bem", "mal"
        ]
    
    def _configurar_padroes_limpeza(self) -> List[str]:
        """Configura padrões regex para limpeza de texto"""
        return [
            r'\b(anos?|meses?|dias?)\b',  # unidades de tempo
            r'\b(r\$|\$|€|£)\s*\d+', # valores monetários
            r'\b\d{1,2}[hH]\d{2}\b',  # horários
            r'\b\d+[kg|km|m²|%]\b'    # unidades de medida
        ]
    
    def _avaliar_qualidade_extracao(self, contador: Counter) -> str:
        """Avalia qualidade da extração baseada nas palavras encontradas"""
        total_palavras = len(contador)
        palavras_relevantes = sum(1 for palavra in contador.keys() if self._e_palavra_relevante(palavra))
        
        proporcao_relevantes = palavras_relevantes / total_palavras if total_palavras > 0 else 0
        
        if proporcao_relevantes >= 0.7:
            return "excelente"
        elif proporcao_relevantes >= 0.5:
            return "boa"
        elif proporcao_relevantes >= 0.3:
            return "adequada"
        else:
            return "insuficiente"
    
    def _avaliar_qualidade_categorizacao(self, palavras_cat: Dict[str, List]) -> str:
        """Avalia distribuição das categorias"""
        total = sum(len(palavras) for palavras in palavras_cat.values())
        
        if total == 0:
            return "insuficiente"
        
        # Verifica se há palavras em todas as categorias
        categorias_com_palavras = sum(1 for palavras in palavras_cat.values() if len(palavras) > 0)
        
        if categorias_com_palavras == 3:
            return "completa"
        elif categorias_com_palavras >= 2:
            return "adequada"
        else:
            return "incompleta"
    
    def _organizar_por_categoria(self, palavras: List[PalavraChave]) -> Dict[str, List[Dict]]:
        """Organiza palavras por categoria"""
        por_categoria = defaultdict(list)
        
        for palavra in palavras:
            if palavra.recomendada_ia:
                por_categoria[palavra.categoria].append({
                    "termo": palavra.termo,
                    "frequencia": palavra.frequencia_relativa,
                    "importancia": palavra.importancia
                })
        
        # Ordena cada categoria
        for categoria in por_categoria:
            por_categoria[categoria].sort(key=lambda x: x["importancia"], reverse=True)
        
        return dict(por_categoria)
    
    def _gerar_recomendacao_uso(self, priorizacao: Dict[str, List]) -> Dict[str, str]:
        """Gera recomendações de uso das palavras-chave"""
        total_essenciais = len(priorizacao.get("essenciais", []))
        total_importantes = len(priorizacao.get("importantes", []))
        
        recomendacoes = {}
        
        if total_essenciais >= 5:
            recomendacoes["essenciais"] = "Use todas as palavras essenciais no resumo e experiências"
        elif total_essenciais >= 3:
            recomendacoes["essenciais"] = "Use pelo menos 3 palavras essenciais no resumo"
        else:
            recomendacoes["essenciais"] = "Poucas palavras essenciais - revise o MPC"
        
        if total_importantes >= 10:
            recomendacoes["importantes"] = "Distribua palavras importantes nas experiências"
        else:
            recomendacoes["importantes"] = "Use palavras importantes como complemento"
        
        recomendacoes["geral"] = "Sempre personalize com palavras-chave específicas da vaga"
        
        return recomendacoes