#!/usr/bin/env python3
"""
Minimal test app to verify Railway deployment and CORS
"""
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# Simple CORS configuration
CORS(app, origins=['*'])

@app.route('/')
def root():
    return jsonify({
        'status': 'online',
        'message': 'Test app is running',
        'port': os.environ.get('PORT', 'not set')
    })

@app.route('/api/test', methods=['GET', 'POST', 'OPTIONS'])
def test_endpoint():
    if request.method == 'OPTIONS':
        return '', 200
    
    return jsonify({
        'method': request.method,
        'origin': request.headers.get('Origin'),
        'message': 'CORS test successful'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)