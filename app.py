# ===== setup.py =====
"""
ASTHA Setup Script
Run this to set up the application environment
"""

import os
import subprocess
import sys

def create_directory_structure():
    """Create the required directory structure"""
    directories = [
        "app",
        "app/pages",
        "app/components", 
        "app/utils",
        "app/services",
        "app/agents",
        "config",
        "data/raw",
        "data/processed",
        "data/external",
        "data/exports",
        "logs",
        "tests"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def create_sample_data():
    """Create sample CSV data file"""
    csv_content = """Tahun,BPIH,Bipih,NilaiManfaat
2022,85452883,39886009,45566874
2023,89629474,49812700,39816774
2024,94482028,56046172,38435856
2025,91493896,60559399,30934497"""
    
    with open("data/raw/biaya_haji_historis.csv", "w") as f:
        f.write(csv_content)
    print("✅ Created sample data file: data/raw/biaya_haji_historis.csv")

def create_env_file():
    """Create .env file from template"""
    env_content = """# ASTHA Environment Configuration
APP_NAME=ASTHA - Hajj Treasury Analytics
APP_VERSION=1.0.0
DEBUG=True

# Free API Keys (Replace with your keys)
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
EXCHANGE_RATE_API_KEY=your_exchange_rate_key_here
FRED_API_KEY=your_fred_api_key_here
OPENAI_API_KEY=your_openai_key_here

# Cache Settings
CACHE_TTL=3600

# Logging
LOG_LEVEL=INFO
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    print("✅ Created .env file")

def install_requirements():
    """Install Python requirements"""
    requirements = [
        "streamlit==1.28.1",
        "pandas==2.1.3", 
        "numpy==1.24.4",
        "plotly==5.17.0",
        "requests==2.31.0",
        "python-dotenv==1.0.0",
        "scikit-learn==1.3.2",
        "openpyxl==3.1.2"
    ]
    
    for requirement in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", requirement])
            print(f"✅ Installed: {requirement}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {requirement}: {e}")

def main():
    """Main setup function"""
    print("🚀 Setting up ASTHA - Hajj Treasury Analytics")
    print("=" * 50)
    
    create_directory_structure()
    create_sample_data()
    create_env_file()
    
    print("\n📦 Installing Python packages...")
    install_requirements()
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your API keys")
    print("2. Run: streamlit run app/main.py")
    print("3. Open browser at: http://localhost:8501")
    print("\n🎯 Happy analyzing!")

if __name__ == "__main__":
    main()
