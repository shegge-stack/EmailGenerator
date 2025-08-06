#!/usr/bin/env python3
"""
Startup script for the Powerful 1:1 Email Generator UI
"""

import subprocess
import sys
import os
import webbrowser
import time
from pathlib import Path

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, capture_output=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("Please run manually: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has required keys."""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("⚠️  .env file not found!")
        print("Creating example .env file...")
        
        with open(".env", "w") as f:
            f.write("""# API Keys for Powerful 1:1 Email Generator
OPENAI_API_KEY=your_openai_api_key_here
# OPENROUTER_API_KEY=your_openrouter_api_key_here

# Postmark for email sending (THE MOST POWERFUL feature)
POSTMARK_API_KEY=your_postmark_api_key_here
FROM_EMAIL=your@company.com

# Optional: Third-party enrichment
# APOLLO_API_KEY=your_apollo_api_key_here

# Your site URL
YOUR_SITE_URL=http://localhost:5000
""")
        print("📝 .env file created. Please add your API keys!")
        return False
    
    # Check for required keys
    with open(".env", "r") as f:
        env_content = f.read()
        
    has_openai = "OPENAI_API_KEY=" in env_content and "your_openai_api_key_here" not in env_content
    has_openrouter = "OPENROUTER_API_KEY=" in env_content and "your_openrouter_api_key_here" not in env_content
    
    if not has_openai and not has_openrouter:
        print("⚠️  No valid API keys found in .env file!")
        print("Please add either OPENAI_API_KEY or OPENROUTER_API_KEY to your .env file")
        return False
        
    print("✅ API keys configured!")
    return True

def start_server():
    """Start the Flask server."""
    print("🚀 Starting Email Generator UI Server...")
    print("=" * 50)
    
    try:
        # Start the server
        from api_server import app
        
        # Open browser after short delay
        def open_browser():
            time.sleep(2)
            webbrowser.open('http://localhost:5000')
            
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        print("🌐 Opening browser at http://localhost:5000")
        print("📧 Ready to generate powerful 1:1 emails!")
        print("=" * 50)
        
        app.run(debug=False, port=5000, host='0.0.0.0')
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install dependencies: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Server error: {e}")

def main():
    """Main startup function."""
    print("🎯 Powerful 1:1 Email Generator")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return
        
    # Install dependencies if needed
    try:
        import flask
        import flask_cors
        print("✅ Dependencies already installed")
    except ImportError:
        if not install_dependencies():
            return
    
    # Check environment setup
    if not check_env_file():
        print("\n🔧 Setup required:")
        print("1. Add your API keys to the .env file")
        print("2. Run this script again")
        return
    
    print("\n🎉 Everything looks good!")
    print("Starting the Email Generator UI...")
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()