import os

def create_directory_structure():
    """Create the required directory structure"""
    directories = [
        "app",
        "data",
        "logs"
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
    
    os.makedirs("data", exist_ok=True)
    with open("data/biaya_haji_historis.csv", "w") as f:
        f.write(csv_content)
    print("✅ Created sample data file: data/biaya_haji_historis.csv")

def main():
    """Main setup function"""
    print("🚀 Setting up ASTHA - Hajj Treasury Analytics")
    print("=" * 50)
    
    create_directory_structure()
    create_sample_data()
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Install requirements: pip install -r requirements.txt")
    print("2. Run application: python run_app.py")
    print("3. Open browser at: http://localhost:8501")
    print("\n🎯 Happy analyzing!")

if __name__ == "__main__":
    main()
