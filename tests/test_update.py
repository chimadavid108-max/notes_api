import time


def test_patch_empty_body_returns_400(client, make_note):
    note = make_note()
    response = client.patch(f"/notes/{note["id"]}", json={})

    assert response.status_code == 400
    assert "detail" in response.json()


def test_patch_null_title_returns_422(client, make_note):
    note = make_note()
    response = client.patch(f"/notes/{note["id"]}", json={"title": None})

    assert response.status_code == 422


def test_patch_resending_own_title_returns_200(client, make_note):
    note = make_note()
    response = client.patch(f"/notes/{note["id"]}", json={"title": "Shopping list"})

    assert response.status_code == 200


def test_patch_changes_only_the_sent_fields(client, make_note):
    note = make_note(category="home", pinned=True)
    updated = client.patch(
        f"/notes/{note['id']}", json={"category": "food", "pinned": False}
    ).json()

    assert note["title"] == updated["title"]
    assert note["category"] != updated["category"]


def test_patch_category_null_clears_it(client, make_note):
    note = make_note(category="home")
    updated = client.patch(f"/notes/{note['id']}", json={"category": None}).json()

    assert note["category"] == "home"
    assert updated["category"] is None


def test_patch_rename_to_another_notes_title_returns_409(client, make_note):
    make_note()
    note = make_note(title="today's entry")
    response = client.patch(f"/notes/{note['id']}", json={"title": "shopping list"})

    assert response.status_code == 409


def test_patch_updates_updated_at_but_not_created_at(client, make_note):
    note = make_note()
    time.sleep(0.01)
    updated = client.patch(f"/notes/{note['id']}", json={"category": "cooking"}).json()

    assert note["created_at"] == updated["created_at"]
    assert note["updated_at"] != updated["updated_at"]
