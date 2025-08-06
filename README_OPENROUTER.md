# SDR Email Generator - OpenRouter Integration Guide

## 🚀 New Features Implemented

### 1. **OpenRouter Support**
- Switch between OpenAI and OpenRouter with a simple config change
- Access to multiple LLMs: Claude 3, GPT-4, Gemini, Llama 3, and more
- Automatic API routing and error handling

### 2. **Configuration System**
- YAML-based configuration (`config.yaml`)
- Easy model switching without code changes
- Customizable temperature, max tokens, and output settings

### 3. **Enhanced CLI**
- Interactive command-line interface
- Built-in setup wizard
- Batch processing support
- Progress bars and colored output

### 4. **Robust Error Handling**
- Comprehensive logging with Loguru
- Graceful error recovery
- Detailed error messages

## 📦 Installation

```bash
# Install new dependencies
source venv/bin/activate
pip install -r requirements.txt
```

## 🔧 Setup

### Option 1: Interactive Setup
```bash
python cli.py setup
```

### Option 2: Manual Setup

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Add your API keys:
```env
# For OpenAI
OPENAI_API_KEY=your_openai_key_here

# For OpenRouter
OPENROUTER_API_KEY=your_openrouter_key_here
```

3. Configure `config.yaml`:
```yaml
model_provider: "openrouter"  # or "openai"

openrouter:
  model: "anthropic/claude-3-sonnet"  # Choose your model
```

## 🎯 Usage Examples

### CLI Commands

1. **List available models:**
```bash
python cli.py list-models
```

2. **Generate single email:**
```bash
python cli.py generate -f John -l Doe -c "Acme Corp" -a "Raised Series B"
```

3. **Generate email sequence:**
```bash
python cli.py sequence -f Jane -l Smith -c "TechCo" -a "Expanding to EMEA" --parse
```

4. **Batch processing from CSV:**
```bash
python cli.py batch -f prospects.csv -o results.csv
```

### Python API

```python
from sdr_generator_v2 import SDRGenerator
from sdr_sequence_generator_v2 import SDRSequenceGenerator

# Single email
generator = SDRGenerator()
email = generator.generate_email(prospect_data)

# Email sequence
seq_generator = SDRSequenceGenerator()
result = seq_generator.generate_and_parse(prospect_data)
```

## 🤖 Available Models

### OpenRouter Models:
- `anthropic/claude-3-opus` - Most capable Claude model
- `anthropic/claude-3-sonnet` - Balanced performance (recommended)
- `anthropic/claude-3-haiku` - Fast and efficient
- `openai/gpt-4-turbo` - Latest GPT-4
- `google/gemini-pro` - Google's Gemini
- `meta-llama/llama-3-70b-instruct` - Open source alternative

### OpenAI Models:
- `gpt-4-turbo-preview` - Latest GPT-4
- `gpt-4` - Standard GPT-4
- `gpt-3.5-turbo` - Fast and cost-effective

## 📊 Configuration Options

Edit `config.yaml` to customize:

```yaml
# Model settings
model_provider: "openrouter"
openrouter:
  model: "anthropic/claude-3-sonnet"
  temperature: 0.7  # 0-1, higher = more creative
  max_tokens: 2000

# Email settings
email:
  tone: "professional"  # professional, casual, provocative
  length: "medium"      # short, medium, long
  
# Output settings
output:
  format: "text"        # text, html, json
  save_to_file: true
  output_dir: "generated_emails"
```

## 🧪 Testing

Run the test suite:
```bash
python test_openrouter.py
```

This will:
- Test both OpenAI and OpenRouter (if keys are available)
- Generate sample emails and sequences
- Save outputs to `test_outputs/`

## 📝 Logs

Logs are automatically saved to:
- Default: `email_generator.log`
- Configurable in `config.yaml`

## 🔑 Getting API Keys

### OpenRouter
1. Sign up at https://openrouter.ai
2. Get your API key from https://openrouter.ai/keys
3. Add to `.env`: `OPENROUTER_API_KEY=your_key`

### OpenAI
1. Sign up at https://platform.openai.com
2. Get your API key from https://platform.openai.com/api-keys
3. Add to `.env`: `OPENAI_API_KEY=your_key`

## 🎉 Next Steps

1. **HubSpot Integration**: Use the existing `hubspot_integration.py` with the new generators
2. **A/B Testing**: Generate multiple variations by changing models or temperature
3. **Custom Prompts**: Add new prompt templates in the `prompts/` directory
4. **Analytics**: Track performance across different models

## 🐛 Troubleshooting

1. **"API key not found"**: Check your `.env` file
2. **"Model not found"**: Verify model name in `config.yaml`
3. **Rate limits**: OpenRouter handles rate limiting automatically
4. **Logs**: Check `email_generator.log` for detailed errors

Happy email generating! 🚀