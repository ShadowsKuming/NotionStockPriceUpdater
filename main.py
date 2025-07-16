import os
from alpaca.data.historical import StockHistoricalDataClient, CryptoHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest, CryptoLatestQuoteRequest
from notion_client import Client as NotionClient

# Load credentials from environment variables
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Initialize Alpaca clients for stock and crypto
stock_client = StockHistoricalDataClient(ALPACA_API_KEY, ALPACA_SECRET_KEY)
crypto_client = CryptoHistoricalDataClient(ALPACA_API_KEY, ALPACA_SECRET_KEY)

# Initialize Notion client
notion = NotionClient(auth=NOTION_API_KEY)


def get_price(asset):
    """Fetch the latest price of an asset using Alpaca."""
    try:
        # Skip if required fields are missing
        if not asset.get("symbol") or not asset.get("name") or not asset.get("type"):
            print("⚠️ Missing required fields: 'symbol', 'name', or 'type'. Skipping.")
            return -1

        # Handle stocks and ETFs
        if asset["type"] in {"stock", "etf"}:
            quote = stock_client.get_stock_latest_quote(
                StockLatestQuoteRequest(symbol_or_symbols=asset["symbol"])
            )
            q = quote.get(asset["symbol"])
            if not q:
                return -1
            price = q.ask_price if q.ask_price and q.ask_price > 0 else q.bid_price
            return price if price and price > 0 else -1

        # Handle cryptocurrencies
        elif asset["type"] == "crypto":
            quote = crypto_client.get_crypto_latest_quote(
                CryptoLatestQuoteRequest(symbol_or_symbols=asset["symbol"])
            )
            q = quote.get(asset["symbol"])
            if not q:
                return -1
            price = q.ask_price if q.ask_price and q.ask_price > 0 else q.bid_price
            return price if price and price > 0 else -1

        else:
            print(f"⚠️ Unknown asset type: {asset['type']}")
            return -1

    except Exception as e:
        print(f"Error fetching {asset.get('name', 'Unknown')}: {e}")
        return -1


def update_page(page, new_price):
    """Update the Notion page with the latest price."""
    try:
        notion.pages.update(
            page_id=page["id"],
            properties={
                "Current Price": {
                    "number": new_price
                }
            }
        )
        print(f"✅ Updated {page['id']} with price: {new_price}")
    except Exception as e:
        print(f"❌ Failed to update page: {e}")


def main():
    """Main script logic: fetch all assets from Notion and update their prices."""
    pages = notion.databases.query(database_id=DATABASE_ID)["results"]

    for page in pages:
        props = page["properties"]

        # Get asset name
        try:
            name = props["Name"]["title"][0]["text"]["content"]
        except (KeyError, IndexError):
            name = None

        # Get asset type
        try:
            type_ = props["Type"]["select"]["name"]
        except KeyError:
            type_ = None

        asset = {
            "name": name,
            "symbol": name,  # We assume the name is also the ticker symbol
            "type": type_
        }

        # Fetch price and update if valid
        new_price = get_price(asset)
        if new_price != -1:
            update_page(page, new_price)


if __name__ == "__main__":
    main()
