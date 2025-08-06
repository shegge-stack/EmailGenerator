#!/usr/bin/env python3
"""
API Server for Powerful 1:1 Email Generator
Serves the web UI and handles email generation requests
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from sdr_generator_enhanced import EnhancedSDRGenerator
from linkedin_enricher import LinkedInEnricher
from postmark_sender import PowerfulPostmarkSender
import os
import json
from loguru import logger
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Initialize generators
email_generator = EnhancedSDRGenerator()
linkedin_enricher = LinkedInEnricher()

# Initialize Postmark sender if API key is available
postmark_api_key = os.getenv('POSTMARK_API_KEY')
from_email = os.getenv('FROM_EMAIL', 'your@company.com')

if postmark_api_key and postmark_api_key != 'your_postmark_api_key_here':
    postmark_sender = PowerfulPostmarkSender(postmark_api_key, from_email)
    logger.info("Postmark integration enabled")
else:
    postmark_sender = None
    logger.warning("Postmark not configured - email sending disabled")

@app.route('/')
def serve_ui():
    """Serve the main UI."""
    return send_from_directory('.', 'powerful_ui.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files."""
    return send_from_directory('.', filename)

@app.route('/api/enrich-linkedin', methods=['POST'])
def enrich_linkedin():
    """
    Enrich prospect data from LinkedIn URL.
    
    POST /api/enrich-linkedin
    Body: {"linkedin_url": "https://linkedin.com/in/username"}
    """
    try:
        data = request.json
        linkedin_url = data.get('linkedin_url')
        
        if not linkedin_url:
            return jsonify({
                'success': False,
                'error': 'LinkedIn URL is required'
            }), 400
        
        # Enrich data using compliant methods
        enriched_data = linkedin_enricher.extract_from_url(linkedin_url)
        
        # Determine if enrichment was successful
        success = bool(
            enriched_data.get('firstName') and 
            enriched_data.get('lastName') and 
            enriched_data.get('companyName')
        )
        
        return jsonify({
            'success': success,
            'data': enriched_data,
            'source': enriched_data.get('enrichment_source', 'unknown'),
            'message': 'Data enriched successfully' if success else 'Manual input required'
        })
        
    except Exception as e:
        logger.error(f"LinkedIn enrichment error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-email', methods=['POST'])
def generate_email():
    """
    Generate personalized email.
    
    POST /api/generate-email
    Body: {prospect and sender data}
    """
    try:
        data = request.json
        
        # Validate required fields
        required_fields = [
            'firstName', 'lastName', 'companyName', 'activity',
            'caseStudy', 'ICP', 'senderName', 'senderTitle', 
            'senderCompany', 'meetingLink'
        ]
        
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Generate email with style support
        enhanced = data.get('enhanced', True)
        include_analysis = data.get('includeAnalysis', True)
        model = data.get('model')
        style = data.get('style', 'professional')  # Default to professional
        
        # Import email styles
        from email_styles import get_style_prompt, EMAIL_STYLES
        
        if enhanced:
            # Check if using style-based generation
            if style in EMAIL_STYLES:
                # Generate style-specific prompt
                style_prompt = get_style_prompt(style, data)
                # Pass style prompt to generator
                email_content = email_generator.generate_email(
                    data, 
                    model=model, 
                    include_analysis=include_analysis,
                    custom_prompt=style_prompt
                )
            else:
                # Standard generation
                email_content = email_generator.generate_email(
                    data, 
                    model=model, 
                    include_analysis=include_analysis
                )
        else:
            # Fallback to basic generator if needed
            from sdr_generator_v2 import SDRGenerator
            basic_generator = SDRGenerator()
            email_content = basic_generator.generate_email(data, model=model)
        
        # Parse email content
        parsed_email = parse_email_content(email_content)
        
        # Create analysis
        analysis = create_email_analysis(parsed_email, data)
        
        return jsonify({
            'success': True,
            'email': parsed_email,
            'analysis': analysis,
            'prospect': f"{data['firstName']} {data['lastName']} at {data['companyName']}",
            'word_count': len(parsed_email['body'].split()),
            'generation_method': 'enhanced' if enhanced else 'basic',
            'postmark_enabled': postmark_sender is not None
        })
        
    except Exception as e:
        logger.error(f"Email generation error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/validate-email', methods=['POST'])
def validate_email():
    """
    Validate email content for compliance and quality.
    
    POST /api/validate-email
    Body: {"email": "email content"}
    """
    try:
        data = request.json
        email_content = data.get('email', '')
        
        validation_results = {
            'word_count': len(email_content.split()),
            'char_count': len(email_content),
            'has_personalization': check_personalization(email_content),
            'has_cta': check_call_to_action(email_content),
            'spam_risk': assess_spam_risk(email_content),
            'recommendations': generate_recommendations(email_content)
        }
        
        return jsonify({
            'success': True,
            'validation': validation_results
        })
        
    except Exception as e:
        logger.error(f"Email validation error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/templates', methods=['GET'])
def get_templates():
    """Get available email templates and examples."""
    from email_styles import list_available_styles, EMAIL_STYLES
    
    templates = {
        'industries': [
            'B2B SaaS', 'Mobile Marketing Technology', 'E-commerce', 
            'Fintech', 'Healthcare', 'AI/ML', 'Cybersecurity'
        ],
        'tones': ['professional', 'casual', 'provocative'],
        'lengths': ['short', 'medium', 'long'],
        'sample_case_studies': [
            "We helped TechCorp increase their qualified meetings by 45% in 3 months using our outbound platform",
            "Our client MobileApp Co saw a 40% improvement in user acquisition efficiency after implementing our solution",
            "DataFlow Inc reduced their sales cycle by 30% and increased deal size by 25% with our analytics platform"
        ],
        'sample_icps': [
            "B2B SaaS companies with 50-500 employees looking to scale their outbound sales efforts",
            "Mobile app companies and marketing teams seeking better user acquisition strategies",
            "Growing tech companies that need to optimize their sales and marketing processes"
        ]
    }
    
    return jsonify(templates)

@app.route('/api/email-styles', methods=['GET'])
def get_email_styles():
    """Get available email generation styles."""
    from email_styles import list_available_styles, EMAIL_STYLES
    
    styles = []
    for name, style in EMAIL_STYLES.items():
        styles.append({
            'name': name,
            'display_name': style.name,
            'description': style.description,
            'example_subject': style.example_subject
        })
    
    return jsonify({
        'success': True,
        'styles': styles,
        'default': 'professional'
    })

@app.route('/api/send-email', methods=['POST'])
def send_email():
    """Send email via Postmark."""
    if not postmark_sender:
        return jsonify({
            'success': False,
            'error': 'Postmark not configured. Add POSTMARK_API_KEY to .env file.'
        }), 400
    
    try:
        data = request.json
        
        # Validate required fields
        required = ['prospectEmail', 'prospectName', 'companyName', 'subject', 'body', 'meetingLink', 'senderName']
        missing = [f for f in required if not data.get(f)]
        
        if missing:
            return jsonify({
                'success': False,
                'error': f'Missing: {", ".join(missing)}'
            }), 400
        
        # Convert plain text body to HTML
        html_body = data['body'].replace('\n', '<br>')
        html_body = f"<p>{html_body}</p>"
        
        # Send via Postmark
        result = postmark_sender.send_powerful_email(
            prospect_email=data['prospectEmail'],
            prospect_name=data['prospectName'],
            company_name=data['companyName'],
            subject=data['subject'],
            html_body=html_body,
            text_body=data['body'],
            meeting_link=data['meetingLink'],
            sender_name=data['senderName'],
            track_opens=True,
            track_links=True
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Email sending error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/email-performance/<email_id>', methods=['GET'])
def get_email_performance(email_id):
    """Get performance data for specific email."""
    if not postmark_sender:
        return jsonify({'error': 'Postmark not configured'}), 400
    
    try:
        performance = postmark_sender.get_email_performance(email_id)
        return jsonify(performance)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Webhook endpoints for tracking
@app.route('/track/open/<email_id>', methods=['GET'])
def track_open(email_id):
    """Track email open."""
    if postmark_sender:
        postmark_sender.track_email_opened(email_id)
    
    # Return 1x1 transparent pixel
    from flask import Response
    import base64
    
    pixel = base64.b64decode('R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7')
    return Response(pixel, mimetype='image/gif')

@app.route('/track/click/<email_id>', methods=['GET'])
def track_click(email_id):
    """Track link click and redirect."""
    from flask import redirect
    
    url = request.args.get('url')
    link_type = request.args.get('type', 'general')
    
    if postmark_sender:
        postmark_sender.track_link_clicked(email_id, link_type)
    
    return redirect(url) if url else redirect('/')

def parse_email_content(content):
    """Parse email content into structured format."""
    import re
    
    # Extract subject line
    subject_match = re.search(r'Subject:\s*(.+?)(?:\n|$)', content, re.MULTILINE)
    subject = subject_match.group(1).strip() if subject_match else "Generated Email"
    
    # Extract email body (everything after subject)
    body_match = re.search(r'Subject:.*?\n\n(.+)', content, re.DOTALL)
    if body_match:
        body = body_match.group(1).strip()
    else:
        # Fallback: use entire content if no subject found
        body = content.strip()
    
    # Clean up body
    body = re.sub(r'<email>|</email>', '', body)
    body = body.strip()
    
    return {
        'subject': subject,
        'body': body
    }

def create_email_analysis(email, prospect_data):
    """Create analysis of the generated email."""
    body = email['body']
    words = body.split()
    
    # Check personalization elements
    personalization = []
    if prospect_data['firstName'] in body:
        personalization.append('First name')
    if prospect_data['companyName'] in body:
        personalization.append('Company name')
    if prospect_data.get('industry') and prospect_data['industry'] in body:
        personalization.append('Industry')
    if 'linkedin' in body.lower():
        personalization.append('LinkedIn reference')
    
    # Check for call to action
    cta_indicators = ['book', 'schedule', 'calendly', 'meeting', 'call', 'demo', 'time']
    has_cta = any(indicator in body.lower() for indicator in cta_indicators)
    
    return {
        'word_count': len(words),
        'char_count': len(body),
        'sentiment': 'Professional',  # Could integrate sentiment analysis
        'personalization': personalization,
        'call_to_action': 'Meeting booking link' if has_cta else 'None detected',
        'compliance_score': 85,  # Mock compliance score
        'readability': 'Good'
    }

def check_personalization(email_content):
    """Check if email has personalization elements."""
    personalization_indicators = [
        'first name', 'company name', 'industry', 'recent activity',
        'linkedin', 'specific mention', 'custom reference'
    ]
    return len([ind for ind in personalization_indicators if ind in email_content.lower()]) > 2

def check_call_to_action(email_content):
    """Check if email has a clear call to action."""
    cta_patterns = [
        r'book.*time', r'schedule.*meeting', r'calendly', r'demo',
        r'call.*discuss', r'time.*chat', r'meeting.*link'
    ]
    return any(re.search(pattern, email_content, re.IGNORECASE) for pattern in cta_patterns)

def assess_spam_risk(email_content):
    """Assess spam risk of email content."""
    spam_indicators = [
        'urgent', 'limited time', 'act now', 'guaranteed', 'free money',
        'winner', 'congratulations', 'cash', 'investment', 'loan'
    ]
    
    spam_count = sum(1 for indicator in spam_indicators if indicator in email_content.lower())
    
    if spam_count == 0:
        return 'Low'
    elif spam_count <= 2:
        return 'Medium'
    else:
        return 'High'

def generate_recommendations(email_content):
    """Generate improvement recommendations."""
    recommendations = []
    words = email_content.split()
    
    if len(words) > 150:
        recommendations.append('Consider shortening email to under 150 words')
    
    if 'I' in email_content and email_content.count('I ') > 3:
        recommendations.append('Reduce self-focused language, focus more on prospect')
    
    if not check_call_to_action(email_content):
        recommendations.append('Add a clear call to action')
    
    if not check_personalization(email_content):
        recommendations.append('Add more personalization elements')
    
    return recommendations

if __name__ == '__main__':
    print("🎯 Powerful 1:1 Email Generator Server")
    print("=" * 50)
    print("UI available at: http://localhost:5001")
    print("API endpoints:")
    print("- POST /api/enrich-linkedin")
    print("- POST /api/generate-email") 
    print("- POST /api/send-email")
    print("- POST /api/validate-email")
    print("- GET /api/templates")
    if postmark_sender:
        print("📧 Postmark integration: ENABLED")
    else:
        print("⚠️  Postmark integration: DISABLED (add POSTMARK_API_KEY to .env)")
    print("=" * 50)
    
    app.run(debug=True, port=5001, host='0.0.0.0')