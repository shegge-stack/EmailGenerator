"""
Enhanced SDR Generator with comprehensive outreach analysis
"""
import os
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from loguru import logger
from model_manager import ModelManager
from typing import Dict, Optional
import re

load_dotenv()

class EnhancedSDRGenerator:
    def __init__(self, api_key: Optional[str] = None, config_path: str = "config.yaml"):
        """Initialize the Enhanced SDR Generator with model manager."""
        self.model_manager = ModelManager(config_path)
        self.env = Environment(loader=FileSystemLoader("prompts"))
        
        # Load enhanced system prompt
        try:
            with open("prompts/enhanced_static_instructions.txt", "r") as f:
                self.system_prompt = f.read()
        except FileNotFoundError:
            logger.error("Enhanced system prompt file not found")
            raise
            
        self.user_template = self.env.get_template("enhanced_dynamic_prompt.txt")
        
        # Configure logging
        log_config = self.model_manager.config.get("logging", {})
        logger.add(
            log_config.get("file", "enhanced_email_generator.log"),
            level=log_config.get("level", "INFO"),
            rotation="10 MB"
        )
        
    def validate_data(self, data: Dict) -> bool:
        """Validate required fields including new enhanced fields."""
        # Required fields from original prompt
        base_required_fields = [
            "caseStudy", "ICP", "companyName", "activity", 
            "companyWebsite", "senderCompany", "ourWebsite", 
            "meetingLink", "senderName", "senderTitle", 
            "firstName", "lastName", "linkedinURL"
        ]
        
        # New enhanced fields (optional but recommended)
        enhanced_fields = ["industry", "title"]
        
        # Check base required fields
        missing_fields = [field for field in base_required_fields if field not in data]
        
        if missing_fields:
            logger.error(f"Missing required fields: {missing_fields}")
            raise ValueError(f"Missing required fields: {missing_fields}")
        
        # Log if enhanced fields are missing (but don't fail)
        missing_enhanced = [field for field in enhanced_fields if field not in data]
        if missing_enhanced:
            logger.warning(f"Missing enhanced fields (will use defaults): {missing_enhanced}")
            # Set defaults for missing enhanced fields
            if "industry" not in data:
                data["industry"] = "Technology"  # Default industry
            if "title" not in data:
                data["title"] = "Decision Maker"  # Default title
            
        return True
        
    def extract_email_from_output(self, output: str) -> Dict[str, str]:
        """Extract the email content and analysis from the model output."""
        result = {
            "full_output": output,
            "analysis": "",
            "email": "",
            "subject": "",
            "body": ""
        }
        
        # Extract analysis section
        analysis_match = re.search(r'<outreach_analysis>(.*?)</outreach_analysis>', output, re.DOTALL)
        if analysis_match:
            result["analysis"] = analysis_match.group(1).strip()
        
        # Extract email section
        email_match = re.search(r'<email>(.*?)</email>', output, re.DOTALL)
        if email_match:
            email_content = email_match.group(1).strip()
            result["email"] = email_content
            
            # Extract subject line
            subject_match = re.search(r'Subject:\s*(.+?)(?:\n|$)', email_content)
            if subject_match:
                result["subject"] = subject_match.group(1).strip()
            
            # Extract body (everything after subject line)
            body_match = re.search(r'Subject:.*?\n\n(.+)', email_content, re.DOTALL)
            if body_match:
                result["body"] = body_match.group(1).strip()
        
        return result
        
    def generate_email(self, data: Dict, model: Optional[str] = None, include_analysis: bool = False, custom_prompt: Optional[str] = None) -> str:
        """Generate a personalized email with comprehensive analysis."""
        try:
            # Validate input data
            self.validate_data(data)
            
            # Log the generation request
            logger.info(f"Generating enhanced email for {data['firstName']} {data['lastName']} at {data['companyName']}")
            
            # Use custom prompt if provided, otherwise use template
            if custom_prompt:
                # Custom prompt replaces both system and user messages
                messages = [
                    {"role": "system", "content": "You are an expert at writing personalized outreach emails. Follow the style instructions EXACTLY. Do not deviate from the format, tone, or structure specified."},
                    {"role": "user", "content": custom_prompt + "\n\nIMPORTANT: Generate ONLY the email content, no analysis or explanation. Follow the style format exactly."}
                ]
            else:
                # Render the standard user prompt
                user_prompt = self.user_template.render(**data)
                
                # Create messages
                messages = [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
            ]
            
            # Generate email with analysis
            response = self.model_manager.create_completion(messages, model=model)
            
            output = response.choices[0].message.content
            
            # Extract structured content
            extracted = self.extract_email_from_output(output)
            
            # Save output if configured
            if self.model_manager.config.get("output", {}).get("save_to_file", True):
                self._save_output(data, extracted)
                
            logger.success(f"Enhanced email generated successfully for {data['firstName']} {data['lastName']}")
            
            # Return either full output or just email based on preference
            if include_analysis:
                return output
            else:
                return extracted["email"] if extracted["email"] else output
            
        except Exception as e:
            logger.error(f"Error generating enhanced email: {str(e)}")
            raise
            
    def _save_output(self, data: Dict, extracted: Dict) -> None:
        """Save generated email and analysis to files."""
        output_dir = self.model_manager.config.get("output", {}).get("output_dir", "generated_emails")
        os.makedirs(output_dir, exist_ok=True)
        
        # Save full output
        filename = f"enhanced_{data['firstName']}_{data['lastName']}_{data['companyName']}.txt".replace(" ", "_")
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"FULL OUTPUT:\n{'='*60}\n")
            f.write(extracted["full_output"])
            f.write(f"\n\n{'='*60}\n")
            f.write(f"EXTRACTED EMAIL:\n{'='*60}\n")
            f.write(f"Subject: {extracted['subject']}\n\n")
            f.write(extracted["body"])
            
        # Save analysis separately
        analysis_filename = f"analysis_{data['firstName']}_{data['lastName']}_{data['companyName']}.txt".replace(" ", "_")
        analysis_filepath = os.path.join(output_dir, analysis_filename)
        
        with open(analysis_filepath, "w", encoding="utf-8") as f:
            f.write("OUTREACH ANALYSIS:\n")
            f.write("="*60 + "\n")
            f.write(extracted["analysis"])
            
        logger.debug(f"Enhanced email saved to: {filepath}")
        logger.debug(f"Analysis saved to: {analysis_filepath}")
        
    def generate_batch(self, prospects: list[Dict], model: Optional[str] = None, include_analysis: bool = False) -> list[Dict]:
        """Generate emails for multiple prospects."""
        results = []
        
        for i, prospect in enumerate(prospects, 1):
            logger.info(f"Processing prospect {i}/{len(prospects)}")
            
            try:
                email = self.generate_email(prospect, model=model, include_analysis=include_analysis)
                prospect["generated_email"] = email
                prospect["status"] = "success"
                results.append(prospect)
            except Exception as e:
                logger.error(f"Failed to generate email for {prospect.get('firstName', 'Unknown')}: {str(e)}")
                prospect["generated_email"] = None
                prospect["status"] = "failed"
                prospect["error"] = str(e)
                results.append(prospect)
                
        return results