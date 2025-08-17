#!/usr/bin/env python3
"""
Docker setup script for Open WebUI
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
                f.write("OPENAI_API_KEY=your_actual_openai_api_key_here\n\n")
                f.write("# Open WebUI Configuration\n")
                f.write("WEBUI_SECRET_KEY=your_secret_key_for_webui_access\n\n")
                f.write("# Monitoring Configuration\n")
                f.write("GRAFANA_PASSWORD=admin\n\n")
                f.write("# MLflow Configuration\n")
                f.write("MLFLOW_TRACKING_URI=http://localhost:5000\n")
                f.write("MINIO_ACCESS_KEY=minioadmin\n")
                f.write("MINIO_SECRET_KEY=minioadmin\n\n")
                f.write("# Optional: Customize these if needed\n")
                f.write("# DEFAULT_USER_ROLE=admin\n")
                f.write("# DEFAULT_MODELS=gpt-4o-mini,gpt-4o,gpt-4-turbo,gpt-3.5-turbo\n")
                f.write("# DEFAULT_MODEL=gpt-4o-mini\n")
            print("✅ .env file created successfully")
            print("⚠️  Please edit .env and add your actual OpenAI API key")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("✅ .env file already exists")
        return True

def check_docker():
    """Check if Docker is running"""
    print("🔍 Checking Docker status...")
    try:
        result = subprocess.run("docker info", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker is running")
            return True
        else:
            print("❌ Docker is not running")
            return False
    except Exception as e:
        print(f"❌ Docker check failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Open WebUI Docker Setup")
    print("=" * 40)
    
    # Check Docker
    if not check_docker():
        print("\n❌ Please start Docker Desktop first!")
        print("1. Open Docker Desktop application")
        print("2. Wait for it to start (green light)")
        print("3. Run this script again")
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        print("❌ Setup failed. Please check the error messages above.")
        sys.exit(1)
    
    print("\n🎉 Docker setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Run: docker-compose up -d")
    print("3. Open http://localhost:8080 in your browser")
    print("\n💡 For help, see the README.md")

if __name__ == "__main__":
    main()
