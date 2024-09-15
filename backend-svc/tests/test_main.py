from fastapi.testclient import TestClient
import io
from main import app

client = TestClient(app)

def test_read_users_void():
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []

def test_upload_user():
    hex_string = "ffd8ffe000104a46494600010101004800480000ffdb004300030202020202030202020303030304060404040404080606050609080a0a090809090a0c0f0c0a0b0e0b09090d110d0e0f101011100a0c12131210130f101010ffc9000b080001000101011100ffcc000600101005ffda0008010100003f00d2cf20ffd9"
    image_bytes = bytes.fromhex(hex_string)

    form_data = {
        'name': 'Pippo234',
        'email': 'pluto@no.mail',
    }

    files = {
        'avatar': ('avatar.jpg', image_bytes, 'image/jpeg')
    }
    response = client.post("/users", files=files, data=form_data)
    assert response.status_code == 201

def test_read_users_after_post():
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == [{'avatar_url': 'https://svc-bucket.s3.us-east-1.amazonaws.com/avatar.jpg', 'email': 'pluto@no.mail', 'name': 'Pippo234'}]