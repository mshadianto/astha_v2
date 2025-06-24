# ===== run_app.py =====
"""
Quick launcher for ASTHA application
"""
import subprocess
import sys
import os

def main():
    """Launch the Streamlit app"""
    # Check if main.py exists
    if not os.path.exists("app/main.py"):
        print("❌ app/main.py not found!")
        print("Please make sure you have the complete ASTHA application files.")
        return
    
    # Check if streamlit is installed
    try:
        import streamlit
    except ImportError:
        print("❌ Streamlit not installed!")
        print("Run: pip install streamlit")
        return
    
    print("🚀 Launching ASTHA - Hajj Treasury Analytics...")
    print("🌐 App will open at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the application")
    print("=" * 50)
    
    # Launch Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "app/main.py",
            "--server.port=8501",
            "--server.headless=false"
        ])
    except KeyboardInterrupt:
        print("\n👋 ASTHA application stopped.")
    except Exception as e:
        print(f"❌ Error launching app: {e}")

if __name__ == "__main__":
    main()

