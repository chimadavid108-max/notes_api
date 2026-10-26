def test_get_notes_pinned_comes_first(client, make_note):
    make_note(pinned=True)
    make_note(title="today's entry")
    response = client.get("/notes")

    assert response.json()[0]["id"] == 1


def test_query_search_work_and_not_found_return_empty_list(client, make_note):
    make_note()
    make_note(title="today's entry", content="I ate an egg yesterday")
    data1 = client.get("/notes?q=egg").json()
    data2 = client.get("/notes?q=999999").json()

    assert len(data1) == 2
    assert len(data2) == 0


def test_get_wronguse_limit_and_offset_return_422(client, make_note):
    make_note()
    response1 = client.get("/notes?limit=0")
    response2 = client.get("/notes?offset=-1")

    assert response1.status_code == 422
    assert response2.status_code == 422


def test_get_category_keyword_returns_note_with_keyword(client, make_note):
    make_note()
    make_note(title="today's entry", category="home")
    data = client.get("/notes?category=home").json()

    assert len(data) == 1 and data[0]["category"] == "home"


def test_get_missing_note_returns_404(client):
    response = client.get("/notes/999999")

    assert response.status_code == 404
    assert "detail" in response.json()


def test_get_note_by_id_returns_200_and_body(client, make_note):
    note = make_note(category="home")
    response = client.get(f"/notes/{note['id']}")
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == note["title"]
    assert data["content"] == note["content"]
    assert data["category"] == note["category"]


def test_limit_and_offset_slice_the_results(client, make_note):
    for i in range(1, 21):
        make_note(title=f"Day {i}")
    data = client.get("/notes?limit=5&offset=10").json()

    assert len(data) == 5
    assert data[0]["title"] == "Day 10"


def test_health_and_root_return_200(client):
    health = client.get("/health")
    root = client.get("/")

    assert health.json() == {"status": "ok"}
    assert health.status_code == 200
    assert root.status_code == 200
