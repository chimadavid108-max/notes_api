import time
import uuid

import requests

BASE = "http://127.0.0.1:8000"
TAG = uuid.uuid4().hex[:6]
http = requests.Session()
results = []


def url(path):
    return BASE + path


def body(r):
    try:
        return r.json()
    except ValueError:
        return {}


def ids(r):
    try:
        return [n["id"] for n in r.json()]
    except (ValueError, TypeError, KeyError):
        return []


def expect(label, condition, detail=""):
    results.append(bool(condition))
    print(f"{'✅' if condition else '❌'} {label}")
    if not condition and detail:
        print(f"   → {detail[:300]}")


def status(label, r, expected, need=False):
    expect(f"{label} (got {r.status_code}, want {expected})",
           r.status_code == expected, r.text)
    if need and r.status_code != expected:
        raise SystemExit(f"Stop: fix '{label}' first, later checks need it.")
    return r


try:
    http.get(url("/health"), timeout=3)
except requests.ConnectionError:
    raise SystemExit("Server not running. Start: uvicorn main:app --reload")

title = f"Shopping list {TAG}"

# 1
r = status("1 create note", http.post(url("/notes"), json={
    "title": title, "content": f"eggs, rice {TAG}", "category": "home"}), 201, need=True)
note = body(r)
nid = note["id"]
expect("1 body: id, timestamps, pinned false, title unchanged",
       {"id", "created_at", "updated_at"} <= note.keys()
       and note["pinned"] is False and note["title"] == title, str(note))

# 2, 3, 4
status("2 same title, other case", http.post(url("/notes"),
       json={"title": title.upper(), "content": "again"}), 409)
status("3 title of only spaces", http.post(url("/notes"),
       json={"title": "     ", "content": "x"}), 422)
status("4 no content", http.post(url("/notes"),
       json={"title": f"No content {TAG}"}), 422)

# 5, 6
r = status("5 search by word", http.get(url("/notes"),
           params={"q": TAG, "limit": 100}), 200)
expect("5 note is in results", nid in ids(r), r.text)
r = status("6 search with no match", http.get(url("/notes"),
           params={"q": f"zzzz{TAG}"}), 200)
expect("6 result is []", body(r) == [], r.text)

# 7
status("7a limit=0", http.get(url("/notes"), params={"limit": 0}), 422)
status("7b offset=-1", http.get(url("/notes"), params={"offset": -1}), 422)

# 8
r = status("8 create second (newer) note", http.post(url("/notes"), json={
    "title": f"Second note {TAG}", "content": f"newer {TAG}"}), 201, need=True)
nid2 = body(r)["id"]
status("8 pin the older note", http.patch(url(f"/notes/{nid}"),
       json={"pinned": True}), 200)
r = http.get(url("/notes"), params={"q": TAG, "limit": 100})
expect("8 pinned older note is first", ids(r)[:1] == [nid], f"order: {ids(r)}")

# 9
r = status("9 missing note", http.get(url("/notes/999999")), 404)
expect("9 body has detail", "detail" in body(r), r.text)

# 10
status("10a PATCH {}", http.patch(url(f"/notes/{nid}"), json={}), 400)
status("10b PATCH title null", http.patch(url(f"/notes/{nid}"),
       json={"title": None}), 422)
r = status("10c PATCH category null", http.patch(url(f"/notes/{nid}"),
           json={"category": None}), 200)
expect("10c category is now null", r.status_code == 200
       and body(r).get("category") is None, r.text)

# 11
status("11a rename to another note's title", http.patch(url(f"/notes/{nid}"),
       json={"title": f"Second note {TAG}"}), 409)
status("11b re-send own title", http.patch(url(f"/notes/{nid}"),
       json={"title": title}), 200)

# 12
before = body(http.get(url(f"/notes/{nid}")))
time.sleep(0.05)
after = body(http.patch(url(f"/notes/{nid}"), json={"content": f"changed {TAG}"}))
expect("12 updated_at changed",
       after.get("updated_at") != before.get("updated_at"), f"{before} / {after}")
expect("12 created_at unchanged",
       after.get("created_at") == before.get("created_at"), f"{before} / {after}")

# 14 (needs the note to still exist, so it runs before the deletes)
input("\n14: Stop the server (Ctrl+C), start it again, then press Enter... ")
r = status("14 note survived restart", requests.get(url(f"/notes/{nid}")), 200)
expect("14 same title", body(r).get("title") == title, r.text)

# 13
r = status("13a delete", http.delete(url(f"/notes/{nid}")), 204)
expect("13a body is empty", r.content == b"", repr(r.content))
status("13b delete again", http.delete(url(f"/notes/{nid}")), 404)
http.delete(url(f"/notes/{nid2}"))   # clean up

print(f"\n{sum(results)}/{len(results)} checks passed")
