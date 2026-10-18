# audicode_desktop.py
"""Native Windows Desktop Application wrapper for AudiCode (ISO/IEC 27701:2025).

Launches the FastAPI/Uvicorn backend in a background daemon thread with
desktop single-user mode enabled (AUTH_ENABLED=false), and opens a native
Windows desktop window via pywebview (Microsoft Edge WebView2) with no browser
address bar, tabs, or chrome.
"""
import os
import sys
import time
import socket
import threading
import urllib.request

# Ensure working directory and module path point to the app root
if getattr(sys, "frozen", False):
    APP_DIR = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(sys.executable)))
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

os.chdir(APP_DIR)
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

# Desktop mode: bypass web login screen
os.environ["AUTH_ENABLED"] = "false"
os.environ["APP_BIND"] = "127.0.0.1"
os.environ["APP_PORT"] = "7000"

class NullWriter:
    def write(self, text):
        pass
    def flush(self):
        pass
    def isatty(self):
        return False

if sys.stdout is None:
    sys.stdout = NullWriter()
if sys.stderr is None:
    sys.stderr = NullWriter()


def is_port_in_use(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0


def start_backend_server(host: str, port: int):
    import uvicorn
    from app import app
    uvicorn.run(app, host=host, port=port, log_level="warning")


def wait_for_server(url: str, timeout: float = 25.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url + "/api/version", timeout=1.5) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(0.25)
    return False


def main():
    host = "127.0.0.1"
    port = 7000
    url = f"http://{host}:{port}"

    # Start backend in background thread if not already running
    if not is_port_in_use(host, port):
        server_thread = threading.Thread(
            target=start_backend_server,
            args=(host, port),
            daemon=True
        )
        server_thread.start()

    # Wait for backend readiness
    wait_for_server(url, timeout=25.0)

    # Launch native Windows Desktop Window via pywebview (Edge WebView2)
    import webview
    icon_path = os.path.join(APP_DIR, "assets", "icon.ico")
    if not os.path.exists(icon_path):
        icon_path = os.path.join(APP_DIR, "static", "icon.ico")

    window = webview.create_window(
        title="AudiCode — Autonomous PIMS & AI Audit Agent (ISO/IEC 27701:2025)",
        url=url,
        width=1440,
        height=900,
        min_size=(1024, 680),
        background_color="#0a0c10",
        text_select=True,
    )

    webview.start(
        gui="edgechromium",
        icon=icon_path if os.path.exists(icon_path) else None,
    )

    # Cleanly exit backend thread when native desktop window is closed
    os._exit(0)


if __name__ == "__main__":
    main()
