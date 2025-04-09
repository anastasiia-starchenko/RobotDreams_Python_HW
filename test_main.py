import pytest
from fastapi.testclient import TestClient
from fastapi_project.main import app
from fastapi_project import crud, models
from fastapi_project.database import SessionLocal, engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi_project.models import Base

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "postgresql://anastasiistarchenko:Qwerty@localhost:5432/test_lms_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_user(setup_database):
    response = client.post("/users/", json={
        "username": "test_user",
        "email": "testuser@example.com",
        "hashed_password": "testpassword"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "test_user"
    assert response.json()["email"] == "testuser@example.com"


def test_get_users(setup_database):
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_user(setup_database):

    user_data = {
        "username": "test_user_2",
        "email": "testuser2@example.com",
        "hashed_password": "testpassword2"
    }
    client.post("/users/", json=user_data)

    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["username"] == "test_user_2"
    assert response.json()["email"] == "testuser2@example.com"


def test_create_course(setup_database):
    response = client.post("/courses/", json={
        "name": "Test Course",
        "description": "This is a test course.",
        "user_id": 1
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Test Course"
    assert response.json()["description"] == "This is a test course."


def test_get_courses(setup_database):
    response = client.get("/courses/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_course(setup_database):

    course_data = {
        "name": "Test Course 2",
        "description": "This is another test course.",
        "user_id": 1
    }
    client.post("/courses/", json=course_data)

    response = client.get("/courses/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Course 2"
    assert response.json()["description"] == "This is another test course."