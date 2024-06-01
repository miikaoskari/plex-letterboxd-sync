from api.tautulli_api import Tautulli
from api.letterboxd import Letterboxd
import json

def read_keys():
    with open('keys.json') as f:
        keys = json.load(f)
    return keys

def debug():
    import os
    # for debugging with burp suite
    os.environ["REQUESTS_CA_BUNDLE"]="cert.pem"
    os.environ["HTTP_PROXY"]="http://127.0.0.1:8080"
    os.environ["HTTPS_PROXY"]="http://127.0.0.1:8080"

def start_sync():
    keys = read_keys()

    tautulli = Tautulli(url=keys["tautulli"]["url"], key=keys["tautulli"]["api_key"])
    tautulli.get_watched(user=keys["tautulli"]["username"])
    tautulli.check_watched_status()
    tautulli.compile_json_to_csv(file="history")

    letterboxd = Letterboxd(keys["letterboxd"]["username"], keys["letterboxd"]["password"])
    letterboxd.login()
    letterboxd.import_data(file="history.csv")

if __name__ == "__main__":
    start_sync()