import json
import httplib
#import requests

from urllib import urlencode
import urllib2

def http_post(url, data, prettyPrint=False):
    conn = httplib.HTTPConnection(url, 9200)
    headers = {"content-type": "application/json"}
    
    if prettyPrint:
        url = '/test_data/_search?pretty=true'
    
    conn.request('GET', url, data, headers)

    response = conn.getresponse()
    print("Code: %d" % response.status)
    print("Reason: %s" % response.reason)
    res = response.read()
    print(res)
    return res


def getQuery(queryTemplate, searchAfter=None):
    if searchAfter:
        queryTemplate['search_after'] = searchAfter

    return json.dumps(queryTemplate)


def searchPlain(uri, queryTemplate, searchAfter):
    query = getQuery(queryTemplate, searchAfter)
    print(query)
    header = {'user-agent': 'my-app/0.0.1', 'Content-Type': 'application/json'}
    response = http_post(uri, query)
    #response = requests.get(uri, data=query, headers=header)
    parsed = json.loads(response)
    #print(json.dumps(parsed, indent=2, sort_keys=False))
    size = len(parsed['hits']['hits'])
    print("Size: %d" % size)

    if size == 0:
        return None

    sorted = parsed['hits']['hits'][size-1]['sort']

    return sorted


file = open('query.json', 'r')
queryTemplate = file.readlines()
file.close()

queryCount = 1
print("Query count: %d" % queryCount)
searchAfter = searchPlain("localhost", queryTemplate, None)

while searchAfter:
    queryCount += 1
    print("Query count: %d" % queryCount)
    searchAfter = searchPlain("localhost", queryTemplate, searchAfter)
