import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

HUBSPOT_API_KEY = os.getenv("HUBSPOT_PRIVATE_APP_TOKEN")
BASE_URL = "https://api.hubapi.com"

HEADERS = {
    "Authorization": f"Bearer {HUBSPOT_API_KEY}",
    "Content-Type": "application/json"
}

MAX_RETRIES = 5
RETRY_BACKOFF = 2  # seconds, exponential backoff base

def _request_with_retry(method, url, **kwargs):
    """Helper to retry on 429 or 5xx errors with exponential backoff."""
    for attempt in range(1, MAX_RETRIES + 1):
        response = requests.request(method, url, headers=HEADERS, **kwargs)
        if response.status_code in (429, 500, 502, 503, 504):
            wait = RETRY_BACKOFF ** attempt
            print(f"⚠️ Rate limit or server error. Retry {attempt}/{MAX_RETRIES} in {wait}s...")
            time.sleep(wait)
            continue
        return response
    print(f"❌ Max retries reached for {url}")
    return response  # Last response (likely error)

def create_sequence(sequence_name, emails):
    steps = []
    for i, email in enumerate(emails):
        steps.append({
            "type": "EMAIL",
            "subject": email["subject"],
            "content": email["body"],
            "delay": i * 3
        })

    payload = {"name": sequence_name, "steps": steps}
    url = f"{BASE_URL}/crm/v3/prospecting/sequences"
    response = _request_with_retry("POST", url, json=payload)

    if response.status_code == 201:
        sequence_id = response.json().get("id")
        print(f"✅ Sequence created: {sequence_id}")
        return sequence_id
    else:
        print(f"❌ Failed to create sequence: {response.status_code} {response.text}")
        return None

def enroll_contact(contact_id, sequence_id):
    payload = {
        "contactId": contact_id,
        "sequenceId": sequence_id
    }
    url = f"{BASE_URL}/crm/v3/prospecting/enrollments"
    response = _request_with_retry("POST", url, json=payload)

    if response.status_code == 201:
        print(f"✅ Contact {contact_id} enrolled in sequence {sequence_id}")
        return True
    else:
        print(f"❌ Enrollment failed: {response.status_code} {response.text}")
        return False
