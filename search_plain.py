import json
import httplib
#import requests

from urllib import urlencode
import urllib2

def http_post(url, data):
    conn = httplib.HTTPConnection(url, 9200)
    headers = {"content-type": "application/json"}
    
    #conn.request('GET', '/test_data/_search', json.dumps(data), hdr)
    conn.request('GET', '/test_data/_search?pretty=true', data, headers)

    response = conn.getresponse()
    print("Code: %d" % response.status)
    print("Reason: %s" % response.reason)
    res = response.read()
    print(res)
    return res


def getQuery(searchAfter=None):
    queryDef = {
        "size": 10000,
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
    }

    if searchAfter:
        queryDef['search_after'] = searchAfter

    return json.dumps(queryDef)


def searchPlain(uri, searchAfter):
    query = getQuery(searchAfter)
    print(query)
    header = {'user-agent': 'my-app/0.0.1', 'Content-Type': 'application/json'}
    response = http_post(uri, query)
    #response = requests.get(uri, data=query, headers=header)
    parsed = json.loads(response.text)
    #print(json.dumps(parsed, indent=2, sort_keys=False))
    size = len(parsed['hits']['hits'])
    print("Size: %d" % size)

    if size == 0:
        return None

    sorted = parsed['hits']['hits'][size-1]['sort']
    #print("Sorted %s: " % sorted)

    return sorted


queryCount = 1
print("Query count: %d" % queryCount)
q = searchPlain("localhost", None)
while q:
    queryCount += 1
    print("Query count: %d" % queryCount)
    q = searchPlain("http://localhost:9200/test_data/_search", q)
