"""
BRD Agent - One-Click Setup Script
===================================
Run this script to set up the entire environment for the BRD Agent.

WHAT IT DOES:
  1. Checks Python version
  2. Installs dependencies from requirements_brd.txt
  3. Creates .env file if missing
  4. Initializes the SQLite database
  5. Loads sample data for testing
  6. Prints run instructions

USAGE:
  python brd_agent_setup.py
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Color codes for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

APP_DIR = Path(__file__).parent.resolve()
REQUIREMENTS_FILE = APP_DIR / "requirements_brd.txt"
ENV_TEMPLATE = APP_DIR / ".env.template"
ENV_FILE = APP_DIR / ".env"

def print_step(message):
    print(f"\n{GREEN}=== {message} ==={RESET}")

def check_python():
    print_step("Checking Python Version")
    version = sys.version_info
    print(f"Current Python: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"{RED}⚠️  Warning: Python 3.10+ is recommended.{RESET}")
    else:
        print("✅ Python version looks good.")

def install_dependencies():
    print_step("Installing Dependencies")
    if not REQUIREMENTS_FILE.exists():
        print(f"{RED}❌ requirements_brd.txt not found!{RESET}")
        return
    
    print("Installing packages from requirements_brd.txt...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)])
        print("✅ Dependencies installed.")
    except subprocess.CalledProcessError as e:
        print(f"{RED}❌ Error installing dependencies: {e}{RESET}")

def setup_env():
    print_step("Setting up Environment Config")
    if ENV_FILE.exists():
        print("✅ .env file already exists.")
    else:
        if ENV_TEMPLATE.exists():
            shutil.copy(ENV_TEMPLATE, ENV_FILE)
            print(f"✅ Created .env file from template.")
            print(f"{YELLOW}⚠️  IMPORTANT: Open .env and add your API keys (Gemini/OpenAI)!{RESET}")
        else:
            print(f"{RED}❌ .env.template not found!{RESET}")

def init_database_and_data():
    print_step("Initializing Database & Sample Data")
    
    # Add current dict to path to import brd_agent modules
    sys.path.insert(0, str(APP_DIR))
    
    try:
        from brd_agent.db_setup import init_database
        from brd_agent.data_ingest import load_sample_data
        
        print("Creating database tables...")
        init_database()
        
        print("Loading sample data (simulated Enron/AMI/Chat)...")
        load_sample_data()
        
        print("✅ Database ready with sample data.")
    except ImportError as e:
        print(f"{RED}❌ Error importing modules. Did dependencies install correctly?{RESET}")
        print(f"Error: {e}")
    except Exception as e:
        print(f"{RED}❌ Error initializing database: {e}{RESET}")

def main():
    print(f"""
{GREEN}==============================================
   BRD AGENT - HACKATHON SETUP WIZARD
=============================================={RESET}
    """)
    
    check_python()
    
    # Ask to install dependencies
    response = input(f"\nInstall dependencies now? (y/n) [y]: ").strip().lower()
    if response in ('', 'y', 'yes'):
        install_dependencies()
    
    setup_env()
    
    # database setup
    response = input(f"\nInitialize database with sample data? (y/n) [y]: ").strip().lower()
    if response in ('', 'y', 'yes'):
        init_database_and_data()
        
    print_step("Setup Complete!")
    print(f"""
To run the application:

{YELLOW}1. Streamlit UI (Recommended for Demo):{RESET}
   streamlit run brd_agent/frontend.py

{YELLOW}2. Flask API Backend:{RESET}
   python -m brd_agent.api

{YELLOW}⚠️  Don't forget to set your GEMINI_API_KEY in the .env file!{RESET}
    """)

if __name__ == "__main__":
    main()
