import os, json
from typing import List, Dict
from .generic_api_client import GenericAPIClient
from dotenv import load_dotenv
load_dotenv()

def _load_headers(env_key: str):
    j = os.getenv(env_key, "").strip()
    if not j:
        return {}
    try:
        return json.loads(j)
    except Exception:
        return {}

class BlinkitAPI:
    def __init__(self, pincode: str):
        self.url = os.getenv("BLINKIT_API_URL", "").strip()
        self.headers = _load_headers("BLINKIT_API_HEADERS_JSON")
        self.pincode = pincode
        self.client = GenericAPIClient(self.url, self.headers, pincode)

    def enabled(self):
        return bool(self.url)

    async def search(self, terms: list[str]) -> List[Dict]:
        results = []
        if not self.url:
            return results
        for q in terms:
            url = self.client._format_url(q)
            data = await self.client._get_json(url)
            # adapt to the JSON schema you captured; below are examples of typical shapes
            products = data.get("products") or data.get("data") or data.get("items") or []
            for p in products:
                title = (p.get("name") or p.get("title") or "").strip()
                if not title:
                    continue
                in_stock = bool(p.get("in_stock") or p.get("available") or p.get("is_available") or (p.get("inventory", {}).get("available", False)))
                price = p.get("price") or p.get("mrp") or p.get("final_price") or ""
                pid = str(p.get("id") or p.get("sku") or title)
                urlp = p.get("url") or p.get("product_url") or ""
                results.append({"id": pid, "name": title, "price": price, "in_stock": in_stock, "url": urlp})
        return results
