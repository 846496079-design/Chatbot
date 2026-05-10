import subprocess
import sys
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

SERVER_PORT = os.getenv("SERVER_PORT", "8001")
FRONTEND_PORT = os.getenv("FRONTEND_PORT", "3000")


def print_message(msg):
    print("=" * 50)
    print(msg)
    print("=" * 50)


def start_backend():
    print_message("Starting Backend Server...")
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", SERVER_PORT],
        cwd=BACKEND_DIR
    )


def start_frontend():
    print_message("Starting Frontend Server...")
    return subprocess.Popen(
        ["npm", "start"],
        cwd=FRONTEND_DIR,
        shell=True
    )


def main():
    print_message("E-Commerce Customer Service System")
    print(f"\n[1/2] Starting Backend (port {SERVER_PORT})...")
    backend = start_backend()
    time.sleep(5)

    print(f"\n[2/2] Starting Frontend (port {FRONTEND_PORT})...")
    frontend = start_frontend()
    time.sleep(3)

    print_message("Services Started Successfully!")
    print(f"\nBackend: http://localhost:{SERVER_PORT}")
    print(f"Frontend: http://localhost:{FRONTEND_PORT}")
    print("\nPress Ctrl+C to stop all services...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping services...")
        backend.terminate()
        frontend.terminate()
        backend.wait()
        frontend.wait()
        print("Done!")


if __name__ == "__main__":
    main()
