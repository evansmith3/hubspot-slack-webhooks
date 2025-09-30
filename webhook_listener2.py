from flask import Flask, request
import requests
import os

app = Flask(__name__)

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

@app.route("/hubspot-webhook", methods=["POST"])
def hubspot_webhook():
    data = request.json
    print("Received HubSpot webhook:", data)

    if SLACK_WEBHOOK_URL:
        message = {
            "text": f"🏢 HubSpot Company Event:\n```{data}```"
        }
        resp = requests.post(SLACK_WEBHOOK_URL, json=message)
        print("Slack response:", resp.status_code)

    return "OK", 200
