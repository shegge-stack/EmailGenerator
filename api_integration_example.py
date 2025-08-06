#!/usr/bin/env python3
"""
API Integration Examples for Email Generator Parameters
"""

from flask import Flask, request, jsonify
from sdr_generator_enhanced import EnhancedSDRGenerator
import json

app = Flask(__name__)

# Method 1: REST API Endpoint
@app.route('/generate-email', methods=['POST'])
def generate_email_api():
    """
    POST /generate-email
    
    Body: {
        "firstName": "Samuel",
        "lastName": "Hegge",
        "companyName": "Singular",
        "activity": "Leading mobile attribution platform",
        "industry": "Mobile Tech",
        "title": "Founder",
        "caseStudy": "We helped...",
        "ICP": "B2B SaaS companies...",
        "senderName": "Sarah",
        "senderTitle": "VP Sales",
        "senderCompany": "OutreachPro",
        "meetingLink": "https://calendly.com/demo"
    }
    """
    try:
        data = request.json
        
        # Validate required fields
        required_fields = [
            'firstName', 'lastName', 'companyName', 'activity',
            'caseStudy', 'ICP', 'senderName', 'senderTitle', 
            'senderCompany', 'meetingLink'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'missing': missing_fields
            }), 400
        
        # Generate email
        generator = EnhancedSDRGenerator()
        email = generator.generate_email(data)
        
        return jsonify({
            'success': True,
            'email': email,
            'prospect': f"{data['firstName']} {data['lastName']} at {data['companyName']}"
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Method 2: Webhook for CRM Integration
@app.route('/webhook/crm-contact-created', methods=['POST'])
def crm_webhook():
    """
    Webhook that receives CRM contact data and generates email
    """
    try:
        crm_data = request.json
        
        # Map CRM fields to email generator parameters
        email_params = {
            'firstName': crm_data.get('contact', {}).get('firstname'),
            'lastName': crm_data.get('contact', {}).get('lastname'),
            'companyName': crm_data.get('contact', {}).get('company'),
            'companyWebsite': crm_data.get('contact', {}).get('website'),
            'activity': crm_data.get('contact', {}).get('notes'),
            'industry': crm_data.get('contact', {}).get('industry'),
            'title': crm_data.get('contact', {}).get('jobtitle'),
            'linkedinURL': crm_data.get('contact', {}).get('linkedin_url'),
            # Static company info (from config)
            'caseStudy': 'We helped TechCorp increase qualified meetings by 45%',
            'ICP': 'B2B SaaS companies looking to scale outbound sales',
            'senderName': 'Sarah Johnson',
            'senderTitle': 'VP of Sales',
            'senderCompany': 'OutreachPro',
            'ourWebsite': 'https://outreachpro.com',
            'meetingLink': 'https://calendly.com/outreachpro/demo'
        }
        
        # Generate and return email
        generator = EnhancedSDRGenerator()
        email = generator.generate_email(email_params)
        
        return jsonify({
            'success': True,
            'email': email
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Method 3: Batch Processing Endpoint
@app.route('/batch-generate', methods=['POST'])
def batch_generate():
    """
    POST /batch-generate
    
    Body: {
        "prospects": [
            {prospect1_data},
            {prospect2_data}
        ]
    }
    """
    try:
        data = request.json
        prospects = data.get('prospects', [])
        
        generator = EnhancedSDRGenerator()
        results = []
        
        for prospect in prospects:
            try:
                email = generator.generate_email(prospect)
                results.append({
                    'prospect': f"{prospect['firstName']} {prospect['lastName']}",
                    'success': True,
                    'email': email
                })
            except Exception as e:
                results.append({
                    'prospect': f"{prospect.get('firstName', 'Unknown')} {prospect.get('lastName', '')}",
                    'success': False,
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'results': results,
            'total': len(prospects),
            'successful': sum(1 for r in results if r['success'])
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Method 4: Parameter Template Endpoint
@app.route('/parameter-template', methods=['GET'])
def parameter_template():
    """
    Returns a template with all available parameters
    """
    template = {
        "prospect_info": {
            "firstName": "string (required)",
            "lastName": "string (required)", 
            "companyName": "string (required)",
            "companyWebsite": "url (optional)",
            "activity": "string (required) - recent company news/activity",
            "industry": "string (optional)",
            "title": "string (optional) - job title",
            "linkedinURL": "url (optional)"
        },
        "sender_info": {
            "senderName": "string (required)",
            "senderTitle": "string (required)",
            "senderCompany": "string (required)",
            "ourWebsite": "url (optional)",
            "meetingLink": "url (required)"
        },
        "messaging": {
            "caseStudy": "string (required) - specific success story with metrics",
            "ICP": "string (required) - ideal customer profile description"
        },
        "options": {
            "enhanced": "boolean (optional) - use enhanced generator",
            "includeAnalysis": "boolean (optional) - include analysis in output",
            "model": "string (optional) - AI model to use"
        }
    }
    
    return jsonify(template)

if __name__ == '__main__':
    print("Email Generator API Examples")
    print("============================")
    print("1. POST /generate-email - Single email generation")
    print("2. POST /webhook/crm-contact-created - CRM webhook")
    print("3. POST /batch-generate - Batch processing")
    print("4. GET /parameter-template - Parameter documentation")
    print("\nRun with: python api_integration_example.py")
    
    app.run(debug=True, port=5000)