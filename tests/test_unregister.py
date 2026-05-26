from urllib.parse import quote


def test_unregister_succeeds_for_existing_student(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity = quote(activity_name, safe="")
    existing_email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/signup",
        params={"email": existing_email},
    )
    payload = response.json()
    activities_response = client.get("/activities")
    activities_payload = activities_response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Unregistered {existing_email} from {activity_name}"
    assert existing_email not in activities_payload[activity_name]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    unknown_activity = "Unknown Club"
    encoded_activity = quote(unknown_activity, safe="")
    student_email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/signup",
        params={"email": student_email},
    )
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_unregister_returns_404_for_student_not_signed_up(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity = quote(activity_name, safe="")
    missing_email = "absent.student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/signup",
        params={"email": missing_email},
    )
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Student not signed up for this activity"
