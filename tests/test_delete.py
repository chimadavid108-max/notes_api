def test_delete_twice(client, make_note):
    note = make_note()
    response1 = client.delete(f"/notes/{note["id"]}")
    response2 = client.delete(f"/notes/{note["id"]}")

    assert response1.status_code == 204
    assert response2.status_code == 404


def test_delete_returns_empty_body_and_note_is_gone(client, make_note):
    note = make_note()
    data1 = client.delete(f"/notes/{note['id']}")
    data2 = client.get(f"/notes/{note['id']}")

    assert data1.status_code == 204
    assert data1.content == b""
    assert data2.status_code == 404
