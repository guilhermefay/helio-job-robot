#!/usr/bin/env python3
import os
from dotenv import load_dotenv

print("=== DEBUG VARIÁVEIS DE AMBIENTE ===\n")

# Tentar carregar .env
result = load_dotenv()
print(f"load_dotenv() retornou: {result}")
print(f"Diretório atual: {os.getcwd()}")
print(f"Arquivo .env existe? {os.path.exists('.env')}")

# Verificar conteúdo do .env
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'API_KEY' in line and not line.strip().startswith('#'):
                key_name = line.split('=')[0].strip()
                print(f"\nEncontrado no .env: {key_name}")

# Verificar variáveis carregadas
print("\n=== VARIÁVEIS CARREGADAS ===")
openai_key = os.getenv('OPENAI_API_KEY', 'NOT_SET')
anthropic_key = os.getenv('ANTHROPIC_API_KEY', 'NOT_SET')

print(f"\nOPENAI_API_KEY: {openai_key[:20]}..." if len(openai_key) > 20 else f"OPENAI_API_KEY: {openai_key}")
print(f"ANTHROPIC_API_KEY: {anthropic_key[:20]}..." if len(anthropic_key) > 20 else f"ANTHROPIC_API_KEY: {anthropic_key}")

# Verificar se as chaves têm o formato esperado
print(f"\nOpenAI tem 'sk-'? {'sk-' in openai_key}")
print(f"Anthropic tem 'sk-'? {'sk-' in anthropic_key}")