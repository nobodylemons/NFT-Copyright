import os
from elasticsearch import Elasticsearch
import numpy as np
es = Elasticsearch(["http://localhost:9200"])

def find_nearest_neighbors(vector):
    INDEX_NAME = 'idkfam'
    sizeq = 10
    search_query = {
        "size": sizeq,
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
    token_dict = {}
    for i in range(sizeq):
        if not "0x" in response['hits']['hits'][i]['_id']:
            continue
        similarity = response['hits']['hits'][i]['_score']
        contract0 = response['hits']['hits'][i]['_id'].split("_")[0]
        token0 = response['hits']['hits'][i]['_id'].split("_")[1].replace(".png.npz", "")
        token_dict["https://opensea.io/assets/{}/{}".format(contract0, token0)] = similarity
    return token_dict



if __name__ == '__main__':
    INDEX_NAME = 'idkfam'
    es.indices.refresh(index=INDEX_NAME)
    count = es.cat.count(index=INDEX_NAME, params={"format": "json"})
    print("Number of documents:", count)
    for outfile_name in os.listdir('/home/ec2-user/feature-vectors/'):
        out_path = os.path.join('/home/ec2-user/feature-vectors/',outfile_name)
        k = outfile_name.split('.')[0]
        contract = k.split('_')[0]
        token = k.split('_')[1].replace(".png.npz", "")

        try:
            vector = np.loadtxt(out_path, delimiter=',')
        except Exception as e:
            print(e)
            continue

        token_dict = find_nearest_neighbors(vector)
        for url,similarity in token_dict.items():
            if contract in url:
                continue
            if similarity > 1.92:
                print(similarity, "{}/{}".format(contract, token), url)



