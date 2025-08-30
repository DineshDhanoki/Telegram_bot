"""
Example store implementation to demonstrate how to add new stores
"""

import os
import json
from typing import List, Dict
from .generic_api_client import GenericAPIClient
from dotenv import load_dotenv
load_dotenv()

def _load_headers(env_key: str):
    """Load headers from environment variable"""
    j = os.getenv(env_key, "").strip()
    if not j:
        return {}
    try:
        return json.loads(j)
    except Exception:
        return {}

class ExampleStoreAPI:
    """
    Example implementation for a new store.
    
    This demonstrates the required interface for adding new stores to the bot.
    """
    
    def __init__(self, pincode: str):
        """
        Initialize the store client.
        
        Args:
            pincode: Delivery pincode for location-based searches
        """
        self.url = os.getenv("EXAMPLE_STORE_API_URL", "").strip()
        self.headers = _load_headers("EXAMPLE_STORE_API_HEADERS_JSON")
        self.pincode = pincode
        self.client = GenericAPIClient(self.url, self.headers, pincode)

    def enabled(self) -> bool:
        """
        Check if this store is properly configured.
        
        Returns:
            True if the store has a valid API URL configured
        """
        return bool(self.url)

    async def search(self, terms: list[str]) -> List[Dict]:
        """
        Search for products across multiple search terms.
        
        Args:
            terms: List of search terms to look for
            
        Returns:
            List of product dictionaries with the following format:
            {
                "id": "unique_product_id",
                "name": "Product Name",
                "price": "₹100",
                "in_stock": True/False,
                "url": "https://store.com/product/123"
            }
        """
        results = []
        
        if not self.url:
            return results
            
        for query in terms:
            try:
                # Format the URL with pincode and query
                url = self.client._format_url(query)
                
                # Get JSON response from the API
                data = await self.client._get_json(url)
                
                # Extract products from the response
                # Adjust these keys based on the actual API response structure
                products = data.get("products") or data.get("data") or data.get("items") or []
                
                for product in products:
                    # Extract product information
                    title = (product.get("name") or product.get("title") or "").strip()
                    if not title:
                        continue
                    
                    # Check if product is in stock
                    in_stock = bool(
                        product.get("in_stock") or 
                        product.get("available") or 
                        product.get("is_available") or 
                        (product.get("inventory", {}).get("available", False))
                    )
                    
                    # Extract price information
                    price = product.get("price") or product.get("mrp") or product.get("final_price") or ""
                    
                    # Generate unique product ID
                    product_id = str(product.get("id") or product.get("sku") or title)
                    
                    # Get product URL
                    product_url = product.get("url") or product.get("product_url") or ""
                    
                    # Add to results
                    results.append({
                        "id": product_id,
                        "name": title,
                        "price": price,
                        "in_stock": in_stock,
                        "url": product_url
                    })
                    
            except Exception as e:
                # Log errors but continue with other search terms
                print(f"Error searching for '{query}' in ExampleStore: {e}")
                continue
                
        return results

# Example usage and testing
if __name__ == "__main__":
    import asyncio
    
    async def test_example_store():
        """Test the example store implementation"""
        store = ExampleStoreAPI("400001")  # Mumbai pincode
        
        if not store.enabled():
            print("Example store not configured")
            return
            
        results = await store.search(["milk", "bread"])
        print(f"Found {len(results)} products")
        
        for product in results:
            status = "✅ In Stock" if product["in_stock"] else "❌ Out of Stock"
            print(f"{product['name']} - {product['price']} - {status}")
    
    # Run the test
    asyncio.run(test_example_store()) 