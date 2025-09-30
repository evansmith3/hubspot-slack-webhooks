from flask import Flask, request
import requests
import os
from dotenv import load_dotenv

# -----------------------
# Load environment variables
# -----------------------
load_dotenv()

app = Flask(__name__)

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
HUBSPOT_CONTACT_TOKEN = os.getenv("HUBSPOT_CONTACT_TOKEN")

# Track contacts we've already posted
posted_contacts = set()

# -----------------------
# Helper: Fetch full contact properties from HubSpot
# -----------------------
def get_contact_properties(contact_id):
    url = f"https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}"
    headers = {"Authorization": f"Bearer {HUBSPOT_CONTACT_TOKEN}"}
    # Specify the properties you want
    params = {
        "properties": "firstname,lastname,email,phone,jobtitle,lifecyclestage"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("properties", {})
    else:
        print(f"Failed to fetch contact {contact_id}: {response.status_code} {response.text}")
        return {}


# -----------------------
# Flask route
# -----------------------
@app.route("/hubspot-webhook", methods=["POST"])
def hubspot_webhook():
    events = request.json

    for event in events:
        contact_id = event.get("objectId")
        if not contact_id or contact_id in posted_contacts:
            continue

        if event.get("subscriptionType") == "contact.creation":
            posted_contacts.add(contact_id)

            # Fetch full contact properties
            props = get_contact_properties(contact_id)

            first = props.get("firstname", "N/A")
            last = props.get("lastname", "N/A")
            email = props.get("email", "N/A")
            phone = props.get("phone", "N/A")
            job = props.get("jobtitle", "N/A")
            stage = props.get("lifecyclestage", "N/A")

            # Slack message
            message = {
                "text": f"👤 New HubSpot Contact:\n"
                        f"*Name:* {first} {last}\n"
                        f"*Email:* {email}\n"
                        f"*Phone:* {phone}\n"
                        f"*Job Title:* {job}\n"
                        f"*Lifecycle Stage:* {stage}"
            }

            try:
                resp = requests.post(SLACK_WEBHOOK_URL, json=message)
                print(f"Slack response ({contact_id}): {resp.status_code}")
            except Exception as e:
                print(f"Error sending contact {contact_id} to Slack:", e)

    return "OK", 200

# -----------------------
# Main
# -----------------------
if __name__ == "__main__":
    app.run(port=5000)

