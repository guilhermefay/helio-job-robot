"""
LinkedIn Scraper usando Apify - Alternativa profissional ao Selenium
Coleta real de vagas do LinkedIn usando a infraestrutura da Apify
"""

import os
import time
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

class LinkedInApifyScraper:
    """
    Coleta vagas do LinkedIn usando Apify Actor
    Mais confiável e escalável que Selenium
    """
    
    def __init__(self):
        self.apify_token = os.getenv('APIFY_API_TOKEN', '')
        # Actor popular e confiável para LinkedIn
        self.actor_id = 'curious_coder~linkedin-jobs-scraper'  # PPR - Actor com formato til
        self.base_url = 'https://api.apify.com/v2'
        
        if not self.apify_token:
            print("⚠️  APIFY_API_TOKEN não configurado. Adicione no .env")
    
    def coletar_vagas_linkedin(
        self, 
        cargo: str, 
        localizacao: str = "São Paulo, Brazil",
        limite: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Coleta vagas reais do LinkedIn usando Apify
        
        Args:
            cargo: Título do cargo para buscar
            localizacao: Localização das vagas
            limite: Número máximo de vagas a coletar
            
        Returns:
            Lista de vagas coletadas do LinkedIn
        """
        
        if not self.apify_token:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ APIFY: Token não configurado. Usando fallback...")
            return self._fallback_linkedin_data(cargo, localizacao, limite)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🚀 APIFY: Iniciando coleta para '{cargo}' em '{localizacao}'...")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📊 APIFY: Meta: {limite} vagas")
        
        try:
            # Configuração para o curious_coder PPR LinkedIn Jobs Scraper
            # Este actor precisa de URLs de busca do LinkedIn
            linkedin_url = self._construir_url_busca(cargo, localizacao)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔗 APIFY: URL construída")
            
            actor_input = {
                "urls": [linkedin_url],  # Campo correto: urls
                "numberOfJobsNeeded": limite,  # Número de vagas desejadas
                "scrapeCompanyDetails": True,  # Incluir detalhes da empresa
                "proxy": {
                    "useApifyProxy": True,
                    "apifyProxyGroups": ["RESIDENTIAL"]
                }
            }
            
            # Executa o Actor
            run_url = f"{self.base_url}/acts/{self.actor_id}/runs?token={self.apify_token}"
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 📤 APIFY: Enviando requisição para Actor...")
            response = requests.post(run_url, json=actor_input)
            
            if response.status_code != 201:
                if response.status_code == 402:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ APIFY: Erro 402 - Créditos esgotados!")
                    print(f"[{datetime.now().strftime('%H:%M:%S')}]    Recarregue em https://console.apify.com/billing")
                else:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ APIFY: Erro {response.status_code}")
                    try:
                        error_data = response.json()
                        print(f"[{datetime.now().strftime('%H:%M:%S')}]    Detalhes: {error_data.get('error', {}).get('message', 'Sem detalhes')}")
                    except:
                        pass
                return self._fallback_linkedin_data(cargo, localizacao, limite)
            
            run_data = response.json()
            run_id = run_data['data']['id']
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ APIFY: Actor iniciado! ID: {run_id}")
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ⏳ APIFY: Aguardando conclusão (máx 2 min)...")
            
            # Aguarda conclusão (máximo 2 minutos)
            max_wait = 120
            start_time = time.time()
            check_count = 0
            
            while time.time() - start_time < max_wait:
                status_url = f"{self.base_url}/actor-runs/{run_id}?token={self.apify_token}"
                status_response = requests.get(status_url)
                
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    status = status_data['data']['status']
                    
                    check_count += 1
                    elapsed = int(time.time() - start_time)
                    
                    if status == 'SUCCEEDED':
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ APIFY: Coleta concluída com sucesso!")
                        break
                    elif status in ['FAILED', 'ABORTED']:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ APIFY: Actor falhou com status: {status}")
                        return self._fallback_linkedin_data(cargo, localizacao, limite)
                    else:
                        # Mostrar progresso a cada 3 verificações (15 segundos)
                        if check_count % 3 == 0:
                            print(f"[{datetime.now().strftime('%H:%M:%S')}] ⏳ APIFY: Status: {status} | Tempo: {elapsed}s")
                
                time.sleep(5)  # Verifica a cada 5 segundos
            
            # Obtém os resultados
            dataset_id = run_data['data']['defaultDatasetId']
            items_url = f"{self.base_url}/datasets/{dataset_id}/items?token={self.apify_token}"
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 📥 APIFY: Baixando resultados...")
            items_response = requests.get(items_url)
            
            if items_response.status_code == 200:
                items = items_response.json()
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 📊 APIFY: {len(items)} resultados obtidos")
                return self._processar_resultados_apify(items, cargo)
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ APIFY: Erro ao obter resultados: {items_response.status_code}")
                return self._fallback_linkedin_data(cargo, localizacao, limite)
                
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ APIFY: Erro na coleta: {e}")
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔄 APIFY: Usando fallback...")
            return self._fallback_linkedin_data(cargo, localizacao, limite)
    
    def _processar_resultados_apify(self, items: List[Dict], cargo_pesquisado: str) -> List[Dict[str, Any]]:
        """
        Processa os resultados do Apify para o formato padrão
        Adaptado para o actor bebity/linkedin-jobs-scraper
        """
        vagas_processadas = []
        
        for item in items:
            try:
                # O actor bebity retorna campos neste formato
                vaga = {
                    "titulo": item.get('title', item.get('jobTitle', 'Título não disponível')),
                    "empresa": item.get('companyName', item.get('company', 'Empresa não informada')),
                    "localizacao": item.get('location', 'Local não informado'),
                    "descricao": item.get('description', item.get('jobDescription', 'Descrição não disponível')),
                    "fonte": "linkedin_apify",
                    "url": item.get('link', item.get('jobUrl', '')),
                    "data_coleta": datetime.now().isoformat(),
                    "cargo_pesquisado": cargo_pesquisado,
                    "data_publicacao": item.get('postedTime', item.get('publishedAt', '')),
                    "salario": item.get('salary', ''),
                    "tipo_emprego": item.get('contractType', item.get('employmentType', '')),
                    "nivel_experiencia": item.get('seniorityLevel', item.get('experienceLevel', '')),
                    "empresa_logo": item.get('companyLogo', ''),
                    "empresa_linkedin": item.get('companyLink', item.get('companyUrl', '')),
                    "apify_real": True  # Marca como dados reais do Apify
                }
                
                vagas_processadas.append(vaga)
                
            except Exception as e:
                print(f"⚠️  Erro ao processar vaga: {e}")
                continue
        
        print(f"✅ Processadas {len(vagas_processadas)} vagas do LinkedIn via Apify")
        return vagas_processadas
    
    def _fallback_linkedin_data(self, cargo: str, localizacao: str, limite: int) -> List[Dict[str, Any]]:
        """
        Dados de fallback quando Apify não está disponível
        Usa API pública limitada do LinkedIn
        """
        print("🔄 Usando fallback: tentando API pública do LinkedIn...")
        
        vagas = []
        
        try:
            # Tenta usar endpoint público (muito limitado)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            query = cargo.replace(' ', '%20')
            location = localizacao.replace(' ', '%20').replace(',', '%2C')
            
            url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={query}&location={location}&start=0"
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Parse HTML response (limitado)
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                job_cards = soup.find_all('div', class_='job-search-card')[:limite]
                
                for card in job_cards:
                    titulo = card.find('h3', class_='job-search-card__title')
                    empresa = card.find('h4', class_='job-search-card__company-name')
                    local = card.find('span', class_='job-search-card__location')
                    
                    vaga = {
                        "titulo": titulo.text.strip() if titulo else cargo,
                        "empresa": empresa.text.strip() if empresa else "Empresa LinkedIn",
                        "localizacao": local.text.strip() if local else localizacao,
                        "descricao": f"Vaga para {cargo} no LinkedIn. Acesse o LinkedIn para mais detalhes.",
                        "fonte": "linkedin_public_api",
                        "url": "https://www.linkedin.com/jobs/",
                        "data_coleta": datetime.now().isoformat(),
                        "cargo_pesquisado": cargo,
                        "api_limitada": True
                    }
                    
                    vagas.append(vaga)
                
                print(f"✅ Coletadas {len(vagas)} vagas via API pública")
                
        except Exception as e:
            print(f"❌ Fallback também falhou: {e}")
        
        return vagas
    
    def _construir_url_busca(self, cargo: str, localizacao: str) -> str:
        """
        Constrói URL de busca do LinkedIn Jobs
        """
        # Formatar parâmetros para URL
        keywords = cargo.replace(' ', '%20')
        location = localizacao.replace(' ', '%20').replace(',', '%2C')
        
        # URL padrão de busca do LinkedIn Jobs
        url = f"https://www.linkedin.com/jobs/search/?keywords={keywords}&location={location}"
        
        print(f"   URL construída: {url}")
        return url
    
    def verificar_credenciais(self) -> bool:
        """
        Verifica se as credenciais do Apify estão válidas
        """
        if not self.apify_token:
            return False
        
        try:
            url = f"{self.base_url}/users/me?token={self.apify_token}"
            response = requests.get(url)
            return response.status_code == 200
        except:
            return False


# Exemplo de uso
if __name__ == "__main__":
    scraper = LinkedInApifyScraper()
    
    # Verifica credenciais
    if scraper.verificar_credenciais():
        print("✅ Apify configurado corretamente!")
    else:
        print("❌ Configure APIFY_API_TOKEN no .env")
        print("📌 Crie uma conta gratuita em: https://apify.com")
        print("📌 Copie seu API token e adicione ao .env")
    
    # Testa coleta
    vagas = scraper.coletar_vagas_linkedin(
        cargo="Python Developer",
        localizacao="São Paulo, Brazil",
        limite=10
    )
    
    print(f"\n📊 Total de vagas coletadas: {len(vagas)}")
    
    for i, vaga in enumerate(vagas[:3], 1):
        print(f"\n--- Vaga {i} ---")
        print(f"Título: {vaga['titulo']}")
        print(f"Empresa: {vaga['empresa']}")
        print(f"Local: {vaga['localizacao']}")