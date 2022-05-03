from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2
from image2vec import *
from find_lowest_distance import * 
import uuid

module_handle = 'https://tfhub.dev/google/imagenet/mobilenet_v2_140_224/feature_vector/4'

module = hub.load(module_handle)

# Initialize the Flask application
app = Flask(__name__)



# route http posts to this method
@app.route('/api/test', methods=['POST'])
def test():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    print(len(nparr))
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    path = '/tmp/' + str(uuid.uuid4().hex) + '.png'
    cv2.imwrite(path, img)
    myimg = load_img(path)
    # build a response dict to send back to client
    features = module(myimg)
    feature_set = np.squeeze(features)
    token_dict = find_nearest_neighbors(feature_set)
#    for url,similarity in token_dict.items():
#        if contract in url:
#            continue
#        if similarity > 1.92:
#            print(similarity, "{}/{}".format(contract, token), url)

#    np.savetxt(out_path, feature_set, delimiter=',')
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])
                }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(token_dict)

    return Response(response=response_pickled, status=200, mimetype="application/json")


# start flask app
app.run(host="0.0.0.0", port=5000)
