#!/usr/bin/env python3
"""Run end-to-end tests"""
import subprocess
import sys
import os

os.chdir(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.exit(subprocess.run([sys.executable, 'test_e2e.py']).returncode)
