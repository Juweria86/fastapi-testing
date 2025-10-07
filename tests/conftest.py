import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
import random

# --- Database config ---
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost/test_db"

# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Setup & Teardown the test database ---
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    This fixture runs once per test session.
    It creates all tables before tests, and drops them after.
    """
    print("\n[SETUP] Creating test database schema...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    print("\n[TEARDOWN] Dropping test database schema...")
    Base.metadata.drop_all(bind=engine)


# --- Dependency override for FastAPI ---
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# --- Test client fixture ---

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def test_user(client):
    """Creates a test user (if not exists) and returns it."""
    email = f"alice{random.randint(1,10000)}@example.com"
    user_data = {"name": "Alice", "email": email, "password": "1234"}
    res = client.post("/users/", json=user_data)
    assert res.status_code in [200, 201]
    return res.json()


