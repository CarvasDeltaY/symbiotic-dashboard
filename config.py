from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    symbiotic_operators_url: str = "https://app.symbiotic.fi/api/v2/operators"
    """ symbiotic operators url. Read more about it in the [documentation](https://docs.symbiotic.fi/category/contracts-api)."""

    symbiotic_networks_url: str = "https://app.symbiotic.fi/api/v2/networks"
    """ symbiotic operators url. Read more about it in the [documentation](https://docs.symbiotic.fi/category/contracts-api)."""

    symbiotic_vaults_url: str = "https://app.symbiotic.fi/api/v2/vaults"
    """ symbiotic operators url. Read more about it in the [documentation](https://docs.symbiotic.fi/category/contracts-api)."""

    coingecko_url: str = "https://api.coingecko.com/api/v3/simple/token_price/ethereum"
    """ coingecko url. Read more about it in the [documentation](https://docs.coingecko.com/v3.0.1/reference/simple-token-price)."""

    dune_url: str = "https://api.dune.com/api/v1/query/"
    """ Dune URL. Read more about it in the [documentation](https://docs.dune.com/api-reference/overview/introduction)."""

    dune_API_Key: str = "l9DIccaXA9UiMwdaALUxg2KuvWGQsoer"
    """ Dune API Key """

    coingecko_API_Key: str = "CG-g8NCyFE1C23Lc7ZLPxjWKLFW"
    """ Coingecko API Key """

    db_host: str = "symbiotic-db.cfq62o644a2p.eu-north-1.rds.amazonaws.com"
    db_port: str = "5432"
    db_name: str = "initial_db"
    db_user: str = "symbioticdb"
    db_password: str = "bootstrappingcities2025"

    @property
    def database_url(self) -> str:
        """ PostGres Database URL."""
        return f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    