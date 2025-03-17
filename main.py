from external.symbiotic.read_info_api import get_operators,get_networks,get_vaults,get_operator_name_manual,get_category_type_manual
from external.symbiotic.read_info_cli import get_staking_data
from external.coingecko.read_info_api import get_prices
from internal.missing_info import data_quality_check,data_quality_control
import asyncio
import polars as pl
from external.aws_rds.db import SessionLocal
from external.aws_rds.database_models import StakingDataCurrent, StakingDataHistory
from itertools import batched
from sqlalchemy import text
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

    # Get operator name manually if not found in API
    df_staking_data = await get_operator_name_manual(df_staking_data)

    # Get category type manually
    df_staking_data = await get_category_type_manual(df_staking_data)

    # Calculate amount staked in USD
    # TOIMPROVE: Get asset decimals for each collateral asset
    asset_decimals = 18
    max_amount_staked = 1_000_000_000
    df_staking_data = df_staking_data.with_columns(
        pl.when(pl.col("amount_staked") > max_amount_staked)
        .then(pl.col("amount_staked") / 10 ** asset_decimals)
        .otherwise(pl.col("amount_staked"))
        .alias("amount_staked")
    )

    df_staking_data = df_staking_data.with_columns(
    (pl.col("amount_staked") * pl.col("collateral_asset_price")).alias("amount_staked_usd")
    )

    # Check data quality
    await data_quality_check(df_staking_data)
    df_staking_data = await data_quality_control(df_staking_data)

    print("Adding data to database...")

    try:
        session = SessionLocal()

        delete_query = text("DELETE FROM staking_data_current")
        session.execute(delete_query)

        dict_staking_data = df_staking_data.to_dicts()
        session.bulk_insert_mappings(StakingDataCurrent, dict_staking_data)
        session.bulk_insert_mappings(StakingDataHistory, dict_staking_data)

        session.commit()
        session.close()
        print("✅ Data added to database successfully")

    except Exception as e:
        print(f"❌ Error adding data to database: {e}")
        session.rollback()
    finally:
        session.close()

asyncio.run(main())


