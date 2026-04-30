#!/usr/bin/env python3
"""Start Angular frontend only"""
import subprocess
import sys
import os

os.chdir(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
sys.exit(subprocess.run(['npm', 'start']).returncode)
