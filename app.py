import json
import os
import http.server
import socketserver
import threading
import webbrowser

PORT = 8000
FILENAME = "portfolio.json"


class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        """Handles form submission and saves portfolio data to portfolio.json."""
        if self.path == "/save":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode("utf-8")

            # Convert form data into JSON
            data = dict(item.split("=") for item in post_data.split("&"))
            portfolio = {
                "name": data.get("name", "").replace("+", " "),
                "bio": data.get("bio", "").replace("+", " "),
                "skills": data.get("skills", "").replace("+", " ").split(","),
                "projects": [{"name": p.strip(), "description": d.strip()} for p, d in zip(
                    data.get("project_names", "").split(","), data.get("project_descriptions", "").split(",")) if p]
            }

            # Save to portfolio.json
            with open(FILENAME, "w") as json_file:
                json.dump(portfolio, json_file, indent=4)

            # Redirect back to index.html
            self.send_response(303)
            self.send_header("Location", "/index.html")
            self.end_headers()


def run_server():
    """Starts the web server."""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    handler = CustomHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()


def open_browser():
    """Opens the web app in the default browser."""
    webbrowser.open(f"http://localhost:{PORT}/index.html")


if __name__ == "__main__":
    # Start the server in a separate thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Open the browser automatically
    open_browser()

    # Keep the script running
    input("\nPress Enter to stop the server...\n")

