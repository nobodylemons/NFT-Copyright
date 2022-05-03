import requests
import json


img_file = 'bored_ape.png'
img_file = 'crypto_kitty.png'

addr = 'http://ec2-54-202-171-244.us-west-2.compute.amazonaws.com:5000/api/test'

headers = {'content-type': 'image/jpeg'}

img = open(img_file, 'rb').read()

response = requests.post(addr, data=img, headers=headers)

token_dict = json.loads(response.content.decode('utf-8'))

for k,v in token_dict.items():
    print(v, k)
