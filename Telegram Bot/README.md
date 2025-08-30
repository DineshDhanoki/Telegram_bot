# Telegram Stock Availability Bot

A Telegram bot that monitors stock availability across multiple grocery delivery platforms including Blinkit, Swiggy Instamart, Zepto, JioMart, and BigBasket. The bot sends notifications when products become available in stock.

## Features

- **Multi-platform monitoring**: Supports Blinkit, Swiggy Instamart, Zepto, JioMart, and BigBasket
- **Real-time notifications**: Sends Telegram messages when products come back in stock
- **Duplicate prevention**: Avoids sending duplicate notifications for the same product
- **Configurable search terms**: Monitor multiple products simultaneously
- **Flexible polling**: Configurable check intervals
- **API and Browser modes**: Supports both API-based and browser-based scraping

## Prerequisites

- Python 3.8 or higher
- A Telegram Bot Token (get from [@BotFather](https://t.me/botfather))
- Your Telegram Chat ID
- Your delivery pincode

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd telegram-stock-bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers** (for browser mode):
   ```bash
   playwright install
   ```

4. **Set up environment variables**:
   ```bash
   cp env_template.txt .env
   ```
   
   Edit the `.env` file with your configuration:
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
   - `TELEGRAM_CHAT_ID`: Your Telegram chat ID
   - `PINCODE`: Your delivery pincode
   - `SEARCH_TERMS`: Comma-separated list of products to monitor
   - `POLL_INTERVAL`: How often to check (in seconds, default: 300)

## Getting Your Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token provided

## Getting Your Chat ID

1. Start a conversation with your bot
2. Send any message to the bot
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Look for the `chat.id` field in the response

## Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token | `123456789:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID | `123456789` |
| `PINCODE` | Your delivery pincode | `400001` |
| `SEARCH_TERMS` | Products to monitor | `hot wheels,lego,action figures` |
| `POLL_INTERVAL` | Check interval (seconds) | `300` |
| `RUN_MODE` | API or browser mode | `api` |

### Store API Configuration

For each store, you can configure:
- **API URL**: The endpoint to query for products
- **Headers**: Custom headers for API requests

Example API URL format:
```
https://store.com/api/search?pincode={PINCODE}&q={QUERY}
```

## Usage

### Running the Bot

```bash
python run.py
```

The bot will:
1. Check each configured store for your search terms
2. Compare results with previously seen products
3. Send Telegram notifications for new in-stock items
4. Wait for the specified interval before checking again

### Logs

The bot logs its activity to stdout. You can redirect logs to a file:

```bash
python run.py > bot.log 2>&1
```

## Store Support

### Currently Supported Stores

1. **Blinkit** - API and Browser modes
2. **Swiggy Instamart** - API and Browser modes  
3. **Zepto** - API mode
4. **JioMart** - API mode
5. **BigBasket** - API mode

### Adding New Stores

To add a new store:

1. Create a new file in `stores/` directory
2. Implement the `StoreClient` protocol
3. Add the store to `bot/app.py`

Example store implementation:
```python
class NewStoreAPI:
    def __init__(self, pincode: str):
        # Initialize store client
        
    def enabled(self):
        # Return True if store is configured
        
    async def search(self, terms: list[str]) -> List[Dict]:
        # Return list of products with format:
        # {"id": "unique_id", "name": "product_name", 
        #  "price": "price", "in_stock": True/False, "url": "product_url"}
```

## Troubleshooting

### Common Issues

1. **Bot not sending messages**:
   - Verify your bot token and chat ID
   - Make sure you've started a conversation with the bot
   - Check if the bot has permission to send messages

2. **No products found**:
   - Verify your pincode is correct
   - Check if the search terms are available in your area
   - Verify API URLs and headers are correct

3. **API errors**:
   - Check network connectivity
   - Verify API endpoints are accessible
   - Review API headers configuration

### Debug Mode

To enable debug logging, modify `infra/logging.py`:
```python
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=fmt)
```

## Security Notes

- Keep your bot token secure and never commit it to version control
- Use environment variables for sensitive configuration
- Consider using a dedicated bot for production use

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This bot is for educational purposes. Please respect the terms of service of the platforms you're monitoring. Some platforms may have rate limits or restrictions on automated access.
