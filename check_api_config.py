#!/usr/bin/env python3
"""
Script para verificar configuração das APIs de IA
"""
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

print("🔍 Verificando configuração das APIs de IA...\n")

# Verificar OpenAI
openai_key = os.getenv('OPENAI_API_KEY', '')
if openai_key and openai_key != 'your_openai_api_key_here':
    print("✅ OpenAI API Key configurada")
    print(f"   Chave: {openai_key[:10]}...{openai_key[-4:]}")
else:
    print("❌ OpenAI API Key NÃO configurada")
    print("   Configure OPENAI_API_KEY no arquivo .env")

print()

# Verificar Anthropic
anthropic_key = os.getenv('ANTHROPIC_API_KEY', '')
if anthropic_key and anthropic_key != 'your_anthropic_api_key_here':
    print("✅ Anthropic API Key configurada")
    print(f"   Chave: {anthropic_key[:10]}...{anthropic_key[-4:]}")
else:
    print("❌ Anthropic API Key NÃO configurada")
    print("   Configure ANTHROPIC_API_KEY no arquivo .env")

print("\n" + "="*50)

if (not openai_key or openai_key == 'your_openai_api_key_here') and \
   (not anthropic_key or anthropic_key == 'your_anthropic_api_key_here'):
    print("⚠️  ATENÇÃO: Nenhuma API de IA está configurada!")
    print("📝 O sistema está usando análise FALLBACK que retorna 35% fixo")
    print("\n🔧 Para ativar análise real com IA:")
    print("1. Abra o arquivo .env")
    print("2. Substitua 'your_openai_api_key_here' pela sua chave da OpenAI")
    print("   OU")
    print("   Substitua 'your_anthropic_api_key_here' pela sua chave da Anthropic")
    print("3. Reinicie o servidor backend")
else:
    print("✅ Pelo menos uma API está configurada!")
    print("🚀 O sistema deve estar fazendo análises reais com IA")

print("\n📌 Dica: Você disse 'no env ja tem a chave da openai e da anthropic'")
print("   Verifique se as chaves estão corretas no arquivo .env")