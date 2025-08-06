#!/usr/bin/env python3
"""Test script to verify email generator functionality"""

from sdr_generator import SDRGenerator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY not found in .env file")
    print("Please add your OpenAI API key to the .env file")
    exit(1)

print("✓ API key found")
print("\nTesting email generation...")
print("-" * 50)

# Initialize generator
generator = SDRGenerator()

# Test data
prospect_data = {
    "caseStudy": "We helped a fintech company increase ARR by 30% in 6 months.",
    "ICP": "B2B SaaS companies scaling into new markets with 50–500 employees.",
    "companyName": "Acme Corp",
    "activity": "Recently raised Series B and is aggressively expanding into EMEA.",
    "companyWebsite": "https://acme.com",
    "senderCompany": "PingPilot",
    "ourWebsite": "https://www.pingit.ai",
    "meetingLink": "https://calendly.com/demo",
    "senderName": "John Doe",
    "senderTitle": "Growth Strategist",
    "firstName": "Sarah",
    "lastName": "Smith",
    "linkedinURL": "https://linkedin.com/in/sarah-smith"
}

try:
    # Generate email
    email_output = generator.generate_email(prospect_data)
    print("\nGENERATED EMAIL:")
    print("=" * 50)
    print(email_output)
    print("=" * 50)
    print("\n✓ Email generation successful!")
    
except Exception as e:
    print(f"\n✗ Error generating email: {str(e)}")
    print("\nPossible causes:")
    print("- Invalid API key")
    print("- Network issues")
    print("- Model name might be incorrect (check if 'gpt-4.5' exists)")