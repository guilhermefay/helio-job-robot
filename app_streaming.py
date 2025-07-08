#!/usr/bin/env python3
"""
API minimalista só para streaming de vagas
"""
import os
import sys
import json
import time
from datetime import datetime
from flask import Flask, request, Response, jsonify
from flask_cors import CORS, cross_origin

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(__file__))

app = Flask(__name__)
CORS(app, origins=['https://agenteslinkedin.vercel.app', 'http://localhost:3000'])

@app.route('/api/health', methods=['GET'])
@cross_origin()
def health():
    return jsonify({
        'status': 'ok',
        'service': 'streaming-api',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/agent1/collect-jobs-stream', methods=['POST', 'OPTIONS'])
@cross_origin()
def collect_jobs_stream():
    """Endpoint de streaming para coleta de vagas"""
    
    if request.method == 'OPTIONS':
        return '', 200
    
    def generate_stream():
        try:
            data = request.get_json()
            
            # Validar dados básicos
            if not data:
                yield f"data: {json.dumps({'error': 'Dados não fornecidos'})}\n\n"
                return
                
            cargo = data.get('cargo_objetivo', 'Desenvolvedor')
            quantidade = data.get('total_vagas_desejadas', 50)
            
            # Simular coleta progressiva
            yield f"data: {json.dumps({'status': 'iniciando', 'message': '🚀 Iniciando busca...', 'timestamp': datetime.now().isoformat()})}\n\n"
            
            time.sleep(2)
            
            # Simular vagas sendo coletadas
            vagas_demo = []
            for i in range(1, min(quantidade + 1, 101)):  # Máximo 100 para demo
                vaga = {
                    'id': i,
                    'titulo': f'{cargo} - Posição {i}',
                    'empresa': f'Empresa Tech {i}',
                    'localizacao': data.get('localizacao', 'São Paulo'),
                    'descricao': f'Vaga para {cargo} com experiência em tecnologias modernas.'
                }
                vagas_demo.append(vaga)
                
                # Enviar vaga individual
                yield f"data: {json.dumps({'type': 'nova_vaga', 'vaga': vaga, 'total': i, 'timestamp': datetime.now().isoformat()})}\n\n"
                
                # Update de progresso a cada 5 vagas
                if i % 5 == 0:
                    yield f"data: {json.dumps({'status': 'executando', 'total_vagas': i, 'message': f'⏳ Coletando... {i} vagas encontradas', 'timestamp': datetime.now().isoformat()})}\n\n"
                
                time.sleep(0.3)  # Simular tempo real
            
            # Finalizar
            yield f"data: {json.dumps({'status': 'concluido', 'total_vagas': len(vagas_demo), 'message': f'✅ Coleta concluída! {len(vagas_demo)} vagas encontradas', 'timestamp': datetime.now().isoformat()})}\n\n"
            yield f"data: {json.dumps({'status': 'finalizado', 'total_vagas': len(vagas_demo), 'vagas': vagas_demo, 'timestamp': datetime.now().isoformat()})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e), 'timestamp': datetime.now().isoformat()})}\n\n"
    
    return Response(
        generate_stream(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 