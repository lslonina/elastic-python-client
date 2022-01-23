import argparse
import httplib
import json
import zlib

def readFile(filename):
    file = open(filename, 'r')
    fileContent = file.read()
    file.close()
    return fileContent

def writeHits(filename, hits):
    file = open(filename, 'w')
    for hit in hits:
        file.write(json.dumps(hit['_source']))
        file.write('\n')
    file.close()

def getHeaders():
    lines = readFile('headers.txt').splitlines()
    headers = {}    
    for line in lines:
        split = line.split(': ', 1)
        key = split[0]
        value = split[1]
        headers[key] = value

    #print(headers)
    return headers

def httpGet(host, indexName, data, headers, prettyPrint=False):
    conn = httplib.HTTPConnection(host, 9200)
    
    url = '/' + indexName + '/_search'
    if prettyPrint:
        url = url + '?pretty=true'

    conn.request('GET', url, data, headers)
    response = conn.getresponse()

    #print(response.getheaders())

    content = response.read()
    content = zlib.decompress(content, 16+zlib.MAX_WBITS)

    if response.status != 200:
        print("Code: %d" % response.status)
        print("Reason: %s" % response.reason)
        print("Response: %s" % content)

    conn.close()

    return content


def getQuery(queryTemplate, searchAfter=None):
    if searchAfter:
        queryTemplate['search_after'] = searchAfter

    return json.dumps(queryTemplate)


def searchPlain(host, indexName, queryTemplate, searchAfter):
    query = getQuery(queryTemplate, searchAfter)
    print(query)
    response = httpGet(host, indexName, query, getHeaders())
    
    parsed = json.loads(response)
    size = len(parsed['hits']['hits'])
    print("Size: %d" % size)

    if size == 0:
        return (None, None)

    sorted = parsed['hits']['hits'][size-1]['sort']

    return (sorted, parsed['hits']['hits'])


queryCounter = 1
searchAfter = None

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--index', type=str, help='Index name')
parser.add_argument('-q', '--query', default='query.json', type=str, help='Path to file with query definition in json format, defaults to query.json')
args = parser.parse_args()

queryDefinition = json.loads(readFile(args.query))

while True:
    print("Query count: %d" % queryCounter)
    searchResult = searchPlain("localhost", args.index, queryDefinition, searchAfter)
    searchAfter = searchResult[0]

    if searchAfter == None:
        break

    filename= './dumps/dump_' + '{:03d}'.format(queryCounter) + '_' + '_'.join(map(str, searchAfter))
    writeHits(filename, searchResult[1])

    queryCounter += 1
