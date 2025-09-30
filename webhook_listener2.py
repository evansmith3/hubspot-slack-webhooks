from flask import Flask, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
posted_contacts = set()
REQUIRED_PROPS = ["firstname", "lastname", "email", "phone", "jobtitle", "lifecyclestage"]

def send_slack(message_text):
    try:
        resp = requests.post(SLACK_WEBHOOK_URL, json={"text": message_text})
        print(f"Slack response: {resp.status_code}")
    except Exception as e:
        print("Error sending to Slack:", e)

@app.route("/hubspot-webhook", methods=["POST"])
def hubspot_webhook():
    events = request.json
    contacts = {}

    for event in events:
        contact_id = event.get("objectId")
        if contact_id not in contacts:
            contacts[contact_id] = {}

        # Collect properties
        prop_name = event.get("propertyName")
        prop_value = event.get("propertyValue")
        if prop_name:
            contacts[contact_id][prop_name] = prop_value

        # Mark creation event
        if event.get("subscriptionType") == "contact.creation":
            contacts[contact_id]["CREATED"] = True

    for contact_id, props in contacts.items():
        if contact_id in posted_contacts:
            continue
        posted_contacts.add(contact_id)

        # Creation notification
        if props.get("CREATED"):
            message_lines = ["👤 *New HubSpot Contact Created!*"]
            for prop in REQUIRED_PROPS:
                value = props.get(prop, "N/A")
                message_lines.append(f"*{prop.capitalize()}:* {value}")
            send_slack("\n".join(message_lines))
        
        # Property update notification
        else:
            changed_props = [k for k in props if k in REQUIRED_PROPS]
            if changed_props:
                message_lines = ["✏️ *HubSpot Contact Updated:*"]
                for k in changed_props:
                    message_lines.append(f"*{k.capitalize()}:* {props[k]}")
                send_slack("\n".join(message_lines))

    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000)
