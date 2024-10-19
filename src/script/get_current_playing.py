import os
import sys

import requests

sys.path.append(f"{os.environ['HOME']}/git/alfred_python/src/")

import config

if __name__ == "__main__":
    # title = sys.argv[1]
    URL = config.LAMBDA_SPOTIFY_API_DOMAIN + "/current/playing"
    headers = {
        "access-token": config.SPOTIFY_CLIENT_SECRET,
    }
    print(URL)
    print(headers)
    response = requests.post(URL, timeout=10, headers=headers)
    print(response.status_code)
    print(response.json())
