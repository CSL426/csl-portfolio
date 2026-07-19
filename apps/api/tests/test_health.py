from fastapi.testclient import TestClient
from server.main import app


def test_health_endpoint() -> None:
    client = TestClient(app)
    r = client.get("/api/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "echo" in body["agents"]


def test_chat_endpoint_echo() -> None:
    client = TestClient(app)
    r = client.post("/api/chat", json={"message": "hi", "agent": "echo"})
    assert r.status_code == 200
    body = r.json()
    assert body["agent"] == "echo"
    assert "hi" in body["text"]


def test_chat_endpoint_unknown_agent() -> None:
    client = TestClient(app)
    r = client.post("/api/chat", json={"message": "hi", "agent": "does-not-exist"})
    assert r.status_code == 404


def test_line_webhook_unconfigured_returns_503() -> None:
    client = TestClient(app)
    r = client.post(
        "/api/webhook/line",
        content="{}",
        headers={"x-line-signature": "fake"},
    )
    assert r.status_code == 503
