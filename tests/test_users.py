# tests/test_users.py
import random


# --- Tests ---

def test_home(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"message": "Welcome to the API!"}

def test_create_user(client):
    email = f"bob{random.randint(1,10000)}@example.com"
    user_data = {"name": "Bob", "email": email, "password": "1234"}
    res = client.post("/users/", json=user_data)
    assert res.status_code in [200, 201]
    assert res.json()["email"] == email

def test_get_users(client, test_user):
    res = client.get("/users/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert any(u["id"] == test_user["id"] for u in res.json())

def test_get_user_by_id(client, test_user):
    user_id = test_user["id"]
    res = client.get(f"/users/{user_id}")
    assert res.status_code == 200
    assert res.json()["name"] == test_user["name"]

def test_update_user(client, test_user):
    user_id = test_user["id"]
    updated_data = {"name": "Alice Updated"}
    res = client.put(f"/users/{user_id}", json=updated_data)
    assert res.status_code == 200
    assert res.json()["name"] == "Alice Updated"

def test_delete_user(client, test_user):
    user_id = test_user["id"]
    res = client.delete(f"/users/{user_id}")
    assert res.status_code == 200
    assert "detail" in res.json()
    # Verify user no longer exists
    res2 = client.get(f"/users/{user_id}")
    assert res2.status_code == 404
