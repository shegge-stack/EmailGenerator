#!/usr/bin/env python3
"""
Deep Personalization Research Tool
Gather intelligence from public sources for hyper-personalized outreach
"""

import requests
from typing import Dict, List, Optional
from dataclasses import dataclass
import json

@dataclass
class PersonalityInsight:
    motivation: str
    pain_point: str
    communication_style: str
    decision_triggers: List[str]
    social_proof_preference: str

@dataclass
class DeepProfile:
    basic_info: Dict[str, str]
    professional_insights: Dict[str, str]
    personality_profile: PersonalityInsight
    messaging_hooks: List[str]
    objection_handlers: Dict[str, str]

class DeepPersonalizationEngine:
    """
    Research engine for gathering public intelligence on prospects
    Uses only compliant, public data sources
    """
    
    def __init__(self, apollo_api_key: Optional[str] = None):
        self.apollo_api_key = apollo_api_key
        
    def research_prospect(self, linkedin_url: str, company_domain: str = None) -> DeepProfile:
        """
        Gather deep intelligence on a prospect from public sources
        """
        
        # 1. Basic enrichment via APIs
        basic_info = self._enrich_basic_data(linkedin_url)
        
        # 2. Company intelligence
        company_intel = self._research_company(company_domain or basic_info.get('companyWebsite'))
        
        # 3. Professional pattern analysis
        professional_insights = self._analyze_professional_patterns(basic_info, company_intel)
        
        # 4. Personality profiling
        personality = self._build_personality_profile(basic_info, professional_insights)
        
        # 5. Messaging hooks
        messaging_hooks = self._generate_messaging_hooks(basic_info, professional_insights, personality)
        
        # 6. Objection handlers
        objection_handlers = self._prepare_objection_handlers(personality)
        
        return DeepProfile(
            basic_info=basic_info,
            professional_insights=professional_insights,
            personality_profile=personality,
            messaging_hooks=messaging_hooks,
            objection_handlers=objection_handlers
        )
    
    def _enrich_basic_data(self, linkedin_url: str) -> Dict[str, str]:
        """Enrich basic prospect data via compliant APIs"""
        
        if self.apollo_api_key:
            # Use Apollo.io for compliant LinkedIn data
            try:
                response = requests.post(
                    'https://api.apollo.io/v1/people/match',
                    json={'api_key': self.apollo_api_key, 'linkedin_url': linkedin_url}
                )
                if response.status_code == 200:
                    data = response.json().get('person', {})
                    return {
                        'firstName': data.get('first_name', ''),
                        'lastName': data.get('last_name', ''),
                        'title': data.get('title', ''),
                        'companyName': data.get('organization', {}).get('name', ''),
                        'companyWebsite': data.get('organization', {}).get('website_url', ''),
                        'industry': data.get('organization', {}).get('industry', ''),
                        'location': data.get('city', ''),
                        'experience_years': str(len(data.get('employment_history', []))),
                        'education': data.get('education', [{}])[0].get('school_name', '') if data.get('education') else ''
                    }
            except Exception as e:
                print(f"Apollo enrichment failed: {e}")
        
        # Fallback to basic URL parsing
        return self._parse_linkedin_url(linkedin_url)
    
    def _parse_linkedin_url(self, url: str) -> Dict[str, str]:
        """Extract basic info from LinkedIn URL structure"""
        import re
        
        match = re.search(r'/in/([^/?]+)', url)
        if not match:
            return {}
            
        username = match.group(1)
        
        # Parse name from username patterns
        if '-' in username:
            parts = username.split('-')
            return {
                'firstName': parts[0].title(),
                'lastName': parts[1].title() if len(parts) > 1 else '',
                'linkedinUsername': username
            }
        
        return {'firstName': username.title(), 'linkedinUsername': username}
    
    def _research_company(self, company_domain: str) -> Dict[str, str]:
        """Research company from public sources"""
        if not company_domain:
            return {}
            
        # You could integrate:
        # - Clearbit Company API
        # - BuiltWith (tech stack)
        # - Crunchbase (funding)
        # - Company news APIs
        
        # Mock company intelligence for demo
        return {
            'funding_stage': 'Series A',
            'employee_count': '50-200',
            'tech_stack': 'Python, React, AWS',
            'recent_news': 'Expanded to new markets',
            'growth_stage': 'scaling',
            'pain_points': 'client acquisition, scaling operations'
        }
    
    def _analyze_professional_patterns(self, basic_info: Dict, company_intel: Dict) -> Dict[str, str]:
        """Analyze professional patterns to understand motivations"""
        
        title = basic_info.get('title', '').lower()
        industry = basic_info.get('industry', '').lower()
        
        # Pattern analysis based on role/industry
        patterns = {}
        
        if 'consultant' in title or 'freelance' in title:
            patterns.update({
                'work_style': 'independent',
                'key_challenges': 'inconsistent pipeline, feast-famine cycle',
                'decision_drivers': 'ROI, time savings, competitive advantage',
                'communication_preference': 'direct, results-focused',
                'social_proof_type': 'case studies, peer testimonials'
            })
        
        if 'ai' in title or 'data' in title or 'machine learning' in title:
            patterns.update({
                'technical_level': 'high',
                'decision_style': 'analytical, evidence-based',
                'objections': 'will want to see the technical approach',
                'value_drivers': 'efficiency, scalability, innovation'
            })
        
        return patterns
    
    def _build_personality_profile(self, basic_info: Dict, professional_insights: Dict) -> PersonalityInsight:
        """Build personality profile for messaging"""
        
        # AI consultant personality pattern
        if professional_insights.get('work_style') == 'independent':
            return PersonalityInsight(
                motivation="Freedom and control over work, helping clients succeed with AI",
                pain_point="Inconsistent client pipeline - feast or famine cycles",
                communication_style="Direct, technical, values expertise",
                decision_triggers=["proven ROI", "time savings", "competitive edge", "peer validation"],
                social_proof_preference="Case studies from similar consultants"
            )
        
        # Default technical professional
        return PersonalityInsight(
            motivation="Professional growth and recognition",
            pain_point="Scaling challenges and inefficient processes", 
            communication_style="Professional, fact-based",
            decision_triggers=["data-driven results", "efficiency gains"],
            social_proof_preference="Industry testimonials"
        )
    
    def _generate_messaging_hooks(self, basic_info: Dict, professional_insights: Dict, personality: PersonalityInsight) -> List[str]:
        """Generate specific messaging hooks based on research"""
        
        name = basic_info.get('firstName', 'there')
        
        hooks = []
        
        # Pain-point hooks
        if 'consultant' in basic_info.get('title', '').lower():
            hooks.extend([
                f"Hi {name}, noticed you're building AI solutions for clients. The hardest part isn't the technical work - it's the unpredictable client pipeline, right?",
                f"{name}, most AI consultants I know are excellent at building solutions but struggle with one thing: consistent high-quality leads.",
                f"Quick question {name} - are you spending more time hunting for clients or actually doing the AI work you love?"
            ])
        
        # Opportunity hooks
        hooks.extend([
            f"{name}, what if you never had to worry about where your next client is coming from?",
            f"Saw your AI work {name} - impressive stuff. Are you getting the caliber of clients who truly value that expertise?",
            f"{name}, you clearly know AI inside and out. The question is: are you getting paid what that expertise is actually worth?"
        ])
        
        return hooks
    
    def _prepare_objection_handlers(self, personality: PersonalityInsight) -> Dict[str, str]:
        """Prepare responses to likely objections"""
        
        return {
            "too_busy": "I get it - you're swamped with client work. That's exactly why this matters. What if the next 30 minutes could save you 10+ hours per week on business development?",
            "already_have_system": "That's great you have something in place. Most consultants do. The question is: are you booking the quality of clients you actually want to work with?",
            "need_to_think": "Absolutely - this is a business decision. What specific concerns would help you think through this faster?",
            "too_expensive": "I understand cost is a factor. What would consistent access to premium clients who value your expertise be worth to your business?",
            "not_interested": "Fair enough. Can I ask - what would have to change about your current client acquisition for you to be interested in exploring alternatives?"
        }

def research_adarsh_solanki() -> Dict[str, any]:
    """
    Research Adarsh Solanki specifically
    This would be populated with actual research
    """
    
    return {
        "basic_profile": {
            "name": "Adarsh Solanki",
            "title": "AI Consultant & Developer", 
            "location": "Unknown",
            "experience": "Independent consultant building AI projects"
        },
        
        "professional_insights": {
            "work_style": "Independent technical consultant",
            "client_type": "Businesses needing AI implementation",
            "key_challenges": [
                "Finding consistent high-quality clients",
                "Positioning expertise effectively", 
                "Scaling beyond 1:1 client work",
                "Competition from agencies and platforms"
            ],
            "decision_drivers": [
                "Proven ROI and results",
                "Time efficiency", 
                "Competitive differentiation",
                "Peer validation from other consultants"
            ]
        },
        
        "personality_analysis": {
            "communication_style": "Technical, direct, values expertise",
            "motivation": "Building innovative AI solutions + business freedom",
            "biggest_fear": "Inconsistent income, competing on price",
            "ideal_outcome": "Consistent pipeline of premium clients who value expertise"
        },
        
        "messaging_strategy": {
            "opening_hook": "The technical work isn't the hard part - it's the feast-famine client cycle",
            "value_proposition": "Consistent premium clients who seek you out",
            "social_proof": "Other AI consultants' success stories",
            "call_to_action": "Explore how to never worry about your next client again"
        }
    }

if __name__ == "__main__":
    # Demo the research
    research = research_adarsh_solanki()
    print("🎯 DEEP PERSONALIZATION RESEARCH")
    print("=" * 50)
    print(json.dumps(research, indent=2))