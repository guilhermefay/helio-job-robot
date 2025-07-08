"""
Job Scraper V2 - Sistema HELIO
Arquitetura simplificada focada em delegação e orquestração inteligente
"""

import os
import time
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from dotenv import load_dotenv

from .query_expander import QueryExpanderV2
from .location_expander import LocationExpander
from .linkedin_apify_scraper import LinkedInApifyScraper

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


@dataclass
class SearchCombination:
    """Representa uma combinação de busca cargo + localização"""
    cargo: str
    localizacao: str
    prioridade: int
    tipo_local: str  # 'presencial', 'hibrido', 'remoto'


class JobScraper:
    """
    Orquestrador de coleta de vagas - V2
    Delega toda complexidade de scraping para serviços especializados
    """
    
    def __init__(self):
        # Serviços de expansão
        self.query_expander = QueryExpanderV2()
        self.location_expander = LocationExpander()
        
        # Serviço único de scraping (Apify)
        self.scraper = LinkedInApifyScraper()
        
        # Verificar configuração
        if not self.scraper.verificar_credenciais():
            logger.warning("⚠️ Apify não configurado. Configure APIFY_API_TOKEN no .env")
        
        # Configurações
        self.max_retries = 3
        self.retry_delay = 2  # segundos
        
    def coletar_vagas_multiplas_fontes(
        self,
        area_interesse: str,
        cargo_objetivo: str,
        localizacao: str = "Brasil",
        tipo_vaga: str = "hibrido",  # presencial, hibrido, remoto
        total_vagas_desejadas: int = 50
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Orquestra a coleta inteligente de vagas
        
        Args:
            area_interesse: Área de atuação (ex: "tecnologia", "marketing")
            cargo_objetivo: Cargo desejado (ex: "desenvolvedor")
            localizacao: Cidade/estado base do usuário
            tipo_vaga: Preferência de trabalho (presencial/hibrido/remoto)
            total_vagas_desejadas: Quantidade alvo de vagas
            
        Returns:
            Tupla com (lista de vagas, metadados da coleta)
        """
        
        inicio = time.time()
        vagas_coletadas = []
        metadados = {
            "tempo_inicio": datetime.now().isoformat(),
            "parametros_busca": {
                "area": area_interesse,
                "cargo": cargo_objetivo,
                "local_base": localizacao,
                "tipo": tipo_vaga,
                "meta": total_vagas_desejadas
            },
            "combinacoes_tentadas": [],
            "erros": [],
            "estatisticas": {}
        }
        
        logger.info(f"\n{'='*60}")
        logger.info(f"🎯 INICIANDO COLETA INTELIGENTE DE VAGAS")
        logger.info(f"{'='*60}")
        logger.info(f"📋 Cargo: {cargo_objetivo}")
        logger.info(f"🏢 Área: {area_interesse}")
        logger.info(f"📍 Local base: {localizacao}")
        logger.info(f"💼 Tipo: {tipo_vaga}")
        logger.info(f"🎯 Meta: {total_vagas_desejadas} vagas")
        
        # 1. EXPANSÃO INTELIGENTE DE QUERIES
        logger.info(f"\n📊 FASE 1: Expansão de queries...")
        cargos_expandidos = self.query_expander.expandir_cargo(
            cargo_objetivo, 
            area_interesse
        )
        logger.info(f"✅ {len(cargos_expandidos)} variações de cargo geradas")
        
        # 2. EXPANSÃO GEOGRÁFICA COM IA
        logger.info(f"\n📍 FASE 2: Expansão geográfica inteligente...")
        locais_expandidos = self.location_expander.expandir_localizacao(
            localizacao,
            tipo_vaga,
            limite=10  # Top 10 locais mais relevantes
        )
        logger.info(f"✅ {len(locais_expandidos)} localizações priorizadas")
        
        # 3. GERAR COMBINAÇÕES PRIORIZADAS
        logger.info(f"\n🔄 FASE 3: Gerando combinações de busca...")
        combinacoes = self._gerar_combinacoes_priorizadas(
            cargos_expandidos,
            locais_expandidos,
            tipo_vaga
        )
        logger.info(f"✅ {len(combinacoes)} combinações geradas")
        
        # 4. COLETA EM CASCATA COM PARADA INTELIGENTE
        logger.info(f"\n🚀 FASE 4: Iniciando coleta em cascata...")
        
        for idx, combo in enumerate(combinacoes):
            # Verificar se já atingiu a meta
            if len(vagas_coletadas) >= total_vagas_desejadas:
                logger.info(f"\n✅ Meta atingida! {len(vagas_coletadas)} vagas coletadas")
                break
            
            # Calcular quantas vagas ainda precisamos
            vagas_faltantes = total_vagas_desejadas - len(vagas_coletadas)
            
            logger.info(f"\n🔍 Tentativa {idx + 1}/{len(combinacoes)}")
            logger.info(f"   Cargo: {combo.cargo}")
            logger.info(f"   Local: {combo.localizacao}")
            logger.info(f"   Coletando até: {vagas_faltantes} vagas")
            
            # Tentar coletar com retry automático
            vagas_combo = self._coletar_com_retry(
                combo.cargo,
                combo.localizacao,
                vagas_faltantes  # Coleta exatamente o que falta para atingir a meta do usuário
            )
            
            if vagas_combo:
                vagas_coletadas.extend(vagas_combo)
                logger.info(f"   ✅ {len(vagas_combo)} vagas coletadas")
                
                metadados["combinacoes_tentadas"].append({
                    "cargo": combo.cargo,
                    "local": combo.localizacao,
                    "vagas_coletadas": len(vagas_combo),
                    "sucesso": True
                })
            else:
                logger.warning(f"   ⚠️ Nenhuma vaga encontrada")
                metadados["combinacoes_tentadas"].append({
                    "cargo": combo.cargo,
                    "local": combo.localizacao,
                    "vagas_coletadas": 0,
                    "sucesso": False
                })
        
        # 5. PROCESSAMENTO FINAL
        logger.info(f"\n📊 FASE 5: Processamento final...")
        
        # Remover duplicatas
        vagas_unicas = self._remover_duplicatas(vagas_coletadas)
        logger.info(f"✅ {len(vagas_coletadas) - len(vagas_unicas)} duplicatas removidas")
        
        # Estatísticas finais
        tempo_total = time.time() - inicio
        metadados["estatisticas"] = {
            "total_coletado": len(vagas_unicas),
            "meta_atingida": len(vagas_unicas) >= total_vagas_desejadas,
            "percentual_meta": (len(vagas_unicas) / total_vagas_desejadas) * 100,
            "tempo_total_segundos": round(tempo_total, 2),
            "combinacoes_sucesso": sum(1 for c in metadados["combinacoes_tentadas"] if c["sucesso"]),
            "combinacoes_total": len(metadados["combinacoes_tentadas"])
        }
        
        # Log final
        logger.info(f"\n{'='*60}")
        logger.info(f"📊 COLETA FINALIZADA")
        logger.info(f"{'='*60}")
        logger.info(f"✅ Total coletado: {len(vagas_unicas)} vagas")
        logger.info(f"🎯 Meta: {total_vagas_desejadas} ({metadados['estatisticas']['percentual_meta']:.1f}% atingido)")
        logger.info(f"⏱️ Tempo total: {tempo_total:.1f} segundos")
        logger.info(f"🔄 Combinações bem-sucedidas: {metadados['estatisticas']['combinacoes_sucesso']}/{len(combinacoes)}")
        
        # Alertar se coleta foi insuficiente
        if len(vagas_unicas) < total_vagas_desejadas * 0.5:  # Menos de 50% da meta
            logger.warning(f"\n⚠️ ATENÇÃO: Coleta abaixo do esperado!")
            logger.warning(f"   Apenas {len(vagas_unicas)} de {total_vagas_desejadas} vagas coletadas")
            logger.warning(f"   Considere:")
            logger.warning(f"   • Usar termos de busca mais genéricos")
            logger.warning(f"   • Ampliar o raio geográfico")
            logger.warning(f"   • Verificar configuração do Apify")
        
        return vagas_unicas[:total_vagas_desejadas], metadados
    
    def _gerar_combinacoes_priorizadas(
        self,
        cargos: List[str],
        locais: List[Dict[str, Any]],
        tipo_vaga: str
    ) -> List[SearchCombination]:
        """
        Gera combinações de busca priorizadas
        """
        combinacoes = []
        
        # Para vagas remotas, adicionar busca específica
        if tipo_vaga == "remoto":
            for cargo in cargos[:3]:  # Top 3 cargos
                combinacoes.append(SearchCombination(
                    cargo=cargo,
                    localizacao="Remote",
                    prioridade=10,
                    tipo_local="remoto"
                ))
        
        # Combinações regulares
        for i, cargo in enumerate(cargos[:5]):  # Top 5 cargos
            for j, local in enumerate(locais[:3]):  # Top 3 locais por cargo
                prioridade = 10 - i - j  # Maior prioridade para primeiras combinações
                
                combinacoes.append(SearchCombination(
                    cargo=cargo,
                    localizacao=local["nome"],
                    prioridade=prioridade,
                    tipo_local=local.get("tipo", tipo_vaga)
                ))
        
        # Ordenar por prioridade
        combinacoes.sort(key=lambda x: x.prioridade, reverse=True)
        
        return combinacoes
    
    def _coletar_com_retry(
        self,
        cargo: str,
        localizacao: str,
        limite: int
    ) -> List[Dict[str, Any]]:
        """
        Coleta vagas com retry automático em caso de falha
        """
        for tentativa in range(self.max_retries):
            try:
                # Delegar para o serviço de scraping
                vagas = self.scraper.coletar_vagas_linkedin(
                    cargo=cargo,
                    localizacao=localizacao,
                    limite=limite
                )
                
                if vagas:
                    return vagas
                    
            except Exception as e:
                logger.warning(f"   Tentativa {tentativa + 1}/{self.max_retries} falhou: {str(e)}")
                
                if tentativa < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"   ❌ Todas as tentativas falharam para {cargo} em {localizacao}")
        
        return []
    
    def _remover_duplicatas(self, vagas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Remove vagas duplicadas baseado em título + empresa
        """
        vagas_unicas = []
        chaves_vistas = set()
        
        for vaga in vagas:
            # Criar chave única
            chave = f"{vaga.get('titulo', '').lower()}_{vaga.get('empresa', '').lower()}"
            
            if chave not in chaves_vistas:
                chaves_vistas.add(chave)
                vagas_unicas.append(vaga)
        
        return vagas_unicas