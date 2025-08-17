#!/usr/bin/env python3
"""
Setup script for OpenWebUI FastAPI application
"""
import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = ".env"
    if not os.path.exists(env_file):
        print("📝 Creating .env file...")
        try:
            with open(env_file, "w") as f:
                f.write("# OpenAI API Configuration\n")
                f.write("OPENAI_API_KEY=your_openai_api_key_here\n\n")
                f.write("# Server Configuration (optional)\n")
                f.write("HOST=0.0.0.0\n")
                f.write("PORT=8000\n\n")
                f.write("# Logging (optional)\n")
                f.write("LOG_LEVEL=INFO\n")
            print("✅ .env file created successfully")
            print("⚠️  Please edit .env and add your actual OpenAI API key")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("✅ .env file already exists")
        return True

def main():
    """Main setup function"""
    print("🚀 OpenWebUI FastAPI Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("❌ Setup failed. Please check the error messages above.")
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        print("❌ Setup failed. Please check the error messages above.")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Run: python run.py")
    print("3. Open http://localhost:8000 in your browser")
    print("\n💡 For help, see INSTALL.md")

if __name__ == "__main__":
    main()
