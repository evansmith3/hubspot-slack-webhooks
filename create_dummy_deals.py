import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

HUBSPOT_DEAL_TOKEN = os.getenv("HUBSPOT_DEAL_TOKEN")
HUBSPOT_DEAL_URL = os.getenv("HUBSPOT_DEAL_URL")

# Debug: confirm variables loaded
print("HUBSPOT_TOKEN:", "Loaded" if HUBSPOT_DEAL_TOKEN else "Not found")
print("HUBSPOT_URL:", HUBSPOT_DEAL_URL if HUBSPOT_DEAL_URL else "Not found")

if not HUBSPOT_DEAL_TOKEN or not HUBSPOT_DEAL_URL:
    raise ValueError("Missing HubSpot token or URL. Check your .env file.")

headers = {
    "Authorization": f"Bearer {HUBSPOT_DEAL_TOKEN}",
    "Content-Type": "application/json"
}

# Dummy deals
dummy_deals = [
    {"dealname": "Big Deal", "amount": "5000", "dealstage": "closedwon"},
    {"dealname": "Small Deal", "amount": "1200", "dealstage": "appointmentscheduled"},
    {"dealname": "Medium Deal", "amount": "2500", "dealstage": "closedwon"}
]

for deal in dummy_deals:
    data = {"properties": deal}
    response = requests.post(HUBSPOT_DEAL_URL, headers=headers, json=data)
    if response.status_code == 201:
        print(f"✅ Created deal: {deal['dealname']}")
    else:
        print(f"❌ Failed to create deal: {deal['dealname']}")
        print(response.json())

