#!/usr/bin/env python3
"""
Different ways to capture and pass email generation parameters
"""

# Method 1: Direct Python Dictionary (Best for API/programmatic use)
def method_1_python_dict():
    prospect_data = {
        "firstName": "Samuel",
        "lastName": "Hegge",
        "companyName": "Singular",
        "companyWebsite": "https://singular.net",
        "activity": "Leading mobile attribution platform serving TikTok, Airbnb",
        "industry": "Mobile Marketing Technology", 
        "title": "Founder",
        "linkedinURL": "https://linkedin.com/in/samuel-hegge",
        "caseStudy": "We helped TechCorp increase qualified meetings by 45% using our outbound platform",
        "ICP": "B2B SaaS companies looking to scale outbound sales",
        "senderName": "Sarah Johnson",
        "senderTitle": "VP of Sales", 
        "senderCompany": "OutreachPro",
        "ourWebsite": "https://outreachpro.com",
        "meetingLink": "https://calendly.com/outreachpro/demo"
    }
    return prospect_data

# Method 2: CSV File (Best for batch processing)
def method_2_csv_example():
    """
    Create a CSV file with headers:
    firstName,lastName,companyName,companyWebsite,activity,industry,title,linkedinURL,caseStudy,ICP,senderName,senderTitle,senderCompany,ourWebsite,meetingLink
    
    Then use:
    python cli.py batch -f prospects.csv -o results.csv --enhanced
    """
    pass

# Method 3: JSON File (Best for complex data structures)
def method_3_json_file():
    import json
    
    data = {
        "prospect": {
            "firstName": "Samuel",
            "lastName": "Hegge",
            "companyName": "Singular",
            "companyWebsite": "https://singular.net",
            "activity": "Leading mobile attribution platform",
            "industry": "Mobile Marketing Technology",
            "title": "Founder",
            "linkedinURL": "https://linkedin.com/in/samuel-hegge"
        },
        "sender": {
            "senderName": "Sarah Johnson",
            "senderTitle": "VP of Sales",
            "senderCompany": "OutreachPro", 
            "ourWebsite": "https://outreachpro.com",
            "meetingLink": "https://calendly.com/outreachpro/demo"
        },
        "messaging": {
            "caseStudy": "We helped TechCorp increase qualified meetings by 45%",
            "ICP": "B2B SaaS companies looking to scale outbound sales"
        }
    }
    
    # Flatten for generator
    flat_data = {}
    for category, fields in data.items():
        flat_data.update(fields)
    
    return flat_data

# Method 4: Interactive CLI (Best for one-off emails)
def method_4_interactive_cli():
    """
    Use the CLI with prompts:
    python cli.py generate -f Samuel -l Hegge -c "Singular" -a "Leading attribution platform" --enhanced
    """
    pass

# Method 5: Web Form Integration (Best for non-technical users)
def method_5_web_form():
    """
    Create a simple web interface that captures:
    
    PROSPECT INFO:
    - First Name: [input]
    - Last Name: [input] 
    - Company: [input]
    - Recent Activity: [textarea]
    - Industry: [dropdown]
    - Title: [input]
    - LinkedIn: [input]
    
    YOUR COMPANY:
    - Case Study: [textarea]
    - ICP: [textarea]
    - Sender Name: [input]
    - Meeting Link: [input]
    
    Then POST to your email generator API
    """
    pass

# Method 6: CRM Integration (Best for sales teams)
def method_6_crm_integration():
    """
    Pull data directly from:
    - HubSpot contacts
    - Salesforce leads
    - Pipedrive deals
    
    Map CRM fields to email parameters:
    contact.first_name -> firstName
    contact.company -> companyName  
    contact.industry -> industry
    etc.
    """
    pass

# Method 7: Google Sheets Integration (Best for sales ops)
def method_7_google_sheets():
    """
    Set up a Google Sheet with columns:
    A: firstName
    B: lastName  
    C: companyName
    D: activity
    E: industry
    ...
    
    Use Google Sheets API to pull data and generate emails
    """
    pass

if __name__ == "__main__":
    # Example of Method 1
    data = method_1_python_dict()
    print("Method 1 - Python Dict:")
    for key, value in data.items():
        print(f"  {key}: {value}")
        
    print("\nMethod 3 - JSON Structure:")
    json_data = method_3_json_file()
    for key, value in json_data.items():
        print(f"  {key}: {value}")