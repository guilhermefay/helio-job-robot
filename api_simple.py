#!/usr/bin/env python3
"""
API SIMPLES - Só pega texto e manda pra IA
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from core.services.ai_keyword_extractor import AIKeywordExtractor

app = Flask(__name__)
CORS(app)

@app.route('/api/agent1/analyze-simple', methods=['POST', 'OPTIONS'])
def analyze_simple():
    """Endpoint simples: recebe texto, manda pra IA, retorna resultado"""
    
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        texto_vagas = data.get('texto_vagas', '')
        cargo = data.get('cargo', 'Desenvolvedor')
        
        if not texto_vagas:
            return jsonify({'error': 'Texto vazio'}), 400
        
        # Criar uma "vaga" fake só com o texto
        vagas_fake = [{
            'titulo': 'Vaga',
            'descricao': texto_vagas,
            'empresa': 'Empresa',
            'localizacao': 'Local'
        }]
        
        # Usar o extrator de IA
        extractor = AIKeywordExtractor()
        
        # Processar com IA (síncrono por simplicidade)
        import asyncio
        resultado = asyncio.run(
            extractor.extrair_palavras_chave_ia(
                vagas=vagas_fake,
                cargo_objetivo=cargo,
                area_interesse=cargo
            )
        )
        
        return jsonify(resultado)
        
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    print(f"🚀 API Simples rodando na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=True)