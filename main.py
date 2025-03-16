from external.symbiotic.read_info_api import get_operators,get_networks,get_vaults
from external.symbiotic.read_info_cli import get_staking_data
from external.coingecko.read_info_api import get_prices
import asyncio
import polars as pl
from external.aws_rds.db import SessionLocal
from external.aws_rds.database_models import StakingData
from itertools import batched
pl.Config.set_tbl_cols(50)


async def main():
### Get data from Symbiotic API
    df_operators = await get_operators()
    df_networks = await get_networks()
    #df_vaults = await get_vaults()

    df_staking_data = get_staking_data("python symb.py nets")

    # Get unique addresses
    unique_price_list = df_staking_data["collateral_asset_address"].unique().to_list()

    # Store results in a list and convert to DataFrame at the end
    price_results = []

    for batch in batched(unique_price_list, 5):  # Batch size of 5
        contract_addresses_string = ",".join(batch)    
        price_results.append(await get_prices(contract_addresses_string))

    # Convert the list of results into a Polars DataFrame
    prices = pl.concat(price_results)
    print("✅ Prices fetched successfully")


    df_staking_data = df_staking_data.with_columns(
        pl.col("collateral_asset_address").str.to_lowercase().alias("collateral_asset_address")
    )

    df_staking_data = df_staking_data.join(
                            df_operators,
                            on=['node_operator_address'],
                            how='left'
                        ).join(
                            df_networks,
                            on=['network_address'],
                            how='left'
                            ).join(
                            prices,
                            on=['collateral_asset_address'],
                            how='left'
                        )

    df_staking_data = df_staking_data.with_columns(
        pl.col("amount_staked") * pl.col("collateral_asset_price").alias("amount_staked_usd")
    )


    print(df_staking_data.null_count())
    print("Adding data to database...")

    dict_staking_data = df_staking_data.to_dicts()
    session = SessionLocal()
    session.bulk_insert_mappings(StakingData, dict_staking_data)
    session.commit()
    session.close()
    print("✅ Data added to database successfully")

asyncio.run(main())


