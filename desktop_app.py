import threading
import webview
import socket
from main import app

def get_local_ip():
    """Get the local IP address"""
    try:
        # Create a socket to get the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def run_flask():
    """Run Flask server in a separate thread"""
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    local_ip = get_local_ip()
    print(f"Server will be accessible at: http://{local_ip}:5000")
    print("You can access this from any device on the same network using the above URL.")

    # Start Flask server in background thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Create pywebview window for desktop access
    window = webview.create_window(
        'Giebee Engineering Management System',
        'http://127.0.0.1:5000',
        width=1200,
        height=800,
        resizable=True,
        fullscreen=False
    )

    # Start the webview application
    webview.start()
