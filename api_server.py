#!/usr/bin/env python3
"""
Compatibility wrapper para Railway - Usa app_streaming.py com logs detalhados
"""
from app_streaming import app

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Iniciando HELIO via api_server.py (wrapper) na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=False) 