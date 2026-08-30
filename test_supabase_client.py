import pytest

from config import Settings
from supabase_client import SupabaseClient, SupabaseError


def test_missing_config_raises_supabase_error():
    with pytest.raises(SupabaseError):
        SupabaseClient(Settings(supabase_url=None, supabase_anon_key=None))


def test_headers_include_bearer_token_when_provided():
    client = SupabaseClient(Settings(supabase_url="https://example.supabase.co", supabase_anon_key="anon-key"))
    headers = client._headers(access_token="token-123")
    assert headers["apikey"] == "anon-key"
    assert headers["Authorization"] == "Bearer token-123"


def test_headers_omit_authorization_when_no_token():
    client = SupabaseClient(Settings(supabase_url="https://example.supabase.co", supabase_anon_key="anon-key"))
    headers = client._headers()
    assert "Authorization" not in headers
