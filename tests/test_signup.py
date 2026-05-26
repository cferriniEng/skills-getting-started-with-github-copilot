from urllib.parse import quote


def test_signup_succeeds_for_new_student(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity = quote(activity_name, safe="")
    student_email = "new.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{encoded_activity}/signup",
        params={"email": student_email},
    )
    payload = response.json()
    activities_response = client.get("/activities")
    activities_payload = activities_response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {student_email} for {activity_name}"
    assert student_email in activities_payload[activity_name]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    unknown_activity = "Unknown Club"
    encoded_activity = quote(unknown_activity, safe="")
    student_email = "ghost.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{encoded_activity}/signup",
        params={"email": student_email},
    )
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_student(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity = quote(activity_name, safe="")
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{encoded_activity}/signup",
        params={"email": existing_email},
    )
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up for this activity"
