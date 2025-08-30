import asyncio
from typing import List, Dict
from playwright.async_api import async_playwright
from infra.user_agents import random_ua

class SwiggyBrowser:
    def __init__(self, pincode: str, selectors: dict):
        self.pincode = pincode
        # Use default selectors if none provided
        self.sel = selectors or {
            "search_input": "input[placeholder*='search'], input[type='search'], input[name='search']",
            "product_card": "[data-testid*='product'], .product-card, .item-card",
            "product_title": "h3, h4, .product-title, .item-title",
            "add_button": "button[aria-label*='add'], .add-to-cart, button:has-text('Add')"
        }

    async def search(self, terms: list[str]) -> List[Dict]:
        results: List[Dict] = []
        ua = random_ua()
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                ctx = await browser.new_context(user_agent=ua, locale="en-IN")
                page = await ctx.new_page()

                # 1. Open Swiggy Instamart
                await page.goto("https://www.swiggy.com/instamart", wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_timeout(2000)

                # 2. Try to search for each term
                for term in terms:
                    try:
                        # Try to find and click search input
                        search_selectors = [
                            "input[placeholder*='search']",
                            "input[type='search']", 
                            "input[name='search']",
                            "[data-testid*='search']",
                            "input"
                        ]
                        
                        search_input = None
                        for selector in search_selectors:
                            try:
                                search_input = await page.wait_for_selector(selector, timeout=5000)
                                if search_input:
                                    break
                            except:
                                continue
                        
                        if search_input:
                            await search_input.click()
                            await search_input.fill(term)
                            await page.keyboard.press("Enter")
                            await page.wait_for_timeout(3000)
                            
                            # Try to find products
                            product_selectors = [
                                "[data-testid*='product']",
                                ".product-card",
                                ".item-card", 
                                ".product",
                                "[class*='product']"
                            ]
                            
                            for prod_selector in product_selectors:
                                try:
                                    cards = await page.query_selector_all(prod_selector)
                                    if cards:
                                        for card in cards[:5]:  # Limit to first 5 products
                                            try:
                                                # Try to get title
                                                title_selectors = ["h3", "h4", ".product-title", ".item-title", "[class*='title']"]
                                                title = ""
                                                for title_sel in title_selectors:
                                                    title_el = await card.query_selector(title_sel)
                                                    if title_el:
                                                        title = (await title_el.inner_text()).strip()
                                                        if title:
                                                            break
                                                
                                                if title and term.lower() in title.lower():
                                                    # Check if in stock
                                                    add_buttons = await card.query_selector_all("button")
                                                    in_stock = len(add_buttons) > 0
                                                    
                                                    # Get price
                                                    price_el = await card.query_selector("text=₹")
                                                    price = (await price_el.inner_text()) if price_el else ""
                                                    
                                                    # Get URL
                                                    link_el = await card.query_selector("a")
                                                    url = ""
                                                    if link_el:
                                                        href = await link_el.get_attribute("href")
                                                        if href:
                                                            url = "https://www.swiggy.com" + href if href.startswith("/") else href
                                                    
                                                    results.append({
                                                        "id": url or title,
                                                        "name": title,
                                                        "price": price,
                                                        "in_stock": in_stock,
                                                        "url": url
                                                    })
                                            except Exception as e:
                                                continue
                                        break
                                except:
                                    continue
                    except Exception as e:
                        continue

                await browser.close()
        except Exception as e:
            # Return empty results if browser fails
            pass
            
        return results
