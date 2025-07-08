#!/usr/bin/env python3
"""
Script para executar o frontend de teste do HELIO
Configura ambiente e inicia Streamlit
"""

import os
import sys
import subprocess
import platform

def verificar_dependencias():
    """Verifica se as dependências estão instaladas"""
    dependencias = ['streamlit', 'PyPDF2', 'python-docx', 'beautifulsoup4', 'requests']
    
    faltando = []
    for dep in dependencias:
        try:
            __import__(dep.replace('-', '_'))
        except ImportError:
            faltando.append(dep)
    
    if faltando:
        print("❌ Dependências faltando:")
        for dep in faltando:
            print(f"   - {dep}")
        print("\n💡 Para instalar:")
        print(f"pip install {' '.join(faltando)}")
        return False
    
    return True

def verificar_apis():
    """Verifica configuração das APIs"""
    openai_key = os.getenv('OPENAI_API_KEY', '')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY', '')
    
    print("🔍 Verificando APIs:")
    
    if openai_key and openai_key != 'your_openai_api_key_here':
        print("   ✅ OpenAI API configurada")
    else:
        print("   ⚠️  OpenAI API não configurada")
    
    if anthropic_key and anthropic_key != 'your_anthropic_api_key_here':
        print("   ✅ Anthropic API configurada")
    else:
        print("   ⚠️  Anthropic API não configurada")
    
    if not (openai_key and openai_key != 'your_openai_api_key_here') and not (anthropic_key and anthropic_key != 'your_anthropic_api_key_here'):
        print("   ⚠️  Sistema funcionará com fallbacks (sem IA real)")
    
    print()

def main():
    print("🚀 HELIO - Frontend de Teste")
    print("=" * 40)
    
    # Verifica se está no diretório correto
    if not os.path.exists('frontend_teste.py'):
        print("❌ Erro: Execute este script no diretório raiz do HELIO")
        print("   Certifique-se de estar em /Users/Guilherme_1/HELIO/")
        return
    
    # Verifica dependências
    print("🔍 Verificando dependências...")
    if not verificar_dependencias():
        return
    
    print("✅ Todas as dependências estão instaladas!")
    
    # Verifica APIs
    verificar_apis()
    
    # Informa sobre funcionalidades
    print("📋 Funcionalidades disponíveis:")
    print("   • 🩺 Agente 0: Upload e análise real de CV (PDF/DOCX)")
    print("   • 🔍 Agente 1: Coleta real de vagas + validação IA")
    print("   • 📊 Interface visual para resultados")
    print()
    
    # Inicia Streamlit
    print("🌐 Iniciando frontend...")
    print("   URL: http://localhost:8501")
    print("   Para parar: Ctrl+C")
    print("=" * 40)
    
    try:
        # Comando para iniciar Streamlit
        cmd = [sys.executable, "-m", "streamlit", "run", "frontend_teste.py", "--server.port=8501"]
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n\n✅ Frontend encerrado.")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar frontend: {e}")
        print("\n💡 Tente executar manualmente:")
        print("   streamlit run frontend_teste.py")

if __name__ == "__main__":
    main()