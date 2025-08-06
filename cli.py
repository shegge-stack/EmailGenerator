#!/usr/bin/env python3
"""
CLI interface for SDR Email Generator
"""
import click
import json
import csv
from colorama import init, Fore, Style
from sdr_generator_v2 import SDRGenerator
from sdr_sequence_generator_v2 import SDRSequenceGenerator
from sdr_generator_enhanced import EnhancedSDRGenerator
from model_manager import ModelManager
from loguru import logger
import os

init(autoreset=True)

@click.group()
@click.option('--config', default='config.yaml', help='Path to config file')
@click.pass_context
def cli(ctx, config):
    """SDR Email Generator - Generate personalized sales emails with AI"""
    ctx.ensure_object(dict)
    ctx.obj['config'] = config

@cli.command()
@click.pass_context
def list_models(ctx):
    """List available AI models"""
    try:
        manager = ModelManager(ctx.obj['config'])
        models = manager.list_available_models()
        
        click.echo(f"\n{Fore.CYAN}Available models for {manager.provider}:{Style.RESET_ALL}")
        for model in models:
            click.echo(f"  • {model}")
            
        click.echo(f"\n{Fore.GREEN}Current model: {manager.get_model_name()}{Style.RESET_ALL}")
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

@cli.command()
@click.option('--first-name', '-f', required=True, help='Prospect first name')
@click.option('--last-name', '-l', required=True, help='Prospect last name')
@click.option('--company', '-c', required=True, help='Prospect company name')
@click.option('--activity', '-a', required=True, help='Recent company activity')
@click.option('--industry', '-i', help='Prospect company industry')
@click.option('--title', '-t', help='Prospect job title')
@click.option('--model', '-m', help='Override default model')
@click.option('--json-file', '-j', help='Load prospect data from JSON file')
@click.option('--enhanced', '-e', is_flag=True, help='Use enhanced generator with analysis')
@click.option('--include-analysis', is_flag=True, help='Include outreach analysis in output')
@click.pass_context
def generate(ctx, first_name, last_name, company, activity, industry, title, model, json_file, enhanced, include_analysis):
    """Generate a single personalized email"""
    try:
        # Choose generator based on enhanced flag
        if enhanced:
            generator = EnhancedSDRGenerator(config_path=ctx.obj['config'])
        else:
            generator = SDRGenerator(config_path=ctx.obj['config'])
        
        if json_file:
            with open(json_file, 'r') as f:
                data = json.load(f)
        else:
            # Use default values for demo
            data = {
                "firstName": first_name,
                "lastName": last_name,
                "companyName": company,
                "activity": activity,
                "caseStudy": "We helped a fintech company increase ARR by 30% in 6 months.",
                "ICP": "B2B SaaS companies scaling into new markets with 50–500 employees.",
                "companyWebsite": f"https://{company.lower().replace(' ', '')}.com",
                "linkedinURL": f"https://linkedin.com/in/{first_name.lower()}-{last_name.lower()}",
                "senderCompany": "YourCompany",
                "ourWebsite": "https://yourcompany.com",
                "meetingLink": "https://calendly.com/yourcompany/demo",
                "senderName": "John Doe",
                "senderTitle": "Growth Strategist"
            }
            
            # Add enhanced fields if provided
            if industry:
                data["industry"] = industry
            if title:
                data["title"] = title
        
        generator_type = "enhanced" if enhanced else "standard"
        click.echo(f"\n{Fore.YELLOW}Generating {generator_type} email for {first_name} {last_name} at {company}...{Style.RESET_ALL}")
        
        if enhanced:
            email = generator.generate_email(data, model=model, include_analysis=include_analysis)
        else:
            email = generator.generate_email(data, model=model)
        
        click.echo(f"\n{Fore.GREEN}✓ Email generated successfully!{Style.RESET_ALL}")
        click.echo("\n" + "="*60)
        click.echo(email)
        click.echo("="*60 + "\n")
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

@cli.command()
@click.option('--first-name', '-f', required=True, help='Prospect first name')
@click.option('--last-name', '-l', required=True, help='Prospect last name')
@click.option('--company', '-c', required=True, help='Prospect company name')
@click.option('--activity', '-a', required=True, help='Recent company activity')
@click.option('--model', '-m', help='Override default model')
@click.option('--json-file', '-j', help='Load prospect data from JSON file')
@click.option('--parse', '-p', is_flag=True, help='Parse sequence into individual emails')
@click.pass_context
def sequence(ctx, first_name, last_name, company, activity, model, json_file, parse):
    """Generate a 4-5 email sequence"""
    try:
        generator = SDRSequenceGenerator(config_path=ctx.obj['config'])
        
        if json_file:
            with open(json_file, 'r') as f:
                data = json.load(f)
        else:
            # Use default values for demo
            data = {
                "firstName": first_name,
                "lastName": last_name,
                "companyName": company,
                "activity": activity,
                "caseStudy": "We helped a fintech company increase ARR by 30% in 6 months.",
                "ICP": "B2B SaaS companies scaling into new markets with 50–500 employees.",
                "companyWebsite": f"https://{company.lower().replace(' ', '')}.com",
                "linkedinURL": f"https://linkedin.com/in/{first_name.lower()}-{last_name.lower()}",
                "senderCompany": "YourCompany",
                "ourWebsite": "https://yourcompany.com",
                "meetingLink": "https://calendly.com/yourcompany/demo",
                "senderName": "John Doe",
                "senderTitle": "Growth Strategist"
            }
        
        click.echo(f"\n{Fore.YELLOW}Generating sequence for {first_name} {last_name} at {company}...{Style.RESET_ALL}")
        
        if parse:
            result = generator.generate_and_parse(data, model=model)
            
            if result['status'] == 'success':
                click.echo(f"\n{Fore.GREEN}✓ Sequence generated successfully!{Style.RESET_ALL}")
                click.echo(f"\n{Fore.CYAN}Parsed {len(result['emails'])} emails:{Style.RESET_ALL}")
                
                for email in result['emails']:
                    click.echo(f"\n{Fore.YELLOW}Email {email['step']}:{Style.RESET_ALL}")
                    click.echo(f"Subject: {email['subject']}")
                    click.echo(f"Body:\n{email['body']}\n")
                    click.echo("-" * 60)
            else:
                click.echo(f"{Fore.RED}Error: {result['error']}{Style.RESET_ALL}")
        else:
            sequence_content = generator.generate_sequence(data, model=model)
            click.echo(f"\n{Fore.GREEN}✓ Sequence generated successfully!{Style.RESET_ALL}")
            click.echo("\n" + "="*60)
            click.echo(sequence_content)
            click.echo("="*60 + "\n")
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

@cli.command()
@click.option('--csv-file', '-f', required=True, help='CSV file with prospect data')
@click.option('--output', '-o', default='batch_results.csv', help='Output CSV file')
@click.option('--model', '-m', help='Override default model')
@click.pass_context
def batch(ctx, csv_file, output, model):
    """Generate emails for multiple prospects from CSV"""
    try:
        generator = SDRGenerator(config_path=ctx.obj['config'])
        
        # Load prospects from CSV
        prospects = []
        with open(csv_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            prospects = list(reader)
        
        click.echo(f"\n{Fore.CYAN}Loaded {len(prospects)} prospects from {csv_file}{Style.RESET_ALL}")
        
        # Generate emails
        with click.progressbar(prospects, label='Generating emails') as bar:
            results = []
            for prospect in bar:
                try:
                    email = generator.generate_email(prospect, model=model)
                    prospect['generated_email'] = email
                    prospect['status'] = 'success'
                except Exception as e:
                    prospect['generated_email'] = ''
                    prospect['status'] = 'failed'
                    prospect['error'] = str(e)
                results.append(prospect)
        
        # Save results
        if results:
            fieldnames = list(results[0].keys())
            with open(output, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(results)
        
        success_count = sum(1 for r in results if r['status'] == 'success')
        click.echo(f"\n{Fore.GREEN}✓ Batch generation complete!{Style.RESET_ALL}")
        click.echo(f"  • Success: {success_count}/{len(prospects)}")
        click.echo(f"  • Results saved to: {output}")
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

@cli.command()
@click.pass_context
def setup(ctx):
    """Interactive setup wizard"""
    click.echo(f"\n{Fore.CYAN}SDR Email Generator Setup Wizard{Style.RESET_ALL}")
    click.echo("="*40)
    
    # Check for .env file
    if not os.path.exists('.env'):
        click.echo(f"\n{Fore.YELLOW}Creating .env file...{Style.RESET_ALL}")
        with open('.env', 'w') as f:
            f.write("# API Keys\n")
            
            provider = click.prompt("\nWhich provider would you like to use?", 
                                  type=click.Choice(['openai', 'openrouter']), 
                                  default='openai')
            
            if provider == 'openai':
                api_key = click.prompt("Enter your OpenAI API key", hide_input=True)
                f.write(f"OPENAI_API_KEY={api_key}\n")
            else:
                api_key = click.prompt("Enter your OpenRouter API key", hide_input=True)
                f.write(f"OPENROUTER_API_KEY={api_key}\n")
                
            # HubSpot integration (optional)
            if click.confirm("\nDo you want to set up HubSpot integration?"):
                hubspot_key = click.prompt("Enter your HubSpot Private App Token", hide_input=True)
                f.write(f"HUBSPOT_PRIVATE_APP_TOKEN={hubspot_key}\n")
                
        click.echo(f"{Fore.GREEN}✓ .env file created{Style.RESET_ALL}")
    else:
        click.echo(f"{Fore.GREEN}✓ .env file already exists{Style.RESET_ALL}")
    
    # Create directories
    os.makedirs("generated_emails", exist_ok=True)
    os.makedirs("prompts", exist_ok=True)
    
    click.echo(f"\n{Fore.GREEN}✓ Setup complete!{Style.RESET_ALL}")
    click.echo("\nYou can now use the following commands:")
    click.echo("  • sdr-gen generate -f John -l Doe -c 'Acme Corp' -a 'Raised Series B'")
    click.echo("  • sdr-gen sequence -f Jane -l Smith -c 'TechCo' -a 'Expanding to EMEA'")
    click.echo("  • sdr-gen list-models")

if __name__ == '__main__':
    cli()