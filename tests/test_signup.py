from src import app as app_module


def test_signup_new_student_success(client):
    # Arrange
    activity_name = "Programming Class"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {email} for {activity_name}"
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_student_already_signed_up(client):
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert "already signed up" in payload["detail"]


def test_signup_activity_not_found(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "anyone@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_signup_activity_full(client):
    # Arrange
    activity_name = "Chess Club"
    app_module.activities[activity_name]["participants"] = [
        f"student{i}@mergington.edu" for i in range(app_module.activities[activity_name]["max_participants"])
    ]

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": "overflow@mergington.edu"}
    )
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Activity is full"


def test_signup_updates_participants_list(client):
    # Arrange
    activity_name = "Robotics Club"
    email = "fresh@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in app_module.activities[activity_name]["participants"]
