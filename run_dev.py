#!/usr/bin/env python3
"""
Development script to run both Flask backend and React frontend
"""

import subprocess
import sys
import os
import time
from threading import Thread

def run_backend():
    """Run the Flask backend"""
    print("Starting Flask backend...")
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\nBackend stopped.")
    except Exception as e:
        print(f"Backend error: {e}")

def run_frontend():
    """Run the React frontend"""
    print("Starting React frontend...")
    try:
        # Wait a bit for backend to start
        time.sleep(2)
        subprocess.run(["npm", "start"], check=True)
    except KeyboardInterrupt:
        print("\nFrontend stopped.")
    except Exception as e:
        print(f"Frontend error: {e}")

def main():
    print("🚀 Starting News App Development Environment")
    print("=" * 50)
    
    # Check if node_modules exists
    if not os.path.exists("node_modules"):
        print("Installing Node.js dependencies...")
        subprocess.run(["npm", "install"], check=True)
    
    # Check if Python dependencies are installed
    try:
        import flask
        import requests
    except ImportError:
        print("Installing Python dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    print("\nStarting services...")
    print("Backend will run on: http://localhost:5000")
    print("Frontend will run on: http://localhost:3000")
    print("\nPress Ctrl+C to stop both services")
    print("=" * 50)
    
    # Start backend in a separate thread
    backend_thread = Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Start frontend in main thread
    run_frontend()

if __name__ == "__main__":
    main()
