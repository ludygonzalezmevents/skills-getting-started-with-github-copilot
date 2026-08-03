def test_get_activities_returns_expected_structure(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert "Chess Club" in payload

    chess_club = payload["Chess Club"]
    assert set(chess_club.keys()) == {
        "description",
        "schedule",
        "max_participants",
        "participants",
    }
    assert isinstance(chess_club["participants"], list)


def test_get_activities_shows_current_participants_after_mutation(client):
    new_email = "new.student@mergington.edu"
    signup_response = client.post(
        "/activities/Chess%20Club/signup", params={"email": new_email}
    )
    assert signup_response.status_code == 200

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200

    payload = activities_response.json()
    assert new_email in payload["Chess Club"]["participants"]