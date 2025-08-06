#!/usr/bin/env python3
"""
Simple API for MVP 1:1 Email Generator
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from sdr_generator_enhanced import EnhancedSDRGenerator
import re

app = Flask(__name__)
CORS(app)

# Initialize generator
email_generator = EnhancedSDRGenerator()

@app.route('/')
def serve_ui():
    return send_from_directory('.', 'simple_1to1_ui.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/api/generate-email', methods=['POST'])
def generate_email():
    """Generate email - simplified for MVP."""
    try:
        data = request.json
        
        # Validate required fields
        required = ['firstName', 'lastName', 'companyName', 'activity', 'caseStudy', 'senderName', 'meetingLink']
        missing = [f for f in required if not data.get(f)]
        
        if missing:
            return jsonify({
                'success': False, 
                'error': f'Missing: {", ".join(missing)}'
            }), 400
        
        # Generate email
        email_content = email_generator.generate_email(data, include_analysis=False)
        
        # Parse email
        subject_match = re.search(r'Subject:\s*(.+?)(?:\n|$)', email_content, re.MULTILINE)
        subject = subject_match.group(1).strip() if subject_match else "Personalized Outreach"
        
        body_match = re.search(r'Subject:.*?\n\n(.+)', email_content, re.DOTALL)
        body = body_match.group(1).strip() if body_match else email_content.strip()
        
        # Clean body
        body = re.sub(r'<email>|</email>', '', body).strip()
        
        return jsonify({
            'success': True,
            'email': {
                'subject': subject,
                'body': body
            },
            'word_count': len(body.split())
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Simple 1:1 Email Generator")
    print("UI: http://localhost:5000")
    app.run(debug=True, port=5000)