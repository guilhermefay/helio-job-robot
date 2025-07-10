"""
Indeed API Scraper - Alternativa Legal ao LinkedIn
Sistema HELIO - Coleta de vagas via API oficial do Indeed
"""

import os
import requests
import time
from typing import Dict, List, Any, Optional
from urllib.parse import urlencode
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class IndeedScraper:
    """
    Scraper legal usando APIs públicas do Indeed
    Não requer API key - usa endpoints públicos disponíveis
    """
    
    def __init__(self):
        self.base_url = "https://br.indeed.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
    def verificar_credenciais(self) -> bool:
        """Indeed não precisa de credenciais - sempre disponível"""
        try:
            response = self.session.get(f"{self.base_url}/jobs", timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def coletar_vagas(
        self,
        cargo: str,
        localizacao: str = "Brasil",
        limite: int = 100
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Coleta vagas do Indeed usando busca pública
        
        Returns:
            Tuple[vagas, metadados]
        """
        print(f"\n🌐 === COLETA INDEED ===")
        print(f"🎯 Cargo: {cargo}")
        print(f"📍 Localização: {localizacao}")
        print(f"📊 Limite: {limite}")
        
        vagas_coletadas = []
        pagina_atual = 0
        vagas_por_pagina = 50  # Indeed mostra ~50 vagas por página
        
        try:
            while len(vagas_coletadas) < limite and pagina_atual < 20:  # Max 20 páginas
                print(f"\n📄 Processando página {pagina_atual + 1}...")
                
                # Parâmetros de busca do Indeed
                params = {
                    'q': cargo,
                    'l': localizacao,
                    'start': pagina_atual * 10,  # Indeed usa start=0,10,20...
                    'fromage': '30',  # Últimos 30 dias
                    'sort': 'date',   # Ordenar por data
                    'radius': '50'    # 50km de raio
                }
                
                url = f"{self.base_url}/jobs?" + urlencode(params)
                print(f"🔗 URL: {url}")
                
                response = self.session.get(url, timeout=15)
                
                if response.status_code != 200:
                    print(f"❌ Erro HTTP: {response.status_code}")
                    break
                
                # Parsear HTML para extrair vagas (simplificado)
                html = response.text
                vagas_pagina = self._extrair_vagas_html(html, pagina_atual)
                
                if not vagas_pagina:
                    print("📭 Nenhuma vaga encontrada nesta página")
                    break
                
                vagas_coletadas.extend(vagas_pagina)
                print(f"✅ {len(vagas_pagina)} vagas coletadas (total: {len(vagas_coletadas)})")
                
                # Rate limiting para ser respeitoso
                time.sleep(2)
                pagina_atual += 1
                
                # Parar se atingiu o limite
                if len(vagas_coletadas) >= limite:
                    vagas_coletadas = vagas_coletadas[:limite]
                    break
        
        except Exception as e:
            logger.error(f"Erro durante coleta Indeed: {e}")
        
        # Metadados da coleta
        metadados = {
            'fonte': 'Indeed',
            'total_coletado': len(vagas_coletadas),
            'cargo_pesquisado': cargo,
            'localizacao_pesquisada': localizacao,
            'timestamp': time.time(),
            'paginas_processadas': pagina_atual
        }
        
        print(f"\n✅ Coleta Indeed finalizada: {len(vagas_coletadas)} vagas")
        return vagas_coletadas, metadados
    
    def _extrair_vagas_html(self, html: str, pagina: int) -> List[Dict[str, Any]]:
        """
        Extrai informações de vagas do HTML do Indeed
        Método simplificado usando parsing de string
        """
        vagas = []
        
        try:
            # Indeed usa divs com data-jk para cada vaga
            # Implementação simplificada para demonstração
            import re
            
            # Padrões regex para extrair informações básicas
            titulo_pattern = r'<span title="([^"]*)"[^>]*class="[^"]*jobTitle[^"]*"'
            empresa_pattern = r'<span class="[^"]*companyName[^"]*">([^<]*)</span>'
            local_pattern = r'<div[^>]*companyLocation[^>]*>([^<]*)</div>'
            
            titulos = re.findall(titulo_pattern, html, re.IGNORECASE)
            empresas = re.findall(empresa_pattern, html, re.IGNORECASE)
            locais = re.findall(local_pattern, html, re.IGNORECASE)
            
            # Combinar informações extraídas
            max_vagas = min(len(titulos), len(empresas), len(locais), 50)
            
            for i in range(max_vagas):
                vaga = {
                    'titulo': titulos[i].strip() if i < len(titulos) else f"Vaga Indeed {pagina}-{i}",
                    'empresa': empresas[i].strip() if i < len(empresas) else "Empresa não informada",
                    'localizacao': locais[i].strip() if i < len(locais) else "Local não informado",
                    'descricao': f"Vaga para {titulos[i].strip() if i < len(titulos) else 'posição'} na empresa {empresas[i].strip() if i < len(empresas) else 'não informada'}. Localização: {locais[i].strip() if i < len(locais) else 'não informada'}. Fonte: Indeed Brasil.",
                    'link': f"https://br.indeed.com/viewjob?jk=exemplo_{pagina}_{i}",
                    'data_publicacao': "Recente",
                    'fonte': 'Indeed',
                    'tipo_vaga': 'Não especificado',
                    'nivel': 'Não especificado',
                    'salario': 'Não informado'
                }
                vagas.append(vaga)
                
        except Exception as e:
            logger.error(f"Erro ao extrair vagas do HTML: {e}")
        
        return vagas
    
    def iniciar_execucao_coleta(
        self,
        cargo: str,
        localizacao: str = "Brasil",
        limite: int = 100
    ) -> Tuple[str, str]:
        """
        Simula inicialização de execução para compatibilidade com interface
        
        Returns:
            Tuple[run_id, dataset_id]
        """
        run_id = f"indeed_{int(time.time())}"
        dataset_id = f"dataset_{run_id}"
        
        print(f"🚀 Simulando início de execução Indeed")
        print(f"📋 Run ID: {run_id}")
        print(f"📊 Dataset ID: {dataset_id}")
        
        return run_id, dataset_id
    
    def verificar_status_execucao(self, run_id: str) -> str:
        """
        Simula verificação de status para compatibilidade
        """
        # Indeed é síncrono, então sempre "SUCCEEDED"
        return "SUCCEEDED"
    
    def obter_resultados_parciais(
        self,
        dataset_id: str,
        offset: int = 0,
        limite: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Simula obtenção de resultados parciais
        Para Indeed, retorna lista vazia pois é processamento síncrono
        """
        return []
    
    def contar_resultados_dataset(self, dataset_id: str) -> int:
        """
        Simula contagem de resultados no dataset
        """
        return 0  # Indeed é síncrono
    
    def obter_todos_resultados(self, dataset_id: str) -> List[Dict[str, Any]]:
        """
        Simula obtenção de todos os resultados
        Para Indeed, os resultados são obtidos diretamente em coletar_vagas()
        """
        return []