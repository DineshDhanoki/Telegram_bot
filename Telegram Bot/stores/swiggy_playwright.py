from typing import List, Dict
from playwright.async_api import async_playwright
from infra.user_agents import random_ua

class SwiggyBrowser:
    def __init__(self, pincode: str, selectors: dict):
        self.pincode = pincode
        self.sel = selectors

    async def search(self, terms: list[str]) -> List[Dict]:
        results: List[Dict] = []
        ua = random_ua()
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            ctx = await browser.new_context(user_agent=ua, locale="en-IN")
            page = await ctx.new_page()

            # 1. Open Swiggy Instamart
            await page.goto("https://www.swiggy.com/instamart", wait_until="domcontentloaded")

            # 2. Set pincode (UI can vary)
            try:
                if self.sel.get("pincode_input"):
                    await page.click(self.sel["pincode_input"])
                    await page.fill(self.sel["pincode_input"], self.pincode)
                if self.sel.get("pincode_submit"):
                    await page.click(self.sel["pincode_submit"])
                    await page.wait_for_timeout(2000)
            except:
                pass

            # 3. Search
            await page.click(self.sel["search_input"])
            await page.fill(self.sel["search_input"], "hot wheels")
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)

            # 4. Parse results
            cards = await page.query_selector_all(self.sel["product_card"])
            for c in cards:
                title_el = await c.query_selector(self.sel["product_title"])
                title = (await title_el.inner_text()).strip() if title_el else ""
                if "hot" in title.lower() and "wheel" in title.lower():
                    add_btn = await c.query_selector(self.sel["add_button"])
                    oos = await c.query_selector(self.sel["out_of_stock_badge"]) if self.sel.get("out_of_stock_badge") else None
                    in_stock = bool(add_btn) and not bool(oos)

                    href = ""
                    a = await c.query_selector("a")
                    if a:
                        href = await a.get_attribute("href") or ""
                        if href.startswith("/"):
                            href = "https://www.swiggy.com" + href

                    price_el = await c.query_selector("text=₹")
                    price = (await price_el.inner_text()) if price_el else ""

                    results.append({
                        "id": href or title,
                        "name": title,
                        "price": price,
                        "in_stock": in_stock,
                        "url": href
                    })

            await browser.close()
        return results
