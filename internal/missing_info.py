import polars as pl

async def data_quality_check(
    df : pl.DataFrame
):
    """Return information on missing data"""

    print("################### Starting data quality check ###################")

    # Check missing operator names
    missing_operator_names = (
    df
    .filter(pl.col("node_operator_name").is_null())
    .select("node_operator_address")
    .unique()
    .to_series()
    .to_list()
    )

    print("The following node operator addresses don't have a node operator name:", missing_operator_names)

    # Check missing network names
    missing_network_names = (
    df
    .filter(pl.col("network_name").is_null())
    .select("network_address")
    .unique()
    .to_series()
    .to_list()
    )

    print("The following network addresses don't have a network name:", missing_network_names)


    # Check missing amount staked
    missing_amount_staked = (
    df
    .filter(pl.col("amount_staked").is_null())
    .select("network_name")
    .unique()
    .to_series()
    .to_list()
    )

    print("The following networks have some node operators that don't have an amount staked:", missing_amount_staked)

    # Check missing collateral asset price
    missing_collateral_asset_price = (
    df
    .filter(pl.col("collateral_asset_price").is_null())
    .select("collateral_asset_address")
    .unique()
    .to_series()
    .to_list()
    )

    print("The following collateral addresses don't have an collateral asset price:", missing_collateral_asset_price)
    
    missing_collateral_asset_price = (
    df
    .filter(pl.col("collateral_asset_price").is_null())
    .select("collateral_asset_symbol")
    .unique()
    .to_series()
    .to_list()
    )

    print("The following collateral symbols don't have an collateral asset price:", missing_collateral_asset_price)

    # Check missing category type
    missing_categories = (
    df
    .filter(pl.col("network_category").is_null())
    .select("network_name")
    .unique()
    .to_series()
    .to_list()
    )

    print("The following networks don't have a category type:", missing_categories)

    print("################### ✅ End of data quality check ✅ ###################")



async def data_quality_control(
    df : pl.DataFrame
) -> pl.DataFrame:
    """Fills missing informaiton data"""

    df = df.with_columns(
    pl.when(pl.col("node_operator_name").is_null())
    .then(pl.lit("Other"))
    .otherwise(pl.col("node_operator_name"))
    .alias("node_operator_name")
    )

    df = df.with_columns(
    pl.when(pl.col("network_name").is_null())
    .then(pl.lit("Other"))
    .otherwise(pl.col("network_name"))
    .alias("network_name")
    )

    df = df.with_columns(
    pl.when(pl.col("collateral_asset_symbol").is_null())
    .then(pl.lit("Other"))
    .otherwise(pl.col("collateral_asset_symbol"))
    .alias("collateral_asset_symbol")
    )

    df = df.with_columns(
    pl.when(pl.col("network_category").is_null())
    .then(pl.lit("Other"))
    .otherwise(pl.col("network_category"))
    .alias("network_category")
    )
    
    # Remove rows with null collateral asset price
    df = df.with_columns(pl.col("collateral_asset_price").fill_null(pl.lit(0.0)))
    
    # Remove rows with null amount staked in USD
    df = df.with_columns(pl.col("amount_staked_usd").fill_null(pl.lit(0.0)))
    

    return df
