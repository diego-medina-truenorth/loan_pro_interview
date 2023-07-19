import pytest
from fastapi.testclient import TestClient
from main import app
from app.model.orm import User
from app.database import SessionLocal, engine
from app.authentication import pwd_context
from app.database import get_db

from fastapi.testclient import TestClient



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

client = TestClient(app)

def test_calculator_addition():
    payload = {"operation_type": "addition", "amount": 5}
    response = client.post("/calculator/addition", json=payload)
    assert response.status_code == 200
    assert response.json() == {"result": 15} 

def test_calculator_subtraction():
    payload = {"operation_type": "subtraction", "amount": 3}
    response = client.post("/calculator/subtraction", json=payload)
    assert response.status_code == 200
    assert response.json() == {"result": 7}

