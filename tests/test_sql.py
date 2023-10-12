from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/hi")
    assert response.status_code == 200
    assert response.json() == {"message": "Capybaramen wish you a good day!"}

# def test_create_user():
#     # case 1: 成功建立
#     payload = {
#         "username": "Wyatt",
#         "email": "wyatt@test.com"
#     }
#
#     create_user_response = client.post("/user", json=payload)
#     assert create_user_response.status_code == 200
#     user_id = create_user_response.json()["User"]["id"]
#
#     get_user_response = client.get(f"/users/{user_id}")
#
#     assert get_user_response.status_code == 200
#     assert get_user_response.json() == {
#         "id": user_id,
#         "username": "Wyatt",
#         "email": "wyatt@test.com"
#     }
#
#     # case 2: payload 資料不全
#     payload = {
#         "username": "Wyatt"
#     }
#
#     create_user_response = client.post("/user", json=payload)
#
#     assert create_user_response.status_code == 422
