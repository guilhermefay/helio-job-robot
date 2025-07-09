#!/usr/bin/env python3
"""
Teste simples para verificar se o problema está no api_server.py
"""
import os
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)

# CORS específico para o Vercel
CORS(app, origins=[
    'https://agenteslinkedin.vercel.app',
    'https://helio-job-robot.vercel.app',
    'http://localhost:3000'
])

@app.route('/api/health', methods=['GET'])
@cross_origin()
def health():
    return jsonify({
        'status': 'ok',
        'message': 'Simple test working',
        'port': os.environ.get('PORT', 5000),
        'service': 'helio-simple-test'
    })

@app.route('/api/agent1/collect-keywords', methods=['POST', 'OPTIONS'])
@cross_origin()
def collect_keywords():
    if request.method == 'OPTIONS':
        return '', 200
    
    # Pegar dados da requisição
    data = request.get_json() if request else {}
    cargo = data.get('cargo_objetivo', 'Desenvolvedor')
    localizacao = data.get('localizacao', 'São Paulo')
    
    # Dados demo
    vagas_demo = []
    for i in range(1, 21):
        vaga = {
            'id': i,
            'titulo': f'{cargo} - Posição {i}',
            'empresa': f'Empresa Tech {i}',
            'localizacao': localizacao,
            'descricao': f'Vaga para {cargo} com experiência em tecnologias modernas.',
            'link': f'https://linkedin.com/jobs/view/{1000000 + i}',
            'nivel': 'Pleno' if i % 3 == 0 else 'Júnior',
            'tipo': 'Híbrido' if i % 2 == 0 else 'Remoto'
        }
        vagas_demo.append(vaga)
    
    return jsonify({
        'demo_mode': True,
        'message': 'Simple test endpoint working',
        'parametros': data,
        'estatisticas': {
            'totalVagas': len(vagas_demo),
            'vagasAnalisadas': len(vagas_demo),
            'successRate': 100,
            'tempoColeta': 'Demo instantâneo'
        },
        'transparencia': {
            'fontes_utilizadas': ['Demo'],
            'metodo_coleta': 'Dados de demonstração',
            'filtros_aplicados': f'Cargo: {cargo}, Localização: {localizacao}',
            'observacoes': 'Teste simples funcionando'
        },
        'vagas': vagas_demo
    })

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'service': 'HELIO Simple Test',
        'status': 'online',
        'endpoints': ['/api/health', '/api/agent1/collect-keywords']
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 