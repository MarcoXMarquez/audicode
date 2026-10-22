import pytest
from fastapi import HTTPException

from core.request_guard import assert_safe_bind, parse_allowed_origins


def test_cross_origin_post_blocked(client):
    r = client.post("/api/auth/login", json={}, headers={"Origin": "http://evil.example"})
    assert r.status_code == 403


def test_null_origin_blocked(client):
    r = client.post("/api/auth/login", json={}, headers={"Origin": "null"})
    assert r.status_code == 403


def test_same_origin_post_not_blocked(client):
    r = client.post("/api/auth/login", json={}, headers={"Origin": "http://testserver"})
    assert r.status_code != 403 or "Cross-origin" not in r.text


def test_foreign_host_header_rejected_in_desktop_mode(client):
    r = client.get("/api/version", headers={"Host": "evil.example"})
    assert r.status_code == 400


def test_auth_off_requires_loopback_bind():
    assert_safe_bind(False, "127.0.0.1")
    with pytest.raises(RuntimeError):
        assert_safe_bind(False, "0.0.0.0")
    assert_safe_bind(True, "0.0.0.0")


def test_allowed_origins_are_stripped():
    assert parse_allowed_origins("http://a.com, http://b.com/ ,") == ["http://a.com", "http://b.com"]


def test_setup_requires_token_when_configured(monkeypatch):
    from types import SimpleNamespace
    from core.request_guard import check_setup_allowed
    monkeypatch.setenv("AUDICODE_SETUP_TOKEN", "s3cret")
    req = SimpleNamespace(headers={"x-setup-token": "wrong"}, client=SimpleNamespace(host="127.0.0.1"))
    with pytest.raises(HTTPException):
        check_setup_allowed(req)
    req.headers = {"x-setup-token": "s3cret"}
    check_setup_allowed(req)


def test_setup_rejects_remote_and_proxied(monkeypatch):
    from types import SimpleNamespace
    from core.request_guard import check_setup_allowed
    monkeypatch.delenv("AUDICODE_SETUP_TOKEN", raising=False)
    monkeypatch.delenv("AUDICODE_SETUP_ALLOW_PRIVATE", raising=False)
    check_setup_allowed(SimpleNamespace(headers={}, client=SimpleNamespace(host="127.0.0.1")))
    for host, hdrs in (("8.8.8.8", {}), ("192.168.1.5", {}), ("127.0.0.1", {"x-forwarded-for": "8.8.8.8"})):
        with pytest.raises(HTTPException):
            check_setup_allowed(SimpleNamespace(headers=hdrs, client=SimpleNamespace(host=host)))
