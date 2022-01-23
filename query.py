from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}
res = es.index(index="test-index", id=1, document=doc)
print(res['result'])

#res = es.get(index="test_data", id=1)
#print(res['_source'])

es.indices.refresh(index="test_data")

res = es.search(index="test_data", query={"match_all": {}}, sort="last_updated")

count = res['hits']['total']['value']

print("Got %s Hits:" % count)
print("Last entry: %s Hits." % res['hits']['hits'])

counter = 0

for hit in res['hits']['hits']:
    counter+=1
#    print("%(name)s %(age)s: %(last_updated)s" % hit["_source"])

print("Count: %d" % counter)

sort_params = res['hits']['hits'][counter - 1]['sort']
print("last sort: %s " % sort_params)

res = es.search(index="test_data", query={"match_all": {}}, sort="last_updated", search_after=sort_params)
