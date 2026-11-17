"""
Main entry point to launch the AI Resume Matching & Ranking Application.
Usage:
    python run.py
or
    uv run run.py
"""

import os
import sys
import socket
import subprocess
import time
import uvicorn

# Add backend directory to sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.sample_data.generate_samples import generate_all_samples


def get_available_port(preferred_port=8000, max_attempts=10):
    """
    Checks if preferred_port is open. If occupied, attempts to free it by terminating
    stale python/uvicorn listeners, or automatically falls back to the next free port.
    Prevents Errno 10048 (address already in use).
    """
    # 1. Test if preferred port is already free
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("0.0.0.0", preferred_port))
            return preferred_port
        except OSError:
            pass

    # 2. Port is in use - attempt to free it on Windows
    if sys.platform == "win32":
        try:
            out = subprocess.check_output(f"netstat -ano | findstr :{preferred_port}", shell=True, text=True)
            for line in out.strip().splitlines():
                parts = line.strip().split()
                if len(parts) >= 5 and "LISTENING" in parts:
                    pid = int(parts[-1])
                    if pid != os.getpid() and pid > 0:
                        print(f"[*] Port {preferred_port} is in use by process {pid}. Terminating stale listener...")
                        subprocess.call(f"taskkill /F /PID {pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        time.sleep(1)
                        # Re-verify
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                            try:
                                s2.bind(("0.0.0.0", preferred_port))
                                return preferred_port
                            except OSError:
                                pass
        except Exception:
            pass

    # 3. Fallback: find next available port
    for port in range(preferred_port + 1, preferred_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("0.0.0.0", port))
                print(f"[*] Port {preferred_port} unavailable. Automatically binding to next open port: {port}")
                return port
            except OSError:
                continue

    return preferred_port


def main():
    sample_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "sample_resumes"))
    if not os.path.exists(sample_dir) or len(os.listdir(sample_dir)) == 0:
        print("[*] Generating 12 synthetic sample resumes (PDF & DOCX)...")
        generate_all_samples(sample_dir)

    # Determine free port safely
    port = get_available_port(preferred_port=8000)

    print("\n" + "="*70)
    print("  AI-BASED RESUME MATCHING & CANDIDATE RANKING SYSTEM")
    print("="*70)
    print(f"  • Web Application Dashboard: http://localhost:{port}")
    print(f"  • Interactive API Documentation: http://localhost:{port}/docs")
    print("  • AI Engine: SentenceTransformers all-MiniLM-L6-v2 + Skills Ontology")
    print("="*70 + "\n")

    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)


if __name__ == "__main__":
    main()
