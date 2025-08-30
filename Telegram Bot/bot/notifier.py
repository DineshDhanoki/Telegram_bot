import os
from telegram import Bot
from telegram.error import TelegramError
import asyncio
import logging

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

class Notifier:
    def __init__(self):
        if not BOT_TOKEN or not CHAT_ID:
            raise RuntimeError("Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID")
        self.bot = Bot(BOT_TOKEN)
        self.chat_id = int(CHAT_ID)

    async def send(self, text: str):
        """Send a text message to Telegram"""
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=text,
                parse_mode='HTML',
                disable_web_page_preview=True
            )
            logger.info(f"Message sent successfully: {text[:50]}...")
        except TelegramError as e:
            logger.error(f"Failed to send Telegram message: {e}")
        except Exception as e:
            logger.error(f"Unexpected error sending message: {e}")

    async def send_products(self, store: str, items):
        """Send product availability notifications"""
        if not items:
            return
        
        try:
            # Create a formatted message
            lines = [f"🔔 <b>Restock Alert on {store}</b>"]
            
            for item in items:
                name = item.get("name", "Unknown Product")
                price = item.get("price", "")
                url = item.get("url", "")
                
                # Format the product line
                product_line = f"• <b>{name}</b>"
                if price:
                    product_line += f" - {price}"
                if url:
                    product_line += f"\n  <a href='{url}'>View Product</a>"
                
                lines.append(product_line)
            
            # Split long messages if needed (Telegram has a 4096 character limit)
            message = "\n\n".join(lines)
            if len(message) > 4000:
                # Split into multiple messages
                chunks = self._split_message(message, 4000)
                for chunk in chunks:
                    await self.send(chunk)
            else:
                await self.send(message)
                
        except Exception as e:
            logger.error(f"Error formatting product message: {e}")
            # Fallback to simple message
            await self.send(f"🔔 New products available on {store}")

    def _split_message(self, message: str, max_length: int):
        """Split a long message into chunks"""
        chunks = []
        current_chunk = ""
        
        for line in message.split('\n'):
            if len(current_chunk) + len(line) + 1 > max_length:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = line
            else:
                current_chunk += '\n' + line if current_chunk else line
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks

    async def send_error(self, error_msg: str):
        """Send error notifications"""
        await self.send(f"⚠️ <b>Bot Error</b>\n{error_msg}")

    async def send_startup_message(self):
        """Send startup notification"""
        await self.send("🤖 <b>Stock Monitor Bot Started</b>\nMonitoring for product availability...")
