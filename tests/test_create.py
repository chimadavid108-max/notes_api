def test_create_note_returns_201_and_body(client):
    response = client.post(
        "/notes",
        json={"title": "  Shopping list ", "content": "eggs, rice", "category": "home"},
    )

    assert response.status_code == 201
    data = response.json()
    assert isinstance(data["id"], int)
    assert data["title"] == "Shopping list"
    assert data["pinned"] is False
    assert "created_at" in data


def test_duplicate_title_different_case_returns_409(client, make_note):
    make_note()
    response = client.post(
        "/notes", json={"title": "SHOPPING LIST", "content": "bread, beans"}
    )

    assert response.status_code == 409
    assert "detail" in response.json()


def test_blank_title_returns_422(client):
    response = client.post("/notes", json={"title": "   ", "content": "x"})

    assert response.status_code == 422


def test_post_missing_content_returns_422(client):
    response = client.post("/notes", json={"title": "today's entry"})

    assert response.status_code == 422


def test_post_keeps_content_exactly_as_sent(client, make_note):
    note = make_note(content="Eggs  And RICE")
    data = client.get(f"/notes/{note['id']}").json()

    assert data["content"] == "Eggs  And RICE"
