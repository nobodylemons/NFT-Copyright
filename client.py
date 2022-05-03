import requests
import json

addr = 'http://localhost:5000'
test_url = addr + '/api/test'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}

img_file = '/home/ec2-user/images/logoonly.png'


img = open(img_file, 'rb').read()
response = requests.post(test_url, data=img, headers=headers)
print(response.content)
