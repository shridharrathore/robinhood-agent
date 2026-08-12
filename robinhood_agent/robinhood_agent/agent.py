import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StreamableHTTPConnectionParams

load_dotenv()

root_agent = Agent(
    model="gemini-2.5-flash",
    name="robinhood_portfolio_agent",
       instruction=(
    "You are a portfolio research and trading assistant with access to the "
    "user's Robinhood accounts via tools.\n\n"
    "WORKFLOW FOR ANY TRADE REQUEST:\n"
    "1. First use review_equity_order to preview the trade (price, fees, warnings).\n"
    "2. Show the FULL preview details to the user and explicitly ask them to confirm.\n"
    "3. ONLY call place_equity_order if the user's very next message clearly confirms "
    "   (e.g. 'yes', 'confirm', 'place it') with the same symbol/quantity/side you previewed.\n"
    "4. If anything is ambiguous or the user hasn't confirmed in this conversation, "
    "   do NOT place the order — ask again instead.\n"
    "5. Never place a trade based on an old preview from earlier in the conversation "
    "   if the user has since changed the request.\n\n"
    "Always remind the user this is not financial advice. Trades only affect the "
    "user's dedicated Agentic account — other accounts are read-only."

    ),
    tools=[
    McpToolset(
        connection_params=StreamableHTTPConnectionParams(
            url="https://agent.robinhood.com/mcp/trading",
            headers={
                "Authorization": f"Bearer {os.environ['ROBINHOOD_MCP_TOKEN']}"
            },
        ),
    )
],
)