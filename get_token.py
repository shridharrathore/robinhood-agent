import base64
import hashlib
import http.server
import os
import secrets
import threading
import urllib.parse
import webbrowser

import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ["ROBINHOOD_CLIENT_ID"]
AUTH_ENDPOINT = "https://robinhood.com/oauth"
TOKEN_ENDPOINT = "https://api.robinhood.com/oauth2/token/"
REDIRECT_URI = "http://localhost:8765/callback"

# --- PKCE setup ---
code_verifier = secrets.token_urlsafe(64)
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).decode().rstrip("=")

auth_code_holder = {}

class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if "code" in params:
            auth_code_holder["code"] = params["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Login successful. You can close this tab and return to your terminal.")
        else:
            self.send_response(400)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # silence default logging

def run_server():
    server = http.server.HTTPServer(("localhost", 8765), CallbackHandler)
    while "code" not in auth_code_holder:
        server.handle_request()

# --- Build authorization URL ---
params = {
    "response_type": "code",
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "code_challenge": code_challenge,
    "code_challenge_method": "S256",
    "scope": "internal",
}
auth_url = f"{AUTH_ENDPOINT}?{urllib.parse.urlencode(params)}"

print("Opening browser for Robinhood login/authorization...")
print(auth_url)

server_thread = threading.Thread(target=run_server)
server_thread.start()
webbrowser.open(auth_url)
server_thread.join()

auth_code = auth_code_holder["code"]
print(f"Got authorization code: {auth_code[:10]}...")

# --- Exchange code for tokens ---
token_resp = requests.post(TOKEN_ENDPOINT, data={
    "grant_type": "authorization_code",
    "code": auth_code,
    "redirect_uri": REDIRECT_URI,
    "client_id": CLIENT_ID,
    "code_verifier": code_verifier,
})
token_resp.raise_for_status()
tokens = token_resp.json()

print("Access token acquired.")
with open(".env", "a") as f:
    f.write(f"\nROBINHOOD_MCP_TOKEN={tokens['access_token']}\n")
    if "refresh_token" in tokens:
        f.write(f"ROBINHOOD_REFRESH_TOKEN={tokens['refresh_token']}\n")

print("Saved to .env")