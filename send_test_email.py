#!/usr/bin/env python3
"""
Test script to send email to Adarsh
"""

import requests
import json

# Email data
email_data = {
    "prospectEmail": "test@hegge.ai",
    "prospectName": "Adarsh Solanki", 
    "companyName": "Meta",
    "subject": "your hdr at meta story",
    "body": """read about you pushing hdr video at meta despite the skeptics

made me curious - when you reach out cold (for any reason), does anyone actually respond?

we're solving this for technical leaders. they send specific messages about what they actually built.

result: 47% response rate vs normal 2%

want to see how it works?

sam
https://calendly.com/sam-pingit/30min

ps - we use the same approach for our own outreach. hence this email

---
Sent with Pingit: https://www.pingit.ai""",
    "meetingLink": "https://calendly.com/sam-pingit/30min",
    "senderName": "Sam Hegge"
}

# Send the email
try:
    response = requests.post(
        "http://localhost:5001/api/send-email",
        headers={"Content-Type": "application/json"},
        json=email_data
    )
    
    result = response.json()
    print("Send Result:")
    print(json.dumps(result, indent=2))
    
    if result.get('success'):
        print("\n🎉 EMAIL SENT SUCCESSFULLY!")
        print(f"📧 To: {email_data['prospectEmail']}")
        print(f"📊 Email ID: {result.get('email_id', 'N/A')}")
        print(f"🔗 Tracking: {result.get('tracking_url', 'N/A')}")
    else:
        print("\n❌ SEND FAILED!")
        print(f"Error: {result.get('error')}")
        
except Exception as e:
    print(f"❌ Request failed: {str(e)}")