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
        self.actor_id = "easyapi~catho-jobs-scraper"  # ✅ Actor da Catho (Legal)
        
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
        
        print("=" * 50)
        print("🔍 INICIANDO coletar_vagas_linkedin")
        print(f"📝 Parâmetros: cargo='{cargo}', localizacao='{localizacao}', limite={limite}")
        print(f"🔑 Token APIFY: {'✅ PRESENTE' if self.apify_token else '❌ AUSENTE'}")
        print(f"🔑 Token length: {len(self.apify_token) if self.apify_token else 0}")
        print(f"🔑 Token preview: {self.apify_token[:10]}..." if self.apify_token else "N/A")
        print("=" * 50)
        
        if not self.apify_token:
            print("🚨 Token Apify não configurado. Usando fallback.")
            print("🔥 ATENÇÃO: Chamando FALLBACK ao invés de Apify real!")
            return self._fallback_linkedin_data(cargo, localizacao, limite)
        
        try:
            # 🎯 INPUT PARA CATHO: Mesmos parâmetros do iniciar_execucao_apify
            input_data = {
                "query": cargo,  # Termo de busca principal
                "search": cargo,  # Termo de busca (fallback)
                "keyword": cargo,  # Palavra-chave (fallback)
                "location": localizacao,  # Local da vaga  
                "city": localizacao,  # Cidade (fallback)
                "estado": "SP",  # Estado específico
                "maxItems": limite,  # Número máximo de itens
                "maxResults": limite,  # Número máximo (fallback)
                "maxPages": max(1, limite // 20),  # Páginas a percorrer
                "startPage": 1,  # Página inicial
                "proxy": {
                    "useApifyProxy": True,
                    "apifyProxyGroups": ["RESIDENTIAL"]
                }
            }
            
            print(f"🚀 Buscando MÁXIMO de vagas: {cargo} em {localizacao}")
            print(f"📊 Limite do usuário: {limite} | Apify buscará: até 20.000!")
            
            # Iniciar execução
            print(f"🌐 Fazendo request para Apify: {self.base_url}/acts/{self.actor_id}/runs")
            print(f"📦 Input data: {json.dumps(input_data, indent=2)}")
            
            run_response = requests.post(
                f"{self.base_url}/acts/{self.actor_id}/runs",
                headers={
                    "Authorization": f"Bearer {self.apify_token}",
                    "Content-Type": "application/json"
                },
                json=input_data,
                timeout=30
            )
            
            print(f"📡 Response status: {run_response.status_code}")
            print(f"📡 Response headers: {dict(run_response.headers)}")
            
            if run_response.status_code != 201:
                print(f"❌ Erro ao iniciar scraping: {run_response.status_code}")
                print(f"❌ Response body: {run_response.text}")
                print("🔥 ATENÇÃO: Chamando FALLBACK ao invés de Apify real!")
                return self._fallback_linkedin_data(cargo, localizacao, limite)
            
            run_data = run_response.json()
            run_id = run_data["data"]["id"]
            print(f"✅ Scraping iniciado - ID: {run_id}")
            
            # 🕐 AGUARDAR com paciência mas não demais
            max_attempts = 20  # ~3.5 minutos máximo (para API ser mais rápida)
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
                    status_data = status_response.json()
                    status = status_data["data"]["status"]
                    
                    # 📊 Log progresso a cada minuto
                    if attempt % 6 == 0:  # A cada 6 checks = 1 minuto
                        print(f"⏳ Aguardando... {attempt//6}min | Status: {status}")
                    
                    if status == "SUCCEEDED":
                        print(f"🎉 Scraping concluído em {attempt//6}min!")
                        break
                    elif status in ["FAILED", "ABORTED", "TIMED-OUT"]:
                        print(f"❌ Scraping falhou: {status}")
                        print("🔥 ATENÇÃO: Chamando FALLBACK ao invés de Apify real!")
                        return self._fallback_linkedin_data(cargo, localizacao, limite)
                else:
                    print(f"⚠️ Erro ao verificar status: {status_response.status_code}")
            
            if attempt >= max_attempts:
                print("⏰ Timeout: Mas vamos tentar baixar o que conseguiu...")
                # 🎯 Mesmo com timeout, tenta baixar resultados parciais
            
            # 📥 BAIXAR TODOS OS RESULTADOS
            print(f"📥 Baixando resultados...")
            
            # 🎯 CORREÇÃO: Primeiro obter info do run para pegar o datasetId
            run_info_response = requests.get(
                f"{self.base_url}/actor-runs/{run_id}",
                headers={"Authorization": f"Bearer {self.apify_token}"},
                timeout=30
            )
            
            if run_info_response.status_code == 200:
                run_info = run_info_response.json()
                dataset_id = run_info["data"]["defaultDatasetId"]
            else:
                print(f"⚠️ Erro ao obter dataset ID: {run_info_response.status_code}")
                # Fallback: usar run_id como dataset_id (pode não funcionar)
                dataset_id = run_id
            
            results_response = requests.get(
                f"{self.base_url}/datasets/{dataset_id}/items",
                headers={"Authorization": f"Bearer {self.apify_token}"},
                timeout=60  # Mais tempo para download
            )
            
            if results_response.status_code != 200:
                print(f"❌ Erro ao baixar resultados: {results_response.status_code}")
                print("🔥 ATENÇÃO: Chamando FALLBACK ao invés de Apify real!")
                return self._fallback_linkedin_data(cargo, localizacao, limite)
            
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
            processed_jobs = self._processar_resultados_apify(vagas_finais, cargo)
            
            print(f"🎉 RESULTADO FINAL: {len(processed_jobs)} vagas processadas!")
            print(f"📈 Taxa de sucesso: {len(processed_jobs)/len(vagas_finais)*100:.1f}%")
            return processed_jobs
                
        except Exception as e:
            print(f"🚨 Erro no scraping LinkedIn: {e}")
            print("🔥 ATENÇÃO: Chamando FALLBACK ao invés de Apify real!")
            return self._fallback_linkedin_data(cargo, localizacao, limite)

    def _dados_fallback_linkedin(self) -> List[Dict[str, Any]]:
        """
        Dados de fallback quando APIFY falha
        """
        print("🔄 Usando dados de fallback para demonstração")
        
        vagas_fallback = [
            {
                "titulo": "Desenvolvedor Python",
                "empresa": "TechCorp",
                "localizacao": "São Paulo, SP",
                "descricao": "Vaga para desenvolvedor Python com experiência em Django/Flask",
                "link": "https://linkedin.com/jobs/fallback-1",
                "fonte": "Fallback LinkedIn",
                "data_publicacao": "2 dias atrás",
                "salario": "R$ 8.000,00",
                "tipo_contrato": "CLT",
                "nivel_experiencia": "Pleno"
            },
            {
                "titulo": "Full Stack Developer",
                "empresa": "StartupXYZ",
                "localizacao": "São Paulo, SP", 
                "descricao": "Desenvolvedor full stack para aplicações React/Node.js",
                "link": "https://linkedin.com/jobs/fallback-2",
                "fonte": "Fallback LinkedIn",
                "data_publicacao": "1 dia atrás",
                "salario": "R$ 10.000,00",
                "tipo_contrato": "PJ",
                "nivel_experiencia": "Sênior"
            },
            {
                "titulo": "Backend Developer",
                "empresa": "BigTech",
                "localizacao": "São Paulo, SP",
                "descricao": "Desenvolvedor backend com foco em Python e APIs REST",
                "link": "https://linkedin.com/jobs/fallback-3", 
                "fonte": "Fallback LinkedIn",
                "data_publicacao": "3 dias atrás",
                "salario": "R$ 12.000,00",
                "tipo_contrato": "CLT",
                "nivel_experiencia": "Sênior"
            }
        ]
        
        return vagas_fallback
    
    def _processar_vaga_linkedin(self, job_data: Dict) -> Dict[str, Any]:
        """
        Processa uma única vaga do LinkedIn/Apify para o formato padrão
        """
        try:
            # Debug: ver estrutura dos dados
            print(f"🔍 DEBUG - Estrutura da vaga recebida:")
            print(f"   Chaves: {list(job_data.keys())[:10]}")  # Primeiras 10 chaves
            
            # Verificar possíveis campos de título
            titulo_campos = ['titulo', 'title', 'jobTitle', 'cargo', 'position', 'nome']
            for campo in titulo_campos:
                if campo in job_data:
                    print(f"   Campo '{campo}' encontrado: {job_data.get(campo, '')[:50]}...")
                    
            # Verificar possíveis campos de empresa
            empresa_campos = ['anunciante', 'empresa', 'company', 'employer', 'companyName']
            for campo in empresa_campos:
                if campo in job_data:
                    print(f"   Campo '{campo}' encontrado: {str(job_data.get(campo))[:50]}...")
            
            # Mapeamento baseado na estrutura real do Catho
            # Extrair informações da empresa com múltiplos fallbacks
            anunciante = job_data.get('anunciante', {})
            contratante = job_data.get('contratante', {})
            
            # Tentar várias formas de obter o nome da empresa
            empresa_nome = None
            
            # Se anunciante é dict
            if isinstance(anunciante, dict):
                empresa_nome = anunciante.get('nome') or anunciante.get('name')
            # Se anunciante é string
            elif isinstance(anunciante, str):
                empresa_nome = anunciante
                
            # Se ainda não achou, tentar contratante
            if not empresa_nome and isinstance(contratante, dict):
                empresa_nome = contratante.get('nome') or contratante.get('name')
            elif not empresa_nome and isinstance(contratante, str):
                empresa_nome = contratante
                
            # Outros campos possíveis
            if not empresa_nome:
                empresa_nome = (
                    job_data.get('empresa') or
                    job_data.get('company') or
                    job_data.get('companyName') or
                    job_data.get('employer') or
                    job_data.get('employerName') or
                    'Empresa não informada'
                )
            
            # Extrair localização das vagas com múltiplos fallbacks
            localizacao = None
            
            # Tentar primeiro o array vagas
            vagas_info = job_data.get('vagas', [])
            if vagas_info and len(vagas_info) > 0:
                vaga_local = vagas_info[0]
                cidade = vaga_local.get('cidade', '')
                uf = vaga_local.get('uf', '')
                if cidade and uf:
                    localizacao = f"{cidade}, {uf}"
                elif cidade:
                    localizacao = cidade
                elif uf:
                    localizacao = uf
            
            # Se não achou, tentar outros campos
            if not localizacao:
                localizacao = (
                    job_data.get('location') or
                    job_data.get('localizacao') or
                    job_data.get('local') or
                    job_data.get('cidade') or
                    job_data.get('city') or
                    'Local não informado'
                )
            
            # Montar salário
            salario_info = job_data.get('faixaSalarial', '')
            if not salario_info and job_data.get('salario'):
                salario_info = f"R$ {job_data.get('salario')}"
            if not salario_info:
                salario_info = 'A combinar' if job_data.get('salarioACombinar') else 'Não informado'
            
            # Extrair título com fallbacks
            titulo = (
                job_data.get('titulo') or 
                job_data.get('title') or 
                job_data.get('jobTitle') or 
                job_data.get('cargo') or 
                job_data.get('position') or
                job_data.get('nome') or
                'Título não disponível'
            )
            
            # Extrair descrição com fallbacks
            descricao = (
                job_data.get('descricao') or 
                job_data.get('description') or 
                job_data.get('jobDescription') or
                job_data.get('details') or
                'Descrição não disponível'
            )
            
            # Extrair URL com fallbacks
            url = (
                job_data.get('searchUrl') or
                job_data.get('url') or
                job_data.get('link') or
                job_data.get('jobUrl') or
                ''
            )
            
            vaga = {
                "titulo": titulo,
                "empresa": empresa_nome,
                "localizacao": localizacao,
                "descricao": descricao,
                "fonte": "catho",
                "url": url,
                "data_coleta": datetime.now().isoformat(),
                "data_publicacao": job_data.get('data', job_data.get('datePosted', '')),
                "salario": salario_info,
                "tipo_emprego": job_data.get('regimeContrato', job_data.get('employmentType', 'Não especificado')),
                "nivel_experiencia": job_data.get('level', 'Não especificado'),
                "beneficios": job_data.get('benef', job_data.get('benefits', [])),
                "requisitos": job_data.get('requirements', ''),
                "horario": job_data.get('horario', ''),
                "info_adicional": job_data.get('infoAdicional', ''),
                "job_id": job_data.get('job_id', job_data.get('id', '')),
                "apify_real": True  # Marca como dados reais do Apify
            }
            
            return vaga
            
        except Exception as e:
            print(f"⚠️ Erro ao processar vaga individual: {e}")
            return None
    
    def _processar_resultados_apify(self, items: List[Dict], cargo_pesquisado: str) -> List[Dict[str, Any]]:
        """
        Processa os resultados do Apify para o formato padrão
        Usa o mesmo processamento do _processar_vaga_linkedin
        """
        vagas_processadas = []
        
        for item in items:
            try:
                vaga_processada = self._processar_vaga_linkedin(item)
                if vaga_processada:
                    vaga_processada['cargo_pesquisado'] = cargo_pesquisado
                    vagas_processadas.append(vaga_processada)
                
            except Exception as e:
                print(f"⚠️  Erro ao processar vaga: {e}")
                continue
        
        print(f"✅ Processadas {len(vagas_processadas)} vagas da Catho via Apify")
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
        Verifica se as credenciais do Apify estão configuradas e válidas
        """
        print("=" * 50)
        print("🔐 VERIFICANDO CREDENCIAIS APIFY")
        
        if not self.apify_token:
            print("❌ APIFY_API_TOKEN não encontrado!")
            print("📌 Configure no arquivo .env:")
            print("   APIFY_API_TOKEN=seu_token_aqui")
            print("=" * 50)
            return False
        
        print(f"✅ Token presente: {len(self.apify_token)} caracteres")
        
        # Verificar se o token é válido fazendo uma chamada à API
        try:
            print("🌐 Verificando token com API Apify...")
            url = f"{self.base_url}/users/me"
            headers = {"Authorization": f"Bearer {self.apify_token}"}
            
            response = requests.get(url, headers=headers, timeout=5)
            print(f"📡 Status: {response.status_code}")
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ Token válido! Usuário: {user_data.get('data', {}).get('username', 'Unknown')}")
                print("=" * 50)
                return True
            else:
                print(f"❌ Token inválido! Status: {response.status_code}")
                print(f"❌ Resposta: {response.text[:200]}")
                print("=" * 50)
                return False
                
        except Exception as e:
            print(f"❌ Erro ao verificar token: {e}")
            print("=" * 50)
            return False

    def coletar_vagas(self, cargo: str, localizacao: str = "São Paulo, Brazil", total_vagas: int = 20) -> Dict[str, Any]:
        """
        Método principal para coleta de vagas - usado pela API
        
        Args:
            cargo: Cargo/função desejada
            localizacao: Localização das vagas
            total_vagas: Número total de vagas a coletar
            
        Returns:
            Dict com resultado da coleta
        """
        print(f"🎯 Iniciando coleta APIFY: {cargo} em {localizacao}")
        
        inicio = time.time()
        
        # Usar o método principal de coleta
        vagas = self.coletar_vagas_linkedin(
            cargo=cargo,
            localizacao=localizacao, 
            limite=total_vagas
        )
        
        tempo_execucao = time.time() - inicio
        
        # Montar resultado no formato esperado pela API
        resultado = {
            'vagas': vagas,
            'total_coletadas': len(vagas),
            'tempo_execucao': f"{tempo_execucao:.2f}s",
            'actor_id': self.actor_id,
            'metodo': 'apify_linkedin_scraper',
            'parametros_busca': {
                'cargo': cargo,
                'localizacao': localizacao,
                'total_solicitado': total_vagas
            }
        }
        
        print(f"✅ Coleta finalizada: {len(vagas)} vagas em {tempo_execucao:.2f}s")
        
        return resultado
    
    def iniciar_execucao_apify(self, cargo: str, localizacao: str, limite: int = 800) -> tuple:
        """
        Inicia execução no Apify e retorna (run_id, dataset_id) para streaming
        """
        
        if not self.apify_token:
            return None, None
        
        try:
            # Parâmetros para o actor da Catho easyapi
            # Baseado em scrapers típicos da Catho
            # IMPORTANTE: O campo de busca precisa ser bem específico
            actor_input = {
                "query": cargo,  # Termo de busca principal
                "search": cargo,  # Termo de busca (fallback)
                "keyword": cargo,  # Palavra-chave (fallback)
                "location": localizacao,  # Local da vaga  
                "city": localizacao,  # Cidade (fallback)
                "estado": "SP",  # Estado específico
                "maxItems": limite,  # Número máximo de itens
                "maxResults": limite,  # Número máximo (fallback)
                "maxPages": max(1, limite // 20),  # Páginas a percorrer
                "startPage": 1,  # Página inicial
                "proxy": {
                    "useApifyProxy": True,
                    "apifyProxyGroups": ["RESIDENTIAL"]
                }
            }
            
            print(f"📤 Enviando para Catho actor com input: {json.dumps(actor_input, indent=2)}")
            
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
                
                print(f"📦 Obtidos {len(raw_jobs)} itens do dataset")
                
                # Processar vagas
                vagas_processadas = []
                for i, job in enumerate(raw_jobs):
                    if job and isinstance(job, dict):
                        vaga_processada = self._processar_vaga_linkedin(job)
                        if vaga_processada:
                            vagas_processadas.append(vaga_processada)
                    else:
                        print(f"⚠️ Item {i} não é um dicionário válido: {type(job)}")
                
                print(f"✅ Processadas {len(vagas_processadas)} vagas válidas")
                return vagas_processadas
            else:
                print(f"❌ Erro HTTP {response.status_code} ao obter resultados")
                return []
                
        except Exception as e:
            print(f"❌ Erro ao obter resultados parciais: {e}")
            return []
    
    def cancelar_run(self, run_id: str) -> bool:
        """
        Cancela/aborta uma execução do Apify em andamento
        """
        
        if not self.apify_token or not run_id:
            return False
        
        try:
            # Endpoint para abortar um run
            response = requests.post(
                f"{self.base_url}/actor-runs/{run_id}/abort",
                params={"token": self.apify_token},
                timeout=10
            )
            
            if response.status_code in [200, 204]:
                print(f"✅ Run {run_id} cancelado com sucesso")
                return True
            else:
                print(f"❌ Erro ao cancelar run: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao cancelar run: {e}")
            return False
    
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
                
                print(f"📦 Total de itens no dataset: {len(raw_jobs)}")
                
                # Processar todas as vagas
                vagas_processadas = []
                for i, job in enumerate(raw_jobs):
                    if job and isinstance(job, dict):
                        vaga_processada = self._processar_vaga_linkedin(job)
                        if vaga_processada:
                            vagas_processadas.append(vaga_processada)
                    else:
                        print(f"⚠️ Item {i} não é um dicionário válido: {type(job)}")
                
                print(f"✅ Total processado: {len(vagas_processadas)} vagas válidas de {len(raw_jobs)} itens")
                return vagas_processadas
            else:
                print(f"❌ Erro HTTP {response.status_code} ao obter todos os resultados")
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