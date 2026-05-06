import pytest
from unittest.mock import patch

import app.service
import app.service as service

def test_validate_student_valid():
    student = {"name": "Dana", "age": 25}
    service.validate_student(student)  # לא אמור לזרוק שגיאה

def test_validate_student_invalid_age():
    student = {"name": "Dana", "age": 10}

    with pytest.raises(service.ServiceAppLogicError):
        service.validate_student(student)

def test_validate_student_invalid_name():
    student = {"name": "D", "age": 25}

    with pytest.raises(service.ServiceAppLogicError):
        service.validate_student(student)


# Add_student
def test_add_student_success():
    student = {"name": "Dana", "age": 25}

    with patch("app.service.db.add_student", return_value={"id": 1, **student}) as mock:
        result = service.add_student(student)

    assert result["id"] == 1
    mock.assert_called_once_with(student)


# Get_students
def test_get_student():
    fake_data = [{"id": 18, "name": "Dana", "age": 25}]

    with patch("app.service.db.get_student", return_value=fake_data) as mock:
        result = service.get_student(1)

    assert result == fake_data


# Get_student
def test_get_student_success():
    fake_student = {"id": 1, "name": "Dana", "age": 25}

    with patch("app.service.db.get_student", return_value=fake_student):
        result = service.get_student(1)

    assert result == fake_student


def test_get_student_not_found():
    with patch("app.service.db.get_student", side_effect=service.db.DbNotFoundError("not found")):
        with pytest.raises(service.ServiceNotFoundError):
            service.get_student(1)

#Update_student
def test_update_student_success():
    student = {"id": 19, "name": "Dana", "age": 30}

    with patch("app.service.db.update_student", return_value=student) as mock:
        result = service.update_student(student)

    assert result == student
    mock.assert_called_once_with(student)


def test_update_student_not_found():
    student = {"id": 1, "name": "Dana", "age": 30}

    with patch("app.service.db.update_student", side_effect=service.db.DbNotFoundError("not found")):
        with pytest.raises(service.ServiceNotFoundError):
            service.update_student(student)

# Delete_student
def test_delete_student_success():
    with patch("app.service.db.delete_student", return_value=True) as mock:
        result = service.delete_student(18)

    assert result is True
    mock.assert_called_once_with(18)


def test_delete_student_not_found():
    with patch("app.service.db.delete_student", side_effect=service.db.DbNotFoundError("not found")):
        with pytest.raises(service.ServiceNotFoundError):
            service.delete_student(1)


