#!/usr/bin/env python3
"""
Command-line interface for the Telegram Stock Availability Bot
"""

import argparse
import asyncio
import os
import sys
from dotenv import load_dotenv
from bot.app import App
from test_bot import test_env_variables, test_telegram_connection, test_store_configuration

def setup_parser():
    """Setup command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Telegram Stock Availability Bot CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python bot_cli.py start          # Start the bot
  python bot_cli.py test           # Test configuration
  python bot_cli.py status         # Show current status
  python bot_cli.py config         # Show current configuration
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Start command
    start_parser = subparsers.add_parser('start', help='Start the bot')
    start_parser.add_argument('--daemon', action='store_true', help='Run in background')
    
    # Test command
    subparsers.add_parser('test', help='Test bot configuration')
    
    # Status command
    subparsers.add_parser('status', help='Show bot status')
    
    # Config command
    subparsers.add_parser('config', help='Show current configuration')
    
    return parser

def show_configuration():
    """Display current configuration"""
    print("🔧 Current Configuration")
    print("=" * 40)
    
    config_vars = [
        ("TELEGRAM_BOT_TOKEN", "Bot Token"),
        ("TELEGRAM_CHAT_ID", "Chat ID"),
        ("PINCODE", "Pincode"),
        ("SEARCH_TERMS", "Search Terms"),
        ("POLL_INTERVAL", "Poll Interval"),
        ("RUN_MODE", "Run Mode")
    ]
    
    for var, desc in config_vars:
        value = os.getenv(var, "Not set")
        if var in ["TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"]:
            value = "*" * len(value) if value != "Not set" else value
        print(f"{desc:15}: {value}")
    
    print("\n🏪 Store Configuration:")
    stores = [
        ("BLINKIT_API_URL", "Blinkit"),
        ("SWIGGY_API_URL", "Swiggy"),
        ("ZEPTO_API_URL", "Zepto"),
        ("JIOMART_API_URL", "JioMart"),
        ("BIGBASKET_API_URL", "BigBasket")
    ]
    
    for url_var, store_name in stores:
        url = os.getenv(url_var)
        status = "✅ Configured" if url else "⚠️  Not configured"
        print(f"  {store_name:10}: {status}")

def show_status():
    """Show bot status"""
    print("📊 Bot Status")
    print("=" * 40)
    
    # Check if bot is running (simple check for now)
    print("Status: Not implemented yet")
    print("Note: Use 'python run.py' to start the bot")

async def start_bot(daemon=False):
    """Start the bot"""
    print("🚀 Starting Telegram Stock Availability Bot...")
    
    try:
        app = App()
        if daemon:
            print("Running in daemon mode...")
            # In a real implementation, you'd fork here
            pass
        
        await app.run()
        
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        sys.exit(1)

def main():
    """Main CLI entry point"""
    # Load environment variables
    load_dotenv()
    
    parser = setup_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'start':
        asyncio.run(start_bot(args.daemon))
    elif args.command == 'test':
        print("🧪 Running bot tests...\n")
        env_ok = test_env_variables()
        store_ok = test_store_configuration()
        
        if env_ok:
            telegram_ok = asyncio.run(test_telegram_connection())
        else:
            telegram_ok = False
        
        print("\n" + "="*50)
        print("📋 TEST SUMMARY")
        print("="*50)
        print(f"Environment Variables: {'✅ PASS' if env_ok else '❌ FAIL'}")
        print(f"Store Configuration: {'✅ PASS' if store_ok else '⚠️  PARTIAL'}")
        print(f"Telegram Connection: {'✅ PASS' if telegram_ok else '❌ FAIL'}")
        
    elif args.command == 'status':
        show_status()
    elif args.command == 'config':
        show_configuration()
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()

if __name__ == "__main__":
    main() 