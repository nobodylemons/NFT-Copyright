import os
from elasticsearch import Elasticsearch
import numpy as np
es = Elasticsearch(["http://localhost:9200"])

vectors = {}

for outfile_name in os.listdir('/home/ec2-user/feature-vectors/'):
    out_path = os.path.join('/home/ec2-user/feature-vectors/',outfile_name)
    try:
        vector = np.loadtxt(out_path, delimiter=',')
    except Exception as e:
        print(e)
        continue
    vectors[outfile_name] = vector


create_query = {
    "mappings": {
        "properties": {
            "description_vector": {
                "type": "dense_vector",
                "dims": 1792
            }
        }
    }
}

INDEX_NAME = 'idkfam'

try:
    es.indices.create(index=INDEX_NAME, body=create_query)
except:
    pass
docs = []

for k,v in vectors.items():
    docs.append({
        '_index': INDEX_NAME,
        '_id': k,
        'description_vector': v,
    })
requests = []
for i, doc in enumerate(docs):
    request = doc
    requests.append(request)

from elasticsearch import helpers
helpers.bulk(es, requests)




search_query = {
    "size": 10,
    "_source": {
        "includes": ["_id"]
    },
    "query": {
        "script_score": {
            "query": {
                "match_all": {}
            },
            "script": {
                "source": "cosineSimilarity(params.queryVector, 'description_vector') + 1.0",
                "params": {
                    "queryVector": vector.tolist()
                }
            }
        }
    }
}



response = es.search(
    index=INDEX_NAME,
    body=search_query
)


print(response)
