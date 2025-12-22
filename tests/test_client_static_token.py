"""
Tests for static_token parameter in Client and ClientAsync.

These tests verify the SimSchwab authentication bypass functionality.
"""
import pytest
from schwabdev import Client, ClientAsync, SIMSCHWAB_API_URL, SCHWAB_API_URL


class TestClientStaticToken:
    """Tests for Client class static_token functionality."""

    def test_simschwab_with_static_token_succeeds(self):
        """SimSchwab mode with static_token should initialize successfully."""
        client = Client(base_url=SIMSCHWAB_API_URL, static_token="test-token-123")

        assert client._static_token == "test-token-123"
        assert client.tokens is None
        assert client._get_access_token() == "test-token-123"

    def test_simschwab_without_static_token_fails(self):
        """SimSchwab mode without static_token should raise ValueError."""
        with pytest.raises(ValueError) as exc_info:
            Client(base_url=SIMSCHWAB_API_URL)

        assert "SimSchwab URLs require static_token authentication" in str(exc_info.value)

    def test_production_with_static_token_fails(self):
        """Production mode with static_token should raise ValueError."""
        with pytest.raises(ValueError) as exc_info:
            Client(base_url=SCHWAB_API_URL, static_token="bad-token")

        assert "static_token can only be used with SimSchwab" in str(exc_info.value)

    def test_production_without_credentials_fails(self):
        """Production mode without app_key/app_secret should raise ValueError."""
        with pytest.raises(ValueError) as exc_info:
            Client(base_url=SCHWAB_API_URL)

        assert "app_key and app_secret are required" in str(exc_info.value)

    def test_update_tokens_noop_for_static_token(self):
        """update_tokens should be a no-op when using static_token."""
        client = Client(base_url=SIMSCHWAB_API_URL, static_token="test-token")

        result = client.update_tokens()

        assert result is False
        assert client._get_access_token() == "test-token"

    def test_session_header_uses_static_token(self):
        """Session Authorization header should use static_token."""
        client = Client(base_url=SIMSCHWAB_API_URL, static_token="my-bearer-token")

        auth_header = client._session.headers.get("Authorization")

        assert auth_header == "Bearer my-bearer-token"


class TestURLValidation:
    """Tests for URL validation functionality."""

    def test_any_localhost_port_is_valid(self):
        """Any localhost port should be accepted for SimSchwab."""
        # Test various ports
        for port in [8080, 9004, 3000, 12345]:
            client = Client(base_url=f"http://localhost:{port}", static_token="test-token")
            assert client._static_token == "test-token"

    def test_arbitrary_url_fails(self):
        """Arbitrary external URLs should be rejected."""
        with pytest.raises(ValueError) as exc_info:
            Client(base_url="http://evil.com:9004", static_token="token")

        assert "Invalid base_url" in str(exc_info.value)

    def test_https_localhost_fails(self):
        """HTTPS localhost should be rejected (SimSchwab is HTTP only)."""
        with pytest.raises(ValueError) as exc_info:
            Client(base_url="https://localhost:9004", static_token="token")

        assert "Invalid base_url" in str(exc_info.value)

    def test_localhost_without_port_fails(self):
        """Localhost without port should be rejected."""
        with pytest.raises(ValueError) as exc_info:
            Client(base_url="http://localhost", static_token="token")

        assert "Invalid base_url" in str(exc_info.value)


class TestClientAsyncStaticToken:
    """Tests for ClientAsync class static_token functionality."""

    @pytest.fixture
    def event_loop_policy(self):
        """Provide event loop for async client tests."""
        import asyncio
        return asyncio.DefaultEventLoopPolicy()

    @pytest.mark.asyncio
    async def test_simschwab_with_static_token_succeeds(self):
        """SimSchwab mode with static_token should initialize successfully."""
        client = ClientAsync(base_url=SIMSCHWAB_API_URL, static_token="async-token-456")

        assert client._static_token == "async-token-456"
        assert client.tokens is None
        assert client._get_access_token() == "async-token-456"

        await client._session.close()

    def test_simschwab_without_static_token_fails(self):
        """SimSchwab mode without static_token should raise ValueError."""
        with pytest.raises(ValueError) as exc_info:
            ClientAsync(base_url=SIMSCHWAB_API_URL)

        assert "SimSchwab URLs require static_token authentication" in str(exc_info.value)

    def test_production_with_static_token_fails(self):
        """Production mode with static_token should raise ValueError."""
        with pytest.raises(ValueError) as exc_info:
            ClientAsync(base_url=SCHWAB_API_URL, static_token="bad-token")

        assert "static_token can only be used with SimSchwab" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_update_tokens_noop_for_static_token(self):
        """update_tokens should be a no-op when using static_token."""
        client = ClientAsync(base_url=SIMSCHWAB_API_URL, static_token="async-token")

        result = client.update_tokens()

        assert result is False
        assert client._get_access_token() == "async-token"

        await client._session.close()
