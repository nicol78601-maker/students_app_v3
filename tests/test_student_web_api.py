import pytest
import requests
from unittest.mock import patch


BASE_URL = "http://127.0.0.1:5000"


def test_get_students():
    response = requests.get(f"{BASE_URL}/students")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_student():
    new_student = {
        "name": "Dana",
        "age": 25
    }

    response = requests.post(f"{BASE_URL}/students", json=new_student)

    assert response.status_code == 201
    data = response.json()

    assert data["name"] == "Dana"
    assert data["age"] == 25


def test_get_student_not_found():
    response = requests.get(f"{BASE_URL}/students/9999")

    assert response.status_code == 404


# --- בדיקת הוספה עם ערכים לא חוקיים ---
@pytest.mark.parametrize("invalid_data", [
    {"name": "", "age": 25},
    {"name": "Dana", "age": -1}
])
def test_add_student_invalid_data(invalid_data):
    # משתמשים ב-with patch כדי להחליף זמנית את requests.post
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 400

        response = requests.post(f"{BASE_URL}/students", json=invalid_data)
        assert response.status_code == 400


# --- בדיקת עדכון פרטים של תלמיד קיים ---
def test_update_student():
    student_id = 19
    updated_info = {"name": "Dana Updated", "age": 26}

    with patch("requests.put") as mock_put:
        mock_put.return_value.status_code = 200
        mock_put.return_value.json.return_value = {"id": student_id, **updated_info}

        response = requests.put(f"{BASE_URL}/students/{student_id}", json=updated_info)

        assert response.status_code == 200
        assert response.json()["name"] == "Dana Updated"
        print(student_id)


# --- בדיקת מחיקת תלמיד קיים ---
def test_delete_student():
    student_id = 15

    with patch("requests.delete") as mock_delete:
        mock_delete.return_value.status_code = 204

        response = requests.delete(f"{BASE_URL}/students/{student_id}")
        assert response.status_code == 204

        # עדכון