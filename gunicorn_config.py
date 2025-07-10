# Configuração do Gunicorn para Railway

import os

# Bind
bind = f"0.0.0.0:{os.environ.get('PORT', 8080)}"

# Workers
workers = 1

# Timeout aumentado para streaming (10 minutos)
timeout = 600

# Keep-alive
keepalive = 65

# Logs
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Worker class - sync para SSE funcionar corretamente
worker_class = 'sync'

# Max requests per worker
max_requests = 1000
max_requests_jitter = 50