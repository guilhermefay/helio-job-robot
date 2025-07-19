import requests

# Texto de exemplo
texto = """
Vaga 1: Desenvolvedor Python
Requisitos: Python, Django, PostgreSQL, Docker
Experiência com APIs REST

Vaga 2: Engenheiro de Dados
Requisitos: Python, Spark, Airflow, AWS
Conhecimento em Big Data
"""

response = requests.post('http://localhost:5002/api/agent1/analyze-simple', 
    json={
        'texto_vagas': texto,
        'cargo': 'Desenvolvedor Python'
    }
)

print("Status:", response.status_code)
print("Resultado:")
print(response.json())