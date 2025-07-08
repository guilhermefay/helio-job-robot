#!/usr/bin/env python3
"""
Script para inicializar apenas o frontend React
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Iniciar apenas o frontend"""
    print("🚀 Iniciando Frontend HELIO...")
    print("🔗 Interface: http://localhost:3000")
    print("⚠️  Pressione Ctrl+C para parar")
    
    try:
        subprocess.run(['npm', 'start'])
    except KeyboardInterrupt:
        print("\n🛑 Frontend encerrado pelo usuário")
        print("👋 Até logo!")
    except Exception as e:
        print(f"❌ Erro no frontend: {e}")

if __name__ == "__main__":
    main()