# SDR Email Generator 🚀

An AI-powered Sales Development Representative (SDR) email generator that creates personalized outreach emails and sequences. Supports multiple AI providers including OpenAI and OpenRouter, with advanced personalization features.

## Features ✨

- **Multi-Model Support**: Use OpenAI GPT models or access Claude, Gemini, and others via OpenRouter
- **Three Generation Modes**:
  - Standard: Quick, professional emails
  - Enhanced: Comprehensive outreach analysis with detailed personalization
  - Sequences: 4-5 email campaigns with varied approaches
- **Flexible Integration**: CLI, Python API, and batch processing
- **HubSpot Ready**: Built-in integration for syncing sequences
- **Smart Personalization**: Uses company activity, industry, and LinkedIn data
- **Professional CLI**: Interactive interface with progress tracking

## Quick Start 🏃‍♂️

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/sdr-email-generator.git
cd sdr-email-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Setup

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Add your API keys to `.env`:
```env
# For OpenAI
OPENAI_API_KEY=your_openai_key_here

# For OpenRouter (optional)
OPENROUTER_API_KEY=your_openrouter_key_here

# For HubSpot integration (optional)
HUBSPOT_PRIVATE_APP_TOKEN=your_hubspot_token_here
```

3. Run the interactive setup:
```bash
python cli.py setup
```

## Usage Examples 📧

### Command Line Interface

**Generate a single email:**
```bash
python cli.py generate -f John -l Doe -c "Acme Corp" -a "Raised $50M Series B"
```

**Use the enhanced generator with analysis:**
```bash
python cli.py generate -f Jane -l Smith -c "TechCo" -a "Expanding to Europe" \
  -i "SaaS" -t "VP Sales" --enhanced --include-analysis
```

**Generate an email sequence:**
```bash
python cli.py sequence -f Sarah -l Johnson -c "StartupXYZ" -a "Launched new product"
```

**Batch process from CSV:**
```bash
python cli.py batch -f prospects.csv -o results.csv --enhanced
```

### Python API

```python
from sdr_generator_enhanced import EnhancedSDRGenerator

# Initialize generator
generator = EnhancedSDRGenerator()

# Prepare prospect data
prospect = {
    "firstName": "Michael",
    "lastName": "Chen",
    "companyName": "TechVentures Inc",
    "activity": "Announced expansion into Asian markets",
    "industry": "Sales Technology",
    "title": "VP of Sales",
    # ... other required fields
}

# Generate email
email = generator.generate_email(prospect, include_analysis=True)
print(email)
```

## Configuration 🔧

Edit `config.yaml` to customize settings:

```yaml
# Choose your AI provider
model_provider: "openrouter"  # or "openai"

# Model settings
openrouter:
  model: "anthropic/claude-3-sonnet"
  temperature: 0.7
  
# Email settings  
email:
  tone: "professional"  # professional, casual, provocative
  length: "medium"      # short, medium, long
```

## CSV Format 📊

For batch processing, use a CSV with these columns:

**Required fields:**
- firstName, lastName
- companyName, companyWebsite
- activity (recent company activity)
- linkedinURL
- caseStudy (your company's success story)
- ICP (Ideal Customer Profile)
- senderName, senderTitle, senderCompany
- ourWebsite, meetingLink

**Optional enhanced fields:**
- industry
- title (prospect's job title)

See `example_prospects.csv` for a template.

## Project Structure 📁

```
sdr-email-generator/
├── cli.py                      # Main CLI interface
├── sdr_generator_v2.py         # Standard email generator
├── sdr_generator_enhanced.py   # Enhanced generator with analysis
├── sdr_sequence_generator_v2.py # Email sequence generator
├── model_manager.py            # AI provider management
├── hubspot_integration.py      # HubSpot API integration
├── batch_generate_v2.py        # Batch processing script
├── config.yaml                 # Configuration file
├── prompts/                    # Email templates
│   ├── sdr_static_instructions.txt
│   ├── sdr_dynamic_prompt.txt
│   ├── enhanced_static_instructions.txt
│   └── enhanced_dynamic_prompt.txt
└── archive/                    # Legacy versions (for reference)
```

## AI Models 🤖

### OpenAI Models
- gpt-4-turbo-preview
- gpt-4
- gpt-3.5-turbo

### OpenRouter Models
- anthropic/claude-3-opus
- anthropic/claude-3-sonnet
- google/gemini-pro
- meta-llama/llama-3-70b-instruct

## Advanced Features 🛠️

### Enhanced Email Generation
The enhanced generator provides:
- Detailed outreach analysis
- 11-point personalization strategy
- Problem/solution mapping
- Objection handling
- Multiple opening line options

### HubSpot Integration
```python
from hubspot_integration import create_sequence, enroll_contact

# Create a sequence in HubSpot
sequence_id = create_sequence("Q1 Outreach", email_list)

# Enroll contacts
enroll_contact(contact_id, sequence_id)
```

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support 💬

- **Issues**: [GitHub Issues](https://github.com/yourusername/sdr-email-generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/sdr-email-generator/discussions)

## Acknowledgments 🙏

- Built with OpenAI and OpenRouter APIs
- Inspired by modern sales development best practices
- Enhanced prompt engineering for better personalization

---

**Note**: Remember to never commit your `.env` file or API keys to version control!