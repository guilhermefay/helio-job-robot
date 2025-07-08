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
        """
        Inicializa o scraper do LinkedIn via Apify
        Usando curious_coder~linkedin-jobs-scraper otimizado
        """
        self.apify_token = os.getenv('APIFY_API_TOKEN')
        self.base_url = "https://api.apify.com/v2"
        self.actor_id = "curious_coder~linkedin-jobs-scraper"  # ✅ Actor correto e gratuito
        
        if not self.apify_token:
            print("⚠️  APIFY_API_TOKEN não encontrado. Usando dados de fallback.")
    
    def coletar_vagas_linkedin(
        self, 
        cargo: str, 
        localizacao: str = "São Paulo, Brazil",
        limite: int = 800  # 🔥 PADRÃO ALTO: 800 vagas
    ) -> List[Dict[str, Any]]:
        """
        Coleta vagas do LinkedIn usando Apify (aproveita TODAS as vagas disponíveis)
        
        Args:
            cargo: Cargo/posição desejada
            localizacao: Localização para busca  
            limite: Máximo de vagas (padrão: 800, usa todas se Apify trouxer mais)
        """
        
        if not self.apify_token:
            print("🚨 Token Apify não configurado. Usando fallback.")
            return self._dados_fallback_linkedin()
        
        try:
            # 🔥 URL OTIMIZADA: Filtro últimos 7 dias para relevância
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={cargo}&location={localizacao}&f_TPR=r604800"
            
            # 🎯 INPUT MÁXIMO: Deixa Apify buscar o máximo possível
            input_data = {
                "urls": [search_url],
                "numberOfJobsNeeded": 20000,  # 🚀 MÁXIMO POSSÍVEL! 
                "scrapeCompanyDetails": True,
                "proxy": {
                    "useApifyProxy": True,
                    "apifyProxyGroups": ["RESIDENTIAL"]
                },
                "timeout": 600,  # 🕐 10 minutos - mais tempo para mais vagas
                "maxConcurrency": 3  # Aumenta concorrência
            }
            
            print(f"🚀 Buscando MÁXIMO de vagas: {cargo} em {localizacao}")
            print(f"📊 Limite do usuário: {limite} | Apify buscará: até 20.000!")
            
            # Iniciar execução
            run_response = requests.post(
                f"{self.base_url}/acts/{self.actor_id}/runs",
                headers={
                    "Authorization": f"Bearer {self.apify_token}",
                    "Content-Type": "application/json"
                },
                json=input_data,
                timeout=30
            )
            
            if run_response.status_code != 201:
                print(f"❌ Erro ao iniciar scraping: {run_response.status_code}")
                return self._dados_fallback_linkedin()
            
            run_id = run_response.json()["data"]["id"]
            print(f"✅ Scraping iniciado - ID: {run_id}")
            
            # 🕐 AGUARDAR com paciência para MAIS vagas
            max_attempts = 40  # ~7 minutos máximo (mais tempo = mais vagas)
            attempt = 0
            
            while attempt < max_attempts:
                time.sleep(10)  # Check a cada 10 segundos
                attempt += 1
                
                status_response = requests.get(
                    f"{self.base_url}/actor-runs/{run_id}",
                    headers={"Authorization": f"Bearer {self.apify_token}"},
                    timeout=10
                )
                
                if status_response.status_code == 200:
                    status = status_response.json()["data"]["status"]
                    
                    # 📊 Log progresso a cada minuto
                    if attempt % 6 == 0:  # A cada 6 checks = 1 minuto
                        print(f"⏳ Aguardando... {attempt//6}min | Status: {status}")
                    
                    if status == "SUCCEEDED":
                        print(f"🎉 Scraping concluído em {attempt//6}min!")
                        break
                    elif status in ["FAILED", "ABORTED", "TIMED-OUT"]:
                        print(f"❌ Scraping falhou: {status}")
                        return self._dados_fallback_linkedin()
                else:
                    print(f"⚠️ Erro ao verificar status: {status_response.status_code}")
            
            if attempt >= max_attempts:
                print("⏰ Timeout: Mas vamos tentar baixar o que conseguiu...")
                # 🎯 Mesmo com timeout, tenta baixar resultados parciais
            
            # 📥 BAIXAR TODOS OS RESULTADOS
            results_response = requests.get(
                f"{self.base_url}/datasets/{run_id}/items",
                headers={"Authorization": f"Bearer {self.apify_token}"},
                timeout=60  # Mais tempo para download
            )
            
            if results_response.status_code != 200:
                print(f"❌ Erro ao baixar resultados: {results_response.status_code}")
                return self._dados_fallback_linkedin()
            
            raw_jobs = results_response.json()
            total_encontradas = len(raw_jobs)
            
            print(f"🎊 SUCESSO! {total_encontradas} vagas encontradas pelo Apify!")
            
            # 🎯 ESTRATÉGIA INTELIGENTE DE LIMITE:
            if total_encontradas <= limite:
                # Se Apify trouxe menos que o limite, USA TODAS!
                vagas_finais = raw_jobs
                print(f"✅ Usando TODAS as {total_encontradas} vagas (menor que limite {limite})")
            else:
                # Se Apify trouxe mais, respeita o limite do usuário
                vagas_finais = raw_jobs[:limite] 
                print(f"📊 Limitando para {limite} vagas (Apify trouxe {total_encontradas})")
            
            # 🔧 PROCESSAR RESULTADOS
            processed_jobs = []
            for i, job_data in enumerate(vagas_finais):
                try:
                    processed_job = {
                        "titulo": job_data.get("jobTitle", "Título não informado"),
                        "empresa": job_data.get("companyName", "Empresa não informada"),
                        "localizacao": job_data.get("location", localizacao),
                        "descricao": job_data.get("description", "Descrição não disponível")[:500],
                        "link": job_data.get("jobUrl", "#"),
                        "data_publicacao": job_data.get("postedAt", "Não informado"),
                        "tipo_contrato": job_data.get("jobType", "Não especificado"),
                        "nivel_experiencia": job_data.get("seniorityLevel", "Não especificado"),
                        "salario": job_data.get("salary", "Não informado"),
                        "fonte": "LinkedIn (Apify)"
                    }
                    processed_jobs.append(processed_job)
                except Exception as e:
                    print(f"⚠️ Erro ao processar vaga {i+1}: {e}")
                    continue
            
            print(f"🎉 RESULTADO FINAL: {len(processed_jobs)} vagas processadas!")
            print(f"📈 Taxa de sucesso: {len(processed_jobs)/len(vagas_finais)*100:.1f}%")
            return processed_jobs
            
        except Exception as e:
            print(f"🚨 Erro no scraping LinkedIn: {e}")
            return self._dados_fallback_linkedin()
    
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
    
    def iniciar_execucao_apify(self, cargo: str, localizacao: str, limite: int = 800) -> tuple:
        """
        Inicia execução no Apify e retorna (run_id, dataset_id) para streaming
        """
        
        if not self.apify_token:
            return None, None
        
        try:
            # URL de busca otimizada
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={cargo}&location={localizacao}&f_TPR=r604800"
            
            # Parâmetros para o actor
            actor_input = {
                "urls": [search_url],
                "numberOfJobsNeeded": limite,
                "scrapeCompanyDetails": True,
                "proxy": {
                    "useApifyProxy": True,
                    "apifyProxyGroups": ["RESIDENTIAL"]
                }
            }
            
            # Iniciar execução
            run_response = requests.post(
                f"{self.base_url}/acts/{self.actor_id}/runs",
                params={"token": self.apify_token},
                json=actor_input,
                timeout=30
            )
            
            if run_response.status_code == 201:
                run_data = run_response.json()["data"]
                run_id = run_data["id"]
                dataset_id = run_data["defaultDatasetId"]
                
                print(f"🚀 Run iniciado: {run_id}, Dataset: {dataset_id}")
                return run_id, dataset_id
            else:
                print(f"❌ Erro ao iniciar run: {run_response.status_code}")
                return None, None
                
        except Exception as e:
            print(f"❌ Erro na execução Apify: {e}")
            return None, None
    
    def verificar_status_run(self, run_id: str) -> str:
        """
        Verifica status de um run específico
        """
        
        if not self.apify_token or not run_id:
            return "UNKNOWN"
        
        try:
            response = requests.get(
                f"{self.base_url}/actor-runs/{run_id}",
                params={"token": self.apify_token},
                timeout=10
            )
            
            if response.status_code == 200:
                status = response.json()["data"]["status"]
                return status
            else:
                return "ERROR"
                
        except Exception as e:
            print(f"❌ Erro ao verificar status: {e}")
            return "ERROR"
    
    def contar_resultados_dataset(self, dataset_id: str) -> int:
        """
        Conta quantos itens estão no dataset atualmente
        """
        
        if not self.apify_token or not dataset_id:
            return 0
        
        try:
            response = requests.get(
                f"{self.base_url}/datasets/{dataset_id}",
                params={"token": self.apify_token},
                timeout=10
            )
            
            if response.status_code == 200:
                item_count = response.json()["data"]["itemCount"]
                return item_count
            else:
                return 0
                
        except Exception as e:
            print(f"❌ Erro ao contar resultados: {e}")
            return 0
    
    def obter_resultados_parciais(self, dataset_id: str, offset: int, limit: int) -> List[Dict]:
        """
        Obtém resultados parciais do dataset (offset até limit)
        """
        
        if not self.apify_token or not dataset_id:
            return []
        
        try:
            params = {
                "token": self.apify_token,
                "format": "json",
                "clean": "true",
                "offset": offset,
                "limit": limit - offset
            }
            
            response = requests.get(
                f"{self.base_url}/datasets/{dataset_id}/items",
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                raw_jobs = response.json()
                
                # Processar vagas
                vagas_processadas = []
                for job in raw_jobs:
                    vaga_processada = self._processar_vaga_linkedin(job)
                    if vaga_processada:
                        vagas_processadas.append(vaga_processada)
                
                return vagas_processadas
            else:
                return []
                
        except Exception as e:
            print(f"❌ Erro ao obter resultados parciais: {e}")
            return []
    
    def obter_todos_resultados(self, dataset_id: str) -> List[Dict]:
        """
        Obtém todos os resultados finais do dataset
        """
        
        if not self.apify_token or not dataset_id:
            return []
        
        try:
            params = {
                "token": self.apify_token,
                "format": "json",
                "clean": "true"
            }
            
            response = requests.get(
                f"{self.base_url}/datasets/{dataset_id}/items",
                params=params,
                timeout=60
            )
            
            if response.status_code == 200:
                raw_jobs = response.json()
                
                # Processar todas as vagas
                vagas_processadas = []
                for job in raw_jobs:
                    vaga_processada = self._processar_vaga_linkedin(job)
                    if vaga_processada:
                        vagas_processadas.append(vaga_processada)
                
                print(f"✅ Total processado: {len(vagas_processadas)} vagas")
                return vagas_processadas
            else:
                return []
                
        except Exception as e:
            print(f"❌ Erro ao obter todos os resultados: {e}")
            return []


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