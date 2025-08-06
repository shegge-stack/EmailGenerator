import os
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from openai import OpenAI

load_dotenv()

class SDRSequenceGenerator:
    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.env = Environment(loader=FileSystemLoader("prompts"))
        with open("prompts/sdr_sequence_instructions.txt", "r") as f:
            self.system_prompt = f.read()
        self.user_template = self.env.get_template("sdr_dynamic_prompt.txt")

    def generate_sequence(self, data: dict, model="gpt-4-turbo-preview"):
        """Generate a 4–5 step outbound email sequence."""
        user_prompt = self.user_template.render(**data)
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content
