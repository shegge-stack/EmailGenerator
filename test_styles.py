#!/usr/bin/env python3
"""
Test different email styles for Adarsh
"""

import requests
import json

# Adarsh's data
adarsh_data = {
    "firstName": "Adarsh",
    "lastName": "Solanki",
    "companyName": "Meta",
    "companyWebsite": "https://meta.com",
    "linkedinURL": "https://linkedin.com/in/adarshsolanki",
    "title": "Technical Product Leader",
    "industry": "Technology",
    "activity": "Building AI at Meta after Roblox acquired his computer vision startup Jido",
    "caseStudy": "3 ex-FAANG product leaders booked $400k+ in fractional work using messages that reference specific technical decisions they made - seeing 47% response rates vs 1-3% industry standard",
    "ICP": "Technical leaders exploring fractional/advisory work who need to stand out without corporate brand",
    "senderName": "Sam",
    "senderTitle": "Founder",
    "senderCompany": "Pingit",
    "meetingLink": "https://calendly.com/sam-pingit/30min",
    "ourWebsite": "https://pingit.ai"
}

# Test each style
styles = ["professional", "pattern_interrupt", "casual_conversational", "value_first", "challenge_based"]

for style in styles:
    print(f"\n{'='*60}")
    print(f"🎯 Testing {style.upper()} style")
    print(f"{'='*60}\n")
    
    # Add style to data
    test_data = adarsh_data.copy()
    test_data["style"] = style
    
    try:
        response = requests.post(
            "http://localhost:5001/api/generate-email",
            headers={"Content-Type": "application/json"},
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                email = result['email']
                print(f"✅ Subject: {email['subject']}")
                print(f"\n{email['body']}")
                print(f"\n📊 Word count: {result['word_count']}")
            else:
                print(f"❌ Error: {result.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")
        
print("\n" + "="*60)
print("✅ Style testing complete!")