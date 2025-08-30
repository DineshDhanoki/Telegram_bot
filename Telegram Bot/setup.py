#!/usr/bin/env python3
"""
Setup script for Telegram Stock Availability Bot
"""

import os
import sys
import subprocess
import shutil

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install Python dependencies"""
    return run_command("pip install -r requirements.txt", "Installing Python dependencies")

def install_playwright():
    """Install Playwright browsers"""
    return run_command("playwright install", "Installing Playwright browsers")

def create_env_file():
    """Create .env file from template"""
    print("📝 Creating .env file...")
    
    if os.path.exists(".env"):
        print("⚠️  .env file already exists, skipping creation")
        return True
    
    if os.path.exists("env_template.txt"):
        shutil.copy("env_template.txt", ".env")
        print("✅ .env file created from template")
        print("📝 Please edit .env file with your configuration")
        return True
    else:
        print("❌ env_template.txt not found")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Telegram Stock Availability Bot")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Install Playwright
    if not install_playwright():
        print("⚠️  Failed to install Playwright browsers")
        print("   Browser mode may not work correctly")
    
    # Create .env file
    if not create_env_file():
        print("❌ Failed to create .env file")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit the .env file with your configuration:")
    print("   - TELEGRAM_BOT_TOKEN: Get from @BotFather")
    print("   - TELEGRAM_CHAT_ID: Your chat ID")
    print("   - PINCODE: Your delivery pincode")
    print("   - SEARCH_TERMS: Products to monitor")
    print("\n2. Test your configuration:")
    print("   python test_bot.py")
    print("\n3. Start the bot:")
    print("   python run.py")
    print("\n4. Or use the CLI:")
    print("   python bot_cli.py test")
    print("   python bot_cli.py start")
    
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main() 