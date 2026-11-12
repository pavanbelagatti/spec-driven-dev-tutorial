import pytest

from app import create_app
from app.email_sender import FakeEmailSender


@pytest.fixture
def sender():
    return FakeEmailSender()


@pytest.fixture
def client(sender):
    return create_app(email_sender=sender).test_client()


def test_health_defaults_to_dev_version(client, monkeypatch):
       monkeypatch.delenv("APP_VERSION", raising=False)
       assert client.get("/health").get_json() == {"status": "ok", "version": "dev"}


def test_health_reports_app_version(client, monkeypatch):
       monkeypatch.setenv("APP_VERSION", "1.2.3")
       assert client.get("/health").get_json() == {"status": "ok", "version": "1.2.3"}


def test_password_reset_sends_email(client, sender):
    resp = client.post("/password-reset", json={"email": "Ada@Example.com"})
    assert resp.status_code == 202
    assert sender.count("ada@example.com", "password_reset") == 1


def test_password_reset_rejects_invalid_email(client, sender):
    resp = client.post("/password-reset", json={"email": "not-an-email"})
    assert resp.status_code == 400
    assert sender.sent == []


def test_welcome_email_sends_email(client, sender):
    resp = client.post("/welcome-email", json={"email": "ada@example.com"})
    assert resp.status_code == 202
    assert sender.count("ada@example.com", "welcome") == 1


def test_password_reset_has_no_limit_yet(client, sender):
    """Documents today's bug: 10 requests send 10 emails.

    Whoever implements the rate-limit spec should replace this test
    with ones that check the new limit.
    """
    for _ in range(10):
        client.post("/password-reset", json={"email": "ada@example.com"})
    assert sender.count("ada@example.com", "password_reset") == 10
