#!/usr/bin/env python3
"""
Startup script with enhanced logging for Railway debugging
"""
import os
import sys
import logging

# Configure logging before importing app
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

logger.info("=" * 60)
logger.info("🚀 HELIO Startup Script")
logger.info("=" * 60)

# Log environment
logger.info(f"Python version: {sys.version}")
logger.info(f"Working directory: {os.getcwd()}")
logger.info(f"PORT: {os.environ.get('PORT', 'not set')}")
logger.info(f"RAILWAY_ENVIRONMENT: {os.environ.get('RAILWAY_ENVIRONMENT', 'not set')}")
logger.info(f"APIFY_API_TOKEN: {'set' if os.environ.get('APIFY_API_TOKEN') else 'not set'}")

# List files in current directory
logger.info(f"Files in current directory: {os.listdir('.')}")

# Try to import the app
try:
    logger.info("Attempting to import app_streaming...")
    from app_streaming import app
    logger.info("✅ Successfully imported app_streaming")
    
    # List all routes
    logger.info("Registered routes:")
    for rule in app.url_map.iter_rules():
        logger.info(f"  {rule.endpoint}: {rule.rule} [{', '.join(rule.methods)}]")
    
except Exception as e:
    logger.error(f"❌ Failed to import app_streaming: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

logger.info("=" * 60)
logger.info("App module loaded successfully, handing over to gunicorn...")
logger.info("=" * 60)