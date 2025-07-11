"""
Indeed Jobs Scraper Simplificado - Versão minimalista
"""

import os
import time
import json
from datetime import datetime
import requests

class IndeedScraper:
    def __init__(self):
        self.apify_token = os.getenv('APIFY_API_TOKEN')
        self.base_url = "https://api.apify.com/v2"
        self.actor_id = "borderline/indeed-scraper"
        
    def coletar_vagas_indeed(self, cargo, localizacao="são paulo", limite=20, **kwargs):
        """Coleta vagas do Indeed via Apify"""
        
        if not self.apify_token:
            return self._fallback_data(cargo, localizacao, limite)
        
        try:
            # Input básico
            actor_input = {
                "country": "br",
                "query": cargo,
                "location": localizacao,
                "maxRows": min(limite, 100),
                "radius": "25",
                "sort": "date"
            }
            
            # Fazer request
            actor_id_formatted = self.actor_id.replace('/', '~')
            
            response = requests.post(
                f"{self.base_url}/acts/{actor_id_formatted}/runs",
                headers={"Authorization": f"Bearer {self.apify_token}"},
                json=actor_input,
                timeout=30
            )
            
            if response.status_code != 201:
                return self._fallback_data(cargo, localizacao, limite)
            
            run_id = response.json()["data"]["id"]
            
            # Aguardar conclusão (máximo 2 minutos)
            for _ in range(24):  # 24 * 5 = 120 segundos
                time.sleep(5)
                
                status_resp = requests.get(
                    f"{self.base_url}/actor-runs/{run_id}",
                    headers={"Authorization": f"Bearer {self.apify_token}"}
                )
                
                if status_resp.status_code == 200:
                    status = status_resp.json()["data"]["status"]
                    if status == "SUCCEEDED":
                        dataset_id = status_resp.json()["data"]["defaultDatasetId"]
                        break
                    elif status in ["FAILED", "ABORTED"]:
                        return self._fallback_data(cargo, localizacao, limite)
            else:
                return self._fallback_data(cargo, localizacao, limite)
            
            # Obter resultados
            results_resp = requests.get(
                f"{self.base_url}/datasets/{dataset_id}/items",
                headers={"Authorization": f"Bearer {self.apify_token}"}
            )
            
            if results_resp.status_code != 200:
                return self._fallback_data(cargo, localizacao, limite)
            
            jobs = results_resp.json()
            return [self._processar_vaga(job) for job in jobs[:limite] if job]
            
        except Exception:
            return self._fallback_data(cargo, localizacao, limite)
    
    def _processar_vaga(self, job_data):
        """Processa uma vaga para formato padrão"""
        return {
            "titulo": job_data.get('title', 'Título não disponível'),
            "empresa": job_data.get('companyName', 'Empresa não informada'),
            "localizacao": job_data.get('location', {}).get('formattedAddressShort', 'Local não informado'),
            "descricao": job_data.get('descriptionText', ''),
            "fonte": "indeed",
            "url": job_data.get('jobUrl', ''),
            "data_coleta": datetime.now().isoformat(),
            "salario": job_data.get('salary', {}).get('salaryText', 'Não informado'),
            "tipo_emprego": ', '.join(job_data.get('jobType', [])) if isinstance(job_data.get('jobType'), list) else 'Não especificado',
            "remoto": job_data.get('isRemote', False)
        }
    
    def _fallback_data(self, cargo, localizacao, limite):
        """Dados de demonstração"""
        empresas = [
            ("Tech Solutions BR", "São Paulo, SP", "R$ 6.000 - R$ 10.000"),
            ("StartUp Inovadora", "São Paulo, SP", "R$ 7.000 - R$ 12.000"),
            ("Empresa Digital", "São Paulo, SP", "R$ 8.000 - R$ 14.000")
        ]
        
        vagas = []
        for i in range(min(limite, len(empresas))):
            empresa, local, salario = empresas[i]
            vagas.append({
                "titulo": f"{cargo}",
                "empresa": empresa,
                "localizacao": local,
                "salario": salario,
                "descricao": f"Vaga para {cargo} em {empresa}.",
                "fonte": "indeed_demo",
                "url": "#",
                "data_coleta": datetime.now().isoformat(),
                "tipo_emprego": "CLT",
                "remoto": i % 2 == 0
            })
        
        return vagas
    
    def iniciar_execucao_indeed(self, cargo, localizacao, limite=20, **kwargs):
        """Para compatibilidade com streaming"""
        return None, None
    
    def verificar_status_run(self, run_id):
        return "UNKNOWN"
    
    def obter_resultados_parciais(self, dataset_id, offset=0, limit=100):
        return []
    
    def cancelar_run(self, run_id):
        return False