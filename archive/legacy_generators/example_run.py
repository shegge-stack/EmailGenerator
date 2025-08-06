from sdr_generator import SDRGenerator

generator = SDRGenerator()

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

email_output = generator.generate_email(prospect_data)
print(email_output)
