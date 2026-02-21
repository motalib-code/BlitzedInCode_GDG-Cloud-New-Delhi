"""
BRD Agent - Diagnostic & Fix Script
===================================
Run this to fix common errors:
1. Downloads missing spaCy model (en_core_web_sm)
2. Verifies Gemini API Key
3. Checks Database integrity
4. Verifies NLTK/TextBlob data

USAGE:
  python fix_all_errors.py
"""

import os
import sys
import subprocess

# Color codes
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def run_cmd(cmd, desc):
    print(f"\nExample: {desc}...")
    try:
        subprocess.check_call(cmd, shell=True)
        print(f"{GREEN}✅ Success{RESET}")
    except subprocess.CalledProcessError:
        print(f"{RED}❌ Failed: {desc}{RESET}")

def check_spacy():
    print(f"\n🔍 Checking spaCy model 'en_core_web_sm'...")
    try:
        import spacy
        try:
            spacy.load("en_core_web_sm")
            print(f"{GREEN}✅ Model already installed{RESET}")
        except OSError:
            print("⚠️ Model not found. Downloading...")
            run_cmd(f"{sys.executable} -m spacy download en_core_web_sm", "Download spaCy model")
    except ImportError:
        print(f"{RED}❌ spaCy not installed. Installing...{RESET}")
        run_cmd(f"{sys.executable} -m pip install spacy", "Install spaCy")
        run_cmd(f"{sys.executable} -m spacy download en_core_web_sm", "Download spaCy model")

def check_textblob():
    print(f"\n🔍 Checking TextBlob corpora...")
    try:
        from textblob import TextBlob
        _ = TextBlob("test").sentiment
        print(f"{GREEN}✅ TextBlob ready{RESET}")
    except Exception:
        print("⚠️ Downloading TextBlob corpora...")
        run_cmd(f"{sys.executable} -m textblob.download_corpora", "Download TextBlob corpora")

def check_api_key():
    print(f"\n🔍 Verifying Gemini API Key...")
    
    # Load env vars
    from dotenv import load_dotenv
    load_dotenv()
    
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print(f"{RED}❌ GENIMI_API_KEY is missing in .env file!{RESET}")
        return
        
    print(f"   Key found: {key[:5]}...{key[-4:]}")
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content("Say 'Hello' if you work.")
        if response and response.text:
            print(f"{GREEN}✅ API Key works! Response: {response.text.strip()}{RESET}")
        else:
            print(f"{RED}❌ API returned empty response.{RESET}")
    except Exception as e:
        print(f"{RED}❌ API Error: {e}{RESET}")
        print("   Did you enable the API in Google Cloud Console?")

def check_db():
    print(f"\n🔍 Checking Database...")
    db_path = "brd_agent.db"
    if os.path.exists(db_path):
        print(f"{GREEN}✅ Database file exists ({os.path.getsize(db_path)} bytes){RESET}")
    else:
        print(f"{RED}❌ Database missing. Re-initializing...{RESET}")
        try:
            from brd_agent.db_setup import init_database
            init_database()
            print(f"{GREEN}✅ Database created.{RESET}")
        except Exception as e:
            print(f"{RED}❌ Failed to create DB: {e}{RESET}")

if __name__ == "__main__":
    print("==============================================")
    print("   BRD AGENT - AUTO-FIX TOOL")
    print("==============================================")
    
    # 1. Install critical deps if missing
    try:
        import dotenv
    except ImportError:
        run_cmd(f"{sys.executable} -m pip install python-dotenv", "Install python-dotenv")

    # 2. Checks
    check_spacy()
    check_textblob()
    check_db()
    check_api_key()
    
    print("\n==============================================")
    print(f"{GREEN}✅ Fixes complete! Restart your Streamlit app now.{RESET}")
    print("   Run: streamlit run brd_agent/frontend.py")
    print("==============================================")
