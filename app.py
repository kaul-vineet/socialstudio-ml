import os
import sys
import json
import time
import pprint
import traceback

import jwt_helper
import prediction
import token_generator

from language.dataset import dataset

def main():

    try:
        # Read account id and private from environment variables
        #account_id = os.environ['EINSTEIN_VISION_ACCOUNT_ID']
        #private_key = os.environ['EINSTEIN_VISION_PRIVATE_KEY'].decode('string_escape')

        account_id = 'vkaul@salesforce.com'
        private_key = """
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEApndK94LOWGJATet94opTPR4kjv0j66LrhsQtzyG+Ji6pVrJa
Nv6HEVpbE4Iy1cZJ4IyyeQ0yUMNDcJ4E0HZVT514ckNhJWIS0pO9lCrFsWNabc+7
U2q7nL4/7iS5QGvbFU37E1l7Vwtx2Ic0/Xm7czSHngALs9j0IWE6CGbaJfKosJKZ
CCsVIF6hnRV5/mjDWhav8m6gEeqqMPhZ6in74sPTEd/r5xXJ7hQu1lbtb2IyMNN6
K0o3gGPSiREvPvkh8KPWOtqzuMH+LHXvb/TPMCDV10q2/5b05NJ9sEnVQ9Rh54R/
EibKaBvNLBAmVm3IzW4sIFjE4bn8OIG11xz2CQIDAQABAoIBAQCjOO0k6/lv6Eat
IG76pi8gCmJGYifKcKEIL2vLYYaU4cPg4lha/A9sEHClHFDEE/10VADbePkQ/6Us
04Rc8uqLehgT0cV7ZkKWf46vrZDSclzEt58yF8GF23XMB+4tIJRcu22od2Dc5Lfo
XAq1T5thRuyDHABdhCk8YZ0Jh+/2q/L+k9utFZuHkHfBfKrzzpDktFu1vh4qK2xi
ZCu+3/P72oZ5OUKz/kheDP2NTKJiIjt3HPxXuIBXDDlarVb+8YA05KIYOvSaSH0b
r1Odm4CRJbJkkCkXp+5GPxuJRI5Iz4kXfJO4nQEPYDelTFW0c9e1Rwn4adJUrs7s
+juOarRRAoGBAPBWvVnDm9Ito7urQhWXinOGfQHIfujltWmtzV6Pq8F+MDLt9yfc
TWdenVx1N951U3l26bNtB7tjnJKFaYefX+Ox+N1eAVGdoAm6SqsN/hsoIIUI5FzR
C0QSEDLTYEfk/pJrqQ7DBgtWkNc9OMyGvOzguckMLfE2HobVzpSg+y63AoGBALFQ
OoXPOSEEbyUKXUc9CEQ+mcIjZUlILxtUA2Pgbh9BglOWmKzqQUS6b6cK0rrX8Aoy
pyMiDxPRYudzUYixJC+jeJKqmeC9FA/OXmPmHkswyVdAQ1X91+rVu7xmcv7jSCeD
nGr7Yp226fRlq6kJzPPKi19mYM34spD0U9WxEEE/AoGBAOmzfrY9llR/GrqPYlg6
nl+NxBqqynVPgOM9JPkxfVNOkDHF4dJ5zy6X+y5/sQ75SW1QKxnVCHK3/vUfE6nU
WNrBIXyoP2IMgyVSZ+8DUTc5Ar46Ek0K3QiZA/VYQ0RFsSHR3HdFPqhhyb/ygTuo
PSedsiqEVFw8QtzcJN+z1evrAoGABflN/3Qb2KDtnbHbsqq7vJDfXUsT/oQQEjui
YZsOGr96RJauTiUWTdp6KIaU0vazf6R1PRnIqEJFssaP2KsfLPu09DwLMycrpdyu
EW+PVbkvD2F640rKG39X8+D/vtapd6tXecM+b1HaUAGc5vUNkqkgSPaKDGZ0na2d
pXVxtsECgYBi/XuDRPviQuZE7nWGRhKOSKmQZ2qy/6zBaUGU1m/ArUACmU6NuI2t
KeF7J38BAtTCrhpp5whWW7Uooe8FxvhWNe+CkxdNoNoz5GyFUAl4IKfb/HX5nUkL
Xpd2APOZoLNf2gJZCycDmratthie+Ex9YULGSxYFgAlg3Ev5tQz20g==
-----END RSA PRIVATE KEY-----
"""

        # Set expiry time
        expiry = int(time.time()) + (15*60)

        # Generate an assertion using RSA private key
        assertion = jwt_helper.generate_assertion(account_id, private_key, expiry)

        # Obtain oauth token
        token = token_generator.generate_token(assertion)
        response = token.json()

        # If there is no token print the response
        if 'access_token' not in response:
            raise ValueError("Access token generation failed. Received reply: \"{}\"".format(response))
        else:
        # Collect the access token from response
            access_token = response['access_token']

        # Upload the dataset to einstein.ai
        DS = dataset(access_token=access_token)
        path = 'data/intent_tagging.csv'
        response = DS.create_intent_dataset(path)
        print(json.dumps(response, indent=4, sort_keys=True))

        # Train the model on einstein.ai [1127611 - 1127609]
        """ id = '1127611'
        DS = dataset(access_token=access_token)
        response = DS.train_dataset(id)
        if('available' in response):
            print(json.dumps(response, indent=4, sort_keys=True))
        else:
            print('Response status ok?: ' + str(response.ok))
            print(json.dumps(response.text, indent=4, sort_keys=True)) """
        
        # Make a prediction call using image url
        #prediction_url_response = prediction.predict_with_url(access_token, 'GeneralImageClassifier',
            #'https://animalso.com/wp-content/uploads/2017/01/Siberian-Husky_7.jpg')

        # Print prediction response
        #pprint.pprint(prediction_url_response.json())

        # Make a prediction call using image file
        # prediction_file_response = prediction.predict_with_image_file(access_token, 'GeneralImageClassifier',
        #     '/path/to/image/file/Siberian-Husky.jpg')
        
        # Print prediction response
        # pprint.pprint(prediction_file_response.json())

    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    main()
