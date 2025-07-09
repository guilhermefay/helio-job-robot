#!/usr/bin/env python3
"""
Teste simples para verificar se o problema está no api_server.py
"""
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'message': 'Simple test working',
        'port': os.environ.get('PORT', 5000)
    })

@app.route('/api/agent1/collect-keywords', methods=['POST', 'OPTIONS'])
def collect_keywords():
    if request.method == 'OPTIONS':
        return '', 200
    return jsonify({
        'demo_mode': True,
        'message': 'Simple test endpoint working'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 