from src import app as app_module


def test_unregister_existing_participant_success(client):
    # Arrange
    activity_name = "Soccer Club"
    email = "ryan@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Unregistered {email} from {activity_name}"


def test_unregister_participant_not_found(client):
    # Arrange
    activity_name = "Soccer Club"
    email = "missing@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Participant not found in this activity"


def test_unregister_activity_not_found(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "someone@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_unregister_removes_from_participants(client):
    # Arrange
    activity_name = "Music Ensemble"
    email = "lucas@mergington.edu"
    assert email in app_module.activities[activity_name]["participants"]

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]
