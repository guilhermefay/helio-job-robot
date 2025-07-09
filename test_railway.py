#!/usr/bin/env python3
"""
Teste mínimo para Railway
"""
import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'service': 'helio-test',
        'port': os.environ.get('PORT', '5000')
    })

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'message': 'Railway Test OK',
        'status': 'working'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 