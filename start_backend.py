#!/usr/bin/env python3
"""
Script para inicializar apenas o backend Flask
"""

import subprocess
import sys
import os

def main():
    """Iniciar apenas o backend"""
    print("🚀 Iniciando Backend HELIO...")
    print("🔗 API: http://localhost:5000")
    print("📚 Health Check: http://localhost:5000/api/health")
    print("⚠️  Pressione Ctrl+C para parar")
    
    try:
        # Definir variáveis de ambiente
        env = os.environ.copy()
        env['FLASK_ENV'] = 'development'
        env['FLASK_DEBUG'] = '1'
        
        subprocess.run([sys.executable, 'api_server.py'], env=env)
    except KeyboardInterrupt:
        print("\n🛑 Backend encerrado pelo usuário")
        print("👋 Até logo!")
    except Exception as e:
        print(f"❌ Erro no backend: {e}")

if __name__ == "__main__":
    main()