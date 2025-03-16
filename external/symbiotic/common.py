from aiohttp_retry import RetryOptionsBase, ExponentialRetry
from pydantic import BaseModel
from typing import Optional

## ================================
## Request Configuration
## ================================

RETRY_OPTIONS: RetryOptionsBase = ExponentialRetry(
    attempts=3,
    start_timeout=0.2,
    max_timeout=10,
    factor=2.0,
    statuses={429, 500, 502, 503, 504},
)
""" Retrial configuration for querying the Morpho API with aiohttp."""


""" Operators """

class Meta(BaseModel):
    """Meta information of Operators/Tokens"""

    name: Optional[str] = None
    """Name"""

    decimals: Optional[int] = None
    """Decimals"""    

class NetworksPreview(BaseModel):
    """NetworksPreview information of Operators. E.g., Blockhunters"""

    totalCount: Optional[int] = 0
    """Number of networks."""

class VaultsPreview(BaseModel):
    """VaultsPreview information of Operators. E.g., Blockhunters"""

    totalCount: Optional[int] = 0
    """Number of vaults."""
    

class Operators(BaseModel):
    """Operators information. E.g., Blockhunters"""

    address: str
    """Address of the operator."""

    meta: Optional[Meta] = []
    """Chain of the asset."""

    stakeUsd: Optional[float] = 0.0
    """Decimals of the asset."""

    networksPreview: Optional[NetworksPreview] = []
    """Networks preview."""

    vaultsPreview: Optional[VaultsPreview] = []
    """Vaults preview."""

""" Networks """

class OperatorsPreview(BaseModel):
    """OperatorsPreview information of Networks. E.g., zkLink"""

    totalCount: Optional[int] = 0
    """Number of networks."""

class Networks(BaseModel):
    """Networks information. E.g., zkLink"""

    address: str
    """Address of the network."""

    meta: Optional[Meta] = []
    """Meta information of the network."""

    stakeUsd: Optional[float] = 0.0
    """Stake in USD."""

    vaultsPreview: Optional[VaultsPreview] = []
    """Vaults preview."""

    operatorsPreview: Optional[OperatorsPreview] = []
    """Operators preview."""
    
""" Vaults """  
    
class Token(BaseModel):
    """Token information. E.g., ETH"""

    address: str
    """Address of the token."""

    decimals: Optional[int] = 0
    """Decimals of the token."""

    usdPrice: Optional[float] = 0.0
    """USD price of the token."""

    symbol: Optional[str] = None
    """Symbol of the token."""

class Points(BaseModel):
    """Points information of vault"""

    pointsType: Optional[str] = None
    """Type of the point."""

    points: Optional[float] = 0.0
    """Points of the vault."""

    meta: Optional[Meta] = []
    """Metadata of the point."""

class Vaults(BaseModel):
    """Vaults information. E.g., zkLink"""

    address: str
    """Address of the network."""

    token: Optional[Token] = []
    """Meta information of the network."""

    totalSupply: Optional[float] = 0.0
    """Total supply of the vault."""

    slashed: Optional[bool] = False
    """Is the vault slashable"""

    tvl: Optional[float] = 0.0
    """TVL of the vault."""

    points: Optional[list[Points]] = []

    vaultsPreview: Optional[VaultsPreview] = []
    """Vaults preview."""

    operatorsPreview: Optional[OperatorsPreview] = []
    """Operators preview."""


