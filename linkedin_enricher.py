#!/usr/bin/env python3
"""
LinkedIn-Compliant Data Enrichment System

IMPORTANT: This system DOES NOT scrape LinkedIn directly to comply with their Terms of Service.
Instead, it uses:
1. Third-party enrichment APIs (Apollo, ZoomInfo, Clearbit)
2. Manual input assistance
3. URL parsing for basic validation only

NO DIRECT LINKEDIN SCRAPING IS PERFORMED
"""

import re
from typing import Dict, Optional
from loguru import logger

class LinkedInEnricher:
    def __init__(self, apollo_api_key: Optional[str] = None):
        """
        Initialize LinkedIn-compliant data enricher.
        
        Args:
            apollo_api_key: API key for Apollo.io enrichment service
        """
        self.apollo_api_key = apollo_api_key
        
        # Supported enrichment services (add your API keys)
        self.enrichment_services = {
            'apollo': apollo_api_key,
            # 'zoominfo': os.getenv('ZOOMINFO_API_KEY'),
            # 'clearbit': os.getenv('CLEARBIT_API_KEY'),
        }
        
    def extract_from_url(self, linkedin_url: str) -> Dict[str, str]:
        """
        Extract prospect information using COMPLIANT methods only.
        
        COMPLIANCE NOTICE: 
        - Does NOT scrape LinkedIn directly
        - Uses third-party APIs that have proper data licensing
        - Only validates URL format and extracts basic structure
        - Encourages manual input when APIs aren't available
        """
        try:
            # Clean and validate URL (no scraping, just validation)
            cleaned_url = self._clean_linkedin_url(linkedin_url)
            if not cleaned_url:
                raise ValueError("Invalid LinkedIn URL")
            
            # Extract basic info from URL structure only (no content scraping)
            url_info = self._extract_from_url_structure(cleaned_url)
            
            # Try enrichment APIs (compliant third-party services)
            if self.apollo_api_key:
                enriched_info = self._enrich_with_apollo(cleaned_url)
                if enriched_info:
                    logger.info(f"Successfully enriched via Apollo: {cleaned_url}")
                    return enriched_info
            
            # If no API enrichment available, return template for manual input
            template = self._get_manual_input_template(url_info)
            logger.info(f"LinkedIn URL validated, manual input required: {cleaned_url}")
            return template
            
        except Exception as e:
            logger.error(f"Failed to process LinkedIn URL {linkedin_url}: {str(e)}")
            return self._get_empty_template()
    
    def _clean_linkedin_url(self, url: str) -> Optional[str]:
        """Clean and validate LinkedIn URL."""
        if not url:
            return None
            
        # Remove whitespace and common prefixes
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        # Validate LinkedIn URL pattern
        linkedin_pattern = r'https?://(www\.)?linkedin\.com/in/([^/?]+)'
        match = re.match(linkedin_pattern, url, re.IGNORECASE)
        
        if not match:
            return None
            
        # Return clean URL
        username = match.group(2)
        return f"https://www.linkedin.com/in/{username}"
    
    def _extract_from_url_structure(self, url: str) -> Dict[str, str]:
        """Extract basic info from LinkedIn URL structure."""
        # Extract username from URL
        match = re.search(r'/in/([^/?]+)', url)
        if not match:
            return {}
            
        username = match.group(1)
        
        # Try to parse name from username (common patterns)
        name_parts = self._parse_name_from_username(username)
        
        return {
            'linkedinURL': url,
            'linkedinUsername': username,
            **name_parts
        }
    
    def _parse_name_from_username(self, username: str) -> Dict[str, str]:
        """Attempt to parse name from LinkedIn username."""
        # Common patterns: firstname-lastname, firstnamelastname, etc.
        name_info = {}
        
        if '-' in username:
            parts = username.split('-')
            if len(parts) >= 2:
                name_info['firstName'] = parts[0].title()
                name_info['lastName'] = parts[1].title()
        elif len(username) > 3:
            # Fallback: treat as first name
            name_info['firstName'] = username.title()
            
        return name_info
    
    def _mock_enrichment(self, url_info: Dict[str, str]) -> Dict[str, str]:
        """
        Mock enrichment data for demonstration.
        In production, replace with actual API calls to:
        - LinkedIn Sales Navigator API
        - Apollo.io
        - ZoomInfo
        - Clearbit
        - PhantomBuster
        etc.
        """
        
        # Simulate API delay
        time.sleep(0.5)
        
        # Start with URL info
        enriched = url_info.copy()
        
        # Mock data based on common LinkedIn patterns
        mock_data = {
            'samuel-hegge': {
                'firstName': 'Samuel',
                'lastName': 'Hegge',
                'companyName': 'Singular',
                'companyWebsite': 'https://singular.net',
                'title': 'Founder & CEO',
                'industry': 'Mobile Marketing Technology',
                'activity': 'Leading mobile attribution and marketing analytics platform serving top mobile apps',
                'location': 'Tel Aviv, Israel'
            },
            'john-doe': {
                'firstName': 'John',
                'lastName': 'Doe',
                'companyName': 'TechCorp',
                'companyWebsite': 'https://techcorp.com',
                'title': 'VP of Sales',
                'industry': 'B2B SaaS',
                'activity': 'Recently expanded sales team and launched new product line',
                'location': 'San Francisco, CA'
            }
        }
        
        # Get username and look for mock data
        username = enriched.get('linkedinUsername', '')
        if username in mock_data:
            enriched.update(mock_data[username])
        else:
            # Generic enrichment based on patterns
            if 'firstName' not in enriched:
                enriched['firstName'] = 'Unknown'
            if 'lastName' not in enriched:
                enriched['lastName'] = 'Contact'
            enriched['companyName'] = 'Unknown Company'
            enriched['title'] = 'Professional'
            enriched['industry'] = 'Technology'
            
        return enriched
    
    def _enrich_with_apollo(self, url: str) -> Optional[Dict[str, str]]:
        """
        Enrich data using Apollo.io API (compliant third-party service).
        Apollo has proper data licensing and LinkedIn partnership.
        """
        if not self.apollo_api_key:
            return None
            
        try:
            # Apollo.io API call (they have proper LinkedIn data licensing)
            import requests
            
            response = requests.post(
                'https://api.apollo.io/v1/people/match',
                json={
                    'api_key': self.apollo_api_key,
                    'linkedin_url': url
                },
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                person = data.get('person', {})
                
                return {
                    'firstName': person.get('first_name', ''),
                    'lastName': person.get('last_name', ''),
                    'companyName': person.get('organization', {}).get('name', ''),
                    'companyWebsite': person.get('organization', {}).get('website_url', ''),
                    'title': person.get('title', ''),
                    'industry': person.get('organization', {}).get('industry', ''),
                    'linkedinURL': url,
                    'location': person.get('city', ''),
                    'enrichment_source': 'apollo'
                }
            else:
                logger.warning(f"Apollo API returned {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Apollo enrichment failed: {str(e)}")
            return None
    
    def _get_manual_input_template(self, url_info: Dict[str, str]) -> Dict[str, str]:
        """
        Return template with URL info for manual completion.
        This encourages users to input data manually rather than scraping.
        """
        template = {
            'linkedinURL': url_info.get('linkedinURL', ''),
            'firstName': url_info.get('firstName', ''),
            'lastName': url_info.get('lastName', ''),
            'companyName': '',
            'companyWebsite': '',
            'title': '',
            'industry': '',
            'activity': '',
            'location': '',
            'enrichment_source': 'manual_input_required',
            'instructions': 'Please fill in the missing information manually. No LinkedIn scraping performed.'
        }
        return template
    
    def _get_empty_template(self) -> Dict[str, str]:
        """Return empty template for manual input."""
        return {
            'firstName': '',
            'lastName': '',
            'companyName': '',
            'companyWebsite': '',
            'title': '',
            'industry': '',
            'activity': '',
            'linkedinURL': '',
            'location': ''
        }
    
    def validate_enriched_data(self, data: Dict[str, str]) -> Dict[str, str]:
        """Validate and clean enriched data."""
        required_fields = ['firstName', 'lastName', 'companyName']
        
        # Check for missing required fields
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            logger.warning(f"Missing required fields after enrichment: {missing_fields}")
        
        # Clean data
        cleaned_data = {}
        for key, value in data.items():
            if isinstance(value, str):
                cleaned_data[key] = value.strip()
            else:
                cleaned_data[key] = value
                
        return cleaned_data

# Example usage and testing
if __name__ == "__main__":
    enricher = LinkedInEnricher()
    
    # Test URLs
    test_urls = [
        "https://linkedin.com/in/samuel-hegge",
        "linkedin.com/in/john-doe",
        "https://www.linkedin.com/in/jane-smith",
        "invalid-url"
    ]
    
    print("LinkedIn Enrichment Test Results:")
    print("=" * 50)
    
    for url in test_urls:
        print(f"\nTesting: {url}")
        result = enricher.extract_from_url(url)
        for key, value in result.items():
            print(f"  {key}: {value}")
    print("\n" + "=" * 50)