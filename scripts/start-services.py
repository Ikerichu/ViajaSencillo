#!/usr/bin/env python3
"""
ViajaSencillo - Start All Services
Coordinates starting both backend (FastAPI) and frontend (Angular) services
"""

import subprocess
import sys
import os
import time
import signal
import socket
import urllib.request
import urllib.error
from pathlib import Path
import threading

# Colors
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
RED = '\033[0;31m'
NC = '\033[0m'  # No Color

PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"

# Process handles
backend_process = None
frontend_process = None

def print_header():
    print()
    print(f"{BLUE}╔════════════════════════════════════════╗{NC}")
    print(f"{BLUE}║  ViajaSencillo - Starting Services    ║{NC}")
    print(f"{BLUE}╚════════════════════════════════════════╝{NC}")
    print()

def print_status(msg):
    print(f"{GREEN}✓{NC} {msg}")

def print_error(msg):
    print(f"{RED}✗{NC} {msg}")

def print_warning(msg):
    print(f"{YELLOW}⚠{NC} {msg}")

def print_info(msg):
    print(f"{BLUE}→{NC} {msg}")

def cleanup(signum=None, frame=None):
    """Clean up processes on exit"""
    global backend_process, frontend_process
    
    print()
    print_warning("Shutting down services...")
    
    if backend_process:
        try:
            backend_process.terminate()
            backend_process.wait(timeout=5)
        except:
            backend_process.kill()
    
    if frontend_process:
        try:
            frontend_process.terminate()
            frontend_process.wait(timeout=5)
        except:
            frontend_process.kill()
    
    print_status("Services stopped")
    sys.exit(0)

def is_port_available(port):
    """Check if a port is available"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result != 0

def kill_port(port):
    """Kill process using a specific port"""
    try:
        result = subprocess.run(
            ["lsof", "-ti", f":{port}"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.stdout:
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    os.kill(int(pid), signal.SIGTERM)
                    time.sleep(0.5)
            return True
    except:
        pass
    return False

def check_command(cmd):
    """Check if a command exists"""
    try:
        subprocess.run(["which", cmd], capture_output=True, check=True)
        return True
    except:
        return False


def wait_for_http(url, timeout=30, expect_text=None):
    """Wait until an HTTP endpoint returns a successful response."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                if response.status == 200:
                    if expect_text:
                        body = response.read().decode('utf-8', errors='ignore')
                        if expect_text in body:
                            return True
                    else:
                        return True
        except urllib.error.HTTPError as exc:
            if exc.code >= 400:
                pass
        except Exception:
            pass
        time.sleep(1)
    return False


def start_backend():
    """Start FastAPI backend"""
    global backend_process
    
    print_info("Starting Backend (FastAPI)...")
    
    os.chdir(BACKEND_DIR)
    
    # Determine Python executable
    python_cmd = sys.executable
    
    try:
        backend_process = subprocess.Popen(
            [python_cmd, "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Read initial output to confirm it started
        for _ in range(20):  # Try for up to 10 seconds
            if backend_process.poll() is not None:
                print_error("Backend failed to start")
                output, _ = backend_process.communicate()
                print(output)
                return False
            time.sleep(0.5)
        
        print_status(f"Backend started (PID: {backend_process.pid})")
        print_status("Backend available at: http://localhost:8000")
        print_status("Swagger UI: http://localhost:8000/docs")

        if not wait_for_http("http://127.0.0.1:8000/docs", timeout=20):
            print_error("Backend did not become ready in time")
            return False

        return True
        
    except Exception as e:
        print_error(f"Failed to start backend: {e}")
        return False

def start_frontend():
    """Start Angular frontend"""
    global frontend_process
    
    print_info("Starting Frontend (Angular)...")
    
    os.chdir(FRONTEND_DIR)
    
    try:
        frontend_process = subprocess.Popen(
            ["npm", "start"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Wait a bit for npm to initialize
        for _ in range(30):  # Try for up to 15 seconds
            if frontend_process.poll() is not None:
                print_error("Frontend failed to start")
                output, _ = frontend_process.communicate()
                print(output[-500:])  # Print last 500 chars
                return False
            time.sleep(0.5)
        
        print_status(f"Frontend started (PID: {frontend_process.pid})")
        print_status("Frontend available at: http://localhost:4200")

        if not wait_for_http("http://localhost:4200", timeout=45, expect_text="ViajaSencillo"):
            print_error("Frontend did not become available or did not render the app page in time")
            return False

        print_status("Frontend page is available")
        return True
        
    except Exception as e:
        print_error(f"Failed to start frontend: {e}")
        return False

def monitor_processes():
    """Monitor processes and keep them running"""
    global backend_process, frontend_process
    
    while True:
        time.sleep(1)
        
        if backend_process and backend_process.poll() is not None:
            print_error("Backend process died!")
            cleanup()
        
        if frontend_process and frontend_process.poll() is not None:
            print_error("Frontend process died!")
            cleanup()

def main():
    os.chdir(PROJECT_ROOT)
    
    print_header()
    
    # Check requirements
    print_info("Checking requirements...")
    
    if not check_command("npm"):
        print_error("npm not found. Please install Node.js and npm")
        sys.exit(1)
    print_status("npm found")
    
    # Check and free ports
    print_info("Checking ports...")
    if not is_port_available(8000):
        print_warning("Port 8000 is in use, killing existing process...")
        if kill_port(8000):
            print_status("Port 8000 freed")
            time.sleep(1)
        else:
            print_error("Could not free port 8000")
            sys.exit(1)
    else:
        print_status("Port 8000 available")
    
    if not is_port_available(4200):
        print_warning("Port 4200 is in use, killing existing process...")
        if kill_port(4200):
            print_status("Port 4200 freed")
            time.sleep(1)
        else:
            print_error("Could not free port 4200")
            sys.exit(1)
    else:
        print_status("Port 4200 available")
    
    # Install dependencies if needed
    if not (FRONTEND_DIR / "node_modules").exists():
        print_warning("Installing frontend dependencies...")
        os.chdir(FRONTEND_DIR)
        result = subprocess.run(["npm", "install"], capture_output=True)
        if result.returncode != 0:
            print_error("Failed to install frontend dependencies")
            sys.exit(1)
        print_status("Frontend dependencies installed")
    
    print()
    print(f"{GREEN}═══════════════════════════════════════{NC}")
    print(f"{GREEN}Starting Services...{NC}")
    print(f"{GREEN}═══════════════════════════════════════{NC}")
    print()
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    
    # Start services
    if not start_backend():
        sys.exit(1)
    
    print()
    
    if not start_frontend():
        cleanup()
        sys.exit(1)
    
    print()
    print(f"{GREEN}╔════════════════════════════════════════╗{NC}")
    print(f"{GREEN}║     ✨ All Services Started! ✨       ║{NC}")
    print(f"{GREEN}╚════════════════════════════════════════╝{NC}")
    print()
    print(f"{BLUE}Backend:{NC}  http://localhost:8000")
    print(f"{BLUE}Frontend: http://localhost:4200")
    print(f"{BLUE}API Docs: http://localhost:8000/docs")
    print()
    print(f"{YELLOW}Press Ctrl+C to stop all services{NC}")
    print()
    
    # Monitor processes
    try:
        monitor_processes()
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    main()
