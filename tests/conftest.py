
#alll fixures are inside it
import pytest
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base,get_db
from app.main import app
from fastapi.testclient import TestClient
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


testingSessionLocal = sessionmaker(autocommit = False,autoflush=False,bind = engine)


# scope="module"
@pytest.fixture() # by default for every function so chnage property to module
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = testingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture() # by default for every function
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    # command.upgrade("head")
    # command.upgrade("base")
    app.dependency_overrides[get_db] = override_get_db
    yield  TestClient(app)
    
    #run code after this

  
@pytest.fixture
def test_user(client):
    user_data = {"email":"user1@email.com","password":"123"}
    res = client.post("/users/",json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = "123"
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "sanjeev123@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user
 

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user['id']})


@pytest.fixture
def authorized_client(client,token):
    client.headers = {**client.headers,
                      "Authorization":f"Bearer {token}"
    }
    return client



@pytest.fixture
def test_posts(test_user, session,test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }
    , {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
      }
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']), models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])
    session.commit()
    posts = session.query(models.Post).all()
    return posts