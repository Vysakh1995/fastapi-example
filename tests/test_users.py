from app import schemas
import pytest
# call pytest -v -s .\tests\test_users.py --disable-warnings
from jose import jwt
from app.config import settings




# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.status_code == 200
#     assert res.json().get('message') == "Hello World"

def test_create_user(client):
    res = client.post("/users/",json={"email":"user@email.com","password":"123"})
    print(res.json())
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "user@email.com"
    assert res.status_code == 201


def test_login(client,test_user):
    res = client.post("/login/",data={"username":test_user['email'],"password":test_user['password']})
    print(res.json())
    login_res = schemas.Token(**res.json())
    payload =  jwt.decode(login_res.access_token,settings.secret_key,algorithms=[settings.algorithm])
    id  = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'Bearer'
    assert res.status_code ==200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login(client,test_user,email, password, status_code):
    res = client.post('/login',data={"username":email,"password":password})

    assert res.status_code == status_code
    
