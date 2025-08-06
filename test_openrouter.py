#!/usr/bin/env python3
"""Test script for the new OpenRouter implementation"""

from sdr_generator_v2 import SDRGenerator
from sdr_sequence_generator_v2 import SDRSequenceGenerator
import os
from dotenv import load_dotenv
import yaml

load_dotenv()

# Test data
test_prospect = {
    "caseStudy": "We helped a fintech company increase ARR by 30% in 6 months.",
    "ICP": "B2B SaaS companies scaling into new markets with 50–500 employees.",
    "companyName": "TechVentures Inc",
    "activity": "Just announced expansion into Asian markets with new Singapore office.",
    "companyWebsite": "https://techventures.com",
    "senderCompany": "YourCompany",
    "ourWebsite": "https://yourcompany.com",
    "meetingLink": "https://calendly.com/yourcompany/demo",
    "senderName": "Sarah Johnson",
    "senderTitle": "Growth Strategist",
    "firstName": "Michael",
    "lastName": "Chen",
    "linkedinURL": "https://linkedin.com/in/michael-chen"
}

def test_with_provider(provider):
    """Test email generation with specified provider"""
    print(f"\n{'='*60}")
    print(f"Testing with {provider.upper()}")
    print('='*60)
    
    # Update config to use specified provider
    config = {
        "model_provider": provider,
        "openai": {
            "model": "gpt-4-turbo-preview",
            "temperature": 0.7
        },
        "openrouter": {
            "base_url": "https://openrouter.ai/api/v1",
            "model": "anthropic/claude-3-sonnet",
            "temperature": 0.7
        },
        "logging": {
            "level": "INFO",
            "file": "test_output.log"
        },
        "output": {
            "save_to_file": True,
            "output_dir": "test_outputs"
        }
    }
    
    # Save temporary config
    with open('test_config.yaml', 'w') as f:
        yaml.dump(config, f)
    
    try:
        # Test single email generation
        print("\n1. Testing single email generation...")
        generator = SDRGenerator(config_path='test_config.yaml')
        email = generator.generate_email(test_prospect)
        print("✓ Single email generated successfully!")
        print(f"   Length: {len(email)} characters")
        
        # Test sequence generation
        print("\n2. Testing sequence generation...")
        seq_generator = SDRSequenceGenerator(config_path='test_config.yaml')
        result = seq_generator.generate_and_parse(test_prospect)
        
        if result['status'] == 'success':
            print(f"✓ Sequence generated successfully!")
            print(f"   Number of emails: {len(result['emails'])}")
            for email in result['emails']:
                print(f"   - Email {email['step']}: {email['subject'][:50]}...")
        else:
            print(f"✗ Sequence generation failed: {result['error']}")
            
    except Exception as e:
        print(f"✗ Error with {provider}: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        if os.path.exists('test_config.yaml'):
            os.remove('test_config.yaml')

def main():
    print("\nSDR Email Generator Test Suite")
    print("==============================")
    
    # Check which API keys are available
    has_openai = bool(os.getenv("OPENAI_API_KEY"))
    has_openrouter = bool(os.getenv("OPENROUTER_API_KEY"))
    
    print(f"\nAPI Keys found:")
    print(f"- OpenAI: {'✓' if has_openai else '✗'}")
    print(f"- OpenRouter: {'✓' if has_openrouter else '✗'}")
    
    if has_openai:
        test_with_provider('openai')
    else:
        print("\nSkipping OpenAI test (no API key found)")
        
    if has_openrouter:
        test_with_provider('openrouter')
    else:
        print("\nSkipping OpenRouter test (no API key found)")
        print("\nTo test OpenRouter, add OPENROUTER_API_KEY to your .env file")
        print("Get your key at: https://openrouter.ai/keys")
    
    print("\n" + "="*60)
    print("Test suite complete!")
    
    # Show generated files
    if os.path.exists('test_outputs'):
        files = os.listdir('test_outputs')
        if files:
            print(f"\nGenerated files in test_outputs/:")
            for f in files:
                print(f"  - {f}")

if __name__ == "__main__":
    main()