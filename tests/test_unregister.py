def test_unregister_success(client):
    email = "michael@mergington.edu"

    response = client.delete("/activities/Chess%20Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Chess Club"}


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete(
        "/activities/Unknown%20Club/signup", params={"email": "a@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_non_participant_returns_404(client):
    response = client.delete(
        "/activities/Chess%20Club/signup", params={"email": "notenrolled@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Student is not signed up for this activity"
    }


def test_signup_then_unregister_flow(client):
    email = "flow@mergington.edu"

    signup_response = client.post("/activities/Robotics%20Club/signup", params={"email": email})
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        "/activities/Robotics%20Club/signup", params={"email": email}
    )
    assert unregister_response.status_code == 200

    repeated_unregister = client.delete(
        "/activities/Robotics%20Club/signup", params={"email": email}
    )
    assert repeated_unregister.status_code == 404