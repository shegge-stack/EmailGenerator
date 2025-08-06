from setuptools import setup, find_packages
import os

setup(
    name="sdr_email_generator",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "openai>=0.27.0",
        "requests>=2.28.0",
        "jinja2>=3.1.0",
        "python-dotenv>=1.0.0",
        "pandas>=1.5.0",
        "retrying>=1.3.3",
        "pyyaml>=6.0.0",
        "click>=8.1.0",
        "colorama>=0.4.6",
        "loguru>=0.7.0",
    ],
    entry_points={
        "console_scripts": [
            "sdr-gen=cli:cli",
            "sdr-batch=batch_generate_v2:main",
        ],
    },
    python_requires=">=3.8",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered SDR email generator with OpenRouter support",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sdr-email-generator",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)