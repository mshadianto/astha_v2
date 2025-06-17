import subprocess
import sys
import os

def main():
    print("🚀 Launching ASTHA - Hajj Treasury Analytics...")
    print("🌐 App will open at: http://localhost:8501")
    print("=" * 50)
    
    if not os.path.exists("app/main.py"):
        print("❌ app/main.py not found!")
        return
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "app/main.py",
            "--server.port=8501"
        ])
    except KeyboardInterrupt:
        print("\n👋 ASTHA application stopped.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()