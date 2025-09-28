#!/usr/bin/env python3
"""
Khel Bhoomi Backend Server
Entry point for running the FastAPI application
"""

import os
import uvicorn
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

if __name__ == "__main__":
    # Get configuration from environment variables
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 8001))
    environment = os.environ.get('ENVIRONMENT', 'development')
    
    # Configure uvicorn based on environment
    if environment == 'production':
        # Production configuration
        uvicorn.run(
            "server:app",
            host=host,
            port=port,
            workers=1,  # Render.com typically works better with 1 worker
            log_level="info",
            access_log=True
        )
    else:
        # Development configuration
        uvicorn.run(
            "server:app",
            host=host,
            port=port,
            reload=True,
            log_level="debug",
            access_log=True
        )