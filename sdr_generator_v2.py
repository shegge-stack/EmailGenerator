"""
Enhanced SDR Generator with OpenRouter support and better error handling
"""
import os
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from loguru import logger
from model_manager import ModelManager
from typing import Dict, Optional
import json

load_dotenv()

class SDRGenerator:
    def __init__(self, api_key: Optional[str] = None, config_path: str = "config.yaml"):
        """Initialize the SDR Generator with model manager."""
        self.model_manager = ModelManager(config_path)
        self.env = Environment(loader=FileSystemLoader("prompts"))
        
        # Load system prompt
        try:
            with open("prompts/sdr_static_instructions.txt", "r") as f:
                self.system_prompt = f.read()
        except FileNotFoundError:
            logger.error("System prompt file not found")
            raise
            
        self.user_template = self.env.get_template("sdr_dynamic_prompt.txt")
        
        # Configure logging
        log_config = self.model_manager.config.get("logging", {})
        logger.add(
            log_config.get("file", "email_generator.log"),
            level=log_config.get("level", "INFO"),
            rotation="10 MB"
        )
        
    def validate_data(self, data: Dict) -> bool:
        """Validate required fields in prospect data."""
        required_fields = [
            "caseStudy", "ICP", "companyName", "activity", 
            "companyWebsite", "senderCompany", "ourWebsite", 
            "meetingLink", "senderName", "senderTitle", 
            "firstName", "lastName", "linkedinURL"
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            logger.error(f"Missing required fields: {missing_fields}")
            raise ValueError(f"Missing required fields: {missing_fields}")
            
        return True
        
    def generate_email(self, data: Dict, model: Optional[str] = None) -> str:
        """Generate a personalized email with error handling and logging."""
        try:
            # Validate input data
            self.validate_data(data)
            
            # Log the generation request
            logger.info(f"Generating email for {data['firstName']} {data['lastName']} at {data['companyName']}")
            
            # Render the user prompt
            user_prompt = self.user_template.render(**data)
            
            # Create messages
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            # Generate email
            response = self.model_manager.create_completion(messages, model=model)
            
            email_content = response.choices[0].message.content
            
            # Save output if configured
            if self.model_manager.config.get("output", {}).get("save_to_file", True):
                self._save_output(data, email_content)
                
            logger.success(f"Email generated successfully for {data['firstName']} {data['lastName']}")
            
            return email_content
            
        except Exception as e:
            logger.error(f"Error generating email: {str(e)}")
            raise
            
    def _save_output(self, data: Dict, email_content: str) -> None:
        """Save generated email to file."""
        output_dir = self.model_manager.config.get("output", {}).get("output_dir", "generated_emails")
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{data['firstName']}_{data['lastName']}_{data['companyName']}.txt".replace(" ", "_")
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(email_content)
            
        logger.debug(f"Email saved to: {filepath}")
        
    def generate_batch(self, prospects: list[Dict], model: Optional[str] = None) -> list[Dict]:
        """Generate emails for multiple prospects."""
        results = []
        
        for i, prospect in enumerate(prospects, 1):
            logger.info(f"Processing prospect {i}/{len(prospects)}")
            
            try:
                email = self.generate_email(prospect, model=model)
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