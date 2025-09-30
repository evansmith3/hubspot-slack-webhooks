import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

HUBSPOT_DEAL_TOKEN = os.getenv("HUBSPOT_DEAL_TOKEN")
HUBSPOT_DEAL_URL = os.getenv("HUBSPOT_DEAL_URL")

headers = {"Authorization": f"Bearer {HUBSPOT_DEAL_TOKEN}"}
params = {"limit": 5, "properties": "dealname,amount,dealstage"}

response = requests.get(HUBSPOT_DEAL_URL, headers=headers, params=params)
deals = response.json().get("results", [])

for deal in deals:
    print(deal["properties"])
