from typing import List, Dict, Protocol

class StoreClient(Protocol):
    async def search(self, terms: list[str]) -> List[Dict]:
        """Return list of dicts: {id, name, price, in_stock (bool), url}"""
        ...
