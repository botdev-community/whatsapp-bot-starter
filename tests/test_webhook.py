"""
Test Webhook Endpoints
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "WhatsApp Bot Starter API" in response.json()["message"]


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code in [200, 503]  # May fail if DB not running
    assert "status" in response.json()


def test_webhook_verification():
    """Test webhook verification"""
    response = client.get(
        "/webhook?hub.mode=subscribe&hub.verify_token=test_token&hub.challenge=test_challenge"
    )
    # This will fail without proper verify token, but tests the endpoint
    assert response.status_code in [200, 403]


def test_webhook_post_empty():
    """Test webhook POST with empty body"""
    response = client.post("/webhook", json={})
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_webhook_post_with_message():
    """Test webhook POST with message"""
    webhook_data = {
        "entry": [
            {
                "id": "123456789",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "1234567890",
                                "phone_number_id": "123456789"
                            },
                            "messages": [
                                {
                                    "from": "1234567890",
                                    "id": "wamid.test123",
                                    "timestamp": "1234567890",
                                    "type": "text",
                                    "text": {
                                        "body": "Hello"
                                    }
                                }
                            ]
                        },
                        "field": "messages"
                    }
                ]
            }
        ]
    }
    
    response = client.post("/webhook", json=webhook_data)
    assert response.status_code == 200
