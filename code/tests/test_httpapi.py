import requests
import logging
import uuid

logging.basicConfig(level=logging.DEBUG)

URL = 'http://localhost'
pref_url = lambda uid, pref="" : f"{URL}/{uid}/{pref}" if pref else f"{URL}/{uid}"
new_id = lambda: str(uuid.uuid1())

def test_can_get_added_pref():
    prefUrl = pref_url(new_id(), "pref1")
    expected = ["set1", "set2"]
    assert requests.put(prefUrl, json=expected).status_code == 200
    assert requests.get(prefUrl).json() == expected 

def test_same_preference_is_overridden():
    prefUrl = pref_url(new_id(), "pref1")
    prefs = [["set1", "set2", "val3"], ["pref2", "val1", "val2"]]
    for pref in prefs:
        assert requests.put(prefUrl, json=pref).status_code == 200
    assert requests.get(prefUrl).json() == prefs[-1]

def test_all_prefs_are_saved():
    uid = new_id()
    expected = { "pref1": ["set1", "set2", "val3"], "pref2": ["val1", "val2"]}
    for (k,v) in expected.items():
        assert requests.put(pref_url(uid, k), json=v).status_code == 200
    assert requests.get(pref_url(uid)).json() == expected 

def test_empty_response_for_non_existent_user():
    resp = requests.get(pref_url(new_id()))
    assert resp.status_code == 200 and not resp.json()

def test_empty_response_for_non_existent_pref():
    uid = new_id()
    assert requests.put(pref_url(uid, "pref1"), json="").status_code == 200
    resp = requests.get(pref_url(uid, "--- non existent ---"))
    assert resp.status_code == 200 and not resp.json()
