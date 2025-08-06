#!/usr/bin/env python3
"""Test with better company differentiation"""

from sdr_generator_enhanced import EnhancedSDRGenerator

# Better differentiated prospect data
singular_data = {
    "firstName": "Samuel",
    "lastName": "Hegge", 
    "companyName": "Singular",
    "companyWebsite": "https://singular.net",
    "activity": "Leading mobile attribution and marketing analytics platform serving top mobile apps like TikTok, Airbnb, and others",
    "industry": "Mobile Marketing Technology",
    "title": "Founder",
    "linkedinURL": "https://linkedin.com/in/samuel-hegge",
    # Clear case study showing we do EMAIL/OUTBOUND, not attribution
    "caseStudy": "We helped TechStartup increase their qualified sales meetings by 60% and reduce their sales cycle by 30% using our AI-powered email outreach and lead generation platform",
    "ICP": "B2B SaaS companies and marketing teams looking to scale their outbound sales efforts and book more qualified meetings",
    "senderName": "Sarah Johnson", 
    "senderTitle": "VP of Sales",
    "senderCompany": "OutreachPro",  # Clear company name showing different service
    "ourWebsite": "https://outreachpro.com",
    "meetingLink": "https://calendly.com/outreachpro/demo"
}

def test_singular_fixed():
    generator = EnhancedSDRGenerator()
    
    print("Testing with better company differentiation...")
    print("=" * 60)
    
    # Generate with updated prompts
    result = generator.generate_email(singular_data, include_analysis=False)
    print(result)

if __name__ == "__main__":
    test_singular_fixed()