#!/usr/bin/env python3
"""Test script for the enhanced email generator with comprehensive prompts"""

from sdr_generator_enhanced import EnhancedSDRGenerator
import os
from dotenv import load_dotenv
from colorama import init, Fore, Style

init(autoreset=True)
load_dotenv()

# Test data with enhanced fields
test_prospect = {
    "caseStudy": "We helped TechCorp, a B2B SaaS company, increase their enterprise pipeline by 45% in just 4 months by implementing our AI-powered lead scoring and personalization engine.",
    "ICP": "B2B SaaS companies with 50-500 employees that are scaling their outbound sales efforts and looking to improve conversion rates.",
    "companyName": "ScaleFlow Solutions",
    "activity": "Just raised $25M Series B funding and announced plans to double their sales team while expanding into European markets.",
    "companyWebsite": "https://scaleflow.com",
    "industry": "Sales Technology",
    "senderCompany": "YourCompany",
    "ourWebsite": "https://yourcompany.com",
    "meetingLink": "https://calendly.com/yourcompany/demo",
    "senderName": "Sarah Johnson",
    "senderTitle": "Head of Strategic Accounts",
    "firstName": "Michael",
    "lastName": "Rodriguez",
    "linkedinURL": "https://linkedin.com/in/michael-rodriguez",
    "title": "VP of Sales"
}

def test_enhanced_generator():
    """Test the enhanced email generator"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Testing Enhanced Email Generator{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    try:
        # Initialize generator
        generator = EnhancedSDRGenerator()
        
        # Test 1: Generate email without analysis
        print(f"\n{Fore.YELLOW}Test 1: Generating email without analysis...{Style.RESET_ALL}")
        email_only = generator.generate_email(test_prospect, include_analysis=False)
        
        print(f"\n{Fore.GREEN}✓ Email generated successfully!{Style.RESET_ALL}")
        print("\n" + "-"*40 + " EMAIL ONLY " + "-"*40)
        print(email_only)
        print("-"*92 + "\n")
        
        # Test 2: Generate email with full analysis
        print(f"\n{Fore.YELLOW}Test 2: Generating email with full analysis...{Style.RESET_ALL}")
        full_output = generator.generate_email(test_prospect, include_analysis=True)
        
        print(f"\n{Fore.GREEN}✓ Full output generated successfully!{Style.RESET_ALL}")
        print("\n" + "-"*35 + " FULL OUTPUT WITH ANALYSIS " + "-"*35)
        print(full_output)
        print("-"*97 + "\n")
        
        # Check saved files
        output_dir = "generated_emails"
        if os.path.exists(output_dir):
            files = [f for f in os.listdir(output_dir) if f.startswith("enhanced_") or f.startswith("analysis_")]
            if files:
                print(f"\n{Fore.GREEN}✓ Files saved successfully:{Style.RESET_ALL}")
                for f in files:
                    print(f"  - {f}")
        
    except Exception as e:
        print(f"\n{Fore.RED}✗ Error: {str(e)}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

def test_cli_commands():
    """Show example CLI commands"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Example CLI Commands:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    print("\n1. Basic enhanced email generation:")
    print(f"{Fore.GREEN}python cli.py generate -f Michael -l Rodriguez -c 'ScaleFlow Solutions' -a 'Raised $25M Series B' --enhanced{Style.RESET_ALL}")
    
    print("\n2. Enhanced with industry and title:")
    print(f"{Fore.GREEN}python cli.py generate -f Michael -l Rodriguez -c 'ScaleFlow Solutions' -a 'Raised $25M Series B' -i 'Sales Technology' -t 'VP of Sales' --enhanced{Style.RESET_ALL}")
    
    print("\n3. Enhanced with full analysis:")
    print(f"{Fore.GREEN}python cli.py generate -f Michael -l Rodriguez -c 'ScaleFlow Solutions' -a 'Raised $25M Series B' --enhanced --include-analysis{Style.RESET_ALL}")
    
    print("\n4. Using different AI model:")
    print(f"{Fore.GREEN}python cli.py generate -f Michael -l Rodriguez -c 'ScaleFlow Solutions' -a 'Raised $25M Series B' --enhanced -m 'anthropic/claude-3-opus'{Style.RESET_ALL}")

def compare_outputs():
    """Compare standard vs enhanced generator outputs"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Comparing Standard vs Enhanced Generators{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    try:
        from sdr_generator_v2 import SDRGenerator
        
        # Standard generator
        print(f"\n{Fore.YELLOW}Generating with STANDARD generator...{Style.RESET_ALL}")
        standard_gen = SDRGenerator()
        standard_email = standard_gen.generate_email(test_prospect)
        
        print("\n" + "-"*40 + " STANDARD " + "-"*40)
        print(standard_email[:500] + "..." if len(standard_email) > 500 else standard_email)
        
        # Enhanced generator
        print(f"\n{Fore.YELLOW}Generating with ENHANCED generator...{Style.RESET_ALL}")
        enhanced_gen = EnhancedSDRGenerator()
        enhanced_email = enhanced_gen.generate_email(test_prospect, include_analysis=False)
        
        print("\n" + "-"*40 + " ENHANCED " + "-"*40)
        print(enhanced_email[:500] + "..." if len(enhanced_email) > 500 else enhanced_email)
        
        print(f"\n{Fore.GREEN}Key Differences:{Style.RESET_ALL}")
        print("- Enhanced version includes more detailed personalization")
        print("- Enhanced version uses industry and title information")
        print("- Enhanced version follows a more structured approach")
        print("- Enhanced version includes comprehensive outreach analysis")
        
    except Exception as e:
        print(f"\n{Fore.RED}✗ Comparison failed: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    print(f"\n{Fore.CYAN}Enhanced SDR Email Generator Test Suite{Style.RESET_ALL}")
    print(f"{Fore.CYAN}======================================{Style.RESET_ALL}")
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("OPENROUTER_API_KEY"):
        print(f"\n{Fore.RED}ERROR: No API key found!{Style.RESET_ALL}")
        print("Please add OPENAI_API_KEY or OPENROUTER_API_KEY to your .env file")
        exit(1)
    
    # Run tests
    test_enhanced_generator()
    test_cli_commands()
    compare_outputs()
    
    print(f"\n{Fore.GREEN}✓ All tests completed!{Style.RESET_ALL}")