set -ex
python image2vec.py
python push_to_elasticsearch.py
python find_lowest_distance.py
