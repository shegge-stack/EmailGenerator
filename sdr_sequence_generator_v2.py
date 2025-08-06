"""
Enhanced SDR Sequence Generator with OpenRouter support
"""
import os
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from loguru import logger
from model_manager import ModelManager
from typing import Dict, Optional, List
import re

load_dotenv()

class SDRSequenceGenerator:
    def __init__(self, api_key: Optional[str] = None, config_path: str = "config.yaml"):
        """Initialize the SDR Sequence Generator with model manager."""
        self.model_manager = ModelManager(config_path)
        self.env = Environment(loader=FileSystemLoader("prompts"))
        
        # Load system prompt
        try:
            with open("prompts/sdr_sequence_instructions.txt", "r") as f:
                self.system_prompt = f.read()
        except FileNotFoundError:
            logger.error("Sequence instructions file not found")
            raise
            
        self.user_template = self.env.get_template("sdr_dynamic_prompt.txt")
        
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
        
    def generate_sequence(self, data: Dict, model: Optional[str] = None) -> str:
        """Generate a 4-5 step outbound email sequence."""
        try:
            # Validate input data
            self.validate_data(data)
            
            logger.info(f"Generating sequence for {data['firstName']} {data['lastName']} at {data['companyName']}")
            
            # Render the user prompt
            user_prompt = self.user_template.render(**data)
            
            # Create messages
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            # Generate sequence
            response = self.model_manager.create_completion(messages, model=model)
            
            sequence_content = response.choices[0].message.content
            
            # Save output if configured
            if self.model_manager.config.get("output", {}).get("save_to_file", True):
                self._save_output(data, sequence_content)
                
            logger.success(f"Sequence generated successfully for {data['firstName']} {data['lastName']}")
            
            return sequence_content
            
        except Exception as e:
            logger.error(f"Error generating sequence: {str(e)}")
            raise
            
    def parse_sequence(self, sequence_content: str) -> List[Dict[str, str]]:
        """Parse the generated sequence into individual emails."""
        emails = []
        
        # Extract emails using regex
        pattern = r'<email step="(\d+)">\s*Subject:\s*(.+?)\s*Body:\s*(.*?)\s*</email>'
        matches = re.findall(pattern, sequence_content, re.DOTALL)
        
        for match in matches:
            step, subject, body = match
            emails.append({
                "step": int(step),
                "subject": subject.strip(),
                "body": body.strip()
            })
            
        logger.info(f"Parsed {len(emails)} emails from sequence")
        return emails
        
    def _save_output(self, data: Dict, sequence_content: str) -> None:
        """Save generated sequence to file."""
        output_dir = self.model_manager.config.get("output", {}).get("output_dir", "generated_emails")
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"sequence_{data['firstName']}_{data['lastName']}_{data['companyName']}.txt".replace(" ", "_")
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(sequence_content)
            
        logger.debug(f"Sequence saved to: {filepath}")
        
    def generate_and_parse(self, data: Dict, model: Optional[str] = None) -> Dict:
        """Generate sequence and return parsed emails."""
        try:
            # Generate the sequence
            sequence_content = self.generate_sequence(data, model)
            
            # Parse into individual emails
            emails = self.parse_sequence(sequence_content)
            
            return {
                "prospect": data,
                "raw_sequence": sequence_content,
                "emails": emails,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error in generate_and_parse: {str(e)}")
            return {
                "prospect": data,
                "raw_sequence": None,
                "emails": [],
                "status": "failed",
                "error": str(e)
            }