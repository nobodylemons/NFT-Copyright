import sqlite3
import requests
import shutil
import os
import json


def download_file(url, collection, token):
    local_filename = "/data/{}_{}.png".format(collection, token)
    if os.path.exists(local_filename):
        return local_filename
    try:
        with requests.get(url, stream=True) as r:
            print("STATUS:", r.status_code)
            r.raw.decode_content = True
            with open(local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
    except:
        print(local_filename, "ERROR PULLING URL", url)

    return local_filename

con = sqlite3.connect('/root/nfts.sqlite')

cur = con.cursor()

i = 0
for row in cur.execute('SELECT nft_address, token_id FROM mints ORDER BY token_id'):
    try:
        local_filename = "/data/{}_{}.png".format(row[0], row[1])
        if os.path.exists(local_filename):
            continue
        i += 1
        # print(row)
        url = 'https://eth-mainnet.alchemyapi.io/v2/demo/getNFTMetadata?contractAddress={}&tokenId={}&tokenType=erc721'.format(row[0], row[1])
        print(url)    
        r = requests.get(url) 
        # print( r.text )
        myj = json.loads(r.text)

        img_url = ""
        try:
            img_url = myj['metadata']['image']
        except:
            try:
                img_url = myj['media']['gateway']
            except:
#                print(myj)
                continue
        img_url = img_url.replace('ipfs://', 'https://ipfs.io/ipfs/')


        imgname = download_file(img_url, row[0], row[1])
    except Exception as e:
        continue #print(e)

con.close()


