#import dotenv
#from external.dune.common import RETRY_OPTIONS
#from aiohttp_retry import RetryClient
#from config import Settings
#import requests

#async def execute_query(
#    params : list,
#    query_ID: int,
#) -> pd.DataFrame:
    
#    dotenv.load_dotenv(".envi")
#    dune = DuneClient.from_env()
#    query = QueryBase(
#        name="Get Updated Historical Pricing Data",
#        query_id=4855294,
#        params=params,
#    )

#    df_historical_prices_latest = dune.run_query_dataframe(
#        query = query,
#        performance = "medium"
#    )

#    return df_historical_prices_latest

