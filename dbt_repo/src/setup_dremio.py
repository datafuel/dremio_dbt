from email import header
import requests as rq

## Endpoints
HOST = "http://@dremio:9047"
LOGIN_ENDPOINT = "apiv2/login"
SOURCE_ENDPOINT = "api/v3/source"
credentials = {"userName":"admin", "password":"P@ss4dremio"}
LOGIN_URL = f"{HOST}/{LOGIN_ENDPOINT}"
SOURCE_URL = f"{HOST}/{SOURCE_ENDPOINT}"
MINIO_ACCESS_KEY = "minio"
MINIO_SECRET_KEY = "minio123"



def get_authentication_headers():
    response = rq.post(url=LOGIN_URL, json=credentials)
    response.raise_for_status()
    headers = {'Authorization':f'_dremio{response.json()["token"]}'}
    return headers

def add_datalake():
    payload = {
        "name":"minio-datalake",
        "type":"S3",
        "config": {
            'accessKey': MINIO_ACCESS_KEY, 
            'accessSecret': MINIO_SECRET_KEY, 
            'secure': False, 
            'propertyList': [
                {'name': 'fs.s3a.path.style.access', 'value': 'true'},
                {'name': 'fs.s3a.endpoint', 'value': 'minio:9000'}
            ],
            'rootPath': '/', 
            'credentialType': 'ACCESS_KEY', 
            'enableAsync': True, 
            'compatibilityMode': True, 
            'isCachingEnabled': True, 
            'maxCacheSpacePct': 100, 
            'requesterPays': False, 
            'enableFileStatusCheck': True
        }
    }
    headers = get_authentication_headers()
    try:
        response = rq.post(url=SOURCE_URL, headers=headers, json=payload)
        response.raise_for_status()
        print('Successfully added minio-datalake to Dremio !')
    except rq.HTTPError as err:
        if response.status_code != 409:
            raise err
        else:
            print('minio-datalake already added')

def list_sources():
    headers = get_authentication_headers()
    response = rq.get(url=SOURCE_URL, headers=headers)
    response.raise_for_status()        
    return response.json()


def main():
    add_datalake()

if __name__ == "__main__":
    main()







