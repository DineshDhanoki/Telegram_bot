import os, json, aiohttp
from typing import List, Dict
from infra.user_agents import random_ua
from yarl import URL

class GenericAPIClient:
    def __init__(self, url_template: str, headers: dict, pincode: str):
        self.url_template = url_template
        self.headers = headers or {}
        self.pincode = pincode

    def _format_url(self, query: str) -> str:
        url = self.url_template.replace("{PINCODE}", self.pincode).replace("{QUERY}", query)
        return url

    async def _get_json(self, url: str):
        headers = dict(self.headers)
        if "User-Agent" not in headers:
            headers["User-Agent"] = random_ua()
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, timeout=15) as resp:
                try:
                    return await resp.json(content_type=None)
                except Exception:
                    text = await resp.text()
                    raise RuntimeError(f"Failed parsing JSON. Status={resp.status}. Body={text[:400]}")
