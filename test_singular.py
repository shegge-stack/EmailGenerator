#!/usr/bin/env python3
"""Test with Singular.net data"""

from sdr_generator_enhanced import EnhancedSDRGenerator

# Real prospect data
singular_data = {
    "firstName": "Samuel",
    "lastName": "Hegge", 
    "companyName": "Singular",
    "companyWebsite": "https://singular.net",
    "activity": "Leading mobile attribution and marketing analytics platform serving top mobile apps like TikTok, Airbnb, and others",
    "industry": "Mobile Marketing Technology",
    "title": "Founder",
    "linkedinURL": "https://linkedin.com/in/samuel-hegge",
    "caseStudy": "We helped MobileApp Co increase their user acquisition efficiency by 40% and reduce their cost per install by 25% using our attribution and analytics platform",
    "ICP": "Mobile app companies and marketing teams looking to optimize their user acquisition and attribution strategies",
    "senderName": "Sarah Johnson", 
    "senderTitle": "VP of Partnerships",
    "senderCompany": "MarketingTech Solutions",
    "ourWebsite": "https://marketingtech.com",
    "meetingLink": "https://calendly.com/marketingtech/demo"
}

def test_singular():
    generator = EnhancedSDRGenerator()
    
    print("Testing with Singular.net data...")
    print("=" * 60)
    
    # Generate with full analysis
    result = generator.generate_email(singular_data, include_analysis=True)
    print(result)

if __name__ == "__main__":
    test_singular()