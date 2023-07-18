import pytest
from fastapi.testclient import TestClient
from main import app
from app.model.orm import User
from app.database import SessionLocal, engine
from app.authentication import pwd_context
from app.database import get_db

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        override_get_db = lambda: SessionLocal(bind=engine)
        app.dependency_overrides[get_db] = override_get_db

        username = "testuser"
        password = "testpassword"
        user = User(username=username, password=pwd_context.hash(password))
        db = SessionLocal(bind=engine)
        db.add(user)
        db.commit()
        db.refresh(user)

        yield test_client

        db.delete(user)
        db.commit()

def test_login_success(client):
    username = "testuser"
    password = "testpassword"

    response = client.post(
        "/login",
        data={"username": username, "password": password}
    )

    assert response.status_code == 200

    assert "access_token" in response.json()
    access_token = response.json()["access_token"]
