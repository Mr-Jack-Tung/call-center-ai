from helpers.config import CONFIG
from helpers.config_models.cache import ModeEnum as CacheModeEnum
import pytest


_cache = CONFIG.cache.instance()


@pytest.mark.parametrize(
    "cache_mode",
    [
        pytest.param(
            CacheModeEnum.MEMORY,
            id="memory",
        ),
        pytest.param(
            CacheModeEnum.REDIS,
            id="redis",
        ),
    ],
)
@pytest.mark.asyncio  # Allow async functions
@pytest.mark.repeat(10)  # Catch multi-threading and concurrency issues
async def test_acid(random_text: str, cache_mode: CacheModeEnum) -> None:
    """
    Test ACID properties of the cache backend.

    Steps:
    1. Create a mock data
    2. Test not exists
    3. Insert test data
    4. Check it exists

    Test is repeated 10 times to catch multi-threading and concurrency issues.
    """
    # Set cache mode
    CONFIG.cache.mode = cache_mode

    # Init values
    test_key = random_text
    test_value = "lorem ipsum"

    # Check not exists
    assert not await _cache.aget(test_key)

    # Insert test call
    await _cache.aset(test_key, test_value)

    # Check point read
    assert await _cache.aget(test_key) == test_value.encode()
