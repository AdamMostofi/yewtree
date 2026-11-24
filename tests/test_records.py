"""Generic records (0.3.0): a caller-defined type, versioned fields, indexed lookups, recorded links.

The engine stores, versions, indexes and links records; it never interprets them. ADAM keeps its facts,
derivations and sources this way (ADAM Stage 4.1, decision DSM.1).
"""
from __future__ import annotations

import pytest

from agent_memory import Store
from agent_memory.schema import SchemaError

S, W = "s1", "adam"


def fact(subject, predicate, obj, **extra):
    return {"subject": subject, "predicate": predicate, "object": obj, **extra}


def test_a_record_is_stored_versioned_and_never_overwritten(store):
    rid = store.put_record("adam.fact", "socrates|is|man", fact("socrates", "is", "man", confidence=0.9), S, W,
                           index=["subject"])
    assert rid == Store.record_id("adam.fact", "socrates|is|man")
    store.put_record("adam.fact", "socrates|is|man", fact("socrates", "is", "man", confidence=1.0), S, W,
                     index=["subject"])
    rec = store.get_record(rid)
    assert rec["version"] == 2 and rec["fields"]["confidence"] == 1.0 and rec["status"] == "current"
    assert [v["fields"]["confidence"] for v in store.record_history(rid)] == [0.9, 1.0]


def test_a_put_that_changes_nothing_stores_nothing(store):
    store.put_record("adam.fact", "k", fact("a", "b", "c"), S, W)
    before = len(list(store.events()))
    store.put_record("adam.fact", "k", fact("a", "b", "c"), S, W)
    assert len(list(store.events())) == before
    assert store.get_record(Store.record_id("adam.fact", "k"))["version"] == 1


def test_a_caller_that_tracks_changes_itself_can_skip_the_unchanged_check(store):
    item = {"type": "adam.fact", "key": "k", "fields": fact("a", "b", "c")}
    store.put_records([item], S, W)
    store.put_records([item], S, W)                          # checked: skipped
    store.put_records([item], S, W, check_unchanged=False)   # not checked: a new version
    assert store.get_record(Store.record_id("adam.fact", "k"))["version"] == 2


def test_records_are_found_through_their_indexed_fields(store):
    for s, p, o in (("socrates", "is", "man"), ("plato", "is", "man"), ("socrates", "teaches", "plato")):
        store.put_record("adam.fact", f"{s}|{p}|{o}", fact(s, p, o), S, W, index=["subject", "predicate", "object"])
    assert {r["key"] for r in store.find_records("adam.fact", subject="socrates")} == {"socrates|is|man",
                                                                                       "socrates|teaches|plato"}
    assert [r["key"] for r in store.find_records("adam.fact", subject="socrates", predicate="is")] == \
        ["socrates|is|man"]
    assert store.find_records("adam.fact", subject="nobody") == []
    assert [r["key"] for r in store.records("adam.fact")] == ["socrates|is|man", "plato|is|man",
                                                              "socrates|teaches|plato"]


def test_a_retired_record_keeps_its_history_and_can_come_back(store):
    rid = store.put_record("adam.fact", "k", fact("a", "b", "c"), S, W, index=["subject"])
    store.retire_record(rid, S, W, reason="superseded")
    assert store.get_record(rid)["status"] == "retired"
    assert store.find_records("adam.fact", subject="a") == [] and store.records("adam.fact") == []
    assert [r["id"] for r in store.records("adam.fact", include_retired=True)] == [rid]
    store.put_record("adam.fact", "k", fact("a", "b", "c"), S, W, index=["subject"])
    assert store.get_record(rid)["status"] == "current"
    assert [r["id"] for r in store.find_records("adam.fact", subject="a")] == [rid]


def test_links_between_records_can_carry_a_recorded_basis_and_attributes(store):
    premise = store.put_record("adam.fact", "p", fact("socrates", "is", "man"), S, W)
    conclusion = store.put_record("adam.fact", "c", fact("socrates", "is", "mortal"), S, W)
    store.relate(conclusion, premise, "based_on", S, W, basis="recorded",
                 attrs={"rule": "syllogism", "rule_version": "1", "confidence": 1.0})
    (edge,) = store.record_edges(conclusion, types=["based_on"])
    assert edge["to"] == premise and edge["basis"] == "recorded"
    assert edge["attrs"]["rule"] == "syllogism" and edge["attrs"]["confidence"] == 1.0
    assert store.record_edges(premise, direction="in")[0]["from"] == conclusion


def test_a_body_is_archived_encrypted_and_restored_exactly(store):
    text = "Socrates is a man.\nAll men are mortal.\n".encode()
    rid = store.put_record("adam.source", "plato/apology.md", {"title": "Apology"}, S, W, body=text)
    assert store.get_record(rid)["has_body"] and store.record_body(rid) == text
    raw = b"".join(p.read_bytes() for p in store.path.rglob("*") if p.is_file() and "objects" in p.parts)
    assert b"All men are mortal" not in raw


def test_a_batch_is_one_transaction(store):
    ids = store.put_records([{"type": "adam.fact", "key": f"k{i}", "fields": fact("s", "p", str(i)),
                              "index": ["subject"]} for i in range(50)], S, W)
    assert len(set(ids)) == 50 and len(store.find_records("adam.fact", subject="s")) == 50
    with pytest.raises(SchemaError):    # one bad item refuses the whole batch
        store.put_records([{"type": "adam.fact", "key": "ok", "fields": fact("x", "p", "o")},
                           {"type": "Bad Type", "key": "no", "fields": {}}], S, W)
    assert store.get_record(Store.record_id("adam.fact", "ok")) is None


def test_a_batch_can_link_records_it_creates(store):
    p, c = Store.record_id("adam.fact", "p"), Store.record_id("adam.fact", "c")
    store.put_records([{"type": "adam.fact", "key": "p", "fields": fact("a", "is", "b")},
                       {"type": "adam.fact", "key": "c", "fields": fact("a", "is", "c")}], S, W,
                      links=[{"from": c, "to": p, "type": "based_on", "basis": "recorded", "attrs": {"rule": "r"}}])
    assert store.record_edges(c)[0]["to"] == p
    with pytest.raises(SchemaError):    # a link to a record that doesn't exist refuses the whole batch
        store.put_records([{"type": "adam.fact", "key": "x", "fields": fact("x", "is", "y")}], S, W,
                          links=[{"from": Store.record_id("adam.fact", "x"), "to": "record:adam.fact:nope",
                                  "type": "based_on", "basis": "recorded"}])
    assert store.get_record(Store.record_id("adam.fact", "x")) is None


def test_bad_records_are_refused(store):
    for args in (("Bad Type", "k", {}), ("adam.fact", "", {}), ("adam.fact", "k", "not a dict")):
        with pytest.raises(SchemaError):
            store.put_record(*args, S, W)
    with pytest.raises(SchemaError):
        store.put_record("adam.fact", "k", {"subject": ["a", "list"]}, S, W, index=["subject"])
    with pytest.raises(SchemaError):
        store.put_record("adam.fact", "k", {"subject": "a"}, S, W, index=["missing"])
    with pytest.raises(SchemaError):
        store.retire_record(Store.record_id("adam.fact", "never"), S, W)


def test_records_survive_reopening_verify_and_a_rebuild(store, tmp_path):
    a = store.put_record("adam.fact", "a", fact("a", "is", "b"), S, W, index=["subject"])
    b = store.put_record("adam.fact", "b", fact("b", "is", "c"), S, W, index=["subject"])
    store.relate(b, a, "based_on", S, W, basis="recorded", attrs={"rule": "r"})
    store.retire_record(a, S, W)
    assert store.verify(full=True)["ok"]                      # the record tables match a rebuild from the log
    store.rebuild_derived()
    again = Store(store.path, project_id="test-project", min_free_bytes=0)
    assert again.get_record(a)["status"] == "retired" and again.find_records("adam.fact", subject="b")[0]["id"] == b
    assert again.record_edges(b)[0]["attrs"]["rule"] == "r"


def test_reopening_a_store_with_the_same_profiles_writes_nothing(tmp_path):
    """An application that opens its store on every start (ADAM does) must not change it by opening it."""
    path = tmp_path / "app.store"
    first = Store(path, project_id="app", profiles=["generic"])
    first.put_record("app.item", "k", {"v": 1}, S, W)
    Store(path, project_id="app", profiles=["generic"])
    before = (path / "memory.db").read_bytes()
    Store(path, project_id="app", profiles=["generic"])
    assert (path / "memory.db").read_bytes() == before
