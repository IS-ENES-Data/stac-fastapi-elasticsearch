# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '30 Nov 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

import pytest
import json
import os
from elasticsearch import NotFoundError
from stac_fastapi.types.errors import ConflictError

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "../../stac_fastapi/test_data")

def load_file(filename: str):
    with open(os.path.join(TEST_DATA_DIR, filename)) as file:
        return json.load(file)

def test_get_collection(app_client):
    coll_id = "Fj3reHsBhuk7QqVbt7P-"
    resp = app_client.get(f"/collections/{coll_id}")
    resp_json = resp.json()

    assert resp_json["id"] == coll_id

    # check a few keys
    assert resp_json.get("title") == "CMIP6"
    assert resp_json.get("summaries").get("member") == ['r10i1p1f1', 'r1i1p1f1']
    assert resp_json.get("summaries").get("version") == ['v20170706', 'v20180305', 'v20190528']

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
def test_create_new_collection(app_client):
    data = load_file("collections/cmip6/collections.json")

    new_coll = data[0].copy()["_source"]
    new_id = 'Fj3rerRFgu7QqVbt7P-'
    new_coll["id"] = new_id
    resp_json = app_client.post(f"/collections", json=new_coll).json()

    # response appears to be correct
    assert resp_json["id"] == new_id

    # get new collection
    coll = app_client.get(f"/collections/{new_id}").json()
    assert coll["id"] == new_id

    # check a few keys
    assert resp_json.get("title") == "CMIP6"
    assert resp_json.get("summaries").get("member") == ['r10i1p1f1', 'r1i1p1f1']
    assert resp_json.get("summaries").get("version") == ['v20170706', 'v20180305', 'v20190528']


def test_create_collection_already_exists(app_client):
    data = load_file("collections/cmip6/collections.json")[0]
    data["id"] = 'Fj3reHsBhuk7QqVbt7P-'

    resp = app_client.post(f"/collections", json=data)
    assert resp.status_code == 409


def test_update_collection(app_client):
    data = load_file("collections/cmip6/collections.json")[0]["_source"]
    coll_id = "Fj3rerRFgu7QqVbt7P-"

    # check collection exists
    resp_json = app_client.get(f"/collections/{coll_id}").json()
    assert resp_json["id"] == coll_id

    # update with new keyword
    data["keywords"].append("new_keyword")
    data['id'] = coll_id
    app_client.put(f"/collections", json=data)

    # check if collection has been updated
    resp_json = app_client.get(f"/collections/{coll_id}").json()
    assert "new_keyword" in resp_json.get("keywords")


def test_get_collection_does_not_exist(app_client):
    coll_id = "Fj3reHsriut7QqVb34f*"
    with pytest.raises(NotFoundError):
        app_client.get(f"/collections/{coll_id}")
 

def test_get_item(app_client):
    coll_id = "Fj3reHsBhuk7QqVbt7P-"
    item_id = "8c462277a5877d4adc00642e2a78af6e"

    resp = app_client.get(f"/collections/{coll_id}/items/{item_id}")
    resp_json = resp.json()
    assert resp_json.get('collection') == coll_id
    assert resp_json.get("id") == item_id

    # check a few keys
    assert resp_json.get('properties').get('mip_era') == 'CMIP6'
    assert resp_json.get('properties').get('data_provider') == 'PANGEO'
    assert resp_json.get('properties').get('variable_id') == 'evspsbl'


def test_get_collection_items(app_client):
    coll_id = "Fj3reHsBhuk7QqVbt7P-"
    resp = app_client.get(f"/collections/{coll_id}/items")
    resp_json = resp.json()

    assert resp_json['context']["returned"] ==  resp_json["context"]["matched"] == 2

    for item in resp_json['features']:
        assert item["collection"] == coll_id


def test_create_item(app_client):
    data = load_file("collections/cmip6/items.json")
    coll_id = "Fj3rerRFgu7QqVbt7P-"

    new_item = data[0].copy()["_source"]
    new_id = 'e7654b64ea5a3efe7a2c65433a798246'
    new_item["id"] = new_id
    new_item["collection"] = coll_id
    new_item.pop("collection_id")
    # new_item["item_id"] = new_id

    resp_json = app_client.post(f"/collections/{coll_id}/items", json=new_item).json()
    assert resp_json["id"] == new_id
    assert resp_json.get("collection") == coll_id

    # get new item
    item = app_client.get(f"/collections/{coll_id}/items/{new_id}").json()

    assert item.get("id") == new_id
    assert item.get('collection') == coll_id

    # check a few keys
    assert item.get('properties').get('mip_era') == 'CMIP6'
    assert item.get('properties').get('data_provider') == 'PANGEO'
    assert item.get('properties').get('variable_id') == 'va'


def test_create_item_already_exists(app_client):
    data = load_file("collections/cmip6/items.json")[0]
    data["id"] = "a3641b64ea5a3aba7a2c40663e798246"
    coll_id = "Fj3reHsBhuk7QqVbt7P-"

    resp = app_client.post(f"/collections/{coll_id}/items", json=data)
    assert resp.status_code == 409


def test_update_item(app_client):
    data = load_file("collections/cmip6/items.json")[0]["_source"]
    coll_id = "Fj3rerRFgu7QqVbt7P-"
    item_id = "e7654b64ea5a3efe7a2c65433a798246"
    data["collection"] = coll_id
    data["id"] = item_id
    data.pop("collection_id")

    # check items exists
    resp_json = app_client.get(f"/collections/{coll_id}/items/{item_id}").json()
    assert resp_json["id"] == item_id
    assert resp_json["collection"] == coll_id

    # update with new property
    data["properties"]["foo"] = "bar"
    app_client.put(f"/collections/{coll_id}/items", json=data)
    
    # check if item has been updated
    resp_json = app_client.get(f"/collections/{coll_id}/items/{item_id}").json()
    assert resp_json.get("properties").get("foo") == "bar"


def test_delete_item(app_client):
    coll_id = "Fj3rerRFgu7QqVbt7P-"
    item_id = "e7654b64ea5a3efe7a2c65433a798246"

    # check the item exists
    resp_json = app_client.get(f"/collections/{coll_id}/items/{item_id}").json()
    assert resp_json["id"] == item_id

    # delete it
    app_client.delete(f"/collections/{coll_id}/items/{item_id}")

    resp = app_client.get(f"/collections/{coll_id}/items/{item_id}")
    assert resp.status_code == 404


def test_delete_collection(app_client):
    coll_id = 'Fj3rerRFgu7QqVbt7P-' # change this

    # check the collection exists
    resp_json = app_client.get(f"/collections/{coll_id}").json()
    assert resp_json["id"] == coll_id

    # delete it
    app_client.delete(f"/collections/{coll_id}")

    # try and get collection again, should raise exception
    with pytest.raises(NotFoundError):
        app_client.get(f"/collections/{coll_id}").json()


# other tests that could be added
# test_create_duplicate_item_different_collections
# test_bulk_item_insert
# test_bulk_item_inserted_chunked
# test_landing_page_no_collection_title (?)
# test_update_geometry