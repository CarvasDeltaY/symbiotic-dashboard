from aiohttp_retry import RetryClient
from config import Settings
from external.symbiotic.common import (
    RETRY_OPTIONS,
    Operators,
    Networks,
    Vaults,
)
import polars as pl


async def get_operators(
) -> list[Operators]:
    """Returns a list of N operators from the Symbiotic API."""

    print("Getting operators from Symbiotic API")

    async with RetryClient(retry_options=RETRY_OPTIONS) as client:
        async with client.get(
            Settings().symbiotic_operators_url,
        ) as response:
            data = await response.json()
            response = [Operators(**operator) for operator in data]
            print("✅ Operators fetched successfully")


    # Initialize lists to store data for each DataFrame
    data_operators = []


    for operator in response:
        data_operators.append({
            'node_operator_address' : operator.address.lower(),
            'node_operator_name' : operator.meta.name,
        })

    df_data_operators = pl.DataFrame(data_operators, infer_schema_length=len(data_operators))
    
    return df_data_operators


async def get_networks(
) -> list[Networks]:
    """Returns a list of N networks from the Symbiotic API."""

    print("Getting networks from Symbiotic API")

    async with RetryClient(retry_options=RETRY_OPTIONS) as client:
        async with client.get(
            Settings().symbiotic_networks_url,
        ) as response:
            data = await response.json()
            response = [Networks(**network) for network in data]
            print("✅ Networks fetched successfully")

    # Initialize lists to store data for each DataFrame
    data_networks = []

    for network in response:
        data_networks.append({
            'network_address' : network.address.lower(),
            'network_name' : network.meta.name,
        })

    df_data_networks = pl.DataFrame(data_networks, infer_schema_length=len(data_networks))

    return df_data_networks


async def get_vaults(
) -> list[Vaults]:
    """Returns a list of N vaults from the Symbiotic API."""

    print("Getting vaults from Symbiotic API")

    async with RetryClient(retry_options=RETRY_OPTIONS) as client:
        async with client.get(
            Settings().symbiotic_vaults_url,
        ) as response:
            data = await response.json()
            response = [Vaults(**vault) for vault in data]
            print("✅ Vaults fetched successfully")

    # Initialize lists to store data for each DataFrame
    data_vaults = []

    for vault in response:
        for point in vault.points:
            data_vaults.append({
                    'vault_address' : vault.address.lower(),
                    'token_address' : vault.token.address.lower(),
                    'token_symbol' : vault.token.symbol,
                    'token_decimals' : vault.token.decimals,
                    'total_supply' : vault.totalSupply,
                    'tvl' : vault.tvl,
                    'slashed' : vault.slashed,
                    'points_total' : point.points,
                    'points_type' : point.pointsType,
                    'points_name' : point.meta.name
                })

    df_data_vaults = pl.DataFrame(data_vaults, infer_schema_length=len(data_vaults))

    return df_data_vaults
