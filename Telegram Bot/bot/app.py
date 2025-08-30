import os, yaml, asyncio
from dotenv import load_dotenv
load_dotenv()
from infra.logging import setup_logging
logger = setup_logging()

from bot.notifier import Notifier
from bot.repository import SeenRepo
from bot.scheduler import Scheduler

from stores.blinkit_api import BlinkitAPI
from stores.swiggy_api import SwiggyAPI
from stores.zepto_api import ZeptoAPI
from stores.jiomart_api import JioMartAPI
from stores.bigbasket_api import BigBasketAPI
from stores.blinkit_playwright import BlinkitBrowser
from stores.swiggy_playwright import SwiggyBrowser

RUN_MODE = os.getenv("RUN_MODE", "api").lower()
PINCODE = os.getenv("PINCODE", "").strip()
INTERVAL = int(os.getenv("POLL_INTERVAL", "300"))
TERMS = [t.strip() for t in os.getenv("SEARCH_TERMS", "hot wheels").split(",") if t.strip()]

class App:
    def __init__(self):
        self.notifier = Notifier()
        self.seen = SeenRepo()
        self.clients = []
        self.stores_configured = 0

        # Blinkit
        blink = BlinkitAPI(PINCODE)
        if RUN_MODE == "api" and blink.enabled():
            self.clients.append(("Blinkit", blink))
            self.stores_configured += 1
        else:
            self.clients.append(("Blinkit", BlinkitBrowser(PINCODE, {})))
            self.stores_configured += 1

        # Swiggy
        sw = SwiggyAPI(PINCODE)
        if RUN_MODE == "api" and sw.enabled():
            self.clients.append(("Swiggy", sw))
            self.stores_configured += 1
        else:
            self.clients.append(("Swiggy", SwiggyBrowser(PINCODE, {})))
            self.stores_configured += 1

        # Zepto
        z = ZeptoAPI(PINCODE)
        if RUN_MODE == "api" and z.enabled():
            self.clients.append(("Zepto", z))
            self.stores_configured += 1

        # JioMart
        j = JioMartAPI(PINCODE)
        if RUN_MODE == "api" and j.enabled():
            self.clients.append(("JioMart", j))
            self.stores_configured += 1

        # BigBasket
        b = BigBasketAPI(PINCODE)
        if RUN_MODE == "api" and b.enabled():
            self.clients.append(("BigBasket", b))
            self.stores_configured += 1

        logger.info(f"Initialized with {len(self.clients)} stores, {self.stores_configured} configured")
        logger.info(f"Monitoring terms: {TERMS}")
        logger.info(f"Pincode: {PINCODE}")
        logger.info(f"Poll interval: {INTERVAL} seconds")

    async def tick(self):
        """Check all stores for product availability"""
        total_hits = 0
        total_fresh = 0
        
        for name, client in self.clients:
            try:
                items = await client.search(TERMS)
                hits = [i for i in items if i.get("in_stock")]
                fresh = []
                
                for item in hits:
                    key = f"{name}:{item['id']}"
                    if not self.seen.already_seen(key):
                        self.seen.mark_seen(key)
                        fresh.append(item)
                
                if fresh:
                    await self.notifier.send_products(name, fresh)
                
                total_hits += len(hits)
                total_fresh += len(fresh)
                logger.info(f"{name}: checked, hits={len(hits)}, new={len(fresh)}")
                
            except Exception as e:
                logger.exception(f"Error checking {name}: {e}")
                await self.notifier.send_error(f"Error checking {name}: {str(e)[:100]}")

        if total_fresh > 0:
            logger.info(f"Total new products found: {total_fresh}")

    async def run(self):
        """Run the bot with startup message"""
        try:
            # Send startup message
            await self.notifier.send_startup_message()
            
            # Start the scheduler
            scheduler = Scheduler(INTERVAL)
            await scheduler.run_forever(self.tick)
            
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
            await self.notifier.send("🛑 <b>Bot Stopped</b>\nStock monitoring has been stopped.")
        except Exception as e:
            logger.exception(f"Fatal error: {e}")
            await self.notifier.send_error(f"Fatal error: {str(e)[:200]}")
            raise
