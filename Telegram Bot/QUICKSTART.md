# Quick Start Guide

Get your Telegram Stock Availability Bot running in 5 minutes!

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
python setup.py
```

### 2. Get Your Telegram Bot Token
1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot`
3. Follow the instructions to create your bot
4. Copy the bot token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 3. Get Your Chat ID
1. Start a conversation with your bot
2. Send any message to the bot
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Look for `"chat":{"id":123456789}` in the response

### 4. Configure the Bot
Edit the `.env` file:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
PINCODE=your_pincode_here
SEARCH_TERMS=hot wheels,lego,action figures
POLL_INTERVAL=300
```

### 5. Test Your Setup
```bash
python test_bot.py
```

### 6. Start the Bot
```bash
python run.py
```

## 🎯 What You'll Get

- **Real-time notifications** when products come back in stock
- **Multi-store monitoring** across Blinkit, Swiggy, Zepto, JioMart, and BigBasket
- **Duplicate prevention** so you don't get spammed
- **Configurable search terms** to monitor multiple products

## 📱 Example Notifications

You'll receive messages like:
```
🔔 Restock Alert on Blinkit

• Hot Wheels Monster Truck - ₹299
  View Product

• Lego City Police Station - ₹1,999
  View Product
```

## 🔧 Advanced Configuration

### Store API Setup (Optional)
For better performance, configure store API endpoints in your `.env`:
```env
BLINKIT_API_URL=https://blinkit.com/api/search?pincode={PINCODE}&q={QUERY}
SWIGGY_API_URL=https://swiggy.com/api/search?pincode={PINCODE}&q={QUERY}
# ... etc
```

### Custom Search Terms
Monitor any products you want:
```env
SEARCH_TERMS=ps5,iphone,airpods,switch
```

### Adjust Polling Frequency
```env
POLL_INTERVAL=60  # Check every minute
POLL_INTERVAL=1800  # Check every 30 minutes
```

## 🛠️ Troubleshooting

### Bot Not Sending Messages?
- ✅ Verify bot token and chat ID
- ✅ Start a conversation with your bot first
- ✅ Check if the bot has permission to send messages

### No Products Found?
- ✅ Verify your pincode is correct
- ✅ Check if products are available in your area
- ✅ Try different search terms

### Need Help?
- Run `python bot_cli.py config` to check your configuration
- Run `python test_bot.py` to test connectivity
- Check the full [README.md](README.md) for detailed documentation

## 🎉 You're All Set!

Your bot is now monitoring for stock availability and will send you notifications when products become available. The bot runs continuously and will automatically restart if it encounters any errors.

Happy shopping! 🛒 