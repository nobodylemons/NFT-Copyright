# NFT-Copyright
This project allows the user to set up a server which compiles NFTs and compares them via Tensorflow

It's not production ready, so there are many absolute paths, and the flask server simply expects to host on all interfaces on an ec2 instance. 


Requirements:

https://www.kaggle.com/datasets/simiotic/ethereum-nfts -> nfts.sqlite

Elasticsearch database with http hosted on localhost:9200

Change paths as necessary, and use the scripts in this order:


#Pull images of NFTs derived from sqlite database, this will take forever, and other scripts can be run in the meantime. 
python pull_images.py

#Runs other scripts that will turn images into vectors and push them to elasticsearch. Then it will find the NFTs that are closest to each other in the database.
./update.sh


#Starts flask server on port 5000 that allows the upload of an image, and compares that image to other images in the database.
python flaskServer.py


#Client hard coded to my current ec2 instance. Replace the url with your own, and the .png with your own. Returns 10 closest urls to image
python client.py

