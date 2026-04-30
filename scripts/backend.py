#!/usr/bin/env python3
"""Start FastAPI backend only"""
import subprocess
import sys
import os

os.chdir(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.exit(subprocess.run([
    sys.executable, '-m', 'uvicorn', 'app.main:app',
    '--reload', '--host', '0.0.0.0', '--port', '8000'
]).returncode)
