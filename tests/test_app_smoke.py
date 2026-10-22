def test_import_app(client):
    import app

    assert hasattr(app, "app")


def test_api_version(client):
    r = client.get("/api/version")
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body.get("version"), str) and body["version"]


def test_unknown_route_not_found(client):
    assert client.get("/api/definitely-not-a-route").status_code in (404, 405)
