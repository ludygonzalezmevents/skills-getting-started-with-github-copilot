def test_signup_success(client):
    email = "taylor@mergington.edu"

    response = client.post("/activities/Chess%20Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}


def test_signup_duplicate_returns_400(client):
    existing_email = "michael@mergington.edu"

    response = client.post(
        "/activities/Chess%20Club/signup", params={"email": existing_email}
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student already signed up for this activity"
    }


def test_signup_unknown_activity_returns_404(client):
    response = client.post(
        "/activities/Unknown%20Club/signup", params={"email": "a@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_repeated_signup_attempts_only_first_succeeds(client):
    email = "repeat@mergington.edu"

    first = client.post("/activities/Drama%20Club/signup", params={"email": email})
    assert first.status_code == 200

    for _ in range(5):
        duplicate = client.post(
            "/activities/Drama%20Club/signup", params={"email": email}
        )
        assert duplicate.status_code == 400


def test_signup_does_not_enforce_capacity_in_current_behavior(client):
    # This captures existing behavior: max_participants is informational only.
    activity_name = "Micro Activity"
    client_email = "second@mergington.edu"

    from src.app import activities

    activities[activity_name] = {
        "description": "Tiny capacity activity",
        "schedule": "Mondays",
        "max_participants": 1,
        "participants": ["first@mergington.edu"],
    }

    response = client.post(
        "/activities/Micro%20Activity/signup", params={"email": client_email}
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {client_email} for {activity_name}"
    }