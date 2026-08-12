import requests
import json

REGISTRATION_ENDPOINT = "https://agent.robinhood.com/oauth/trading/register"

payload = {
    "client_name": "robinhood-portfolio-agent",
    "redirect_uris": ["http://localhost:8765/callback"],
    "grant_types": ["authorization_code", "refresh_token"],
    "response_types": ["code"],
    "token_endpoint_auth_method": "none",
}

resp = requests.post(REGISTRATION_ENDPOINT, json=payload)
resp.raise_for_status()
client_info = resp.json()

print(json.dumps(client_info, indent=2))

# Save client_id to .env for later steps
with open(".env", "a") as f:
    f.write(f"\nROBINHOOD_CLIENT_ID={client_info['client_id']}\n")