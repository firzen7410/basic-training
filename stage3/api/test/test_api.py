import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"


def test_create_post():
    data = {
        "url": "https://pytestB.com",
        "author": "fromTest"
    }
    resp = requests.post(f"{BASE_URL}/api/posts", json=data)

    assert resp.status_code == 200


def test_get_posts():
    resp = requests.get(f"{BASE_URL}/api/posts")
    assert resp.status_code == 200


def test_update_post():
    data = {
        "url": "https://pytestI.com",
    }
    resp = requests.put(f"{BASE_URL}/api/posts/20328", json=data)
    assert resp.status_code == 200


def test_delete_post():
    resp = requests.delete(f"{BASE_URL}/api/posts/20328")
    assert resp.status_code == 200
