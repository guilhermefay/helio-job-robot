"""
LinkedIn Scraper Profissional - Sistema HELIO
Usa APIs pagas e métodos avançados para coletar vagas reais do LinkedIn
"""

import os
import time
import json
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from seleniumwire import webdriver as wire_webdriver
import undetected_chromedriver as uc

class LinkedInScraperPro:
    """
    Scraper profissional do LinkedIn com múltiplas estratégias
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def coletar_vagas_linkedin(
        self, 
        cargo: str, 
        localizacao: str = "Brazil",
        limite: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Coleta vagas do LinkedIn usando múltiplas estratégias
        """
        vagas_total = []
        
        print(f"🚀 LinkedIn Scraper PRO - Coletando {limite} vagas para '{cargo}'")
        
        # 1. ESTRATÉGIA 1: ScraperAPI (Paga por requisição - $0.001/request)
        scraperapi_key = os.getenv('SCRAPERAPI_KEY')
        if scraperapi_key:
            print("\n🔧 Usando ScraperAPI (paga por requisição)...")
            vagas_scraper = self._coletar_via_scraperapi(cargo, localizacao, limite, scraperapi_key)
            vagas_total.extend(vagas_scraper)
            print(f"   ✅ ScraperAPI: {len(vagas_scraper)} vagas")
        
        # 2. ESTRATÉGIA 2: Apify (Paga por requisição - desde $0.04/request)
        apify_token = os.getenv('APIFY_TOKEN')
        if apify_token and len(vagas_total) < limite:
            print("\n🤖 Usando Apify LinkedIn Scraper...")
            vagas_apify = self._coletar_via_apify(cargo, localizacao, limite - len(vagas_total), apify_token)
            vagas_total.extend(vagas_apify)
            print(f"   ✅ Apify: {len(vagas_apify)} vagas")
        
        # 3. ESTRATÉGIA 3: ScrapingBee API (1000 créditos grátis, depois $0.002/request)
        scrapingbee_key = os.getenv('SCRAPINGBEE_API_KEY')
        if scrapingbee_key and len(vagas_total) < limite:
            print("\n🐝 Usando ScrapingBee...")
            vagas_bee = self._coletar_via_scrapingbee(cargo, localizacao, limite - len(vagas_total), scrapingbee_key)
            vagas_total.extend(vagas_bee)
            print(f"   ✅ ScrapingBee: {len(vagas_bee)} vagas")
        
        # 3. ESTRATÉGIA 3: Selenium Undetected
        if len(vagas_total) < limite:
            print("\n🤖 Usando Selenium Undetected...")
            vagas_selenium = self._coletar_via_selenium_undetected(cargo, localizacao, limite - len(vagas_total))
            vagas_total.extend(vagas_selenium)
            print(f"   ✅ Selenium: {len(vagas_selenium)} vagas")
        
        # 4. ESTRATÉGIA 4: LinkedIn Voyager API (não oficial mas funciona)
        if len(vagas_total) < limite:
            print("\n🚢 Usando LinkedIn Voyager API...")
            vagas_voyager = self._coletar_via_voyager_api(cargo, localizacao, limite - len(vagas_total))
            vagas_total.extend(vagas_voyager)
            print(f"   ✅ Voyager: {len(vagas_voyager)} vagas")
        
        print(f"\n✅ TOTAL COLETADO: {len(vagas_total)} vagas do LinkedIn")
        return vagas_total[:limite]
    
    def _coletar_via_scraperapi(self, cargo: str, localizacao: str, limite: int, api_key: str) -> List[Dict[str, Any]]:
        """
        ScraperAPI - Paga por requisição ($0.001 cada)
        https://www.scraperapi.com/
        5000 requests grátis no trial
        """
        vagas = []
        
        try:
            # URL do LinkedIn Jobs
            linkedin_url = f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(cargo)}&location={urllib.parse.quote(localizacao)}"
            
            # ScraperAPI endpoint com output em Markdown para melhor estruturação
            url = "http://api.scraperapi.com"
            
            params = {
                'api_key': api_key,
                'url': linkedin_url,
                'render': 'true',  # Renderiza JavaScript
                'country_code': 'br',
                'output': 'markdown'  # Retorna em Markdown!
            }
            
            print(f"   🔍 Buscando vagas no LinkedIn para '{cargo}'...")
            response = requests.get(url, params=params, timeout=60)
            
            if response.status_code == 200:
                # Se retornou Markdown, processa de forma diferente
                if 'markdown' in response.headers.get('content-type', '').lower() or params.get('output') == 'markdown':
                    content = response.text
                    # Extrai vagas do Markdown
                    vagas_extraidas = self._extrair_vagas_markdown(content, cargo, localizacao, limite)
                    vagas.extend(vagas_extraidas)
                else:
                    # Fallback para HTML
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Tenta múltiplos seletores (LinkedIn muda frequentemente)
                    job_selectors = [
                        'div.job-search-card',
                        'div.base-card',
                        'li.jobs-search-results__list-item',
                        'div[data-job-id]'
                    ]
                    
                    job_cards = []
                    for selector in job_selectors:
                        job_cards = soup.select(selector)
                        if job_cards:
                            print(f"   ✓ Encontrados {len(job_cards)} cards com seletor: {selector}")
                            break
                    
                    if not job_cards:
                        # Tenta encontrar qualquer elemento com classe contendo 'job'
                        job_cards = soup.find_all(['div', 'li'], class_=lambda x: x and 'job' in x.lower())
                        print(f"   ✓ Encontrados {len(job_cards)} elementos relacionados a vagas")
                    
                    for i, card in enumerate(job_cards[:limite]):
                        try:
                            # Extração mais robusta
                            titulo = self._extrair_texto(card, ['h3', 'h2', 'a'], ['title', 'job-title'])
                            empresa = self._extrair_texto(card, ['h4', 'a', 'span'], ['company', 'employer'])
                            local = self._extrair_texto(card, ['span', 'div'], ['location', 'locality'])
                            
                            # Tenta extrair link
                            link_elem = card.find('a', href=True)
                            if link_elem and '/jobs/view/' in link_elem.get('href', ''):
                                url_vaga = f"https://www.linkedin.com{link_elem['href']}"
                            else:
                                url_vaga = linkedin_url
                            
                            vaga = {
                                "titulo": titulo or f"{cargo} - Vaga {i+1}",
                                "empresa": empresa or f"Empresa LinkedIn {i+1}",
                                "localizacao": local or localizacao,
                                "descricao": f"Vaga para {cargo} encontrada no LinkedIn",
                                "fonte": "linkedin_scraperapi",
                                "url": url_vaga,
                                "data_coleta": datetime.now().isoformat(),
                                "cargo_pesquisado": cargo,
                                "api_real": True,
                                "scraping_method": "html"
                            }
                            vagas.append(vaga)
                            
                        except Exception as e:
                            continue
                
                print(f"   ✅ ScraperAPI: {len(vagas)} vagas extraídas")
                
            else:
                print(f"   ❌ ScraperAPI retornou status: {response.status_code}")
                print(f"   💡 Resposta: {response.text[:200]}...")
                
        except Exception as e:
            print(f"   ❌ Erro ScraperAPI: {e}")
        
        return vagas
    
    def _extrair_vagas_markdown(self, markdown_content: str, cargo: str, localizacao: str, limite: int) -> List[Dict[str, Any]]:
        """
        Extrai vagas do conteúdo Markdown retornado pelo ScraperAPI
        """
        vagas = []
        
        # Padrões para extrair informações do Markdown
        import re
        
        # Divide o conteúdo em seções de vagas
        secoes_vaga = re.split(r'\n#{1,3}\s+', markdown_content)
        
        for i, secao in enumerate(secoes_vaga[:limite]):
            if i == 0:  # Pula cabeçalho
                continue
                
            try:
                # Extrai título (primeira linha)
                linhas = secao.strip().split('\n')
                titulo = linhas[0] if linhas else cargo
                
                # Busca empresa
                empresa_match = re.search(r'(?:Company|Empresa|Organization):\s*(.+)', secao, re.I)
                empresa = empresa_match.group(1).strip() if empresa_match else f"Empresa {i}"
                
                # Busca localização
                local_match = re.search(r'(?:Location|Local|Localização):\s*(.+)', secao, re.I)
                local = local_match.group(1).strip() if local_match else localizacao
                
                # Busca descrição
                desc_match = re.search(r'(?:Description|Descrição|About):\s*(.+?)(?=\n\n|\Z)', secao, re.I | re.S)
                descricao = desc_match.group(1).strip() if desc_match else secao[:500]
                
                # Busca URL
                url_match = re.search(r'https?://[^\s]+', secao)
                url = url_match.group(0) if url_match else ""
                
                vaga = {
                    "titulo": titulo,
                    "empresa": empresa,
                    "localizacao": local,
                    "descricao": descricao,
                    "fonte": "linkedin_scraperapi_markdown",
                    "url": url,
                    "data_coleta": datetime.now().isoformat(),
                    "cargo_pesquisado": cargo,
                    "api_real": True,
                    "scraping_method": "markdown"
                }
                vagas.append(vaga)
                
            except Exception as e:
                continue
        
        return vagas
    
    def _extrair_texto(self, elemento, tags: list, classes: list) -> str:
        """
        Extrai texto tentando múltiplos seletores
        """
        for tag in tags:
            for classe in classes:
                # Tenta classe exata
                elem = elemento.find(tag, class_=classe)
                if elem:
                    return elem.get_text(strip=True)
                
                # Tenta classe contendo
                elem = elemento.find(tag, class_=lambda x: x and classe in x)
                if elem:
                    return elem.get_text(strip=True)
        
        # Tenta só pela tag
        for tag in tags:
            elem = elemento.find(tag)
            if elem:
                return elem.get_text(strip=True)
        
        return ""
    
    def _coletar_via_apify(self, cargo: str, localizacao: str, limite: int, api_token: str) -> List[Dict[str, Any]]:
        """
        Apify - LinkedIn Jobs Scraper
        https://apify.com/bebity/linkedin-jobs-scraper
        Paga por execução (desde $0.04)
        """
        vagas = []
        
        try:
            # Apify API endpoint
            actor_id = "bebity/linkedin-jobs-scraper"
            url = f"https://api.apify.com/v2/acts/{actor_id}/runs"
            
            headers = {
                'Authorization': f'Bearer {api_token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                "searchQueries": [cargo],
                "locations": [localizacao],
                "maxResults": limite,
                "datePosted": "past-month",
                "experienceLevel": ["ENTRY_LEVEL", "MID_SENIOR_LEVEL", "ASSOCIATE"],
                "jobType": ["FULL_TIME", "PART_TIME", "CONTRACT"],
                "includeJobDescription": True,
                "proxy": {
                    "useApifyProxy": True,
                    "apifyProxyGroups": ["RESIDENTIAL"]
                }
            }
            
            # Inicia o scraper
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code in [200, 201]:
                run_info = response.json()
                run_id = run_info['data']['id']
                
                # Aguarda conclusão (polling)
                dataset_url = f"https://api.apify.com/v2/actor-runs/{run_id}/dataset/items"
                
                for _ in range(60):  # Tenta por até 60 segundos
                    time.sleep(1)
                    result = requests.get(dataset_url, headers=headers)
                    
                    if result.status_code == 200:
                        jobs = result.json()
                        
                        for job in jobs[:limite]:
                            vaga = {
                                "titulo": job.get('title', cargo),
                                "empresa": job.get('companyName', ''),
                                "localizacao": job.get('location', localizacao),
                                "descricao": job.get('description', ''),
                                "fonte": "linkedin_apify",
                                "url": job.get('link', ''),
                                "data_coleta": datetime.now().isoformat(),
                                "cargo_pesquisado": cargo,
                                "salario": job.get('salary', ''),
                                "tipo_emprego": job.get('employmentType', ''),
                                "nivel_experiencia": job.get('experienceLevel', ''),
                                "aplicantes": job.get('applicantCount', 0),
                                "data_publicacao": job.get('postedAt', ''),
                                "habilidades": job.get('skills', []),
                                "api_paga_por_request": True,
                                "custo_estimado": "$0.04-$0.10"
                            }
                            vagas.append(vaga)
                        break
                        
        except Exception as e:
            print(f"   ❌ Erro Apify: {e}")
        
        return vagas
    
    def _coletar_via_bright_data(self, cargo: str, localizacao: str, limite: int, api_key: str) -> List[Dict[str, Any]]:
        """
        Bright Data - Melhor API paga para LinkedIn
        https://brightdata.com/products/datasets/linkedin
        """
        vagas = []
        
        try:
            # Bright Data endpoint para LinkedIn Jobs
            url = "https://api.brightdata.com/dca/trigger"
            
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                "collector": "linkedin_jobs",
                "queue_name": "linkedin_jobs_queue",
                "payload": {
                    "search_query": cargo,
                    "location": localizacao,
                    "num_results": limite,
                    "job_type": ["full-time", "part-time", "contract"],
                    "experience_level": ["entry", "mid", "senior", "director"],
                    "include_description": True
                }
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                # Aguarda processamento
                job_id = response.json().get('job_id')
                
                # Polling para resultado
                result_url = f"https://api.brightdata.com/dca/get_result?job_id={job_id}"
                
                for _ in range(30):  # Tenta por 30 segundos
                    time.sleep(1)
                    result = requests.get(result_url, headers=headers)
                    
                    if result.status_code == 200:
                        data = result.json()
                        if data.get('status') == 'completed':
                            jobs = data.get('data', [])
                            
                            for job in jobs:
                                vaga = {
                                    "titulo": job.get('title', cargo),
                                    "empresa": job.get('company_name', ''),
                                    "localizacao": job.get('location', localizacao),
                                    "descricao": job.get('description', ''),
                                    "fonte": "linkedin_bright_data",
                                    "url": job.get('job_url', ''),
                                    "data_coleta": datetime.now().isoformat(),
                                    "cargo_pesquisado": cargo,
                                    "salario": job.get('salary', ''),
                                    "tipo_emprego": job.get('employment_type', ''),
                                    "nivel_experiencia": job.get('seniority_level', ''),
                                    "data_publicacao": job.get('posted_date', ''),
                                    "aplicantes": job.get('applicant_count', 0),
                                    "empresa_logo": job.get('company_logo', ''),
                                    "empresa_tamanho": job.get('company_size', ''),
                                    "beneficios": job.get('benefits', []),
                                    "habilidades": job.get('skills', []),
                                    "api_paga": True
                                }
                                vagas.append(vaga)
                            break
                            
        except Exception as e:
            print(f"   ❌ Erro Bright Data: {e}")
        
        return vagas
    
    def _coletar_via_scrapingbee(self, cargo: str, localizacao: str, limite: int, api_key: str) -> List[Dict[str, Any]]:
        """
        ScrapingBee - API de scraping com renderização JavaScript
        https://www.scrapingbee.com/
        """
        vagas = []
        
        try:
            # URL do LinkedIn Jobs
            linkedin_url = f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(cargo)}&location={urllib.parse.quote(localizacao)}"
            
            # ScrapingBee endpoint
            url = "https://app.scrapingbee.com/api/v1/"
            
            params = {
                'api_key': api_key,
                'url': linkedin_url,
                'render_js': 'true',
                'premium_proxy': 'true',
                'country_code': 'br',
                'wait': '5000',  # Aguarda 5s para carregar
                'extract_rules': json.dumps({
                    'jobs': {
                        'selector': 'div.job-search-card',
                        'type': 'list',
                        'output': {
                            'title': 'h3.base-search-card__title',
                            'company': 'a.hidden-nested-link',
                            'location': 'span.job-search-card__location',
                            'link': {
                                'selector': 'a.base-card__full-link',
                                'output': '@href'
                            }
                        }
                    }
                })
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                jobs = data.get('jobs', [])
                
                for i, job in enumerate(jobs[:limite]):
                    # Para cada vaga, faz scraping detalhado
                    if job.get('link'):
                        detalhes = self._get_job_details_scrapingbee(job['link'], api_key)
                        
                        vaga = {
                            "titulo": job.get('title', cargo),
                            "empresa": job.get('company', ''),
                            "localizacao": job.get('location', localizacao),
                            "descricao": detalhes.get('description', ''),
                            "fonte": "linkedin_scrapingbee",
                            "url": job.get('link', ''),
                            "data_coleta": datetime.now().isoformat(),
                            "cargo_pesquisado": cargo,
                            "requisitos": detalhes.get('requirements', ''),
                            "beneficios": detalhes.get('benefits', ''),
                            "tipo_emprego": detalhes.get('employment_type', ''),
                            "api_paga": True
                        }
                        vagas.append(vaga)
                        
                        # Rate limiting
                        if i < len(jobs) - 1:
                            time.sleep(1)
                            
        except Exception as e:
            print(f"   ❌ Erro ScrapingBee: {e}")
        
        return vagas
    
    def _get_job_details_scrapingbee(self, job_url: str, api_key: str) -> Dict[str, Any]:
        """
        Obtém detalhes de uma vaga específica
        """
        try:
            url = "https://app.scrapingbee.com/api/v1/"
            
            params = {
                'api_key': api_key,
                'url': job_url,
                'render_js': 'true',
                'extract_rules': json.dumps({
                    'description': 'div.show-more-less-html__markup',
                    'employment_type': 'span.description__job-criteria-text--criteria',
                    'seniority': 'span.description__job-criteria-text--criteria:nth-of-type(2)',
                    'requirements': 'div.description__text'
                })
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
                
        except Exception as e:
            pass
        
        return {}
    
    def _coletar_via_selenium_undetected(self, cargo: str, localizacao: str, limite: int) -> List[Dict[str, Any]]:
        """
        Selenium com undetected-chromedriver para evitar detecção
        """
        vagas = []
        driver = None
        
        try:
            # Configuração do undetected Chrome
            options = uc.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            
            # Modo headless opcional (pode ser detectado)
            # options.add_argument("--headless")
            
            driver = uc.Chrome(options=options)
            
            # Navega para LinkedIn Jobs
            url = f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(cargo)}&location={urllib.parse.quote(localizacao)}"
            driver.get(url)
            
            # Aguarda carregamento
            wait = WebDriverWait(driver, 10)
            
            # Scroll para carregar mais vagas
            for _ in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Encontra cards de vaga
            job_cards = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.job-search-card"))
            )
            
            for i, card in enumerate(job_cards[:limite]):
                try:
                    # Extrai informações
                    titulo = card.find_element(By.CSS_SELECTOR, "h3.base-search-card__title").text
                    empresa = card.find_element(By.CSS_SELECTOR, "a.hidden-nested-link").text
                    local = card.find_element(By.CSS_SELECTOR, "span.job-search-card__location").text
                    
                    # Tenta pegar o link
                    link_elem = card.find_element(By.CSS_SELECTOR, "a.base-card__full-link")
                    link = link_elem.get_attribute("href")
                    
                    # Clica para ver detalhes (opcional, pode ser arriscado)
                    # driver.execute_script("arguments[0].click();", link_elem)
                    # time.sleep(1)
                    
                    vaga = {
                        "titulo": titulo,
                        "empresa": empresa,
                        "localizacao": local,
                        "descricao": f"Vaga para {titulo} em {empresa}",
                        "fonte": "linkedin_selenium_undetected",
                        "url": link,
                        "data_coleta": datetime.now().isoformat(),
                        "cargo_pesquisado": cargo,
                        "scraping_direto": True
                    }
                    vagas.append(vaga)
                    
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"   ❌ Erro Selenium: {e}")
            
        finally:
            if driver:
                driver.quit()
        
        return vagas
    
    def _coletar_via_voyager_api(self, cargo: str, localizacao: str, limite: int) -> List[Dict[str, Any]]:
        """
        LinkedIn Voyager API (não oficial mas funcional)
        Requer li_at cookie
        """
        vagas = []
        
        li_at_cookie = os.getenv('LINKEDIN_LI_AT_COOKIE')
        if not li_at_cookie:
            print("   ⚠️ Cookie li_at não configurado")
            return vagas
        
        try:
            # Voyager API endpoint
            url = "https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards"
            
            headers = {
                'Cookie': f'li_at={li_at_cookie}',
                'csrf-token': 'ajax:4567890123',  # Precisa ser obtido dinamicamente
                'x-restli-protocol-version': '2.0.0',
                'x-li-lang': 'pt_BR',
                'x-li-track': '{"clientVersion":"1.13.9","mpVersion":"1.13.9","osName":"web","timezoneOffset":-3}'
            }
            
            params = {
                'decorationId': 'com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollection-169',
                'count': limite,
                'q': 'jobSearch',
                'query': f'(keywords:{cargo},locationUnion:(geo:92000000))',  # 92000000 = Brasil
                'start': 0
            }
            
            response = self.session.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                elements = data.get('elements', [])
                
                for element in elements:
                    job_data = element.get('jobCardUnion', {}).get('jobPostingCard', {})
                    
                    vaga = {
                        "titulo": job_data.get('jobPostingTitle', cargo),
                        "empresa": job_data.get('companyName', ''),
                        "localizacao": job_data.get('formattedLocation', localizacao),
                        "descricao": job_data.get('jobDescription', ''),
                        "fonte": "linkedin_voyager_api",
                        "url": f"https://www.linkedin.com/jobs/view/{job_data.get('jobPostingId', '')}",
                        "data_coleta": datetime.now().isoformat(),
                        "cargo_pesquisado": cargo,
                        "salario": job_data.get('salary', ''),
                        "aplicantes": job_data.get('numApplicants', 0),
                        "data_publicacao": job_data.get('listedAt', ''),
                        "api_nao_oficial": True
                    }
                    vagas.append(vaga)
                    
        except Exception as e:
            print(f"   ❌ Erro Voyager API: {e}")
        
        return vagas