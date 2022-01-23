import json
import requests

from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

def getQuery():
    return json.dumps({
        "size": 5,
        "query": {
            "match_all": {}
        },
        "sort": [{
            "last_updated": {
                "order": "desc"
            },
            "age": {
                "order": "desc"
            }
        }]
    })

def searchPlain(uri, date):
    query = getQuery()
    print(query)
    header={'user-agent': 'my-app/0.0.1', 'Content-Type': 'application/json'}
    response = requests.get(uri, data=query, headers=header)
    parsed = json.loads(response.text)
    print(json.dumps(parsed, indent=2, sort_keys=False))


def getData(param):
    if param:
        return es.search(index="test_data", size=10000, query={"match_all": {}}, sort=["last_updated", "age"], search_after=param)
    return es.search(index="test_data", size=10000, query={"match_all": {}}, sort=["last_updated", "age"])


def query(param=None):
    res = getData(param)
    count = res['hits']['total']['value']

    counter = 0
    for hit in res['hits']['hits']:
        counter += 1
    print("Count: %d" % counter)
    if counter == 0:
        return None

    sort_params = res['hits']['hits'][counter - 1]['sort']
    print("last sort: %s " % sort_params)

    if counter > 0:
        return sort_params
    return None


def esApi():
    q = query()
    while q:
        q = query(q)

searchPlain("http://localhost:9200/test_data/_search", None)