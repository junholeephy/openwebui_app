# Installation Guide

## Quick Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your OpenAI API key:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

3. **Run the application:**
   ```bash
   python run.py
   # OR
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Open your browser:**
   Navigate to http://localhost:8000

## Requirements
- Python 3.8+
- OpenAI API key
- Internet connection

## Troubleshooting
- If you get import errors, make sure you've installed the requirements
- Check that your OpenAI API key is set correctly
- Ensure port 8000 is available
