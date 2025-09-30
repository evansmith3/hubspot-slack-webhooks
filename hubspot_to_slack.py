import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# -----------------------
# CONFIGURATION
# -----------------------
HUBSPOT_DEAL_TOKEN = os.getenv("HUBSPOT_DEAL_TOKEN")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_DEAL_CHANNEL = os.getenv("SLACK_DEAL_CHANNEL")

# -----------------------
# STEP 1: Fetch deals from HubSpot
# -----------------------
HUBSPOT_DEAL_URL = os.getenv("HUBSPOT_DEAL_URL")
hubspot_headers = {"Authorization": f"Bearer {HUBSPOT_DEAL_TOKEN}"}
hubspot_params = {
    "limit": 100,  # get up to 100 deals at a time
    "properties": "dealname,amount,dealstage"
}

response = requests.get(HUBSPOT_DEAL_URL, headers=hubspot_headers, params=hubspot_params)
response.raise_for_status()  # raise an error if request failed

deals = response.json().get("results", [])

# -----------------------
# STEP 2: Filter for Closed Won deals
# -----------------------
closed_won_deals = [d for d in deals if d["properties"].get("dealstage") == "closedwon"]

# -----------------------
# STEP 3: Send message to Slack
# -----------------------
slack_url = "https://slack.com/api/chat.postMessage"
slack_headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}", "Content-Type": "application/json"}

for deal in closed_won_deals:
    deal_name = deal["properties"].get("dealname", "No Name")
    amount = deal["properties"].get("amount", "0")
    
    slack_data = {
        "channel": SLACK_DEAL_CHANNEL,
        "text": f"🎉 Deal closed! {deal_name} worth ${amount}"
    }
    
    slack_response = requests.post(slack_url, headers=slack_headers, json=slack_data)
    result = slack_response.json()
    
    if result.get("ok"):
        print(f"Posted deal '{deal_name}' to Slack.")
    else:
        print(f"Failed to post deal '{deal_name}'. Error: {result.get('error')}")
