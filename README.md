# product-agent
AI-powered Product Data Extraction Agent

## Overview
This project provides an AI agent that extracts structured product data from websites using LLMs (Gemini, OpenAI, Ollama, Groq) and saves the results as CSV files.

## Usage
```bash
python scrape_products.py <URL1>,<URL2>,...
```

Example:
```bash
python scrape_products.py https://www.example.com/products,https://www.example2.com/items
```

## Features
- Fetches and parses HTML content from provided URLs
- Uses AI models to extract structured product/event data
- Saves results as timestamped CSV files in the `files/` directory
- Supports multiple URLs in a single command (comma-separated)

## Dependencies
- beautifulsoup4: HTML parsing
- pandas: Data manipulation and CSV export
- pydantic-ai: AI agent framework
- python-dotenv: Environment variable management
