from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_docs_accessible():
    response = client.get("/docs")

    assert response.status_code == 200


def test_openapi_accessible():
    response = client.get("/openapi.json")

    assert response.status_code == 200

def test_leaderboard_status_code():
    response = client.get("/leaderboard")
    assert response.status_code == 200


def test_get_games_status_code():
    response = client.get("/games")
    assert response.status_code == 200


def test_get_stats_status_code():
    response = client.get("/stats")
    assert response.status_code == 200


def test_auth_me_without_login_status_code():
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_login_bad_credentials_status_code():
    response = client.post(
        "/auth/login",
        json={
            "email": "notfound@example.com",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401


def test_create_stats_without_api_key_status_code():
    response = client.post(
        "/stats",
        json={
            "roblox_id": 123456,
            "pseudo": "TestPlayer",
            "kills": 0,
            "deaths": 0,
            "match_played": 0,
            "win_total": 0,
            "lose_total": 0,
        },
    )

    assert response.status_code in [401, 403]


def test_create_game_without_api_key_status_code():
    response = client.post(
        "/games",
        json={
            "map_name": "Arena",
            "rounds_total": 3,
            "red_score": 0,
            "blue_score": 0,
            "winner_team": None,
        },
    )

    assert response.status_code in [401, 403]


def test_create_round_without_api_key_status_code():
    response = client.post(
        "/rounds",
        json={
            "game_id": 1,
            "round_number": 1,
            "winner_team": None,
        },
    )

    assert response.status_code in [401, 403]
