#!/usr/bin/env python3
"""
Batch email generation script using v2 generators
Supports both standard and enhanced email generation
"""
import csv
import os
import click
from sdr_generator_v2 import SDRGenerator
from sdr_generator_enhanced import EnhancedSDRGenerator
from loguru import logger
from typing import List, Dict

# Required CSV columns for standard generation
STANDARD_COLUMNS = [
    "caseStudy", "ICP", "companyName", "activity", "companyWebsite",
    "senderCompany", "ourWebsite", "meetingLink",
    "senderName", "senderTitle",
    "firstName", "lastName", "linkedinURL"
]

# Additional columns for enhanced generation
ENHANCED_COLUMNS = STANDARD_COLUMNS + ["industry", "title"]

def load_prospects(file_path: str, enhanced: bool = False) -> List[Dict]:
    """Load prospects from CSV file."""
    prospects = []
    required_columns = ENHANCED_COLUMNS if enhanced else STANDARD_COLUMNS
    
    with open(file_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        # Check if all required columns exist
        if not all(col in reader.fieldnames for col in required_columns):
            missing = [col for col in required_columns if col not in reader.fieldnames]
            logger.warning(f"CSV missing columns: {missing}")
            if enhanced and any(col in ["industry", "title"] for col in missing):
                logger.info("Will use default values for missing enhanced fields")
        
        for row in reader:
            prospects.append(row)
    
    logger.info(f"Loaded {len(prospects)} prospects from {file_path}")
    return prospects

def save_results(results: List[Dict], output_file: str):
    """Save generated emails to CSV."""
    if not results:
        logger.warning("No results to save")
        return
        
    with open(output_file, "w", newline='', encoding="utf-8") as f:
        fieldnames = list(results[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    logger.success(f"Results saved to {output_file}")

@click.command()
@click.option('--input', '-i', 'input_file', required=True, help='Input CSV file with prospects')
@click.option('--output', '-o', 'output_file', default='generated_emails.csv', help='Output CSV file')
@click.option('--enhanced', '-e', is_flag=True, help='Use enhanced generator')
@click.option('--model', '-m', help='AI model to use')
@click.option('--config', '-c', default='config.yaml', help='Config file path')
@click.option('--include-analysis', is_flag=True, help='Include analysis in output (enhanced only)')
def main(input_file, output_file, enhanced, model, config, include_analysis):
    """Batch generate personalized emails from CSV file."""
    # Set up logging
    logger.add("batch_generation.log", rotation="10 MB")
    
    logger.info(f"Starting batch generation - Mode: {'enhanced' if enhanced else 'standard'}")
    
    try:
        # Load prospects
        prospects = load_prospects(input_file, enhanced)
        
        if not prospects:
            logger.error("No prospects found in CSV file")
            return
        
        # Initialize generator
        if enhanced:
            generator = EnhancedSDRGenerator(config_path=config)
        else:
            generator = SDRGenerator(config_path=config)
        
        # Generate emails
        results = []
        success_count = 0
        
        with click.progressbar(prospects, label='Generating emails') as bar:
            for prospect in bar:
                try:
                    if enhanced:
                        email = generator.generate_email(
                            prospect, 
                            model=model, 
                            include_analysis=include_analysis
                        )
                    else:
                        email = generator.generate_email(prospect, model=model)
                    
                    prospect['generated_email'] = email
                    prospect['status'] = 'success'
                    success_count += 1
                    
                except Exception as e:
                    logger.error(f"Failed for {prospect.get('firstName', 'Unknown')}: {str(e)}")
                    prospect['generated_email'] = ''
                    prospect['status'] = 'failed'
                    prospect['error'] = str(e)
                
                results.append(prospect)
        
        # Save results
        save_results(results, output_file)
        
        # Summary
        logger.info(f"\nBatch generation complete!")
        logger.info(f"Success: {success_count}/{len(prospects)}")
        logger.info(f"Failed: {len(prospects) - success_count}/{len(prospects)}")
        
    except Exception as e:
        logger.error(f"Batch generation failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()