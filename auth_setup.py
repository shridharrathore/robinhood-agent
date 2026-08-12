import requests
import json

DISCOVERY_URL = "https://agent.robinhood.com/.well-known/oauth-authorization-server/mcp/trading"

resp = requests.get(DISCOVERY_URL)
resp.raise_for_status()
config = resp.json()

print(json.dumps(config, indent=2))