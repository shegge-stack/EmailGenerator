#!/usr/bin/env python3
"""Test script to verify sequence generator functionality"""

from sdr_sequence_generator import SDRSequenceGenerator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY not found in .env file")
    exit(1)

print("✓ API key found")
print("\nTesting sequence generation...")
print("-" * 50)

# Initialize generator
generator = SDRSequenceGenerator()

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
    # Generate sequence
    sequence_output = generator.generate_sequence(prospect_data)
    print("\nGENERATED SEQUENCE:")
    print("=" * 50)
    print(sequence_output)
    print("=" * 50)
    print("\n✓ Sequence generation successful!")
    
except Exception as e:
    print(f"\n✗ Error generating sequence: {str(e)}")