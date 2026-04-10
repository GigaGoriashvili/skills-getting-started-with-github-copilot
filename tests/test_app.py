def test_get_activities(client):
    # Arrange
    url = "/activities"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert "Chess Club" in body
    assert body["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
    assert isinstance(body["Chess Club"]["participants"], list)


def test_signup_adds_participant(client):
    # Arrange
    email = "teststudent@mergington.edu"
    activity_name = "Chess Club"
    signup_url = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(signup_url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    email = "duplicate@student.edu"
    activity_name = "Chess Club"
    signup_url = f"/activities/{activity_name}/signup"

    # Act
    first_response = client.post(signup_url, params={"email": email})
    second_response = client.post(signup_url, params={"email": email})

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up"


def test_unregister_removes_participant(client):
    # Arrange
    email = "michael@mergington.edu"
    activity_name = "Chess Club"
    delete_url = f"/activities/{activity_name}/participants"

    # Act
    response = client.delete(delete_url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]


def test_unregister_missing_participant_returns_404(client):
    # Arrange
    email = "missing@student.edu"
    activity_name = "Chess Club"
    delete_url = f"/activities/{activity_name}/participants"

    # Act
    response = client.delete(delete_url, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
