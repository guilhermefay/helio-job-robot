#!/bin/bash
exec gunicorn app_streaming:app --bind 0.0.0.0:${PORT:-8000} --timeout 300 