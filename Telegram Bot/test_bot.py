#!/usr/bin/env python3
"""
Test script to verify bot configuration and connectivity
"""

import os
import asyncio
from dotenv import load_dotenv
from bot.notifier import Notifier
from infra.logging import setup_logging

logger = setup_logging()

def test_env_variables():
    """Test if all required environment variables are set"""
    print("🔍 Testing environment variables...")
    
    required_vars = [
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID", 
        "PINCODE",
        "SEARCH_TERMS"
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            print(f"✅ {var}: {'*' * len(value)} (length: {len(value)})")
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        return False
    
    print("✅ All required environment variables are set")
    return True

async def test_telegram_connection():
    """Test Telegram bot connection"""
    print("\n🤖 Testing Telegram bot connection...")
    
    try:
        notifier = Notifier()
        await notifier.send("🧪 <b>Bot Test Message</b>\nThis is a test message to verify the bot is working correctly.")
        print("✅ Telegram bot connection successful")
        return True
    except Exception as e:
        print(f"❌ Telegram bot connection failed: {e}")
        return False

def test_store_configuration():
    """Test store API configuration"""
    print("\n🏪 Testing store configuration...")
    
    stores = [
        ("Blinkit", "BLINKIT_API_URL"),
        ("Swiggy", "SWIGGY_API_URL"), 
        ("Zepto", "ZEPTO_API_URL"),
        ("JioMart", "JIOMART_API_URL"),
        ("BigBasket", "BIGBASKET_API_URL")
    ]
    
    configured_stores = 0
    for store_name, url_var in stores:
        url = os.getenv(url_var)
        if url:
            print(f"✅ {store_name}: Configured")
            configured_stores += 1
        else:
            print(f"⚠️  {store_name}: Not configured (will use browser mode)")
    
    print(f"📊 Total stores configured: {configured_stores}/{len(stores)}")
    return configured_stores > 0

def main():
    """Run all tests"""
    print("🚀 Starting bot configuration tests...\n")
    
    # Load environment variables
    load_dotenv()
    
    # Run tests
    env_ok = test_env_variables()
    store_ok = test_store_configuration()
    
    # Test Telegram connection
    if env_ok:
        telegram_ok = asyncio.run(test_telegram_connection())
    else:
        telegram_ok = False
    
    # Summary
    print("\n" + "="*50)
    print("📋 TEST SUMMARY")
    print("="*50)
    print(f"Environment Variables: {'✅ PASS' if env_ok else '❌ FAIL'}")
    print(f"Store Configuration: {'✅ PASS' if store_ok else '⚠️  PARTIAL'}")
    print(f"Telegram Connection: {'✅ PASS' if telegram_ok else '❌ FAIL'}")
    
    if env_ok and telegram_ok:
        print("\n🎉 All critical tests passed! Your bot should work correctly.")
        print("💡 Run 'python run.py' to start the bot.")
    else:
        print("\n⚠️  Some tests failed. Please check your configuration.")
        if not env_ok:
            print("   - Check your .env file and required variables")
        if not telegram_ok:
            print("   - Verify your Telegram bot token and chat ID")
        if not store_ok:
            print("   - Consider configuring store API endpoints for better performance")

if __name__ == "__main__":
    main() 