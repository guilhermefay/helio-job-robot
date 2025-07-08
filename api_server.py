#!/usr/bin/env python3
"""
Compatibility wrapper - Railway keeps trying to run this file
Redirects to app_streaming.py
"""
from app_streaming import app

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False) 