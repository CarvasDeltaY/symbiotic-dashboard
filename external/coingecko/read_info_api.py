from aiohttp_retry import RetryClient
from config import Settings
from external.coingecko.common import (
    RETRY_OPTIONS,
)
import polars as pl


async def get_prices(
        contract_addresses : str
        ) -> pl.DataFrame:
    """Returns prices from the CoinGecko API for specified contract addresses."""

    params = {
        "contract_addresses": contract_addresses,
        "vs_currencies": "usd"
    }

    headers = {
        "Content-Type": "application/json",
        "x-cg-demo-api-key": Settings().coingecko_API_Key  # API Key
    }

    async with RetryClient(retry_options=RETRY_OPTIONS) as client:
        async with client.get(
            Settings().coingecko_url,
            headers=headers,
            params=params  
        ) as response:
            if response.status != 200:
                print(f"Error: {response.status} - {await response.text()}")
                return None  
            
            data = await response.json()
            
            # Initialize list to store price data
            price_data = []
            
            # Process the response data
            for contract, price_info in data.items():
                price_data.append({
                    'collateral_asset_address': contract.lower(),
                    'collateral_asset_price': float(price_info.get('usd', 0.0))
                })
            
            # Create DataFrame from the price data
            df_prices = pl.DataFrame(price_data, infer_schema_length=len(price_data))
            
            return df_prices
