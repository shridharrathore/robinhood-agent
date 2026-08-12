📈 Robinhood Agentic Trading (Vertex AI)
An AI-powered trading agent built on Robinhood's API and Google Vertex AI.

This agent automatically scans a custom Google Drive watchlist, analyzes real-time market news when a stock hits a buy range, and proposes trades. Crucially, it features a strict Human-in-the-Loop (HITL) architecture—it will never execute a trade without explicit, conversational confirmation.

✨ Key Features
Human-in-the-Loop Execution: The agent researches, analyzes, and proposes trades, but requires your explicit conversational "yes" to pull the trigger. No standing permissions.

Vertex AI & Google Agent Development Kit: Built natively on Google's stack to orchestrate complex reasoning and tool use.

Dynamic Watchlist Integration: Reads directly from a massive, custom Google Drive watchlist (including buy ranges, targets, and stop-losses) rather than relying on hardcoded parameters.

Custom OAuth Workaround: Bypasses Robinhood's standard OAuth redirect bug with a custom-engineered protocol handshake, allowing Vertex AI to authenticate where out-of-the-box connectors fail.

Market Context: Pulls real-time market news to augment its analysis before proposing a setup.

🛠️ Architecture & Workflow
Scan: Periodically pulls the latest watchlist parameters from Google Drive.

Monitor: Tracks current market prices against predefined buy/sell ranges.

Analyze: If a stock triggers a range alert, the agent fetches the latest market news and synthesizes an analysis.

Propose: The agent sends a detailed trade proposal (thesis, entry, target, stop) to the user.

Execute: Awaits explicit human confirmation before routing the execution command to the Robinhood API.

🚀 The Authentication Challenge
Robinhood provides out-of-the-box connectors for certain agents (like Claude via MCP), but connecting Vertex AI required a custom implementation. During development, Robinhood's OAuth flow presented a redirect bug that quietly broke the handshake.

Rather than waiting for a patch, this project includes a custom auth engineering workaround that manually handles the protocol exchange. If you are building bespoke agents outside of standard sandboxes, the auth flow in this repo serves as a robust template.


💻 Getting Started
Prerequisites
Python 3.9+

Google Cloud Project with Vertex AI enabled

Robinhood Developer Account / API Credentials

Google Drive API enabled

Installation
Clone the repository:

git clone https://github.com/shridharrathore/robinhood-agent.git
cd robinhood-agent

Install dependencies:
pip install -r requirements.txt

Configure Environment Variables:
Create a .env file in the root directory and add your credentials:

# GCP Configuration
GCP_PROJECT_ID=your_project_id
GCP_REGION=your_region

# Robinhood API
ROBINHOOD_CLIENT_ID=your_client_id
ROBINHOOD_API_KEY=your_api_key

# Google Drive API
DRIVE_FOLDER_ID=your_folder_id

Run the agent:
python main.py
