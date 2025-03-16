from aiohttp_retry import RetryOptionsBase, ExponentialRetry


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

