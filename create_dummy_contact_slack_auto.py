import os
import requests
import random
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# -----------------------
# CONFIGURATION
# -----------------------
HUBSPOT_CONTACT_TOKEN = os.getenv("HUBSPOT_CONTACT_TOKEN")
HUBSPOT_CONTACT_URL = os.getenv("HUBSPOT_CONTACT_URL")
HEADERS = {
    "Authorization": f"Bearer {HUBSPOT_CONTACT_TOKEN}",
    "Content-Type": "application/json"
}

HUBSPOT_OWNER_ID = os.getenv("HUBSPOT_OWNER_ID")  # Evan Smith's HubSpot user ID

first_names = [
    "Alice", "Ben", "Clara", "David", "Evan", "Fiona", "George", "Hannah", "Ian",
    "Julia", "Kevin", "Laura", "Michael", "Nina", "Oscar", "Paula", "Quinn", "Rachel",
    "Sam", "Tina", "Ulysses", "Victor", "Wendy", "Xavier", "Yara", "Zoe"
]

last_names = [
    "Anderson", "Brown", "Carter", "Davis", "Edwards", "Foster", "Green", "Hughes",
    "Irving", "Johnson", "Kelly", "Lopez", "Miller", "Nelson", "Owens", "Parker",
    "Quincy", "Roberts", "Stewart", "Thompson", "Underwood", "Vargas", "Williams",
    "Xu", "Young", "Zimmerman"
]

# -----------------------
# HELPER FUNCTIONS
# -----------------------
def generate_dummy_contact():
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    email = f"{first_name.lower()}.{last_name.lower()}@example.com"
    phone = f"+1-{random.randint(100,999)}-{random.randint(1000,9999)}"
    
    job_titles = ["Engineer", "Marketing Manager", "Account Executive", "Designer", "Analyst"]
    lifecycle_stages = ["subscriber", "lead", "marketingqualifiedlead", "salesqualifiedlead", "opportunity", "customer"]
    lead_statuses = ["NEW", "OPEN", "IN_PROGRESS", "OPEN_DEAL", "UNQUALIFIED", "ATTEMPTED_TO_CONTACT", "CONNECTED", "BAD_TIMING"]

    return {
        "properties": {
            "firstname": first_name,
            "lastname": last_name,
            "email": email,
            "phone": phone,
            "jobtitle": random.choice(job_titles),
            "lifecyclestage": random.choice(lifecycle_stages),
            "hs_lead_status": random.choice(lead_statuses),
            "hubspot_owner_id": HUBSPOT_OWNER_ID
        }
    }

# -----------------------
# MAIN LOOP
# -----------------------
NUM_CONTACTS = 5

for i in range(NUM_CONTACTS):
    contact_data = generate_dummy_contact()
    response = requests.post(HUBSPOT_CONTACT_URL, headers=HEADERS, json=contact_data)
    
    if response.status_code == 201:
        print(f"✅ Created contact: {contact_data['properties']['firstname']} {contact_data['properties']['lastname']}")
    elif response.status_code == 409:
        print(f"⚠️ Skipped duplicate contact: {contact_data['properties']['email']}")
    else:
        print(f"❌ Failed to create contact. Error: {response.json()}")
