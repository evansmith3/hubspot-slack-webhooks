from flask import Flask, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Slack webhook URL
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
print("Loaded Slack URL:", SLACK_WEBHOOK_URL)  # debug

@app.route("/hubspot-webhook", methods=["POST"])
def hubspot_webhook():
    events = request.json
    print("Received HubSpot events:", events)  # debug

    for event in events:
        contact_id = event.get("objectId")
        subscription_type = event.get("subscriptionType")

        # Only post for new contacts
        if subscription_type == "contact.creation":
            message = {
                "text": f"👤 New HubSpot Contact (DEBUG POST):\n{event}"
            }
            try:
                resp = requests.post(SLACK_WEBHOOK_URL, json=message)
                print(f"Slack response for contact {contact_id}: {resp.status_code}, {resp.text}")
            except Exception as e:
                print(f"Error sending contact {contact_id} to Slack:", e)

    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000)
