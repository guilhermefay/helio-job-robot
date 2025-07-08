#!/usr/bin/env python3
"""
Script para inicializar o sistema HELIO completo
Frontend React + Backend Flask
"""

import subprocess
import sys
import os
import time
import threading
from pathlib import Path

def check_dependencies():
    """Verificar se as dependências estão instaladas"""
    print("🔍 Verificando dependências...")
    
    # Verificar Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        print(f"✅ Node.js: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Node.js não encontrado. Instale o Node.js primeiro.")
        return False
    
    # Verificar npm
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        print(f"✅ npm: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ npm não encontrado.")
        return False
    
    # Verificar Python
    print(f"✅ Python: {sys.version}")
    
    return True

def install_python_dependencies():
    """Instalar dependências Python"""
    print("\n📦 Instalando dependências Python...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✅ Dependências Python instaladas")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências Python: {e}")
        return False

def install_frontend_dependencies():
    """Instalar dependências do frontend"""
    print("\n📦 Instalando dependências do frontend...")
    frontend_path = Path('frontend')
    
    if not frontend_path.exists():
        print("❌ Diretório frontend não encontrado")
        return False
    
    try:
        subprocess.run(['npm', 'install'], cwd=frontend_path, check=True)
        print("✅ Dependências do frontend instaladas")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências do frontend: {e}")
        return False

def start_backend():
    """Iniciar servidor backend Flask"""
    print("\n🚀 Iniciando backend Flask...")
    try:
        # Definir variáveis de ambiente
        env = os.environ.copy()
        env['FLASK_ENV'] = 'development'
        env['FLASK_DEBUG'] = '1'
        
        subprocess.run([sys.executable, 'api_server.py'], env=env)
    except KeyboardInterrupt:
        print("\n🛑 Backend interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro no backend: {e}")

def start_frontend():
    """Iniciar servidor frontend React"""
    print("\n🚀 Iniciando frontend React...")
    frontend_path = Path('frontend')
    
    try:
        subprocess.run(['npm', 'start'], cwd=frontend_path)
    except KeyboardInterrupt:
        print("\n🛑 Frontend interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro no frontend: {e}")

def main():
    """Função principal"""
    print("🎯 HELIO - Sistema de Jornada IA")
    print("=" * 50)
    
    # Verificar dependências
    if not check_dependencies():
        print("\n❌ Dependências não atendidas. Instale os pré-requisitos.")
        return
    
    # Perguntar se quer instalar dependências
    install_deps = input("\n🤔 Instalar/atualizar dependências? (y/N): ").lower().strip()
    
    if install_deps == 'y':
        if not install_python_dependencies():
            return
        if not install_frontend_dependencies():
            return
    
    print("\n🎉 Iniciando sistema HELIO...")
    print("🔗 Frontend: http://localhost:3000")
    print("🔗 Backend API: http://localhost:5000")
    print("📚 Documentação API: http://localhost:5000/api/health")
    print("\n⚠️  Pressione Ctrl+C para parar ambos os servidores")
    
    # Iniciar backend em thread separada
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Aguardar um pouco para o backend iniciar
    time.sleep(3)
    
    # Iniciar frontend (processo principal)
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n\n🛑 Sistema HELIO encerrado pelo usuário")
        print("👋 Até logo!")

if __name__ == "__main__":
    main()